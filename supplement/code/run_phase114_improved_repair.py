#!/usr/bin/env python3
"""
Phase 114: Improved Fullvocab Repair for Entity Counting

Goal: Push entity counting fullvocab repair beyond 60.3% (Phase107 baseline).

Key improvements over Phase107/Phase112:
1. Cross-entropy loss (softmax over full vocab) instead of margin-hinge
   - CE gives proper gradient signal from ALL 151K competitors, not just max
   - More stable gradients, especially for borderline cases
2. Count-stratified oversampling (counts 4-7 get 3x weight)
   - Counts 4-7 have worst repair accuracy (30-51% per Table in paper)
   - Focusing training on hard cases may improve overall accuracy
3. L2 norm regularization (controlled norm growth)
   - Phase111 showed digit norms are at 12-29th percentile
   - Allow norm to grow but not too much (preserve other behaviors)
4. More training steps (2000 vs 500)
5. Separate learning rates: higher for hard-count rows (counts 4-7)

Expected: 65-75% fullvocab accuracy (vs 60.3% Phase107, 42.7% Phase112)

Protocol: Qwen3-8B, seeds 11/77/42, N_train=800, N_test=300
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
    print(f"Digit token IDs (1-9): {ids}")
    return ids


def extract_last_layer_hiddens(model, tokenizer, prompts, batch_size=16):
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
        last_h = out.hidden_states[-1]
        row_idx = torch.arange(len(batch), device=device)
        last = last_h[row_idx, seq_lens].float().cpu().numpy()
        all_hiddens.append(last)
        if (i // batch_size) % 5 == 0:
            print(f"  {i + len(batch)}/{len(prompts)}")
    return np.concatenate(all_hiddens, axis=0)


def compute_non_digit_stats(hiddens, W_non, chunk_size=2048):
    """Compute per-example max(non-digit) and logsumexp(non-digit logits) in chunks."""
    N = hiddens.shape[0]
    max_logits = np.full(N, -np.inf, dtype=np.float64)
    sumexp_scaled = np.zeros(N, dtype=np.float64)

    for start in range(0, W_non.shape[0], chunk_size):
        end = min(start + chunk_size, W_non.shape[0])
        chunk_logits = hiddens @ W_non[start:end].T  # [N, chunk]
        chunk_max = chunk_logits.max(axis=1)
        new_max = np.maximum(max_logits, chunk_max)

        sumexp_scaled = (
            sumexp_scaled * np.exp(max_logits - new_max)
            + np.exp(chunk_logits - new_max[:, np.newaxis]).sum(axis=1)
        )
        max_logits = new_max

    logsumexp_logits = max_logits + np.log(sumexp_scaled + 1e-300)
    return max_logits, logsumexp_logits


def ce_loss_and_grad(hiddens, answers, digit_token_ids, W_digit,
                     non_digit_max, non_digit_logsumexp, count_weights=None):
    """
    Cross-entropy loss for fullvocab repair (CPU numpy).
    Only digit rows are modified; non-digit rows are fixed.
    
    Returns: (loss, grad_W_digit [9, hidden])
    """
    N = len(hiddens)
    if count_weights is None:
        count_weights = np.ones(N)
    
    # Compute digit logits [N, 9]
    digit_logits = hiddens @ W_digit.T  # [N, 9]
    max_non_digit = non_digit_max[:, np.newaxis]  # [N, 1]
    max_digit = digit_logits.max(axis=1, keepdims=True)  # [N, 1]
    max_all = np.maximum(max_non_digit, max_digit)  # [N, 1]
    
    # Softmax denominator
    exp_digits = np.exp(digit_logits - max_all)  # [N, 9]
    exp_non_digit_sum = np.exp(non_digit_logsumexp[:, np.newaxis] - max_all)  # [N, 1]
    
    denom = exp_digits.sum(axis=1, keepdims=True) + exp_non_digit_sum  # [N, 1]
    
    # Loss: -log(softmax(correct_digit_logit))
    correct_digit_idx = np.array([a - 1 for a in answers], dtype=np.int64)  # 0..8
    correct_exp = exp_digits[np.arange(N), correct_digit_idx]  # [N]
    probs = correct_exp / denom.squeeze()  # [N]
    loss_per = -np.log(probs + 1e-10)  # [N]
    
    weighted_loss = (loss_per * count_weights).sum() / (count_weights.sum() + 1e-10)
    
    # Gradient: for each example, 
    # dL/dW[d] = softmax(z)[d] * h - (if d == correct) h
    # = (softmax(z)[d] - 1_{d==correct}) * h
    soft_digits = exp_digits / denom  # [N, 9]  (softmax over full vocab for digit positions)
    delta = soft_digits.copy()  # [N, 9]
    delta[np.arange(N), correct_digit_idx] -= 1.0  # [N, 9]
    
    # Weight by count_weights
    delta_weighted = delta * count_weights[:, np.newaxis]  # [N, 9]
    
    # Gradient: [9, hidden]
    grad = (delta_weighted.T @ hiddens) / (count_weights.sum() + 1e-10)  # [9, hidden]
    
    # True full-vocab accuracy proxy for checkpointing:
    # correct digit must beat all non-digits and all other digits.
    correct_logits = digit_logits[np.arange(N), correct_digit_idx]
    max_nd = non_digit_max
    digit_logits_others = digit_logits.copy()
    digit_logits_others[np.arange(N), correct_digit_idx] = -np.inf
    max_other_digit = digit_logits_others.max(axis=1)
    fv_acc2 = (correct_logits > np.maximum(max_nd, max_other_digit)).mean()
    
    return weighted_loss, grad, fv_acc2


def improved_fullvocab_repair(
    lm_head,
    digit_token_ids,
    hiddens_train,
    answers_train,
    n_iters=2000,
    lr=0.01,
    l2_reg=0.001,
    hard_count_weight=3.0,
):
    """
    Improved fullvocab repair using CE loss with count-stratified weights.
    
    hard_count_weight: extra weight for counts 4-7 (hardest cases).
    """
    if hard_count_weight <= 0:
        raise ValueError(f"hard_count_weight must be > 0, got {hard_count_weight}")

    W = lm_head.copy()
    W_digit = np.array([W[tid] for tid in digit_token_ids], dtype=np.float32)  # [9, hidden]
    W_digit_orig = W_digit.copy()  # Keep original for L2 reg
    
    non_digit_mask = np.ones(W.shape[0], dtype=bool)
    for tid in digit_token_ids:
        non_digit_mask[tid] = False
    W_non = W[non_digit_mask].astype(np.float32)  # [V-9, hidden]

    print("  Precomputing non-digit stats (one-time)...")
    non_digit_max, non_digit_logsumexp = compute_non_digit_stats(
        hiddens_train.astype(np.float32), W_non, chunk_size=2048
    )
    print(f"  Non-digit max logit: mean={non_digit_max.mean():.3f}, std={non_digit_max.std():.3f}")
    
    # Count-stratified weights
    count_weights = np.array([
        hard_count_weight if a in [4, 5, 6, 7] else 1.0
        for a in answers_train
    ])
    
    print(f"  Count weight distribution: {np.bincount([int(a in [4,5,6,7]) for a in answers_train], minlength=2)}")
    
    # Adam optimizer state
    m = np.zeros_like(W_digit)
    v = np.zeros_like(W_digit)
    beta1, beta2, eps = 0.9, 0.999, 1e-8
    
    best_W_digit = W_digit.copy()
    best_fv_acc = 0.0
    
    for it in range(n_iters):
        loss, grad, fv_acc = ce_loss_and_grad(
            hiddens_train, answers_train, digit_token_ids,
            W_digit, non_digit_max, non_digit_logsumexp, count_weights
        )
        
        # Add L2 regularization (pull back toward original)
        l2_total = float(0.5 * l2_reg * ((W_digit - W_digit_orig) ** 2).sum())
        grad += l2_reg * (W_digit - W_digit_orig)
        
        total_loss = float(loss) + l2_total
        
        if fv_acc > best_fv_acc:
            best_fv_acc = fv_acc
            best_W_digit = W_digit.copy()
        
        # Adam update
        t = it + 1
        m = beta1 * m + (1 - beta1) * grad
        v = beta2 * v + (1 - beta2) * (grad ** 2)
        m_hat = m / (1 - beta1 ** t)
        v_hat = v / (1 - beta2 ** t)
        W_digit = W_digit - lr * m_hat / (np.sqrt(v_hat) + eps)
        
        if it % 200 == 0:
            print(f"    iter {it}: loss={total_loss:.4f} (CE={loss:.4f}, L2={l2_total:.4f}), "
                  f"train_fv_acc={fv_acc:.4f}")
    
    print(f"  Best train fullvocab acc: {best_fv_acc:.4f}")
    
    # Insert best digit rows back
    W_repaired = W.copy()
    for i, tid in enumerate(digit_token_ids):
        W_repaired[tid] = best_W_digit[i].astype(W.dtype)
    
    return W_repaired


def evaluate_fullvocab(hiddens_test, answers_test, lm_head, digit_token_ids):
    """Full-vocabulary accuracy: argmax over all vocab == correct digit token."""
    logits = hiddens_test @ lm_head.T
    predicted = logits.argmax(axis=1)
    correct = sum(predicted[i] == digit_token_ids[a-1] for i, a in enumerate(answers_test))
    return correct / len(answers_test)


def evaluate_constrained(hiddens_test, answers_test, lm_head, digit_token_ids):
    """Constrained accuracy: argmax over 9 digit tokens."""
    digit_logits = hiddens_test @ lm_head[digit_token_ids].T
    pred = digit_logits.argmax(axis=1) + 1
    correct = sum(p == a for p, a in zip(pred, answers_test))
    return correct / len(answers_test)


def run_entity_counting_experiment(
    model, tokenizer, digit_token_ids,
    seeds=(11, 77, 42), n_train=800, n_test=300,
    n_iters=2000, lr=0.01, l2_reg=0.001, hard_count_weight=3.0,
):
    lm_head = model.lm_head.weight.detach().float().cpu().numpy()
    print(f"lm_head shape: {lm_head.shape}")
    
    results_by_seed = {}
    
    for seed in seeds:
        print(f"\n{'='*50}")
        print(f"SEED {seed}")
        print(f"{'='*50}")
        
        all_prompts = gen_entity_counting(n_train + n_test, seed=seed)
        train_prompts = all_prompts[:n_train]
        test_prompts = all_prompts[n_train:n_train + n_test]
        
        train_answers = [p["answer"] for p in train_prompts]
        test_answers = [p["answer"] for p in test_prompts]
        
        print(f"  Train count distribution: {np.bincount(train_answers, minlength=10)[1:]}")
        print(f"  Test count distribution: {np.bincount(test_answers, minlength=10)[1:]}")
        
        print("  Extracting train hiddens...")
        train_hiddens = extract_last_layer_hiddens(model, tokenizer, train_prompts, batch_size=16)
        print("  Extracting test hiddens...")
        test_hiddens = extract_last_layer_hiddens(model, tokenizer, test_prompts, batch_size=16)
        
        # Baseline
        baseline_constrained = evaluate_constrained(test_hiddens, test_answers, lm_head, digit_token_ids)
        baseline_fv = evaluate_fullvocab(test_hiddens, test_answers, lm_head, digit_token_ids)
        
        print(f"  Baseline constrained: {baseline_constrained:.4f}")
        print(f"  Baseline fullvocab: {baseline_fv:.4f}")
        
        # Improved repair
        print("  Running improved CE repair...")
        lm_head_repaired = improved_fullvocab_repair(
            lm_head, digit_token_ids, train_hiddens, train_answers,
            n_iters=n_iters, lr=lr, l2_reg=l2_reg, hard_count_weight=hard_count_weight,
        )
        
        repair_fv = evaluate_fullvocab(test_hiddens, test_answers, lm_head_repaired, digit_token_ids)
        repair_constrained = evaluate_constrained(test_hiddens, test_answers, lm_head_repaired, digit_token_ids)
        
        print(f"  Repair fullvocab: {repair_fv:.4f}")
        print(f"  Repair constrained: {repair_constrained:.4f}")
        
        # Per-count analysis
        per_count_repair = {}
        for cv in range(1, 10):
            mask = np.array(test_answers) == cv
            if mask.sum() >= 5:
                fv = evaluate_fullvocab(test_hiddens[mask], [cv] * mask.sum(), lm_head_repaired, digit_token_ids)
                per_count_repair[cv] = float(fv)
        
        print(f"  Per-count repair: {per_count_repair}")
        
        results_by_seed[seed] = {
            "baseline_constrained": float(baseline_constrained),
            "baseline_fullvocab": float(baseline_fv),
            "repair_fullvocab": float(repair_fv),
            "repair_constrained": float(repair_constrained),
            "per_count_repair": per_count_repair,
        }
        
        del train_hiddens, test_hiddens
        gc.collect()
    
    seeds_list = list(seeds)
    mean_fv = np.mean([results_by_seed[s]["repair_fullvocab"] for s in seeds_list])
    mean_baseline = np.mean([results_by_seed[s]["baseline_constrained"] for s in seeds_list])
    
    print(f"\nFINAL ENTITY COUNTING SUMMARY")
    print(f"  Baseline constrained (mean): {mean_baseline:.4f}")
    print(f"  Repair fullvocab (mean): {mean_fv:.4f}")
    print(f"  Seeds: {[results_by_seed[s]['repair_fullvocab'] for s in seeds_list]}")
    
    return {
        "task": "entity_counting",
        "seeds": results_by_seed,
        "mean_baseline_constrained": float(mean_baseline),
        "mean_repair_fullvocab": float(mean_fv),
        "hyperparams": {
            "n_iters": n_iters, "lr": lr, "l2_reg": l2_reg,
            "hard_count_weight": hard_count_weight,
            "n_train": n_train, "n_test": n_test,
        }
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=[11, 77, 42])
    parser.add_argument("--n_train", type=int, default=800)
    parser.add_argument("--n_test", type=int, default=300)
    parser.add_argument("--n_iters", type=int, default=2000)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--l2_reg", type=float, default=0.001)
    parser.add_argument("--hard_count_weight", type=float, default=3.0)
    parser.add_argument("--output", type=str, 
                        default="results_phase114_improved_repair.json")
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-8B")
    args = parser.parse_args()
    
    t0 = time.time()
    print(f"Phase114: Improved fullvocab repair for entity counting")
    print(f"Seeds: {args.seeds}, N_train={args.n_train}, N_test={args.n_test}")
    print(f"Iters={args.n_iters}, LR={args.lr}, L2={args.l2_reg}, "
          f"HardWeight={args.hard_count_weight}")
    
    model, tokenizer = load_model_and_tokenizer(args.model)
    digit_token_ids = get_digit_token_ids(tokenizer)
    
    results = run_entity_counting_experiment(
        model, tokenizer, digit_token_ids,
        seeds=tuple(args.seeds),
        n_train=args.n_train, n_test=args.n_test,
        n_iters=args.n_iters, lr=args.lr, l2_reg=args.l2_reg,
        hard_count_weight=args.hard_count_weight,
    )
    
    elapsed = time.time() - t0
    results["elapsed_s"] = elapsed
    
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nTotal time: {elapsed:.1f}s")
    print(f"Results saved to: {args.output}")
    print(f"\nTarget: push entity counting from 60.3%% (Phase107) toward 75%%")
    print(f"Result: {results['mean_repair_fullvocab']:.4f}")


if __name__ == "__main__":
    main()
