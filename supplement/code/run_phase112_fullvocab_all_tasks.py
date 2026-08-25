#!/usr/bin/env python3
"""
Phase 112: Fullvocab Repair on All 4 Tasks (Character Count, Addition, List Length)

Scientific question:
Phase107 showed entity counting fullvocab repair achieves ~60% (vs 98.7% probe-round).
Is this 37pp gap consistent across tasks, or is it specific to entity counting?

Tasks tested:
  1. entity_counting  (already known: ~60% from Phase107 — replication)
  2. char_count       (new: baseline 49.3%, probe-round 96.8%)
  3. addition         (new: baseline 93.3%, probe-round 100%)
  4. list_length      (new: baseline 57.7%, probe-round 100%)

For char_count, addition, list_length: baseline is already >50% for some, but
they all have probe-round near 100%, so the fullvocab gap question is whether
digit rows can be trained to beat full-vocab argmax.

Method: Same fullvocab repair as Phase107
  - Train 9 digit rows of lm_head to beat max non-digit competitor by margin 2.0
  - Evaluate on held-out prompts: argmax(full vocab) == correct digit token

Protocol:
  - Model: Qwen/Qwen3-8B
  - Seeds: 11, 77, 42
  - N_train: 600, N_test: 200
  - Margin: 2.0 (same as Phase107)
  - Iters: 500 (same as Phase107)

Expected outcomes:
  A. All tasks ~60%: fullvocab ceiling is task-independent, likely geometric
     (digit rows need higher norms across all tasks)
  B. Other tasks >80%, entity counting ~60%: entity counting is uniquely hard
     (possibly distribution of hidden states differs)
  C. Other tasks also hit ~baseline: repair fails without constraints
"""

import gc
import json
import os
import random
import time
from pathlib import Path

import numpy as np

os.environ.setdefault("HF_HOME", os.environ.get("HF_CACHE", "./hf_cache"))
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")

import torch
import safetensors.torch as st

print(f"PyTorch: {torch.__version__}")

# ── Task generators (same as Phase97) ────────────────────────────────────────

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
        entity_placed = 0
        for i in range(total_slots):
            if i in entity_positions:
                parts.append(entity)
                entity_placed += 1
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

# ── Model loading ─────────────────────────────────────────────────────────────

def load_model_and_tokenizer(model_name="Qwen/Qwen3-8B"):
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print(f"Loading tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    print(f"Loading model: {model_name}")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    model.eval()
    print(f"Model loaded. Layers: {model.config.num_hidden_layers}")
    return model, tokenizer


def get_digit_token_ids(tokenizer):
    ids = []
    for d in range(1, 10):
        toks = tokenizer.encode(str(d), add_special_tokens=False)
        if len(toks) == 1:
            ids.append(toks[0])
        else:
            # find single-token encoding
            for t in toks:
                if tokenizer.decode([t]).strip() == str(d):
                    ids.append(t)
                    break
    print(f"Digit token IDs: {ids}")
    return ids  # should be 9 IDs for digits 1-9


# ── Hidden state extraction ───────────────────────────────────────────────────

def extract_hiddens_cpu(model, tokenizer, prompts, batch_size=16):
    """Extract final-position hidden states from all layers (CPU, bfloat16)."""
    device = next(model.parameters()).device
    n_layers = model.config.num_hidden_layers + 1  # +1 for embedding layer

    all_hiddens = []
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        texts = [p["text"] for p in batch]
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=256)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            out = model(**inputs, output_hidden_states=True)
        # out.hidden_states: tuple of (n_layers+1) tensors [batch, seq, hidden]
        # Take the last non-padding position for each sequence
        seq_lens = inputs["attention_mask"].sum(dim=1) - 1  # last real token index
        batch_hiddens = []
        for layer_idx in range(len(out.hidden_states)):
            # gather last position
            h = out.hidden_states[layer_idx]  # [batch, seq, hidden]
            last = h[torch.arange(len(batch)), seq_lens]  # [batch, hidden]
            batch_hiddens.append(last.float().cpu().numpy())
        # Stack to [n_layers, batch, hidden] then transpose to [batch, n_layers, hidden]
        stacked = np.stack(batch_hiddens, axis=0)  # [n_layers, batch, hidden]
        stacked = stacked.transpose(1, 0, 2)  # [batch, n_layers, hidden]
        all_hiddens.append(stacked)
        if (i // batch_size) % 5 == 0:
            print(f"  Extracted hiddens {i+len(batch)}/{len(prompts)}")
    return np.concatenate(all_hiddens, axis=0)  # [N, n_layers, hidden]


# ── Probe training ────────────────────────────────────────────────────────────

def train_ridge_cv(X_train, y_train, X_val, y_val,
                   alphas=(0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)):
    d = X_train.shape[1]
    y_mean = float(y_train.mean())
    yc = y_train - y_mean
    ss_tot = float(np.sum((y_val - float(y_val.mean())) ** 2)) + 1e-12
    best_r2, best_w, best_b = -1e9, None, y_mean
    for alpha in alphas:
        A = X_train.T @ X_train + alpha * np.eye(d)
        try:
            w = np.linalg.solve(A, X_train.T @ yc)
        except np.linalg.LinAlgError:
            continue
        preds = X_val @ w + y_mean
        r2 = 1.0 - float(np.sum((y_val - preds) ** 2)) / ss_tot
        if r2 > best_r2:
            best_r2, best_w, best_b = r2, w.copy(), y_mean
    return best_w, best_b, float(best_r2)


def train_probes(hiddens, answers, val_frac=0.2):
    """Train ridge probe per layer. Returns best layer probe info."""
    n, n_layers, _ = hiddens.shape
    y = np.array(answers, dtype=np.float64)
    n_val = max(int(n * val_frac), 20)
    rng = np.random.RandomState(99)
    idx = rng.permutation(n)
    train_idx, val_idx = idx[:n - n_val], idx[n - n_val:]
    y_train, y_val = y[train_idx], y[val_idx]
    best_layer, best_r2, best_probe = -1, -1.0, None
    for l in range(n_layers):
        X_train = hiddens[train_idx, l, :]
        X_val = hiddens[val_idx, l, :]
        w, b, r2 = train_ridge_cv(X_train, y_train, X_val, y_val)
        if r2 > best_r2:
            best_r2 = r2
            best_layer = l
            best_probe = {"w": w, "b": b, "layer": l, "r2": r2}
    return best_probe


# ── Fullvocab repair ─────────────────────────────────────────────────────────

def fullvocab_repair(
    lm_head_weight,        # [vocab, hidden] float32
    digit_token_ids,       # list of 9 int (tokens for digits 1-9)
    hiddens_train,         # [N, hidden] float32 (last layer hidden states)
    answers_train,         # [N] int (1..9)
    margin=2.0,
    n_iters=500,
    lr=0.1,
    lr_decay=0.99,
):
    """Train digit rows to beat full-vocabulary argmax.
    
    Returns: repaired_lm_head [vocab, hidden] float32
    """
    W = lm_head_weight.copy()  # [vocab, hidden]
    digit_rows = np.array([W[tid] for tid in digit_token_ids])  # [9, hidden]
    
    # Precompute all logits from non-digit rows for train set
    # non_digit_indices is expensive to handle; compute max non-digit logit per example
    non_digit_mask = np.ones(W.shape[0], dtype=bool)
    for tid in digit_token_ids:
        non_digit_mask[tid] = False
    W_non = W[non_digit_mask]  # [vocab-9, hidden]
    
    # non_digit_logits: [N, vocab-9]
    print(f"  Computing non-digit baseline logits for {hiddens_train.shape[0]} examples...")
    non_digit_logits = hiddens_train @ W_non.T  # [N, vocab-9]
    max_competitor = non_digit_logits.max(axis=1)  # [N]
    print(f"  Max competitor logit: mean={max_competitor.mean():.3f}, std={max_competitor.std():.3f}")
    
    # Target: digit rows must produce logit >= max_competitor + margin
    # answers_train: 1..9, digit_token_ids[i] is token for digit i+1
    # answer_idx: 0..8 (index into digit_token_ids)
    answer_idx = np.array([a - 1 for a in answers_train], dtype=np.int64)  # 0..8
    
    # Adam-style gradient descent on digit_rows
    m = np.zeros_like(digit_rows)
    v = np.zeros_like(digit_rows)
    beta1, beta2, eps = 0.9, 0.999, 1e-8
    
    best_digit_rows = digit_rows.copy()
    best_loss = float("inf")
    
    for it in range(n_iters):
        # current logits for each example's correct digit row
        digit_logits = hiddens_train @ digit_rows.T  # [N, 9]
        correct_logits = digit_logits[np.arange(len(answer_idx)), answer_idx]  # [N]
        
        # hinge loss: max(0, target - correct_logit)
        target = max_competitor + margin
        loss_per = np.maximum(0.0, target - correct_logits)  # [N]
        loss = loss_per.mean()
        
        if loss < best_loss:
            best_loss = loss
            best_digit_rows = digit_rows.copy()
        
        # gradient for correct rows only
        grad = np.zeros_like(digit_rows)  # [9, hidden]
        active = loss_per > 0  # which examples have nonzero loss
        for k in range(9):
            mask = active & (answer_idx == k)
            if mask.any():
                grad[k] = -hiddens_train[mask].mean(axis=0)
        
        # Adam update
        t = it + 1
        m = beta1 * m + (1 - beta1) * grad
        v = beta2 * v + (1 - beta2) * (grad ** 2)
        m_hat = m / (1 - beta1 ** t)
        v_hat = v / (1 - beta2 ** t)
        step = lr * (lr_decay ** it) * m_hat / (np.sqrt(v_hat) + eps)
        digit_rows = digit_rows - step
        
        if it % 100 == 0:
            acc = (correct_logits > max_competitor).mean()
            print(f"    iter {it}: loss={loss:.4f}, train_fullvocab_acc={acc:.4f}")
    
    # Insert repaired digit rows back
    W_repaired = W.copy()
    for i, tid in enumerate(digit_token_ids):
        W_repaired[tid] = best_digit_rows[i]
    
    print(f"  Best training loss: {best_loss:.4f}")
    return W_repaired


# ── Evaluation ───────────────────────────────────────────────────────────────

def evaluate_repair(hiddens_test, answers_test, lm_head_repaired, digit_token_ids):
    """Evaluate fullvocab accuracy: argmax(full vocab) == correct digit token."""
    logits = hiddens_test @ lm_head_repaired.T  # [N, vocab]
    predicted_token = logits.argmax(axis=1)  # [N]
    correct = 0
    for i, answer in enumerate(answers_test):
        correct_tid = digit_token_ids[answer - 1]
        if predicted_token[i] == correct_tid:
            correct += 1
    return correct / len(answers_test)


def evaluate_constrained(hiddens_test, answers_test, lm_head, digit_token_ids):
    """Constrained: argmax over digit tokens only."""
    digit_logits = hiddens_test @ lm_head[digit_token_ids].T  # [N, 9]
    predicted_digit = digit_logits.argmax(axis=1) + 1  # 1..9
    correct = sum(p == a for p, a in zip(predicted_digit, answers_test))
    return correct / len(answers_test)


# ── Main experiment ───────────────────────────────────────────────────────────

def run_task_experiment(task_name, generator, model, tokenizer, digit_token_ids, 
                        seeds=(11, 77, 42), n_train=600, n_test=200,
                        margin=2.0, n_iters=500):
    print(f"\n{'='*60}")
    print(f"TASK: {task_name}")
    print(f"{'='*60}")
    
    # Get lm_head weight
    lm_head = model.lm_head.weight.detach().float().numpy()  # [vocab, hidden]
    print(f"lm_head shape: {lm_head.shape}")
    
    results_by_seed = {}
    
    for seed in seeds:
        print(f"\n--- Seed {seed} ---")
        # Generate data
        all_prompts = generator(n_train + n_test, seed=seed)
        train_prompts = all_prompts[:n_train]
        test_prompts = all_prompts[n_train:n_train + n_test]
        
        print(f"  Train: {len(train_prompts)}, Test: {len(test_prompts)}")
        
        # Extract hiddens for all prompts
        print("  Extracting train hidden states...")
        train_hiddens = extract_hiddens_cpu(model, tokenizer, train_prompts, batch_size=8)
        print("  Extracting test hidden states...")
        test_hiddens = extract_hiddens_cpu(model, tokenizer, test_prompts, batch_size=8)
        
        train_answers = [p["answer"] for p in train_prompts]
        test_answers = [p["answer"] for p in test_prompts]
        
        # Train probes (find best layer)
        print("  Training probes...")
        best_probe = train_probes(train_hiddens, train_answers)
        print(f"  Best probe layer: {best_probe['layer']}, R²={best_probe['r2']:.4f}")
        
        # Probe-round accuracy (constrained)
        probe_layer = best_probe["layer"]
        probe_preds = test_hiddens[:, probe_layer, :] @ best_probe["w"] + best_probe["b"]
        probe_round_preds = np.clip(np.round(probe_preds).astype(int), 1, 9)
        probe_round_acc = sum(p == a for p, a in zip(probe_round_preds, test_answers)) / len(test_answers)
        
        # Baseline constrained
        last_layer_train = train_hiddens[:, -1, :]
        last_layer_test = test_hiddens[:, -1, :]
        baseline_constrained = evaluate_constrained(last_layer_test, test_answers, lm_head, digit_token_ids)
        baseline_fullvocab = evaluate_fullvocab_baseline(last_layer_test, test_answers, lm_head, digit_token_ids)
        
        print(f"  Baseline constrained: {baseline_constrained:.4f}")
        print(f"  Baseline fullvocab: {baseline_fullvocab:.4f}")
        print(f"  Probe-round (best layer): {probe_round_acc:.4f}")
        
        # Fullvocab repair using last-layer hiddens
        print("  Running fullvocab repair...")
        lm_head_repaired = fullvocab_repair(
            lm_head, digit_token_ids, last_layer_train, train_answers,
            margin=margin, n_iters=n_iters
        )
        
        # Evaluate repair
        repair_fullvocab = evaluate_repair(last_layer_test, test_answers, lm_head_repaired, digit_token_ids)
        repair_constrained = evaluate_constrained(last_layer_test, test_answers, lm_head_repaired, digit_token_ids)
        
        print(f"  Repair fullvocab: {repair_fullvocab:.4f}")
        print(f"  Repair constrained: {repair_constrained:.4f}")
        
        results_by_seed[seed] = {
            "probe_layer": int(probe_layer),
            "probe_r2": float(best_probe["r2"]),
            "probe_round_acc": float(probe_round_acc),
            "baseline_constrained": float(baseline_constrained),
            "baseline_fullvocab": float(baseline_fullvocab),
            "repair_fullvocab": float(repair_fullvocab),
            "repair_constrained": float(repair_constrained),
        }
        
        del train_hiddens, test_hiddens
        gc.collect()
    
    # Aggregate
    mean_repair_fv = np.mean([results_by_seed[s]["repair_fullvocab"] for s in seeds])
    mean_probe_round = np.mean([results_by_seed[s]["probe_round_acc"] for s in seeds])
    mean_baseline = np.mean([results_by_seed[s]["baseline_constrained"] for s in seeds])
    
    print(f"\nTASK SUMMARY: {task_name}")
    print(f"  Baseline constrained (mean): {mean_baseline:.4f}")
    print(f"  Probe-round (mean): {mean_probe_round:.4f}")
    print(f"  Fullvocab repair (mean): {mean_repair_fv:.4f}")
    print(f"  Gap (probe_round - fullvocab): {mean_probe_round - mean_repair_fv:.4f}")
    
    return {
        "task": task_name,
        "seeds": results_by_seed,
        "mean_baseline_constrained": float(mean_baseline),
        "mean_probe_round": float(mean_probe_round),
        "mean_repair_fullvocab": float(mean_repair_fv),
    }


def evaluate_fullvocab_baseline(hiddens_test, answers_test, lm_head, digit_token_ids):
    """Baseline: argmax of full vocab with original lm_head."""
    logits = hiddens_test @ lm_head.T  # [N, vocab]
    predicted_token = logits.argmax(axis=1)
    correct = 0
    for i, answer in enumerate(answers_test):
        correct_tid = digit_token_ids[answer - 1]
        if predicted_token[i] == correct_tid:
            correct += 1
    return correct / len(answers_test)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", nargs="+", default=list(TASK_GENERATORS.keys()),
                        help="Tasks to run")
    parser.add_argument("--seeds", nargs="+", type=int, default=[11, 77, 42])
    parser.add_argument("--n_train", type=int, default=600)
    parser.add_argument("--n_test", type=int, default=200)
    parser.add_argument("--margin", type=float, default=2.0)
    parser.add_argument("--n_iters", type=int, default=500)
    parser.add_argument("--output", type=str, default="results_phase112_fullvocab_all_tasks.json")
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-8B")
    args = parser.parse_args()
    
    t0 = time.time()
    print(f"Phase112: Fullvocab repair on tasks: {args.tasks}")
    print(f"Seeds: {args.seeds}, N_train={args.n_train}, N_test={args.n_test}")
    print(f"Margin={args.margin}, Iters={args.n_iters}")
    
    model, tokenizer = load_model_and_tokenizer(args.model)
    digit_token_ids = get_digit_token_ids(tokenizer)
    assert len(digit_token_ids) == 9, f"Expected 9 digit token IDs, got {len(digit_token_ids)}"
    
    all_results = {}
    for task_name in args.tasks:
        if task_name not in TASK_GENERATORS:
            print(f"Unknown task: {task_name}, skipping")
            continue
        generator = TASK_GENERATORS[task_name]
        result = run_task_experiment(
            task_name, generator, model, tokenizer, digit_token_ids,
            seeds=args.seeds, n_train=args.n_train, n_test=args.n_test,
            margin=args.margin, n_iters=args.n_iters,
        )
        all_results[task_name] = result
        
        # Save intermediate results
        with open(args.output, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"Saved results to {args.output}")
    
    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")
    
    # Final summary
    print("\n" + "="*60)
    print("FINAL SUMMARY: Phase112 Fullvocab Repair All Tasks")
    print("="*60)
    print(f"{'Task':<20} {'Baseline':>10} {'Probe-round':>12} {'Fullvocab':>10} {'Gap':>8}")
    print("-"*60)
    for task, res in all_results.items():
        gap = res["mean_probe_round"] - res["mean_repair_fullvocab"]
        print(f"{task:<20} {res['mean_baseline_constrained']:>9.1%} "
              f"{res['mean_probe_round']:>11.1%} {res['mean_repair_fullvocab']:>9.1%} "
              f"{gap:>7.1%}")
    
    with open(args.output, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
