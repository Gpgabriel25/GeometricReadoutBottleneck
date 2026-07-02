#!/usr/bin/env python3
"""
Phase118: LoRA fine-tuning with generation-mode evaluation.

Goal: Show that LoRA rank-16 Q/V (same as Phase117) achieves high accuracy
  NOT ONLY in next-token fullvocab evaluation, but ALSO in autoregressive
  generation mode (model.generate, greedy decode, max_new_tokens=1).

This directly addresses the R16 reviewer concern:
  "9-row repair achieves 0% in generation mode — addressable by showing
  LoRA IS the deployable fix"

Protocol (matching Phase117/Phase107 exactly):
  - Entity counting task, multi-sentence distractors
  - N=200 test prompts × 3 seeds [42, 11, 77]
  - Training: N=400 training prompts (disjoint from test) per seed
  - Training objective: cross-entropy over FULL vocabulary (152K tokens)
  - Evaluation modes:
      (A) fullvocab next-token: argmax(logits[-1, :]) == correct_digit_id
      (B) generation mode: model.generate(max_new_tokens=1, do_sample=False)
          then check if generated token == correct_digit_id
      (C) constrained next-token: argmax(logits[-1, digit_ids]) == correct
  - Baseline (untrained) evaluated in all three modes

Expected outcome:
  - Baseline fullvocab ≈ 5-8% (Phase117 confirmed)
  - Baseline generation ≈ same as fullvocab (greedy = argmax)
  - LoRA fullvocab ≈ 91.7% (Phase117 confirmed)
  - LoRA generation ≈ same as fullvocab (~91.7%)
  - This shows LoRA IS the generation-mode fix

Output: /tmp/results_phase118_lora_generation.json
"""

import json
import os
import sys
import time
import random
import numpy as np
import torch
import torch.nn as nn
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelForCausalLM

# ─────────────────────────────────────────────────────────────────────────────
# Environment
# ─────────────────────────────────────────────────────────────────────────────

HF_CACHE = os.environ.get("HF_CACHE", "/home/gpgabriel25/hf_cache")
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE
os.environ["HF_HOME"] = HF_CACHE

MODEL_NAME = "Qwen/Qwen3-8B"
OUTPUT_PATH = "/tmp/results_phase118_lora_generation.json"
SEEDS = [42, 11, 77]
N_TRAIN = 400
N_TEST = 200
N_STEPS = 200
LR = 2e-4
BATCH_SIZE = 4
LORA_RANK = 16
LORA_ALPHA = 32.0
LOG_EVERY = 20
DEVICE = "cpu"

def log(msg):
    print(f"[phase118] {msg}", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# Prompt generation (entity counting, same as Phase107/Phase117)
# ─────────────────────────────────────────────────────────────────────────────

ENTITIES = [
    "apple", "car", "dog", "tree", "book",
    "chair", "lamp", "phone", "cloud", "river",
    "bird", "shoe", "ball", "hat", "pen",
    "stone", "star", "fish", "flag", "coin",
]

def make_entity_counting_prompts(n, seed, min_count=1, max_count=9):
    """Generate entity counting prompts MATCHING Phase107/Phase117 format."""
    rng = random.Random(seed)
    prompts, answers = [], []
    while len(prompts) < n:
        entity = rng.choice(ENTITIES)
        count = rng.randint(min_count, max_count)
        n_distractors = rng.randint(0, 3)
        dist_entities = [e for e in ENTITIES if e != entity]
        sentences = []
        dist_counts = {e: rng.randint(1, 4) for e in rng.sample(dist_entities, n_distractors)}
        for i in range(count):
            sentences.append(f"There are {rng.randint(1,3)} {entity} near the pond.")
        for e, c in dist_counts.items():
            sentences.append(f"There are {c} {e} in the area.")
        rng.shuffle(sentences)
        text = " ".join(sentences)
        prompt = f"{text}\n\nCount how many {entity} there are. Answer with just the number: "
        prompts.append(prompt)
        answers.append(count)
    return prompts, answers

# ─────────────────────────────────────────────────────────────────────────────
# Digit token IDs
# ─────────────────────────────────────────────────────────────────────────────

DIGIT_STRS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

def get_digit_token_ids(tokenizer):
    ids = []
    for d in DIGIT_STRS:
        toks = tokenizer.encode(d, add_special_tokens=False)
        assert len(toks) == 1, f"Digit '{d}' tokenized to {toks}"
        ids.append(toks[0])
    return ids

# ─────────────────────────────────────────────────────────────────────────────
# Evaluation: next-token (fullvocab + constrained)
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_next_token(model, tokenizer, prompts, answers, digit_token_ids, batch_size=8):
    """Next-token evaluation: logits at the last position."""
    model.eval()
    device = next(model.parameters()).device
    correct_fv = 0
    correct_cs = 0
    total = len(prompts)
    with torch.no_grad():
        for i in range(0, total, batch_size):
            batch_p = prompts[i:i+batch_size]
            batch_a = answers[i:i+batch_size]
            enc = tokenizer(batch_p, return_tensors="pt", padding=True, truncation=True,
                            max_length=256)
            input_ids = enc["input_ids"].to(device)
            attention_mask = enc["attention_mask"].to(device)
            out = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = out.logits[:, -1, :]  # [B, V]
            preds_fv = torch.argmax(logits, dim=-1).tolist()
            digit_logits = logits[:, digit_token_ids]
            preds_cs_idx = torch.argmax(digit_logits, dim=-1).tolist()
            for pf, pc, a in zip(preds_fv, preds_cs_idx, batch_a):
                correct_digit_id = digit_token_ids[a - 1]
                if pf == correct_digit_id:
                    correct_fv += 1
                if pc == a - 1:
                    correct_cs += 1
    return correct_fv / total, correct_cs / total

# ─────────────────────────────────────────────────────────────────────────────
# Evaluation: autoregressive generation mode
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_generation(model, tokenizer, prompts, answers, digit_token_ids, batch_size=4):
    """Generation mode: model.generate(max_new_tokens=1, do_sample=False).
    
    This is true autoregressive generation — the model picks the next token
    by sampling (greedy) from its own output distribution without teacher forcing.
    Equivalent to argmax(logits) for greedy decoding, but exercises the
    model.generate() code path exactly as in deployment.
    """
    model.eval()
    device = next(model.parameters()).device
    correct = 0
    total = len(prompts)
    digit_token_ids_tensor = torch.tensor(digit_token_ids, device=device)

    with torch.no_grad():
        for i in range(0, total, batch_size):
            batch_p = prompts[i:i+batch_size]
            batch_a = answers[i:i+batch_size]
            enc = tokenizer(batch_p, return_tensors="pt", padding=True, truncation=True,
                            max_length=256)
            input_ids = enc["input_ids"].to(device)
            attention_mask = enc["attention_mask"].to(device)
            # Generate exactly 1 new token (greedy)
            generated = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=1,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
            )
            # The generated token is the last token of each sequence
            new_tokens = generated[:, input_ids.shape[1]:]  # [B, 1]
            for j, a in enumerate(batch_a):
                if j < new_tokens.shape[0]:
                    gen_token_id = new_tokens[j, 0].item()
                    correct_digit_id = digit_token_ids[a - 1]
                    if gen_token_id == correct_digit_id:
                        correct += 1
    return correct / total

# ─────────────────────────────────────────────────────────────────────────────
# LoRA via PEFT
# ─────────────────────────────────────────────────────────────────────────────

def apply_lora_peft(model, rank=16, alpha=32.0):
    from peft import get_peft_model, LoraConfig, TaskType
    lora_config = LoraConfig(
        r=rank,
        lora_alpha=alpha,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.0,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    model = get_peft_model(model, lora_config)
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    log(f"  PEFT LoRA applied: rank={rank}, alpha={alpha}")
    log(f"  Trainable params: {n_trainable:,} ({n_trainable/1e6:.2f}M)")
    return model

# ─────────────────────────────────────────────────────────────────────────────
# Training
# ─────────────────────────────────────────────────────────────────────────────

def train_lora(model, tokenizer, train_prompts, train_answers, digit_token_ids,
               n_steps=200, lr=2e-4, batch_size=4, seed=42):
    """Match Phase117 objective exactly: CE on logits at final prompt position."""
    device = next(model.parameters()).device
    optimizer = AdamW([p for p in model.parameters() if p.requires_grad], lr=lr)
    model.train()
    t0 = time.time()

    rng = random.Random(seed)
    n_train = len(train_prompts)
    losses = []

    for step in range(n_steps):
        batch_idx = rng.choices(range(n_train), k=batch_size)
        batch_p = [train_prompts[i] for i in batch_idx]
        batch_a = [train_answers[i] for i in batch_idx]

        enc = tokenizer(batch_p, return_tensors="pt", padding=True, truncation=True,
                        max_length=256)
        input_ids = enc["input_ids"].to(device)
        attention_mask = enc["attention_mask"].to(device)

        labels = torch.tensor([digit_token_ids[a - 1] for a in batch_a],
                              dtype=torch.long, device=device)

        out = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = out.logits[:, -1, :]
        loss = nn.CrossEntropyLoss()(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            [p for p in model.parameters() if p.requires_grad], max_norm=1.0
        )
        optimizer.step()

        losses.append(loss.item())
        if (step + 1) % LOG_EVERY == 0 or step == 0:
            avg_loss = float(np.mean(losses[-LOG_EVERY:]))
            elapsed = time.time() - t0
            log(f"    Step {step+1}/{n_steps} | loss={avg_loss:.4f} | elapsed={elapsed:.1f}s")

    return time.time() - t0

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    log("Phase118: LoRA generation-mode evaluation")
    log(f"  Model: {MODEL_NAME}")
    log(f"  HF_CACHE: {HF_CACHE}")
    log(f"  Seeds: {SEEDS}")
    log(f"  N_train={N_TRAIN}, N_test={N_TEST}, N_steps={N_STEPS}")
    log(f"  LoRA rank={LORA_RANK}, alpha={LORA_ALPHA}, lr={LR}")
    log("")

    # Load tokenizer once
    log("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        cache_dir=HF_CACHE,
        trust_remote_code=True,
        padding_side="left",
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    digit_token_ids = get_digit_token_ids(tokenizer)
    log(f"Digit token IDs: {digit_token_ids}")
    log("")

    all_results = {}

    for seed in SEEDS:
        log(f"  === Seed {seed} ===")

        # Generate prompts
        all_prompts, all_answers = make_entity_counting_prompts(
            N_TRAIN + N_TEST, seed=seed
        )
        train_prompts = all_prompts[:N_TRAIN]
        train_answers = all_answers[:N_TRAIN]
        test_prompts = all_prompts[N_TRAIN:]
        test_answers = all_answers[N_TRAIN:]

        # Load fresh base model
        log(f"  Loading base model for this seed...")
        t_load = time.time()
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            cache_dir=HF_CACHE,
            trust_remote_code=True,
            dtype=torch.float32,
        )
        model = model.to(DEVICE)
        model.eval()
        log(f"  Model loaded in {time.time()-t_load:.1f}s")

        # Baseline evaluation (next-token fullvocab)
        log(f"  Evaluating baseline (next-token)...")
        base_fv, base_cs = evaluate_next_token(model, tokenizer, test_prompts, test_answers,
                                                digit_token_ids)
        log(f"  Baseline next-token: fullvocab={base_fv:.3f}, constrained={base_cs:.3f}")

        # Baseline evaluation (generation mode)
        log(f"  Evaluating baseline (generation)...")
        base_gen = evaluate_generation(model, tokenizer, test_prompts, test_answers,
                                       digit_token_ids)
        log(f"  Baseline generation: {base_gen:.3f}")

        # Apply LoRA
        log(f"  Applying LoRA...")
        model = apply_lora_peft(model, rank=LORA_RANK, alpha=LORA_ALPHA)

        # Train
        log(f"  Training for {N_STEPS} steps (batch_size={BATCH_SIZE}, lr={LR})...")
        train_time = train_lora(model, tokenizer, train_prompts, train_answers,
                    digit_token_ids, n_steps=N_STEPS, lr=LR,
                    batch_size=BATCH_SIZE, seed=seed)
        log(f"  Training complete in {train_time:.1f}s")

        # Post-training: next-token evaluation
        log(f"  Evaluating post-training (next-token)...")
        trained_fv, trained_cs = evaluate_next_token(model, tokenizer, test_prompts, test_answers,
                                                      digit_token_ids)
        log(f"  Post-train next-token: fullvocab={trained_fv:.3f}, constrained={trained_cs:.3f}")

        # Post-training: generation mode evaluation
        log(f"  Evaluating post-training (generation)...")
        trained_gen = evaluate_generation(model, tokenizer, test_prompts, test_answers,
                                          digit_token_ids)
        log(f"  Post-train generation: {trained_gen:.3f}")
        log(f"  Improvement generation: {trained_gen - base_gen:+.3f}")
        log(f"  Fullvocab vs generation gap: {trained_fv - trained_gen:+.3f}")

        all_results[str(seed)] = {
            "seed": seed,
            "baseline_fullvocab": base_fv,
            "baseline_constrained": base_cs,
            "baseline_generation": base_gen,
            "trained_fullvocab": trained_fv,
            "trained_constrained": trained_cs,
            "trained_generation": trained_gen,
            "training_time_s": train_time,
        }

        # Save intermediate
        result_obj = {
            "seeds": all_results,
            "metadata": {
                "model": MODEL_NAME,
                "lora_rank": LORA_RANK,
                "lora_alpha": LORA_ALPHA,
                "n_train": N_TRAIN,
                "n_test": N_TEST,
                "n_steps": N_STEPS,
                "lr": LR,
                "batch_size": BATCH_SIZE,
                "protocol": "fullvocab_train_three_eval_modes",
                "task": "entity_counting",
                "target_modules": ["q_proj", "v_proj"],
            }
        }
        with open(OUTPUT_PATH, 'w') as f:
            json.dump(result_obj, f, indent=2)
        log(f"  Saved intermediate results to {OUTPUT_PATH}")
        log("")

        del model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

    # Compute summary
    gen_accs = [all_results[str(s)]["trained_generation"] for s in SEEDS]
    fv_accs = [all_results[str(s)]["trained_fullvocab"] for s in SEEDS]
    base_gen_accs = [all_results[str(s)]["baseline_generation"] for s in SEEDS]

    summary = {
        "mean_generation": float(np.mean(gen_accs)),
        "std_generation": float(np.std(gen_accs)),
        "mean_fullvocab": float(np.mean(fv_accs)),
        "std_fullvocab": float(np.std(fv_accs)),
        "mean_baseline_generation": float(np.mean(base_gen_accs)),
        "per_seed_generation": {str(s): all_results[str(s)]["trained_generation"] for s in SEEDS},
        "per_seed_fullvocab": {str(s): all_results[str(s)]["trained_fullvocab"] for s in SEEDS},
    }

    log("=== FINAL SUMMARY ===")
    log(f"LoRA generation accuracy: {summary['mean_generation']:.3f} ± {summary['std_generation']:.3f}")
    log(f"LoRA fullvocab accuracy:  {summary['mean_fullvocab']:.3f} ± {summary['std_fullvocab']:.3f}")
    log(f"Baseline generation:      {summary['mean_baseline_generation']:.3f}")
    log(f"Compare: 9-row repair fullvocab=0.603±0.028 (next-token), generation≈0%")
    log(f"Results saved to {OUTPUT_PATH}")

    result_obj = {
        "seeds": all_results,
        "metadata": {
            "model": MODEL_NAME,
            "lora_rank": LORA_RANK,
            "lora_alpha": LORA_ALPHA,
            "n_train": N_TRAIN,
            "n_test": N_TEST,
            "n_steps": N_STEPS,
            "lr": LR,
            "batch_size": BATCH_SIZE,
            "protocol": "fullvocab_train_three_eval_modes",
            "task": "entity_counting",
            "target_modules": ["q_proj", "v_proj"],
        },
        "summary": summary,
    }
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(result_obj, f, indent=2)

if __name__ == "__main__":
    main()
