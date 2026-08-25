#!/usr/bin/env python3
"""
Phase119: Direct mechanistic test of why LoRA Q/V works.

Goal:
  Address the reviewer blocker that LoRA generation gains are not yet tied to
  direct geometric measurements at the generation position.

Protocol (aligned with Phase117/118):
  - Model: Qwen/Qwen3-8B
  - Seeds: 42, 11, 77
  - Task: entity counting
  - Train: N=400, Test: N=200 per seed
  - LoRA: rank=16, alpha=32, target q_proj/v_proj, steps=200, lr=2e-4

Per seed, we measure at generation position (last prompt token), layer=2:
  1) Baseline fullvocab/generation accuracy
  2) Pre-LoRA probe R^2 and probe-vs-digit-row |cos|
  3) Post-LoRA fullvocab/generation accuracy
  4) Post-LoRA probe R^2 and probe-vs-digit-row |cos|
  5) Delta metrics (accuracy, |cos|, projection strength)

Output:
  /tmp/results_phase119_lora_mechanism.json
"""

import json
import os
import random
import time

import numpy as np
import torch
import torch.nn as nn
from torch.optim import AdamW
from transformers import AutoModelForCausalLM, AutoTokenizer


HF_CACHE = os.environ.get("HF_CACHE", os.environ.get("HF_CACHE", "./hf_cache"))
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE
os.environ["HF_HOME"] = HF_CACHE

MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen3-8B")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/tmp/results_phase119_lora_mechanism.json")

SEEDS = [42, 11, 77]
N_TRAIN = int(os.environ.get("N_TRAIN", "400"))
N_TEST = int(os.environ.get("N_TEST", "200"))
N_STEPS = int(os.environ.get("N_STEPS", "200"))
LR = float(os.environ.get("LR", "2e-4"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "4"))
LORA_RANK = int(os.environ.get("LORA_RANK", "16"))
LORA_ALPHA = float(os.environ.get("LORA_ALPHA", "32.0"))
PROBE_LAYER = int(os.environ.get("PROBE_LAYER", "2"))
RIDGE_ALPHA = float(os.environ.get("RIDGE_ALPHA", "1.0"))
MAX_LENGTH = int(os.environ.get("MAX_LENGTH", "256"))


def log(msg):
    print(f"[phase119] {msg}", flush=True)


ENTITIES = [
    "apple", "car", "dog", "tree", "book",
    "chair", "lamp", "phone", "cloud", "river",
    "bird", "shoe", "ball", "hat", "pen",
    "stone", "star", "fish", "flag", "coin",
]

DIGIT_STRS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def make_entity_counting_prompts(n, seed, min_count=1, max_count=9):
    rng = random.Random(seed)
    prompts, answers = [], []
    while len(prompts) < n:
        entity = rng.choice(ENTITIES)
        count = rng.randint(min_count, max_count)
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
    ids = []
    for d in DIGIT_STRS:
        toks = tokenizer.encode(d, add_special_tokens=False)
        if len(toks) != 1:
            raise ValueError(f"Digit '{d}' tokenized to {toks}")
        ids.append(toks[0])
    return ids


def evaluate_next_token(model, tokenizer, prompts, answers, digit_token_ids, batch_size=8):
    model.eval()
    device = next(model.parameters()).device
    correct_fv = 0
    correct_cs = 0
    total = len(prompts)
    with torch.no_grad():
        for i in range(0, total, batch_size):
            batch_p = prompts[i:i + batch_size]
            batch_a = answers[i:i + batch_size]
            enc = tokenizer(
                batch_p,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
            )
            input_ids = enc["input_ids"].to(device)
            attention_mask = enc["attention_mask"].to(device)
            out = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = out.logits[:, -1, :]
            preds_fv = torch.argmax(logits, dim=-1).tolist()
            digit_logits = logits[:, digit_token_ids]
            preds_cs_idx = torch.argmax(digit_logits, dim=-1).tolist()
            for pf, pc, a in zip(preds_fv, preds_cs_idx, batch_a):
                ai = int(a)
                correct_digit_id = digit_token_ids[ai - 1]
                if pf == correct_digit_id:
                    correct_fv += 1
                if pc == ai - 1:
                    correct_cs += 1
    return correct_fv / total, correct_cs / total


def evaluate_generation(model, tokenizer, prompts, answers, digit_token_ids, batch_size=4):
    model.eval()
    device = next(model.parameters()).device
    correct = 0
    total = len(prompts)
    with torch.no_grad():
        for i in range(0, total, batch_size):
            batch_p = prompts[i:i + batch_size]
            batch_a = answers[i:i + batch_size]
            enc = tokenizer(
                batch_p,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
            )
            input_ids = enc["input_ids"].to(device)
            attention_mask = enc["attention_mask"].to(device)
            generated = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=1,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
            )
            new_tokens = generated[:, input_ids.shape[1]:]
            for j, a in enumerate(batch_a):
                if j < new_tokens.shape[0]:
                    gen_token_id = int(new_tokens[j, 0].item())
                    correct_digit_id = digit_token_ids[int(a) - 1]
                    if gen_token_id == correct_digit_id:
                        correct += 1
    return correct / total


def apply_lora_peft(model, rank=16, alpha=32.0):
    from peft import LoraConfig, TaskType, get_peft_model

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
    log(f"  PEFT LoRA applied: rank={rank}, alpha={alpha}, trainable={n_trainable:,}")
    return model


def train_lora(model, tokenizer, train_prompts, train_answers, digit_token_ids, n_steps, lr, batch_size, seed):
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

        enc = tokenizer(
            batch_p,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
        )
        input_ids = enc["input_ids"].to(device)
        attention_mask = enc["attention_mask"].to(device)

        labels = torch.tensor([digit_token_ids[int(a) - 1] for a in batch_a], dtype=torch.long, device=device)

        out = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = out.logits[:, -1, :]
        loss = nn.CrossEntropyLoss()(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], max_norm=1.0)
        optimizer.step()

        losses.append(float(loss.item()))
        if (step + 1) % 20 == 0 or step == 0:
            avg_loss = float(np.mean(losses[-20:]))
            log(f"    step {step+1}/{n_steps} loss={avg_loss:.4f} elapsed={time.time()-t0:.1f}s")

    return time.time() - t0, float(np.mean(losses[-10:]))


def _as_np_hidden(h):
    return h.detach().to(dtype=torch.float32).cpu().numpy()


def collect_last_token_hidden(model, tokenizer, prompts, layer_idx, batch_size=8):
    model.eval()
    device = next(model.parameters()).device
    all_h = []
    with torch.no_grad():
        for i in range(0, len(prompts), batch_size):
            batch_p = prompts[i:i + batch_size]
            enc = tokenizer(
                batch_p,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
            )
            input_ids = enc["input_ids"].to(device)
            attention_mask = enc["attention_mask"].to(device)
            out = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                output_hidden_states=True,
                return_dict=True,
            )
            hs = out.hidden_states[layer_idx + 1]
            last_h = hs[:, -1, :]
            all_h.append(_as_np_hidden(last_h))
    return np.concatenate(all_h, axis=0)


def fit_ridge_probe(X_train, y_train, X_test, y_test, alpha=1.0):
    y_train = y_train.astype(np.float32)
    y_test = y_test.astype(np.float32)

    x_mean = X_train.mean(axis=0, keepdims=True)
    x_std = X_train.std(axis=0, keepdims=True) + 1e-6
    Xtr = (X_train - x_mean) / x_std
    Xte = (X_test - x_mean) / x_std

    y_mean = y_train.mean()
    ytr = y_train - y_mean

    d = Xtr.shape[1]
    A = Xtr.T @ Xtr + alpha * np.eye(d, dtype=np.float32)
    b = Xtr.T @ ytr
    w = np.linalg.solve(A, b)

    pred = Xte @ w + y_mean
    ss_res = float(np.sum((y_test - pred) ** 2))
    ss_tot = float(np.sum((y_test - y_test.mean()) ** 2) + 1e-8)
    r2 = 1.0 - ss_res / ss_tot

    w_raw = (w / x_std.squeeze(0)).astype(np.float32)
    b_raw = float(y_mean - (x_mean.squeeze(0) * w_raw).sum())

    return {
        "w": w_raw,
        "b": b_raw,
        "r2": float(r2),
        "pred": pred.astype(np.float32),
    }


def compute_probe_digit_cosines(probe_w, digit_rows):
    w = probe_w.astype(np.float32)
    w_norm = np.linalg.norm(w) + 1e-8
    row_norms = np.linalg.norm(digit_rows, axis=1) + 1e-8
    dots = digit_rows @ w
    cos = np.abs(dots / (row_norms * w_norm))
    return {
        "mean_abs_cos": float(np.mean(cos)),
        "max_abs_cos": float(np.max(cos)),
        "min_abs_cos": float(np.min(cos)),
        "per_digit_abs_cos": cos.tolist(),
    }


def projection_strength(X, probe_w):
    w = probe_w.astype(np.float32)
    wn = w / (np.linalg.norm(w) + 1e-8)
    proj = X @ wn
    return {
        "mean_abs_proj": float(np.mean(np.abs(proj))),
        "mean_signed_proj": float(np.mean(proj)),
        "std_proj": float(np.std(proj)),
    }


def main():
    log("Phase119: LoRA mechanism geometry test")
    log(f"  model={MODEL_NAME}")
    log(f"  seeds={SEEDS}, N_train={N_TRAIN}, N_test={N_TEST}, N_steps={N_STEPS}")
    log(f"  lora rank={LORA_RANK}, alpha={LORA_ALPHA}, lr={LR}, layer={PROBE_LAYER}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"  device={device}")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        cache_dir=HF_CACHE,
        trust_remote_code=True,
        padding_side="left",
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    digit_token_ids = get_digit_token_ids(tokenizer)
    log(f"  digit token ids={digit_token_ids}")

    all_results = {}

    for seed in SEEDS:
        log("")
        log(f"=== seed {seed} ===")

        prompts, answers = make_entity_counting_prompts(N_TRAIN + N_TEST, seed=seed)
        train_prompts = prompts[:N_TRAIN]
        train_answers = np.array(answers[:N_TRAIN], dtype=np.float32)
        test_prompts = prompts[N_TRAIN:]
        test_answers = np.array(answers[N_TRAIN:], dtype=np.float32)

        t_load = time.time()
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            cache_dir=HF_CACHE,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
        )
        model = model.to(device)
        model.eval()
        log(f"  model loaded in {time.time()-t_load:.1f}s")

        base_fv, base_cs = evaluate_next_token(model, tokenizer, test_prompts, test_answers.tolist(), digit_token_ids)
        base_gen = evaluate_generation(model, tokenizer, test_prompts, test_answers.tolist(), digit_token_ids)
        log(f"  baseline fullvocab={base_fv:.3f} constrained={base_cs:.3f} generation={base_gen:.3f}")

        lm_head = model.get_output_embeddings().weight.detach().to(dtype=torch.float32).cpu().numpy()
        digit_rows = lm_head[digit_token_ids]

        t_geom_pre = time.time()
        Xtr_pre = collect_last_token_hidden(model, tokenizer, train_prompts, layer_idx=PROBE_LAYER, batch_size=8)
        Xte_pre = collect_last_token_hidden(model, tokenizer, test_prompts, layer_idx=PROBE_LAYER, batch_size=8)
        probe_pre = fit_ridge_probe(Xtr_pre, train_answers, Xte_pre, test_answers, alpha=RIDGE_ALPHA)
        cos_pre = compute_probe_digit_cosines(probe_pre["w"], digit_rows)
        proj_pre = projection_strength(Xte_pre, probe_pre["w"])
        log(
            f"  pre-LoRA layer{PROBE_LAYER}: R2={probe_pre['r2']:.4f}, "
            f"mean|cos|={cos_pre['mean_abs_cos']:.4f}, max|cos|={cos_pre['max_abs_cos']:.4f}"
        )
        log(f"  pre-LoRA geometry collection in {time.time()-t_geom_pre:.1f}s")

        model = apply_lora_peft(model, rank=LORA_RANK, alpha=LORA_ALPHA)
        train_time, final_loss = train_lora(
            model,
            tokenizer,
            train_prompts,
            train_answers.tolist(),
            digit_token_ids,
            n_steps=N_STEPS,
            lr=LR,
            batch_size=BATCH_SIZE,
            seed=seed,
        )

        tr_fv, tr_cs = evaluate_next_token(model, tokenizer, test_prompts, test_answers.tolist(), digit_token_ids)
        tr_gen = evaluate_generation(model, tokenizer, test_prompts, test_answers.tolist(), digit_token_ids)
        log(f"  post-LoRA fullvocab={tr_fv:.3f} constrained={tr_cs:.3f} generation={tr_gen:.3f}")

        t_geom_post = time.time()
        Xtr_post = collect_last_token_hidden(model, tokenizer, train_prompts, layer_idx=PROBE_LAYER, batch_size=8)
        Xte_post = collect_last_token_hidden(model, tokenizer, test_prompts, layer_idx=PROBE_LAYER, batch_size=8)
        probe_post = fit_ridge_probe(Xtr_post, train_answers, Xte_post, test_answers, alpha=RIDGE_ALPHA)
        cos_post = compute_probe_digit_cosines(probe_post["w"], digit_rows)
        proj_post = projection_strength(Xte_post, probe_post["w"])
        log(
            f"  post-LoRA layer{PROBE_LAYER}: R2={probe_post['r2']:.4f}, "
            f"mean|cos|={cos_post['mean_abs_cos']:.4f}, max|cos|={cos_post['max_abs_cos']:.4f}"
        )
        log(f"  post-LoRA geometry collection in {time.time()-t_geom_post:.1f}s")

        res = {
            "seed": seed,
            "baseline": {
                "fullvocab": float(base_fv),
                "constrained": float(base_cs),
                "generation": float(base_gen),
            },
            "trained": {
                "fullvocab": float(tr_fv),
                "constrained": float(tr_cs),
                "generation": float(tr_gen),
            },
            "geometry_pre": {
                "layer": PROBE_LAYER,
                "probe_r2": float(probe_pre["r2"]),
                "probe_digit_cos": cos_pre,
                "projection": proj_pre,
            },
            "geometry_post": {
                "layer": PROBE_LAYER,
                "probe_r2": float(probe_post["r2"]),
                "probe_digit_cos": cos_post,
                "projection": proj_post,
            },
            "delta": {
                "fullvocab": float(tr_fv - base_fv),
                "generation": float(tr_gen - base_gen),
                "generation_gap": float(tr_fv - tr_gen),
                "probe_r2": float(probe_post["r2"] - probe_pre["r2"]),
                "mean_abs_cos": float(cos_post["mean_abs_cos"] - cos_pre["mean_abs_cos"]),
                "max_abs_cos": float(cos_post["max_abs_cos"] - cos_pre["max_abs_cos"]),
                "mean_abs_proj": float(proj_post["mean_abs_proj"] - proj_pre["mean_abs_proj"]),
            },
            "training": {
                "time_s": float(train_time),
                "final_loss": float(final_loss),
            },
        }
        all_results[str(seed)] = res

        payload = {
            "metadata": {
                "phase": 119,
                "model": MODEL_NAME,
                "seeds": SEEDS,
                "n_train": N_TRAIN,
                "n_test": N_TEST,
                "n_steps": N_STEPS,
                "lr": LR,
                "batch_size": BATCH_SIZE,
                "lora_rank": LORA_RANK,
                "lora_alpha": LORA_ALPHA,
                "target_modules": ["q_proj", "v_proj"],
                "probe_layer": PROBE_LAYER,
                "ridge_alpha": RIDGE_ALPHA,
                "position": "last_token_generation_position",
            },
            "seeds": all_results,
        }
        with open(OUTPUT_PATH, "w") as f:
            json.dump(payload, f, indent=2)
        log(f"  wrote intermediate {OUTPUT_PATH}")

        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def _arr(key_fn):
        return np.array([key_fn(all_results[str(s)]) for s in SEEDS], dtype=np.float32)

    mean_delta_cos = float(np.mean(_arr(lambda r: r["delta"]["mean_abs_cos"])))
    mean_delta_gen = float(np.mean(_arr(lambda r: r["delta"]["generation"])))
    mean_delta_fv = float(np.mean(_arr(lambda r: r["delta"]["fullvocab"])))
    mean_pre_cos = float(np.mean(_arr(lambda r: r["geometry_pre"]["probe_digit_cos"]["mean_abs_cos"])))
    mean_post_cos = float(np.mean(_arr(lambda r: r["geometry_post"]["probe_digit_cos"]["mean_abs_cos"])))

    summary = {
        "mean_baseline_fullvocab": float(np.mean(_arr(lambda r: r["baseline"]["fullvocab"]))),
        "mean_baseline_generation": float(np.mean(_arr(lambda r: r["baseline"]["generation"]))),
        "mean_trained_fullvocab": float(np.mean(_arr(lambda r: r["trained"]["fullvocab"]))),
        "mean_trained_generation": float(np.mean(_arr(lambda r: r["trained"]["generation"]))),
        "mean_pre_probe_r2": float(np.mean(_arr(lambda r: r["geometry_pre"]["probe_r2"]))),
        "mean_post_probe_r2": float(np.mean(_arr(lambda r: r["geometry_post"]["probe_r2"]))),
        "mean_pre_abs_cos": mean_pre_cos,
        "mean_post_abs_cos": mean_post_cos,
        "delta_mean_abs_cos": mean_delta_cos,
        "delta_generation": mean_delta_gen,
        "delta_fullvocab": mean_delta_fv,
    }

    payload = {
        "metadata": {
            "phase": 119,
            "model": MODEL_NAME,
            "seeds": SEEDS,
            "n_train": N_TRAIN,
            "n_test": N_TEST,
            "n_steps": N_STEPS,
            "lr": LR,
            "batch_size": BATCH_SIZE,
            "lora_rank": LORA_RANK,
            "lora_alpha": LORA_ALPHA,
            "target_modules": ["q_proj", "v_proj"],
            "probe_layer": PROBE_LAYER,
            "ridge_alpha": RIDGE_ALPHA,
            "position": "last_token_generation_position",
        },
        "seeds": all_results,
        "summary": summary,
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    log("=== Phase119 summary ===")
    log(f"  mean baseline generation: {summary['mean_baseline_generation']:.3f}")
    log(f"  mean trained generation:  {summary['mean_trained_generation']:.3f}")
    log(f"  mean baseline fullvocab:  {summary['mean_baseline_fullvocab']:.3f}")
    log(f"  mean trained fullvocab:   {summary['mean_trained_fullvocab']:.3f}")
    log(f"  mean pre |cos|: {summary['mean_pre_abs_cos']:.4f}")
    log(f"  mean post |cos|: {summary['mean_post_abs_cos']:.4f}")
    log(f"  delta mean |cos|: {summary['delta_mean_abs_cos']:+.4f}")
    log(f"  results saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
