#!/usr/bin/env python3
"""
Phase125: M4 (60% ceiling test) + M7 (multi-seed CoT baseline).
Two experiments in one TPU run for efficiency.

M4: Prompt-diversity test — does varying template diversity at fixed count
    reduce 9-row repair accuracy? If yes → intra-class hidden-state diversity
    is causal for the 60% ceiling.
M7: Multi-seed CoT baseline — 3-seed few-shot CoT on entity counting + char
    counting under same generation protocol as LoRA Q/V.

Output: /tmp/results_phase125_m4_m7.json
"""
import json, os, random, time
import numpy as np
import torch, torch.nn as nn
from torch.optim import AdamW
from transformers import AutoModelForCausalLM, AutoTokenizer

HF_CACHE = os.environ.get("HF_CACHE", os.environ.get("HF_CACHE", "./hf_cache"))
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE; os.environ["HF_HOME"] = HF_CACHE

MODEL = "Qwen/Qwen3-8B"
OUTPUT = "/tmp/results_phase125_m4_m7.json"
MAX_LENGTH = 256

ENTITIES = ["apple","car","dog","tree","book","chair","lamp","phone","cloud","river",
            "bird","shoe","ball","hat","pen","stone","star","fish","flag","coin"]
DIGITS = ["1","2","3","4","5","6","7","8","9"]
LETTERS = list("abcdefghijklmnopqrstuvwxyz")

def log(msg): print(f"[phase125] {msg}", flush=True)

# ============================================================
# M7: Multi-seed CoT baseline
# ============================================================
FEWSHOT_EXAMPLE = (
    "There are 2 cat near the pond. There are 2 cat near the pond. "
    "There are 2 cat near the pond.\n\n"
    "Count how many cat there are. Let's count step by step. "
    "The final answer is: 3"
)

def make_entity_prompts(n, seed):
    rng = random.Random(seed)
    prompts, answers = [], []
    while len(prompts) < n:
        e = rng.choice(ENTITIES); c = rng.randint(1,9)
        nd = rng.randint(0,3)
        de = [x for x in ENTITIES if x != e]
        sents, dc = [], {d: rng.randint(1,4) for d in rng.sample(de, nd)}
        for _ in range(c): sents.append(f"There are {rng.randint(1,3)} {e} near the pond.")
        for d, cn in dc.items(): sents.append(f"There are {cn} {d} in the area.")
        rng.shuffle(sents)
        prompts.append(" ".join(sents) + f"\n\nCount how many {e} there are. ")
        answers.append(c)
    return prompts, answers

def make_char_prompts(n, seed):
    rng = random.Random(seed)
    prompts, answers = [], []
    while len(prompts) < n:
        letter = rng.choice(LETTERS[:15])
        count = rng.randint(1,9)
        words = []
        for _ in range(rng.randint(4, 8)):
            w = ''.join(rng.choice(LETTERS) for _ in range(rng.randint(3,7)))
            words.append(w + letter * rng.randint(0,3))
        for _ in range(count):
            words.append(f"x{letter}xletter{rng.randint(1,10)}")
        rng.shuffle(words)
        text = " ".join(words)
        prompts.append(f"Words: {text}\n\nCount how many words contain the letter '{letter}'. ")
        answers.append(count)
    return prompts, answers

def eval_cot(model, tok, prompts, answers, dids, few_shot=False, max_new=50):
    model.eval(); device = next(model.parameters()).device; correct = 0
    with torch.no_grad():
        for i in range(0, len(prompts), 2):
            bp = prompts[i:i+2]; ba = answers[i:i+2]
            if few_shot:
                bp = [FEWSHOT_EXAMPLE + "\n\n" + p for p in bp]
            bp = [p + "Let's count step by step. The final answer is: " for p in bp]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
            inp = enc["input_ids"].to(device)
            am = enc.get("attention_mask"); am = am.to(device) if am is not None else None
            gen = model.generate(input_ids=inp, attention_mask=am, max_new_tokens=max_new,
                                 do_sample=False, pad_token_id=tok.pad_token_id or tok.eos_token_id)
            new = gen[:, inp.shape[1]:]
            for j, a in enumerate(ba):
                for tid in new[j].tolist():
                    if tid in dids:
                        if tid == dids[int(a)-1]: correct += 1
                        break
    return correct / len(prompts)

# ============================================================
# M4: Prompt-diversity ceiling test
# ============================================================
TEMPLATES = [
    "There are {n} {entity} near the pond.",
    "I observed {n} {entity} by the lake.",
    "The park has {n} {entity} sitting under trees.",
    "A total of {n} {entity} were spotted in the garden.",
    "Near the fountain, {n} {entity} are resting.",
    "The field contained exactly {n} {entity} this morning.",
    "Walking through the forest, I counted {n} {entity}.",
    "On the bench, there are {n} {entity} quietly waiting.",
]

def make_diversity_prompts(n, seed, n_templates=1):
    """n_templates=1: low diversity (all same template). n_templates=8: high diversity."""
    rng = random.Random(seed)
    prompts, answers = [], []
    templates_used = TEMPLATES[:n_templates]
    while len(prompts) < n:
        e = rng.choice(ENTITIES); c = rng.randint(1,9)
        nd = rng.randint(0,3)
        de = [x for x in ENTITIES if x != e]
        sents, dc = [], {d: rng.randint(1,4) for d in rng.sample(de, nd)}
        tmpl = rng.choice(templates_used) if n_templates > 1 else templates_used[0]
        for _ in range(c):
            sents.append(tmpl.format(n=rng.randint(1,3), entity=e))
        for d, cn in dc.items():
            sents.append(tmpl.format(n=cn, entity=d))
        rng.shuffle(sents)
        prompts.append(" ".join(sents) + f"\n\nCount how many {e} there are. Answer with just the number: ")
        answers.append(c)
    return prompts, answers

def compute_9row_repair_acc(model, tok, prompts, answers, dids):
    """9-row repair: overwrite digit rows with probe direction, evaluate constrained."""
    model.eval(); device = next(model.parameters()).device
    # Extract hidden states at layer 2 (best probe layer)
    hs = []
    with torch.no_grad():
        for i in range(0, len(prompts), 8):
            bp = prompts[i:i+8]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
            out = model(input_ids=enc["input_ids"].to(device), output_hidden_states=True, return_dict=True)
            h = out.hidden_states[3][:, -1, :].float().cpu().numpy()  # layer 2 + embedding
            hs.append(h)
    X = np.concatenate(hs, axis=0)
    y = np.array(answers[:len(X)], dtype=np.float32)

    # Ridge probe
    x_mean, x_std = X.mean(0, keepdims=True), X.std(0, keepdims=True) + 1e-6
    Xn = (X - x_mean) / x_std; ym = y.mean()
    A = Xn[:300].T @ Xn[:300] + 1.0 * np.eye(Xn.shape[1])
    w = np.linalg.solve(A, Xn[:300].T @ (y[:300] - ym))
    probe_dir = (w / x_std.squeeze(0)).astype(np.float32)
    probe_norm = np.linalg.norm(probe_dir)

    # 9-row repair: overwrite digit rows with probe direction
    lm_head = model.get_output_embeddings().weight.detach().clone()
    for k, did in enumerate(dids):
        lm_head[did] = torch.from_numpy(probe_dir / probe_norm * np.linalg.norm(lm_head[did].float().numpy())).to(lm_head.device, dtype=lm_head.dtype)
    model.get_output_embeddings().weight.data = lm_head

    # Evaluate constrained accuracy
    correct = 0; total = 0
    with torch.no_grad():
        for i in range(300, len(prompts), 8):
            bp = prompts[i:i+8]; ba = answers[i:i+8]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
            logits = model(input_ids=enc["input_ids"].to(device)).logits[:, -1, dids]
            preds = logits.argmax(-1)
            for j, a in enumerate(ba):
                if j < len(preds) and dids[int(preds[j])] == dids[int(a)-1]:
                    correct += 1
                total += 1
    return correct / max(total, 1)

def get_ids(tok): return [tok.encode(d, add_special_tokens=False)[0] for d in DIGITS]

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Phase125: M4 ceiling + M7 CoT. device={device}")

    tok = AutoTokenizer.from_pretrained(MODEL, cache_dir=HF_CACHE, trust_remote_code=True, padding_side="left")
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    dids = get_ids(tok)

    results = {}

    # ========= M7: Multi-seed CoT =========
    log("\n=== M7: Multi-seed CoT baseline ===")
    cot_results = {}
    for seed in [42, 11, 77]:
        log(f"\nSeed {seed}")
        ep, ea = make_entity_prompts(200, seed=seed)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL, cache_dir=HF_CACHE, trust_remote_code=True,
            torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
        model.eval()

        direct = eval_cot(model, tok, [p + "Answer with just the number: " for p in ep], ea, dids, few_shot=False, max_new=10)
        log(f"  entity-direct: {direct:.1%}")
        cot_zs = eval_cot(model, tok, ep, ea, dids, few_shot=False, max_new=50)
        log(f"  entity-zero-shot CoT: {cot_zs:.1%}")
        cot_fs = eval_cot(model, tok, ep, ea, dids, few_shot=True, max_new=50)
        log(f"  entity-few-shot CoT: {cot_fs:.1%}")

        cd = str(seed)
        cot_results[cd] = {"entity_direct": direct, "entity_cot_zs": cot_zs, "entity_cot_fs": cot_fs}

    # Char counting CoT (seed 42 only, pilot)
    log("\nChar counting CoT (seed 42)")
    cp, ca = make_char_prompts(200, seed=42)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, cache_dir=HF_CACHE, trust_remote_code=True,
        torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    model.eval()
    char_fs = eval_cot(model, tok, cp, ca, dids, few_shot=True, max_new=50)
    log(f"  char-few-shot CoT: {char_fs:.1%}")
    cot_results["42"]["char_cot_fs"] = char_fs

    results["M7_cot"] = cot_results

    # ========= M4: Diversity test =========
    log("\n=== M4: Prompt-diversity ceiling test ===")
    div_results = {}
    for n_templates in [1, 4, 8]:
        log(f"\nSeed 42, {n_templates} templates")
        dp, da = make_diversity_prompts(500, seed=42, n_templates=n_templates)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL, cache_dir=HF_CACHE, trust_remote_code=True,
            torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
        model.eval()
        acc = compute_9row_repair_acc(model, tok, dp, da, dids)
        log(f"  9-row repair acc ({n_templates} templates): {acc:.1%}")
        div_results[str(n_templates)] = float(acc)

    results["M4_diversity"] = div_results

    with open(OUTPUT, "w") as f:
        json.dump({"metadata":{"phase":125,"model":MODEL},"results":results}, f, indent=2)

    log("\nPhase125 complete.")
    log(f"M7 CoT 3-seed entity-fs: {[cot_results[str(s)]['entity_cot_fs'] for s in [42,11,77]]}")
    log(f"M4 diversity: {div_results}")

if __name__ == "__main__":
    main()
