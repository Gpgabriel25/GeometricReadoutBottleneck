#!/usr/bin/env python3
"""
Phase119c: Logit-Lens SNR at final layer pre/post LoRA.

The key measurement: apply lm_head directly to layer-35 hidden states.
Does LoRA Q/V make the hidden state project correctly onto digit rows
even WITHOUT the count-specialized probe?

This directly answers the reviewer concern:
"does LoRA change how lm_head reads counts from the output layer?"

Metrics reported:
- logit-lens accuracy: argmax_{digit-tokens} lm_head(h_35) = correct digit?
- logit-lens correct-digit rank among all vocab (lower = better)
- logit-lens correct-digit logit vs distractors (SNR)

Output:
  /tmp/results_phase119c_logitlens.json
"""

import json, os, random, time
import numpy as np
import torch
import torch.nn as nn
from torch.optim import AdamW
from transformers import AutoModelForCausalLM, AutoTokenizer

HF_CACHE = os.environ.get("HF_CACHE", "/home/gpgabriel25/hf_cache")
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE
os.environ["HF_HOME"] = HF_CACHE

MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen3-8B")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/tmp/results_phase119c_logitlens.json")

SEEDS = [42, 11, 77]
N_TRAIN = int(os.environ.get("N_TRAIN", "400"))
N_TEST = int(os.environ.get("N_TEST", "200"))
N_STEPS = int(os.environ.get("N_STEPS", "200"))
LR = float(os.environ.get("LR", "2e-4"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "4"))
LORA_RANK = int(os.environ.get("LORA_RANK", "16"))
LORA_ALPHA = float(os.environ.get("LORA_ALPHA", "32.0"))
FINAL_LAYER = int(os.environ.get("FINAL_LAYER", "35"))
MAX_LENGTH = int(os.environ.get("MAX_LENGTH", "256"))


def log(msg):
    print(f"[phase119c] {msg}", flush=True)


ENTITIES = [
    "apple", "car", "dog", "tree", "book",
    "chair", "lamp", "phone", "cloud", "river",
    "bird", "shoe", "ball", "hat", "pen",
    "stone", "star", "fish", "flag", "coin",
]
DIGIT_STRS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def make_entity_counting_prompts(n, seed):
    rng = random.Random(seed)
    prompts, answers = [], []
    while len(prompts) < n:
        entity = rng.choice(ENTITIES)
        count = rng.randint(1, 9)
        n_distractors = rng.randint(0, 3)
        dist_entities = [e for e in ENTITIES if e != entity]
        sentences = []
        dist_counts = {e: rng.randint(1, 4) for e in rng.sample(dist_entities, n_distractors)}
        for _ in range(count):
            sentences.append(f"There are {rng.randint(1,3)} {entity} near the pond.")
        for e, c in dist_counts.items():
            sentences.append(f"There are {c} {e} in the area.")
        rng.shuffle(sentences)
        text = " ".join(sentences)
        prompt = f"{text}\n\nCount how many {entity} there are. Answer with just the number: "
        prompts.append(prompt)
        answers.append(count)
    return prompts, answers


def get_digit_token_ids(tokenizer):
    return [tokenizer.encode(d, add_special_tokens=False)[0] for d in DIGIT_STRS]


def apply_lora_peft(model, rank=16, alpha=32.0):
    from peft import LoraConfig, TaskType, get_peft_model
    lora_config = LoraConfig(
        r=rank, lora_alpha=alpha, target_modules=["q_proj", "v_proj"],
        lora_dropout=0.0, bias="none", task_type=TaskType.CAUSAL_LM,
    )
    model = get_peft_model(model, lora_config)
    n_t = sum(p.numel() for p in model.parameters() if p.requires_grad)
    log(f"  LoRA applied: rank={rank}, alpha={alpha}, trainable={n_t:,}")
    return model


def train_lora(model, tokenizer, prompts, answers, digit_ids, n_steps, lr, bs, seed):
    device = next(model.parameters()).device
    optimizer = AdamW([p for p in model.parameters() if p.requires_grad], lr=lr)
    model.train()
    rng = random.Random(seed)
    n = len(prompts)
    t0 = time.time()
    losses = []
    for step in range(n_steps):
        idx = rng.choices(range(n), k=bs)
        enc = tokenizer([prompts[i] for i in idx], return_tensors="pt", padding=True,
                        truncation=True, max_length=MAX_LENGTH)
        inp = enc["input_ids"].to(device)
        labels = torch.tensor([digit_ids[int(answers[i])-1] for i in idx], dtype=torch.long, device=device)
        logits = model(input_ids=inp).logits[:, -1, :]
        loss = nn.CrossEntropyLoss()(logits, labels)
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
        optimizer.step()
        losses.append(float(loss.item()))
        if (step+1) % 40 == 0 or step == 0:
            log(f"    step {step+1}/{n_steps} loss={np.mean(losses[-20:]):.4f} elapsed={time.time()-t0:.1f}s")
    return time.time() - t0, float(np.mean(losses[-10:]))


def compute_logitlens_metrics(model, tokenizer, prompts, answers, digit_ids, layer_idx):
    """Compute logit-lens: apply lm_head directly to layer-35 hidden states."""
    model.eval()
    device = next(model.parameters()).device
    lm_head = model.get_output_embeddings().weight.detach().to(device=device, dtype=torch.float32)
    # Get the base model for accessing internal layers (works for both
    # base HuggingFace model and PeftModel-wrapped variants)
    base = model
    try:
        from peft import PeftModel
        if isinstance(model, PeftModel):
            base = model.base_model.model  # unwrap to base HF model
    except ImportError:
        pass
    final_ln = base.model.norm  # base.model = Qwen3Model, .norm = final LayerNorm

    results = {"correct": 0, "total": 0, "ranks": [], "correct_logits": [],
               "max_wrong_logits": [], "logit_margin": []}

    with torch.no_grad():
        for i in range(0, len(prompts), 8):
            batch_p = prompts[i:i+8]
            batch_a = answers[i:i+8]
            enc = tokenizer(batch_p, return_tensors="pt", padding=True,
                            truncation=True, max_length=MAX_LENGTH)
            inp = enc["input_ids"].to(device)
            out = model(input_ids=inp, output_hidden_states=True, return_dict=True)
            h = out.hidden_states[layer_idx+1][:, -1, :]  # (B, D)
            h_normed = final_ln(h).float()  # cast to float32 for lm_head matmul
            logits_all = h_normed @ lm_head.T  # (B, V)

            for j, a in enumerate(batch_a):
                correct_id = digit_ids[int(a)-1]
                correct_logit = float(logits_all[j, correct_id].item())
                digit_logits = logits_all[j, digit_ids].cpu().float().numpy()
                digit_argmax_id = digit_ids[int(np.argmax(digit_logits))]

                results["total"] += 1
                results["correct_logits"].append(correct_logit)
                if digit_argmax_id == correct_id:
                    results["correct"] += 1

                # Rank among all vocab
                rank = int((logits_all[j] > correct_logit).sum().item()) + 1
                results["ranks"].append(rank)

                # Best wrong-digit logit
                wrong_logits = [float(logits_all[j, did].item()) for did in digit_ids if did != correct_id]
                results["max_wrong_logits"].append(max(wrong_logits) if wrong_logits else -1e10)

    ranks = np.array(results["ranks"])
    logit_ratio = np.exp(np.array(results["correct_logits"])) / np.exp(np.array(results["max_wrong_logits"]))

    return {
        "accuracy": results["correct"] / max(results["total"], 1),
        "median_rank": float(np.median(ranks)),
        "mean_rank": float(np.mean(ranks)),
        "rank_le_10_frac": float(np.mean(ranks <= 10)),
        "median_logit_ratio": float(np.median(logit_ratio)),
        "mean_correct_logit": float(np.mean(results["correct_logits"])),
        "mean_max_wrong_logit": float(np.mean(results["max_wrong_logits"])),
    }


def main():
    log(f"Phase119c: Logit-lens SNR pre/post LoRA at final layer {FINAL_LAYER}")
    log(f"  model={MODEL_NAME}, seeds={SEEDS}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"  device={device}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=HF_CACHE,
                                               trust_remote_code=True, padding_side="left")
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    digit_ids = get_digit_token_ids(tokenizer)

    all_results = {}
    for seed in SEEDS:
        log(f"\n=== seed {seed} ===")
        prompts, answers = make_entity_counting_prompts(N_TRAIN + N_TEST, seed=seed)
        train_prompts = prompts[:N_TRAIN]
        test_prompts = prompts[N_TRAIN:]
        test_answers = answers[N_TRAIN:]

        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, cache_dir=HF_CACHE, trust_remote_code=True,
            torch_dtype=torch.bfloat16, low_cpu_mem_usage=True,
        ).to(device)
        model.eval()

        # Pre-LoRA logit-lens
        t0 = time.time()
        pre = compute_logitlens_metrics(model, tokenizer, test_prompts, test_answers,
                                        digit_ids, layer_idx=FINAL_LAYER)
        log(f"  pre-LoRA logitlens: acc={pre['accuracy']:.3f} rank_med={pre['median_rank']:.0f} "
            f"logit_ratio={pre['median_logit_ratio']:.1f} ({time.time()-t0:.1f}s)")

        # Train LoRA
        model = apply_lora_peft(model, rank=LORA_RANK, alpha=LORA_ALPHA)
        train_time, final_loss = train_lora(
            model, tokenizer, train_prompts, answers[:N_TRAIN], digit_ids,
            n_steps=N_STEPS, lr=LR, bs=BATCH_SIZE, seed=seed)
        log(f"  training done in {train_time:.1f}s, final_loss={final_loss:.4f}")

        # Post-LoRA logit-lens
        t0 = time.time()
        post = compute_logitlens_metrics(model, tokenizer, test_prompts, test_answers,
                                         digit_ids, layer_idx=FINAL_LAYER)
        log(f"  post-LoRA logitlens: acc={post['accuracy']:.3f} rank_med={post['median_rank']:.0f} "
            f"logit_ratio={post['median_logit_ratio']:.1f} ({time.time()-t0:.1f}s)")

        all_results[str(seed)] = {
            "seed": seed,
            "logitlens_pre": pre,
            "logitlens_post": post,
            "delta": {
                "accuracy": post["accuracy"] - pre["accuracy"],
                "median_rank": post["median_rank"] - pre["median_rank"],
                "median_logit_ratio": post["median_logit_ratio"] / (pre["median_logit_ratio"] + 1e-8),
            },
            "train_time_s": train_time,
            "final_loss": final_loss,
        }

        # Write intermediate
        with open(OUTPUT_PATH, "w") as f:
            json.dump({"metadata": {
                "phase": "119c", "model": MODEL_NAME, "seeds": SEEDS,
                "layer": FINAL_LAYER, "n_train": N_TRAIN, "n_test": N_TEST,
                "lora_rank": LORA_RANK, "lora_alpha": LORA_ALPHA,
            }, "seeds": all_results}, f, indent=2)
        log(f"  wrote intermediate {OUTPUT_PATH}")

    # Summary
    acc_pre = np.mean([all_results[str(s)]["logitlens_pre"]["accuracy"] for s in SEEDS])
    acc_post = np.mean([all_results[str(s)]["logitlens_post"]["accuracy"] for s in SEEDS])
    rank_pre = np.mean([all_results[str(s)]["logitlens_pre"]["median_rank"] for s in SEEDS])
    rank_post = np.mean([all_results[str(s)]["logitlens_post"]["median_rank"] for s in SEEDS])
    log(f"\nPhase119c complete.")
    log(f"  pre-LoRA logitlens acc: {acc_pre:.3f} rank_med: {rank_pre:.0f}")
    log(f"  post-LoRA logitlens acc: {acc_post:.3f} rank_med: {rank_post:.0f}")
    log(f"  results saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
