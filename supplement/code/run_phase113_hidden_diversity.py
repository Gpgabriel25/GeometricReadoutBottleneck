#!/usr/bin/env python3
"""
Phase 113: Hidden State Diversity Analysis

Scientific question:
Phase112 showed list_length fullvocab repair achieves 92.7% while entity counting 
achieves only 42.7%/60.3% (with Phase107 optimized training). Both tasks start at 
0% baseline fullvocab and have ~100% probe-round accuracy.

Hypothesis: Entity counting has higher within-count hidden state variance than 
list_length, explaining why 9-row repair generalizes better for list_length.

Method:
  For each task and each count value k (1..9):
  1. Extract last-layer hidden states for all examples where answer=k
  2. Compute within-count variance (mean of diagonal of covariance matrix)
  3. Compare average within-count variance across tasks

Prediction:
  - entity_counting: highest variance (diverse prompts: different entities/distractors)
  - list_length: lowest variance (uniform format: comma-separated items)
  - char_count: intermediate
  - addition: lowest (arithmetic always same format)

Results of this analysis will explain the repair generalization gap mechanistically.

Also compute:
  - Max competitor logit mean/std per task (why do digits fail to win in fullvocab?)
  - Digit logit margin (correct digit - max non-digit) per task
"""

import gc
import json
import os
import random
import time

import numpy as np

os.environ.setdefault("HF_HOME", os.environ.get("HF_CACHE", "./hf_cache"))
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")

import torch

print(f"PyTorch: {torch.__version__}")


# ── Task generators (same as Phase97/Phase112) ────────────────────────────────

def gen_entity_counting(n, seed=42):
    rng = random.Random(seed)
    entities = ["cat", "dog", "bird", "fish", "frog", "bear", "wolf", "duck"]
    distractors = ["tree", "rock", "cloud", "table", "river", "lamp", "chair"]
    prompts = []
    attempts = 0
    while len(prompts) < n and attempts < n * 50:
        attempts += 1
        entity = rng.choice(entities)
        count = rng.randint(1, 9)
        n_dist = rng.randint(0, 4)
        total_slots = count + n_dist
        positions = list(range(total_slots))
        rng.shuffle(positions)
        entity_positions = positions[:count]
        parts = []
        for i in range(total_slots):
            if i in entity_positions:
                parts.append(entity)
            else:
                parts.append(rng.choice(distractors))
        text = " ".join(parts) + f" How many {entity} are there? Answer:"
        if 1 <= count <= 9:
            prompts.append({"text": text, "answer": count})
    return prompts[:n]


def gen_char_count(n, seed=42):
    rng = random.Random(seed)
    words = [
        "banana", "mississippi", "abracadabra", "bookkeeper", "committee",
        "accommodate", "occurrence", "possession", "millennium", "assassin",
        "balloon", "broccoli", "cappuccino", "desiccate", "embarrass",
        "necessary", "recommend", "vaccination", "tobacco", "Tennessee",
        "appellation", "accession", "accessible", "successfully", "communication",
        "association", "acceleration", "inappropriate", "accessibility", "appreciation",
    ]
    prompts = []
    attempts = 0
    while len(prompts) < n and attempts < n * 50:
        attempts += 1
        word = rng.choice(words).lower()
        letters = list(set(word))
        letter = rng.choice(letters)
        count = word.count(letter)
        if 1 <= count <= 9:
            text = f"How many times does '{letter}' appear in '{word}'? Answer:"
            prompts.append({"text": text, "answer": count})
    return prompts[:n]


def gen_addition(n, seed=42):
    rng = random.Random(seed)
    prompts = []
    for _ in range(n):
        result = rng.randint(1, 9)
        a = rng.randint(0, result)
        b = result - a
        if a == 0:
            a, b = b, a
        text = f"{a}+{b}="
        prompts.append({"text": text, "answer": result})
    return prompts


def gen_list_length(n, seed=42):
    rng = random.Random(seed)
    items_pool = [
        "apple", "banana", "cherry", "date", "elderberry", "fig", "grape",
        "honeydew", "kiwi", "lemon", "mango", "nectarine", "orange", "papaya",
        "quince", "raspberry", "strawberry", "tangerine", "watermelon", "plum",
        "pear", "peach", "apricot", "blueberry", "cranberry", "guava", "lime",
    ]
    prompts = []
    for _ in range(n):
        count = rng.randint(1, 9)
        items = rng.sample(items_pool, min(count, len(items_pool)))
        text = f"Items: {', '.join(items)}. Count:"
        prompts.append({"text": text, "answer": count})
    return prompts


TASK_GENERATORS = {
    "entity_counting": gen_entity_counting,
    "char_count": gen_char_count,
    "addition": gen_addition,
    "list_length": gen_list_length,
}


def load_model_and_tokenizer(model_name="Qwen/Qwen3-8B"):
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    model.eval()
    return model, tokenizer


def get_digit_token_ids(tokenizer):
    ids = []
    for d in range(1, 10):
        toks = tokenizer.encode(str(d), add_special_tokens=False)
        for t in toks:
            if tokenizer.decode([t]).strip() == str(d):
                ids.append(t)
                break
    if len(ids) != 9 or len(set(ids)) != 9:
        raise RuntimeError(f"Failed to map unique digit tokens 1..9, got: {ids}")
    return ids


def extract_last_layer_hiddens(model, tokenizer, prompts, batch_size=16):
    """Extract only last layer hidden states (fast)."""
    device = next(model.parameters()).device
    all_hiddens = []
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        texts = [p["text"] for p in batch]
        inputs = tokenizer(texts, return_tensors="pt", padding=True, 
                          truncation=True, max_length=256)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            out = model(**inputs, output_hidden_states=True)
        seq_lens = inputs["attention_mask"].sum(dim=1) - 1
        last_h = out.hidden_states[-1]  # last layer only
        row_idx = torch.arange(len(batch), device=device)
        last = last_h[row_idx, seq_lens]  # [batch, hidden]
        all_hiddens.append(last.float().cpu().numpy())
        if (i // batch_size) % 10 == 0:
            print(f"    {i + len(batch)}/{len(prompts)}")
    return np.concatenate(all_hiddens, axis=0)  # [N, hidden]


def analyze_task_diversity(hiddens, answers, task_name):
    """Compute within-count variance and other diversity metrics."""
    hiddens = np.array(hiddens)
    answers = np.array(answers)
    n, d = hiddens.shape
    
    within_count_variances = []
    count_stats = {}
    pooled_within_ss = 0.0
    pooled_within_dof = 0
    
    for count_val in range(1, 10):
        mask = answers == count_val
        n_k = mask.sum()
        if n_k < 3:
            continue
        h_k = hiddens[mask]  # [n_k, d]
        mean_k = h_k.mean(axis=0)
        
        # Within-count variance (mean over dimensions)
        var_k = ((h_k - mean_k) ** 2).mean()
        within_count_variances.append(float(var_k))
        pooled_within_ss += float(((h_k - mean_k) ** 2).sum())
        pooled_within_dof += int(h_k.size)
        
        # Also compute norm of mean
        norm_mean = float(np.linalg.norm(mean_k))
        count_stats[count_val] = {
            "n": int(n_k),
            "within_var": float(var_k),
            "mean_norm": norm_mean,
        }
    
    mean_within_var = float(np.mean(within_count_variances))
    pooled_within_var = float(pooled_within_ss / max(1, pooled_within_dof))
    
    # Also compute total variance (across all examples)
    total_mean = hiddens.mean(axis=0)
    total_var = float(((hiddens - total_mean) ** 2).mean())
    
    # Intra-class ratio: within_var / total_var (lower = more separable)
    ratio = float(pooled_within_var / (total_var + 1e-10))
    
    print(f"\n  {task_name}: within-count var(unweighted)={mean_within_var:.4f}, "
          f"within-count var(weighted)={pooled_within_var:.4f}, "
          f"total var={total_var:.4f}, ratio={ratio:.4f}")
    for cv, stats in count_stats.items():
        print(f"    count={cv}: n={stats['n']}, var={stats['within_var']:.4f}")
    
    return {
        "task": task_name,
        "mean_within_count_var": float(mean_within_var),
        "pooled_within_count_var": float(pooled_within_var),
        "total_var": float(total_var),
        "intra_class_ratio": float(ratio),
        "count_stats": count_stats,
    }


def analyze_competitor_logits(lm_head, hiddens, answers, digit_token_ids, task_name):
    """Analyze how much digit logits are beaten by non-digit competitors."""
    non_digit_mask = np.ones(lm_head.shape[0], dtype=bool)
    for tid in digit_token_ids:
        non_digit_mask[tid] = False
    W_non = lm_head[non_digit_mask]
    
    # Compute all logits
    digit_logits = hiddens @ lm_head[digit_token_ids].T  # [N, 9]
    non_digit_max = (hiddens @ W_non.T).max(axis=1)  # [N]
    
    # For each example, get the correct digit logit
    correct_digit_idx = np.array([a - 1 for a in answers], dtype=np.int64)
    correct_digit_logits = digit_logits[np.arange(len(answers)), correct_digit_idx]
    digit_logits_others = digit_logits.copy()
    digit_logits_others[np.arange(len(answers)), correct_digit_idx] = -np.inf
    max_other_digit = digit_logits_others.max(axis=1)
    
    # Margin: correct_digit_logit - max_competitor (negative = digit loses)
    margin = correct_digit_logits - np.maximum(non_digit_max, max_other_digit)  # [N]
    
    # Win rate (digit > all competitors)
    win_rate = (margin > 0).mean()
    
    print(f"\n  {task_name} competitor analysis:")
    print(f"    Digit margin mean: {margin.mean():.3f} ± {margin.std():.3f}")
    print(f"    Win rate (digit > all competitors): {win_rate:.4f}")
    print(f"    Max competitor logit: mean={non_digit_max.mean():.3f}")
    
    return {
        "digit_margin_mean": float(margin.mean()),
        "digit_margin_std": float(margin.std()),
        "win_rate": float(win_rate),
        "max_competitor_mean": float(non_digit_max.mean()),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", nargs="+", default=list(TASK_GENERATORS.keys()))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n", type=int, default=800)
    parser.add_argument("--output", type=str, 
                        default="results_phase113_hidden_diversity.json")
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-8B")
    args = parser.parse_args()
    
    t0 = time.time()
    print(f"Phase113: Hidden state diversity analysis on tasks: {args.tasks}")
    print(f"N={args.n}, seed={args.seed}")
    
    model, tokenizer = load_model_and_tokenizer(args.model)
    digit_token_ids = get_digit_token_ids(tokenizer)
    lm_head = model.lm_head.weight.detach().float().cpu().numpy()
    
    all_results = {}
    
    for task_name in args.tasks:
        if task_name not in TASK_GENERATORS:
            raise ValueError(f"Unknown task '{task_name}'. Allowed: {sorted(TASK_GENERATORS.keys())}")
        
        print(f"\n{'='*50}")
        print(f"TASK: {task_name}")
        print(f"{'='*50}")
        
        prompts = TASK_GENERATORS[task_name](args.n, seed=args.seed)
        if len(prompts) != args.n:
            raise RuntimeError(
                f"Task {task_name} generated {len(prompts)} prompts, expected {args.n}."
            )
        answers = [p["answer"] for p in prompts]
        
        print(f"  Extracting hidden states for {len(prompts)} prompts...")
        hiddens = extract_last_layer_hiddens(model, tokenizer, prompts, batch_size=16)
        print(f"  Hidden shape: {hiddens.shape}")
        
        # Diversity analysis
        diversity = analyze_task_diversity(hiddens, np.array(answers), task_name)
        
        # Competitor logit analysis
        competitor = analyze_competitor_logits(
            lm_head, hiddens, answers, digit_token_ids, task_name
        )
        
        all_results[task_name] = {**diversity, "competitor_stats": competitor}
        
        # Save intermediate
        with open(args.output, "w") as f:
            json.dump(all_results, f, indent=2)
        
        del hiddens
        gc.collect()
    
    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")
    
    # Final comparison
    print("\n" + "="*60)
    print("FINAL COMPARISON: Within-Count Variance vs Repair Effectiveness")
    print("="*60)
    print(f"{'Task':<20} {'Within-Var':>12} {'Intra-Ratio':>12} {'Win-Rate':>10}")
    print("-"*60)
    for task, res in all_results.items():
        wr = res["competitor_stats"]["win_rate"]
        print(f"{task:<20} {res['mean_within_count_var']:>11.4f} "
              f"{res['intra_class_ratio']:>11.4f} {wr:>9.4f}")
    
    with open(args.output, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
