#!/usr/bin/env python3
"""
Phase117: LoRA fine-tuning on attention layers under the mode-matched fullvocab protocol.

Goal: Compare LoRA (attention, Q/V projections, all 36 layers) to:
  - Direct 9-row lm_head repair: 60.3%±2.8% fullvocab (Phase107)
  - Rank-4 adapter on digit rows: 59.8%±2.9% fullvocab (Phase115)

Protocol (matching Phase107 exactly):
  - Entity counting task
  - N=200 test prompts × 3 seeds [42, 11, 77]
  - Training: N=400 training prompts (disjoint from test) per seed
  - Training objective: cross-entropy over FULL vocabulary (152K tokens)
    so the digit token must beat all other tokens
  - Evaluation: fullvocab argmax (all 152K tokens, no digit restriction)
  - Also report constrained accuracy (digit-restricted argmax) for comparison

LoRA config:
  - rank=16, alpha=32, target_modules=["q_proj", "v_proj"]
  - All 36 layers
  - ~9.4M trainable parameters
  - 200 gradient steps, lr=2e-4, AdamW
  - batch_size=4

Output: /tmp/results_phase117_lora_fullvocab.json
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

# ─────────────────────────────────────────────────────────────────────────────
# Environment
# ─────────────────────────────────────────────────────────────────────────────

HF_CACHE = os.environ.get("HF_CACHE", os.environ.get("HF_CACHE", "./hf_cache"))
MODEL_NAME = "Qwen/Qwen3-8B"
OUTPUT_PATH = "/tmp/results_phase117_lora_fullvocab.json"
SEEDS = [42, 11, 77]
N_TRAIN = 400
N_TEST = 200
N_STEPS = 200
LR = 2e-4
BATCH_SIZE = 4
LORA_RANK = 16
LORA_ALPHA = 32.0
LOG_EVERY = 20

def log(msg):
    print(f"[phase117] {msg}", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# Prompt generation (entity counting, same as Phase107)
# ─────────────────────────────────────────────────────────────────────────────

# Phase107-matching entity counting prompts (multi-sentence with distractors)
ENTITIES = [
    "apple", "car", "dog", "tree", "book",
    "chair", "lamp", "phone", "cloud", "river",
    "bird", "shoe", "ball", "hat", "pen",
    "stone", "star", "fish", "flag", "coin",
]

def make_entity_counting_prompts(n, seed, min_count=1, max_count=9):
    """Generate entity counting prompts MATCHING Phase107 format exactly.
    
    Multi-sentence context with distractor entities:
    "There are 2 apples near the pond. There are 1 cat in the area...
    Count how many apples there are. Answer with just the number: "
    
    This is the same format as Phase107, ensuring baseline≈13.7% constrained
    and results are directly comparable to Phase107's 60.3% fullvocab repair.
    """
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
# Digit token IDs for Qwen3
# ─────────────────────────────────────────────────────────────────────────────

DIGIT_STRS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

def get_digit_token_ids(tokenizer):
    ids = []
    for d in DIGIT_STRS:
        toks = tokenizer.encode(d, add_special_tokens=False)
        assert len(toks) == 1, f"Digit '{d}' tokenized to {toks}"
        ids.append(toks[0])
    return ids  # list of 9 ints

# ─────────────────────────────────────────────────────────────────────────────
# Evaluate under fullvocab and constrained protocols
# ─────────────────────────────────────────────────────────────────────────────

def evaluate(model, tokenizer, prompts, answers, digit_token_ids, batch_size=8, desc="eval"):
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
            # Fullvocab argmax
            preds_fv = torch.argmax(logits, dim=-1).tolist()
            # Constrained argmax (digit tokens only)
            digit_logits = logits[:, digit_token_ids]  # [B, 9]
            preds_cs_idx = torch.argmax(digit_logits, dim=-1).tolist()
            for j, (pf, pc, a) in enumerate(zip(preds_fv, preds_cs_idx, batch_a)):
                correct_digit_id = digit_token_ids[a - 1]
                if pf == correct_digit_id:
                    correct_fv += 1
                if pc == a - 1:
                    correct_cs += 1
    return correct_fv / total, correct_cs / total

# ─────────────────────────────────────────────────────────────────────────────
# LoRA implementation (manual, lightweight)
# We use PEFT if available, otherwise implement minimal LoRA
# ─────────────────────────────────────────────────────────────────────────────

def apply_lora_peft(model, rank=16, alpha=32.0):
    """Apply LoRA using PEFT library."""
    try:
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
    except ImportError:
        raise RuntimeError("PEFT not available — install with: python3 -m pip install peft")

# ─────────────────────────────────────────────────────────────────────────────
# Training loop
# ─────────────────────────────────────────────────────────────────────────────

def train_one_seed(model_base_path, tokenizer, train_prompts, train_answers,
                   test_prompts, test_answers, digit_token_ids, seed,
                   n_steps=200, lr=2e-4, batch_size=4,
                   lora_rank=16, lora_alpha=32.0):
    """Train LoRA for one seed and return accuracy results."""
    import copy
    log(f"\n  === Seed {seed} ===")

    # Load fresh model weights for this seed
    log("  Loading base model for this seed...")
    t0 = time.time()
    from transformers import AutoModelForCausalLM
    model = AutoModelForCausalLM.from_pretrained(
        model_base_path,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
    )
    model.eval()
    log(f"  Model loaded in {time.time()-t0:.1f}s")

    # Evaluate baseline (no LoRA)
    log("  Evaluating baseline...")
    acc_fv_before, acc_cs_before = evaluate(
        model, tokenizer, test_prompts, test_answers, digit_token_ids, batch_size=8
    )
    log(f"  Baseline: fullvocab={acc_fv_before:.3f}, constrained={acc_cs_before:.3f}")

    # Apply LoRA
    log("  Applying LoRA...")
    model = apply_lora_peft(model, rank=lora_rank, alpha=lora_alpha)
    model.train()

    # Optimizer
    opt = AdamW([p for p in model.parameters() if p.requires_grad], lr=lr)

    # Training
    log(f"  Training for {n_steps} steps (batch_size={batch_size}, lr={lr})...")
    rng = random.Random(seed)
    np_rng = np.random.RandomState(seed)
    n_train = len(train_prompts)
    device = next(model.parameters()).device

    losses = []
    t_train_start = time.time()

    for step in range(n_steps):
        # Sample batch
        batch_idx = rng.choices(range(n_train), k=batch_size)
        batch_p = [train_prompts[i] for i in batch_idx]
        batch_a = [train_answers[i] for i in batch_idx]

        # Tokenize
        enc = tokenizer(batch_p, return_tensors="pt", padding=True, truncation=True,
                        max_length=256)
        input_ids = enc["input_ids"].to(device)
        attention_mask = enc["attention_mask"].to(device)

        # Labels: correct digit token ID for each example
        labels = torch.tensor([digit_token_ids[a - 1] for a in batch_a],
                               dtype=torch.long, device=device)

        # Forward
        out = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = out.logits[:, -1, :]  # [B, V] — last token position

        # Full-vocabulary cross-entropy loss (competitive training)
        loss = nn.CrossEntropyLoss()(logits, labels)

        # Backward
        opt.zero_grad()
        loss.backward()
        # Gradient clip
        torch.nn.utils.clip_grad_norm_(
            [p for p in model.parameters() if p.requires_grad], max_norm=1.0
        )
        opt.step()

        losses.append(loss.item())

        if (step + 1) % LOG_EVERY == 0 or step == 0:
            avg_loss = np.mean(losses[-LOG_EVERY:])
            elapsed = time.time() - t_train_start
            log(f"    Step {step+1}/{n_steps} | loss={avg_loss:.4f} | elapsed={elapsed:.1f}s")

    t_train = time.time() - t_train_start
    log(f"  Training complete in {t_train:.1f}s")

    # Evaluate after training
    log("  Evaluating post-training...")
    model.eval()
    acc_fv_after, acc_cs_after = evaluate(
        model, tokenizer, test_prompts, test_answers, digit_token_ids, batch_size=8
    )
    log(f"  Post-train: fullvocab={acc_fv_after:.3f}, constrained={acc_cs_after:.3f}")
    log(f"  Improvement: fullvocab +{acc_fv_after - acc_fv_before:.3f}, constrained +{acc_cs_after - acc_cs_before:.3f}")

    # Free memory
    del model
    torch.cuda.empty_cache() if torch.cuda.is_available() else None
    import gc; gc.collect()

    return {
        "seed": seed,
        "baseline_fullvocab": acc_fv_before,
        "baseline_constrained": acc_cs_before,
        "trained_fullvocab": acc_fv_after,
        "trained_constrained": acc_cs_after,
        "training_time_s": t_train,
        "final_loss": float(np.mean(losses[-10:])),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    import os
    os.environ["TRANSFORMERS_CACHE"] = HF_CACHE
    os.environ["HF_HOME"] = HF_CACHE

    log(f"Phase117: LoRA fullvocab protocol")
    log(f"  Model: {MODEL_NAME}")
    log(f"  HF_CACHE: {HF_CACHE}")
    log(f"  Seeds: {SEEDS}")
    log(f"  N_train={N_TRAIN}, N_test={N_TEST}, N_steps={N_STEPS}")
    log(f"  LoRA rank={LORA_RANK}, alpha={LORA_ALPHA}, lr={LR}")

    from transformers import AutoTokenizer
    log("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=HF_CACHE)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    # Digit token IDs
    digit_token_ids = get_digit_token_ids(tokenizer)
    log(f"Digit token IDs: {digit_token_ids}")

    # Discover model path
    model_base_path = MODEL_NAME  # PEFT/transformers will use cache

    results = {"seeds": {}, "metadata": {
        "model": MODEL_NAME,
        "lora_rank": LORA_RANK,
        "lora_alpha": LORA_ALPHA,
        "n_train": N_TRAIN,
        "n_test": N_TEST,
        "n_steps": N_STEPS,
        "lr": LR,
        "batch_size": BATCH_SIZE,
        "protocol": "fullvocab_argmax_all_152K_tokens",
        "task": "entity_counting",
        "target_modules": ["q_proj", "v_proj"],
    }}

    for seed in SEEDS:
        # Generate disjoint train/test prompts for this seed
        all_prompts, all_answers = make_entity_counting_prompts(
            N_TRAIN + N_TEST, seed=seed
        )
        train_prompts = all_prompts[:N_TRAIN]
        train_answers = all_answers[:N_TRAIN]
        test_prompts = all_prompts[N_TRAIN:]
        test_answers = all_answers[N_TRAIN:]

        seed_result = train_one_seed(
            model_base_path=MODEL_NAME,
            tokenizer=tokenizer,
            train_prompts=train_prompts,
            train_answers=train_answers,
            test_prompts=test_prompts,
            test_answers=test_answers,
            digit_token_ids=digit_token_ids,
            seed=seed,
            n_steps=N_STEPS,
            lr=LR,
            batch_size=BATCH_SIZE,
            lora_rank=LORA_RANK,
            lora_alpha=LORA_ALPHA,
        )
        results["seeds"][str(seed)] = seed_result

        # Save intermediate results
        with open(OUTPUT_PATH, "w") as f:
            json.dump(results, f, indent=2)
        log(f"  Saved intermediate results to {OUTPUT_PATH}")

    # Summary
    fv_accs = [results["seeds"][str(s)]["trained_fullvocab"] for s in SEEDS]
    cs_accs = [results["seeds"][str(s)]["trained_constrained"] for s in SEEDS]
    results["summary"] = {
        "mean_fullvocab": float(np.mean(fv_accs)),
        "std_fullvocab": float(np.std(fv_accs)),
        "mean_constrained": float(np.mean(cs_accs)),
        "std_constrained": float(np.std(cs_accs)),
        "per_seed_fullvocab": {str(s): results["seeds"][str(s)]["trained_fullvocab"] for s in SEEDS},
    }
    log(f"\n=== FINAL SUMMARY ===")
    log(f"LoRA fullvocab accuracy: {results['summary']['mean_fullvocab']:.3f} ± {results['summary']['std_fullvocab']:.3f}")
    log(f"LoRA constrained accuracy: {results['summary']['mean_constrained']:.3f} ± {results['summary']['std_constrained']:.3f}")
    log(f"Compare: 9-row repair fullvocab=0.603±0.028, constrained=0.607±0.031")

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    log(f"Results saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
