"""
Phase 116: Zero-Training Norm-Rescaling Intervention

Hypothesis: digit rows are at 12-29th percentile of lm_head norms, creating
norm competition that suppresses digit tokens in full-vocabulary argmax.
If we directly rescale digit rows to match the median lm_head row norm, we
should remove this competition without any training.

Approach:
1. Load Qwen3-8B
2. Compute lm_head.weight row norms
3. Rescale digit rows [1-9] to target_norm (test multiple targets: 25th, 50th, 75th percentile)
4. Evaluate fullvocab counting accuracy on entity_counting test prompts (N=200, 3 seeds)
5. Compare to baseline 60.3%

Expected outcome: fullvocab accuracy increases if norm competition is the binding constraint.
Kill criterion: if max rescaling target gives < 55% accuracy, norm is not the primary bottleneck.
"""

import os
import json
import time
import torch
import numpy as np
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

# ========== Configuration ==========
MODEL_NAME = "Qwen/Qwen3-8B"
HF_CACHE = os.environ.get("HF_CACHE", "/home/gpgabriel25/hf_cache")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
N_TEST = 200
SEEDS = [42, 11, 77]
MAX_NEW_TOKENS = 1

# Digit token IDs for Qwen3-8B (1-9)
DIGIT_IDS = [16, 17, 18, 19, 20, 21, 22, 23, 24]  # 1,2,3,4,5,6,7,8,9

# Output path
OUT_PATH = Path(__file__).parent.parent.parent / "results_phase116_norm_rescaling.json"
LOG_DIR = Path(__file__).parent.parent.parent / "logs" / f"phase116_{int(time.time())}"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ========== Data Generation ==========
def generate_entity_counting_prompt(count, seed_offset=0, template_idx=0):
    """Generate entity counting prompts: 'How many [entity] are in this list?'"""
    rng = np.random.default_rng(42 + seed_offset * 1000 + template_idx * 100)
    
    entity_pools = [
        ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"],
        ["cat", "dog", "bird", "fish", "rabbit", "hamster", "turtle"],
        ["red", "blue", "green", "yellow", "purple", "orange", "pink"],
        ["book", "pen", "notebook", "eraser", "ruler", "pencil", "stapler"],
    ]
    
    entity_type_idx = template_idx % len(entity_pools)
    pool = entity_pools[entity_type_idx]
    
    # Sample `count` entities without replacement (pad pool if needed)
    if count > len(pool):
        # sample with replacement
        chosen = rng.choice(pool, size=count, replace=True).tolist()
    else:
        chosen = rng.choice(pool, size=count, replace=False).tolist()
    
    # Add distractors from a different pool (1-2)
    n_distractor = rng.integers(0, 3)
    distractor_pool_idx = (entity_type_idx + 1) % len(entity_pools)
    distractors = entity_pools[distractor_pool_idx]
    if n_distractor > 0:
        distractor_words = rng.choice(distractors, size=n_distractor, replace=False).tolist()
    else:
        distractor_words = []
    
    all_items = chosen + distractor_words
    rng.shuffle(all_items)
    
    entity = pool[0]  # use pool name as entity type
    item_list = ", ".join(all_items)
    
    prompts = [
        f"List: {item_list}\nHow many {entity}s are in this list? Answer with a single digit:",
        f"Items: {item_list}\nCount the number of {entity}s. Reply with one digit:",
        f"Given: {item_list}\nHow many {entity}s appear? Answer:",
    ]
    
    return prompts[template_idx % len(prompts)], count


def generate_test_set(n_per_count=25, counts=range(1, 9), seed=42):
    """Generate balanced test set across counts 1-8."""
    rng = np.random.default_rng(seed)
    prompts = []
    labels = []
    
    for count in counts:
        for i in range(n_per_count):
            template_idx = (i * 7 + count * 3) % 100
            prompt, true_count = generate_entity_counting_prompt(
                count, seed_offset=seed + i, template_idx=template_idx
            )
            prompts.append(prompt)
            labels.append(true_count)
    
    return prompts, labels


# ========== Evaluation ==========
def evaluate_fullvocab(model, tokenizer, prompts, labels, device, batch_size=16):
    """Evaluate fullvocab accuracy: argmax over all 152K tokens."""
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for i in range(0, len(prompts), batch_size):
            batch_prompts = prompts[i:i+batch_size]
            batch_labels = labels[i:i+batch_size]
            
            inputs = tokenizer(
                batch_prompts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            ).to(device)
            
            outputs = model(**inputs)
            logits = outputs.logits  # [B, T, V]
            
            # Get last-token logits
            last_token_logits = logits[:, -1, :]  # [B, V]
            
            # Fullvocab argmax
            pred_ids = last_token_logits.argmax(dim=-1)  # [B]
            
            for j, (pred_id, true_count) in enumerate(zip(pred_ids.tolist(), batch_labels)):
                # Map pred_id to digit (1-9) if it's a digit token
                if pred_id in DIGIT_IDS:
                    pred_digit = DIGIT_IDS.index(pred_id) + 1
                else:
                    pred_digit = -1  # non-digit prediction
                
                if pred_digit == true_count:
                    correct += 1
                total += 1
    
    return correct / total if total > 0 else 0.0


def evaluate_constrained(model, tokenizer, prompts, labels, device, batch_size=16):
    """Evaluate constrained accuracy: argmax over 9 digit tokens only."""
    model.eval()
    correct = 0
    total = 0
    digit_ids_tensor = torch.tensor(DIGIT_IDS, device=device)
    
    with torch.no_grad():
        for i in range(0, len(prompts), batch_size):
            batch_prompts = prompts[i:i+batch_size]
            batch_labels = labels[i:i+batch_size]
            
            inputs = tokenizer(
                batch_prompts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            ).to(device)
            
            outputs = model(**inputs)
            logits = outputs.logits[:, -1, :]  # [B, V]
            
            # Constrained argmax: only over digit tokens
            digit_logits = logits[:, digit_ids_tensor]  # [B, 9]
            pred_digit_indices = digit_logits.argmax(dim=-1)  # [B]
            
            for j, (pred_idx, true_count) in enumerate(zip(pred_digit_indices.tolist(), batch_labels)):
                pred_digit = pred_idx + 1  # 0-indexed → 1-indexed
                if pred_digit == true_count:
                    correct += 1
                total += 1
    
    return correct / total if total > 0 else 0.0


# ========== Norm Rescaling ==========
def get_norm_percentiles(weight):
    """Get row-norm percentiles for lm_head weight matrix."""
    norms = weight.norm(dim=1)
    digit_norms = norms[DIGIT_IDS]
    all_norms_sorted = norms.sort().values
    
    return {
        "digit_norms": digit_norms.tolist(),
        "digit_norm_mean": digit_norms.mean().item(),
        "digit_norm_min": digit_norms.min().item(),
        "digit_norm_max": digit_norms.max().item(),
        "all_norm_p10": all_norms_sorted[int(0.10 * len(all_norms_sorted))].item(),
        "all_norm_p25": all_norms_sorted[int(0.25 * len(all_norms_sorted))].item(),
        "all_norm_p50": all_norms_sorted[int(0.50 * len(all_norms_sorted))].item(),
        "all_norm_p75": all_norms_sorted[int(0.75 * len(all_norms_sorted))].item(),
        "all_norm_p90": all_norms_sorted[int(0.90 * len(all_norms_sorted))].item(),
    }


def apply_norm_rescaling(model, target_norm, digit_ids=DIGIT_IDS):
    """
    Rescale digit rows in lm_head to have L2 norm = target_norm.
    Returns a copy of the weight tensor (does not modify in-place).
    """
    with torch.no_grad():
        w = model.lm_head.weight.clone()
        for idx in digit_ids:
            current_norm = w[idx].norm()
            if current_norm > 1e-8:
                w[idx] = w[idx] * (target_norm / current_norm)
        model.lm_head.weight.data.copy_(w)


def restore_original_weights(model, original_weight):
    """Restore lm_head weights to original."""
    with torch.no_grad():
        model.lm_head.weight.data.copy_(original_weight)


# ========== Main ==========
def main():
    print(f"[Phase116] Starting norm-rescaling experiment")
    print(f"[Phase116] Device: {DEVICE}")
    print(f"[Phase116] Model: {MODEL_NAME}")
    print(f"[Phase116] Output: {OUT_PATH}")
    
    # Load model and tokenizer
    print("[Phase116] Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=HF_CACHE, trust_remote_code=True)
    
    print("[Phase116] Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        cache_dir=HF_CACHE,
        torch_dtype=torch.bfloat16,
        device_map="auto" if DEVICE == "cuda" else None,
        trust_remote_code=True,
    )
    if DEVICE != "cuda":
        model = model.to(DEVICE)
    model.eval()
    
    # Verify digit token IDs
    print("[Phase116] Verifying digit token IDs...")
    for i, (digit, tid) in enumerate(zip(range(1, 10), DIGIT_IDS)):
        decoded = tokenizer.decode([tid])
        print(f"  digit {digit} → token_id {tid} → '{decoded}'")
    assert len(set(DIGIT_IDS)) == 9, "DIGIT_IDS must have 9 unique tokens"
    
    # Save original lm_head weights
    original_weight = model.lm_head.weight.data.clone()
    
    # Compute baseline norm statistics
    print("[Phase116] Computing norm statistics...")
    norm_stats = get_norm_percentiles(original_weight)
    print(f"  Digit norm mean: {norm_stats['digit_norm_mean']:.4f}")
    print(f"  All norms: p10={norm_stats['all_norm_p10']:.4f}, p25={norm_stats['all_norm_p25']:.4f}, "
          f"p50={norm_stats['all_norm_p50']:.4f}, p75={norm_stats['all_norm_p75']:.4f}")
    
    results = {
        "model": MODEL_NAME,
        "digit_ids": DIGIT_IDS,
        "norm_stats": norm_stats,
        "conditions": {},
        "summary": {},
    }
    
    # Target norms to test: multiple percentiles
    target_norms = {
        "baseline": None,  # no modification
        "p25": norm_stats["all_norm_p25"],
        "p50": norm_stats["all_norm_p50"],
        "p75": norm_stats["all_norm_p75"],
        "p90": norm_stats["all_norm_p90"],
        "2x_current": norm_stats["digit_norm_mean"] * 2.0,
        "3x_current": norm_stats["digit_norm_mean"] * 3.0,
    }
    
    for condition_name, target_norm in target_norms.items():
        print(f"\n[Phase116] Condition: {condition_name} (target_norm={target_norm})")
        
        # Apply (or restore) rescaling
        if target_norm is not None:
            apply_norm_rescaling(model, target_norm)
        else:
            restore_original_weights(model, original_weight)
        
        fullvocab_scores = []
        constrained_scores = []
        
        for seed in SEEDS:
            prompts, labels = generate_test_set(n_per_count=N_TEST // 8, seed=seed)
            
            fv = evaluate_fullvocab(model, tokenizer, prompts, labels, DEVICE)
            cs = evaluate_constrained(model, tokenizer, prompts, labels, DEVICE)
            
            fullvocab_scores.append(fv)
            constrained_scores.append(cs)
            
            print(f"  Seed {seed}: fullvocab={fv:.4f}, constrained={cs:.4f}")
        
        results["conditions"][condition_name] = {
            "target_norm": target_norm,
            "fullvocab_per_seed": fullvocab_scores,
            "fullvocab_mean": float(np.mean(fullvocab_scores)),
            "fullvocab_std": float(np.std(fullvocab_scores)),
            "constrained_per_seed": constrained_scores,
            "constrained_mean": float(np.mean(constrained_scores)),
            "constrained_std": float(np.std(constrained_scores)),
        }
        
        print(f"  → fullvocab mean={np.mean(fullvocab_scores):.4f} ± {np.std(fullvocab_scores):.4f}")
        print(f"  → constrained mean={np.mean(constrained_scores):.4f} ± {np.std(constrained_scores):.4f}")
    
    # Restore original weights before exiting
    restore_original_weights(model, original_weight)
    
    # Summary
    baseline_fv = results["conditions"]["baseline"]["fullvocab_mean"]
    best_condition = max(
        [(k, v["fullvocab_mean"]) for k, v in results["conditions"].items()],
        key=lambda x: x[1]
    )
    results["summary"] = {
        "baseline_fullvocab": baseline_fv,
        "best_condition": best_condition[0],
        "best_fullvocab": best_condition[1],
        "improvement": best_condition[1] - baseline_fv,
        "norm_competition_is_binding": best_condition[1] > baseline_fv + 0.05,
    }
    
    print(f"\n[Phase116] Summary:")
    print(f"  Baseline fullvocab: {baseline_fv:.4f}")
    print(f"  Best condition: {best_condition[0]} → {best_condition[1]:.4f}")
    print(f"  Improvement: {best_condition[1] - baseline_fv:+.4f}")
    print(f"  Norm competition is binding: {results['summary']['norm_competition_is_binding']}")
    
    # Save results
    with open(OUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[Phase116] Results saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
