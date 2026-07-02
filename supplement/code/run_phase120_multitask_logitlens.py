#!/usr/bin/env python3
"""
Phase120: Multi-task logit-lens SNR — proves LoRA Q/V mechanism generalizes
across low-vocabulary aggregation tasks.

Tasks:
  1. Entity counting (Phase119c task)
  2. Character counting: "How many 'x' in ...?"
  3. Addition: "X + Y = ?" (single-digit operands)

Each task: pre-LoRA logit-lens, train LoRA Q/V, post-LoRA logit-lens, gen acc.
Key metric: logit-lens correct-digit rank pre→post.

Output:
  /tmp/results_phase120_multitask_logitlens.json
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
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/tmp/results_phase120_multitask_logitlens.json")

# 2 seeds per task (faster than 3 for multi-task)
SEEDS = [42, 11]
N_TRAIN = int(os.environ.get("N_TRAIN", "400"))
N_TEST = int(os.environ.get("N_TEST", "200"))
N_STEPS = int(os.environ.get("N_STEPS", "200"))
LR = float(os.environ.get("LR", "2e-4"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "4"))
LORA_RANK = int(os.environ.get("LORA_RANK", "16"))
LORA_ALPHA = float(os.environ.get("LORA_ALPHA", "32.0"))
FINAL_LAYER = int(os.environ.get("FINAL_LAYER", "35"))
MAX_LENGTH = int(os.environ.get("MAX_LENGTH", "384") if "char_count" in __name__ else "256")


def log(msg):
    print(f"[phase120] {msg}", flush=True)


# ─── Prompt generators ────────────────────────────────────────────────

ENTITIES = ["apple","car","dog","tree","book","chair","lamp","phone","cloud","river",
            "bird","shoe","ball","hat","pen","stone","star","fish","flag","coin"]
DIGIT_STRS = ["1","2","3","4","5","6","7","8","9"]
LETTERS = list("abcdefghjkmnpqrstuvwxyz")  # exclude i,l,o (ambiguous)


def make_entity_counting_prompts(n, seed):
    rng = random.Random(seed)
    prompts, answers = [], []
    while len(prompts) < n:
        entity = rng.choice(ENTITIES)
        count = rng.randint(1, 9)
        sentences = []
        for _ in range(count):
            sentences.append(f"There are {rng.randint(1,3)} {entity} near the pond.")
        for _ in range(rng.randint(0, 3)):
            e2 = rng.choice([e for e in ENTITIES if e != entity])
            sentences.append(f"There are {rng.randint(1,4)} {e2} in the area.")
        rng.shuffle(sentences)
        text = " ".join(sentences)
        prompt = f"{text}\n\nCount how many {entity} there are. Answer with just the number: "
        prompts.append(prompt)
        answers.append(count)
    return prompts, answers


def make_char_counting_prompts(n, seed):
    """Count occurrences of a specific letter in a string of words."""
    rng = random.Random(seed)
    prompts, answers = [], []
    while len(prompts) < n:
        letter = rng.choice(LETTERS)
        count = rng.randint(1, 9)
        # Build a string with exactly `count` occurrences of the letter
        words = []
        placed = 0
        while placed < count:
            # Insert 1-3 of the target letter in a word
            n_here = min(rng.randint(1, 3), count - placed)
            base = ''.join(rng.choices(LETTERS, k=rng.randint(2,5)))
            word = base[:2] + letter * n_here + base[2:]
            words.append(word)
            placed += n_here
        # Add distractor words without the letter
        for _ in range(rng.randint(2, 6)):
            other_letters = [c for c in LETTERS if c != letter]
            w = ''.join(rng.choices(other_letters, k=rng.randint(3,7)))
            words.append(w)
        rng.shuffle(words)
        text = " ".join(words)
        prompt = f"Text: {text}\n\nHow many '{letter}' appear? Answer with just the number: "
        prompts.append(prompt)
        answers.append(count)
    return prompts, answers


def make_addition_prompts(n, seed):
    """Single-digit addition: X + Y = ? where 1 <= X,Y <= 9 and X+Y <= 9."""
    rng = random.Random(seed)
    prompts, answers = [], []
    while len(prompts) < n:
        a = rng.randint(1, 8)
        b = rng.randint(1, 9 - a)  # ensure a+b <= 9
        total = a + b
        prompt = f"What is {a} + {b}? Answer with just the number: "
        prompts.append(prompt)
        answers.append(total)
    return prompts, answers


# ─── LoRA + training helpers ──────────────────────────────────────────

def get_digit_token_ids(tokenizer):
    return [tokenizer.encode(d, add_special_tokens=False)[0] for d in DIGIT_STRS]


def apply_lora(model, rank=16, alpha=32.0):
    from peft import LoraConfig, TaskType, get_peft_model
    cfg = LoraConfig(r=rank, lora_alpha=alpha, target_modules=["q_proj","v_proj"],
                     lora_dropout=0.0, bias="none", task_type=TaskType.CAUSAL_LM)
    m = get_peft_model(model, cfg)
    n = sum(p.numel() for p in m.parameters() if p.requires_grad)
    log(f"  LoRA: rank={rank}, alpha={alpha}, trainable={n:,}")
    return m


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
        labels = torch.tensor([digit_ids[int(answers[i])-1] for i in idx],
                              dtype=torch.long, device=device)
        logits_out = model(input_ids=inp).logits[:, -1, :]
        loss = nn.CrossEntropyLoss()(logits_out, labels)
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
        optimizer.step()
        losses.append(float(loss.item()))
        if (step+1) % 40 == 0 or step == 0:
            log(f"    step {step+1}/{n_steps} loss={np.mean(losses[-20:]):.4f} elapsed={time.time()-t0:.1f}s")
    return time.time()-t0, float(np.mean(losses[-10:]))


def evaluate_gen(model, tokenizer, prompts, answers, digit_ids, bs=4):
    model.eval()
    device = next(model.parameters()).device
    correct = 0
    with torch.no_grad():
        for i in range(0, len(prompts), bs):
            batch_p = prompts[i:i+bs]
            batch_a = answers[i:i+bs]
            enc = tokenizer(batch_p, return_tensors="pt", padding=True, truncation=True,
                            max_length=MAX_LENGTH)
            inp = enc["input_ids"].to(device)
            gen = model.generate(inp, attention_mask=enc["attention_mask"].to(device),
                                 max_new_tokens=1, do_sample=False,
                                 pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id)
            new = gen[:, inp.shape[1]:]
            for j, a in enumerate(batch_a):
                if j < new.shape[0] and int(a) >= 1 and int(a) <= 9:
                    if int(new[j,0].item()) == digit_ids[int(a)-1]:
                        correct += 1
    return correct / max(len(prompts), 1)


def compute_logitlens(model, tokenizer, prompts, answers, digit_ids, layer_idx):
    model.eval()
    device = next(model.parameters()).device
    lm_head = model.get_output_embeddings().weight.detach().to(device=device, dtype=torch.float32)
    try:
        from peft import PeftModel
        if isinstance(model, PeftModel):
            final_ln = model.base_model.model.model.norm
        else:
            final_ln = model.model.norm
    except ImportError:
        final_ln = model.model.norm

    results = {"correct": 0, "total": 0, "ranks": [], "correct_logits": [],
               "max_wrong_logits": []}

    with torch.no_grad():
        for i in range(0, len(prompts), 8):
            batch_p = prompts[i:i+8]
            batch_a = answers[i:i+8]
            enc = tokenizer(batch_p, return_tensors="pt", padding=True,
                            truncation=True, max_length=MAX_LENGTH)
            inp = enc["input_ids"].to(device)
            out = model(input_ids=inp, output_hidden_states=True, return_dict=True)
            h = out.hidden_states[layer_idx+1][:, -1, :]
            h_normed = final_ln(h).float()
            logits_all = h_normed @ lm_head.T

            for j, a in enumerate(batch_a):
                if int(a) < 1 or int(a) > 9:
                    continue
                cid = digit_ids[int(a)-1]
                cl = float(logits_all[j, cid].item())
                dl = logits_all[j, digit_ids].cpu().float().numpy()
                da_id = digit_ids[int(np.argmax(dl))]

                results["total"] += 1
                results["correct_logits"].append(cl)
                if da_id == cid:
                    results["correct"] += 1
                rank = int((logits_all[j] > cl).sum().item()) + 1
                results["ranks"].append(rank)
                wl = [float(logits_all[j, d].item()) for d in digit_ids if d != cid]
                results["max_wrong_logits"].append(max(wl) if wl else -1e10)

    ranks = np.array(results["ranks"])
    logit_ratio = np.exp(np.array(results["correct_logits"])) / \
                  np.exp(np.array(results["max_wrong_logits"]) + 1e-8)

    return {
        "accuracy": results["correct"] / max(results["total"], 1),
        "median_rank": float(np.median(ranks)),
        "mean_rank": float(np.mean(ranks)),
        "median_logit_ratio": float(np.median(logit_ratio)),
    }


# ─── Main ──────────────────────────────────────────────────────────────

TASKS = {
    "entity_counting": make_entity_counting_prompts,
    "character_counting": make_char_counting_prompts,
    "addition": make_addition_prompts,
}


def main():
    log(f"Phase120: Multi-task logit-lens across {len(TASKS)} task types")
    log(f"  model={MODEL_NAME}, seeds={SEEDS} per task")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"  device={device}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=HF_CACHE,
                                               trust_remote_code=True, padding_side="left")
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    digit_ids = get_digit_token_ids(tokenizer)

    all_results = {}

    for task_name, prompt_fn in TASKS.items():
        log(f"\n{'='*60}")
        log(f"TASK: {task_name}")
        log(f"{'='*60}")
        task_results = {}

        for seed in SEEDS:
            log(f"\n  --- seed {seed} ---")
            prompts, answers = prompt_fn(N_TRAIN + N_TEST, seed=seed)
            train_p, train_a = prompts[:N_TRAIN], answers[:N_TRAIN]
            test_p, test_a = prompts[N_TRAIN:], answers[N_TRAIN:]

            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME, cache_dir=HF_CACHE, trust_remote_code=True,
                torch_dtype=torch.bfloat16, low_cpu_mem_usage=True,
            ).to(device)
            model.eval()

            # Pre-LoRA logit-lens
            t0 = time.time()
            pre = compute_logitlens(model, tokenizer, test_p, test_a, digit_ids, layer_idx=FINAL_LAYER)
            log(f"  pre-LoRA logitlens: acc={pre['accuracy']:.3f} rank_med={pre['median_rank']:.0f} "
                f"ratio={pre['median_logit_ratio']:.1f} ({time.time()-t0:.1f}s)")

            base_gen = evaluate_gen(model, tokenizer, test_p, test_a, digit_ids)
            log(f"  baseline generation={base_gen:.3f}")

            # Train LoRA
            model = apply_lora(model, rank=LORA_RANK, alpha=LORA_ALPHA)
            train_time, final_loss = train_lora(
                model, tokenizer, train_p, train_a, digit_ids,
                n_steps=N_STEPS, lr=LR, bs=BATCH_SIZE, seed=seed)
            log(f"  training done in {train_time:.1f}s, final_loss={final_loss:.4f}")

            post_gen = evaluate_gen(model, tokenizer, test_p, test_a, digit_ids)
            log(f"  post-LoRA generation={post_gen:.3f}")

            # Post-LoRA logit-lens
            t0 = time.time()
            post = compute_logitlens(model, tokenizer, test_p, test_a, digit_ids, layer_idx=FINAL_LAYER)
            log(f"  post-LoRA logitlens: acc={post['accuracy']:.3f} rank_med={post['median_rank']:.0f} "
                f"ratio={post['median_logit_ratio']:.1f} ({time.time()-t0:.1f}s)")

            task_results[str(seed)] = {
                "seed": seed,
                "baseline_gen": base_gen,
                "post_gen": post_gen,
                "logitlens_pre": pre,
                "logitlens_post": post,
                "delta": {
                    "accuracy": post["accuracy"] - pre["accuracy"],
                    "median_rank": post["median_rank"] - pre["median_rank"],
                    "logit_ratio_mult": post["median_logit_ratio"] / (pre["median_logit_ratio"] + 1e-8),
                },
                "train_time_s": train_time,
                "final_loss": final_loss,
            }

            del model  # free memory between seeds
            import gc; gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        all_results[task_name] = task_results

        # Write intermediate
        meta = {"phase": "120", "model": MODEL_NAME, "seeds": SEEDS,
                "tasks": list(TASKS.keys()), "layer": FINAL_LAYER}
        with open(OUTPUT_PATH, "w") as f:
            json.dump({"metadata": meta, "tasks": all_results}, f, indent=2)
        log(f"  wrote intermediate {OUTPUT_PATH}")

    # Final summary
    log(f"\n{'='*60}")
    log(f"Phase120 COMPLETE — Multi-task Summary")
    for task_name in TASKS:
        td = all_results[task_name]
        pre_acc = np.mean([td[str(s)]["logitlens_pre"]["accuracy"] for s in SEEDS])
        post_acc = np.mean([td[str(s)]["logitlens_post"]["accuracy"] for s in SEEDS])
        pre_rank = np.mean([td[str(s)]["logitlens_pre"]["median_rank"] for s in SEEDS])
        post_rank = np.mean([td[str(s)]["logitlens_post"]["median_rank"] for s in SEEDS])
        post_gen = np.mean([td[str(s)]["post_gen"] for s in SEEDS])
        log(f"  {task_name}: acc {pre_acc:.3f}→{post_acc:.3f} "
            f"rank {pre_rank:.0f}→{post_rank:.0f} gen_acc={post_gen:.1%}")
    log(f"  results saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
