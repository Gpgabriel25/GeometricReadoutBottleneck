#!/usr/bin/env python3
"""
Phase124: LoRA variant ablation — tests routing specificity.
Compares Q/V (Phase118) vs Q-only, K-only, V-only, O-only, FFN-only.
All rank-16, same training protocol, same multi-task prompts.
1 seed (42), measures generation accuracy + logit-lens rank.
"""
import json, os, random, time
import numpy as np
import torch, torch.nn as nn
from torch.optim import AdamW
from transformers import AutoModelForCausalLM, AutoTokenizer

HF_CACHE = os.environ.get("HF_CACHE", "/home/gpgabriel25/hf_cache")
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE; os.environ["HF_HOME"] = HF_CACHE

MODEL = "Qwen/Qwen3-8B"
SEED, N_TRAIN, N_TEST, N_STEPS = 42, 400, 200, 200
LR, BS, RANK, ALPHA = 2e-4, 4, 16, 32.0
MAX_LENGTH, FINAL_LAYER = 256, 35
OUTPUT = "/tmp/results_phase124_lora_variants.json"

ENTITIES = ["apple","car","dog","tree","book","chair","lamp","phone","cloud","river",
            "bird","shoe","ball","hat","pen","stone","star","fish","flag","coin"]
DIGITS = ["1","2","3","4","5","6","7","8","9"]

def log(msg): print(f"[phase124] {msg}", flush=True)

def make_prompts(n, seed):
    rng = random.Random(seed)
    prompts, answers = [], []
    while len(prompts) < n:
        e = rng.choice(ENTITIES); c = rng.randint(1,9)
        nd = rng.randint(0,3)
        de = [x for x in ENTITIES if x != e]
        sents = []
        dc = {d: rng.randint(1,4) for d in rng.sample(de, nd)}
        for _ in range(c): sents.append(f"There are {rng.randint(1,3)} {e} near the pond.")
        for d, cn in dc.items(): sents.append(f"There are {cn} {d} in the area.")
        rng.shuffle(sents)
        text = " ".join(sents)
        prompts.append(f"{text}\n\nCount how many {e} there are. Answer with just the number: ")
        answers.append(c)
    return prompts, answers

def get_ids(tok): return [tok.encode(d, add_special_tokens=False)[0] for d in DIGITS]

def eval_gen(model, tok, prompts, answers, dids, bs=4):
    model.eval(); device = next(model.parameters()).device; correct = 0
    with torch.no_grad():
        for i in range(0, len(prompts), bs):
            bp = prompts[i:i+bs]; ba = answers[i:i+bs]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
            inp = enc["input_ids"].to(device)
            am = enc.get("attention_mask"); am = am.to(device) if am is not None else None
            gen = model.generate(input_ids=inp, attention_mask=am, max_new_tokens=1,
                                 do_sample=False, pad_token_id=tok.pad_token_id or tok.eos_token_id)
            new = gen[:, inp.shape[1]:]
            for j, a in enumerate(ba):
                if j < new.shape[0] and int(new[j,0].item()) == dids[int(a)-1]: correct += 1
    return correct / len(prompts)

def logitlens_rank(model, tok, prompts, answers, dids, bs=8):
    """Median correct-digit rank via lm_head on layer-35 h."""
    model.eval(); device = next(model.parameters()).device
    # Unwrap PeftModel to get internal model access
    base = model
    try:
        from peft import PeftModel
        if isinstance(model, PeftModel): base = model.base_model.model
    except ImportError: pass
    final_ln = base.model.norm
    lm_head_w = model.get_output_embeddings().weight.detach().to(device=device, dtype=torch.float32)
    ranks = []
    with torch.no_grad():
        for i in range(0, len(prompts), bs):
            bp = prompts[i:i+bs]; ba = answers[i:i+bs]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
            out = model(input_ids=enc["input_ids"].to(device), output_hidden_states=True, return_dict=True)
            h = out.hidden_states[FINAL_LAYER+1][:, -1, :].float()
            h_n = final_ln(h.to(device))
            logits = h_n @ lm_head_w.T
            for j, a in enumerate(ba):
                cid = dids[int(a)-1]
                r = int((logits[j] > logits[j, cid]).sum().item()) + 1
                ranks.append(r)
    return float(np.median(ranks))

def apply_lora(model, target_modules):
    from peft import LoraConfig, TaskType, get_peft_model
    cfg = LoraConfig(r=RANK, lora_alpha=ALPHA, target_modules=target_modules,
                     lora_dropout=0.0, bias="none", task_type=TaskType.CAUSAL_LM)
    return get_peft_model(model, cfg)

def train_lora(model, tok, prompts, answers, dids):
    opt = AdamW([p for p in model.parameters() if p.requires_grad], lr=LR)
    model.train(); device = next(model.parameters()).device
    rng = random.Random(42); n = len(prompts)
    t0 = time.time()
    for step in range(N_STEPS):
        idx = rng.choices(range(n), k=BS)
        enc = tok([prompts[i] for i in idx], return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
        inp = enc["input_ids"].to(device)
        labels = torch.tensor([dids[int(answers[i])-1] for i in idx], dtype=torch.long, device=device)
        logits = model(input_ids=inp).logits[:, -1, :]
        loss = nn.CrossEntropyLoss()(logits, labels)
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
        opt.step()
        if (step+1) % 40 == 0:
            log(f"    step {step+1}/{N_STEPS} loss={loss.item():.4f} elapsed={time.time()-t0:.0f}s")
    return time.time() - t0

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Phase124: LoRA variant ablation. device={device}")

    tok = AutoTokenizer.from_pretrained(MODEL, cache_dir=HF_CACHE, trust_remote_code=True, padding_side="left")
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    dids = get_ids(tok)
    prompts, answers = make_prompts(N_TRAIN + N_TEST, seed=SEED)
    tp, ta = prompts[:N_TRAIN], answers[:N_TRAIN]
    ep, ea = prompts[N_TRAIN:], answers[N_TRAIN:]

    variants = {
        "q_only": ["q_proj"],
        "k_only": ["k_proj"],
        "v_only": ["v_proj"],
        "o_only": ["o_proj"],
        "ffn_only": ["gate_proj"],  # FFN down-projection
        "q_v": ["q_proj", "v_proj"],  # baseline
    }

    results = {}
    for name, targets in variants.items():
        log(f"\n=== {name} ===")
        log(f"  targets={targets}")
        n_params = 2 * len(targets) * RANK * 4096  # rough estimate for rank-16
        log(f"  est params: {n_params:,}")

        model = AutoModelForCausalLM.from_pretrained(
            MODEL, cache_dir=HF_CACHE, trust_remote_code=True,
            torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
        model.eval()

        # Pre-LoRA baseline
        base_gen = eval_gen(model, tok, ep, ea, dids)
        base_rank = logitlens_rank(model, tok, ep, ea, dids)
        log(f"  baseline: gen={base_gen:.1%} rank_med={base_rank:.0f}")

        model = apply_lora(model, targets)
        train_time = train_lora(model, tok, tp, ta, dids)
        log(f"  training: {train_time:.0f}s")

        post_gen = eval_gen(model, tok, ep, ea, dids)
        post_rank = logitlens_rank(model, tok, ep, ea, dids)
        log(f"  post: gen={post_gen:.1%} rank_med={post_rank:.0f}")

        results[name] = {
            "target_modules": targets,
            "base_gen": float(base_gen), "post_gen": float(post_gen),
            "base_rank_med": base_rank, "post_rank_med": post_rank,
            "train_time_s": train_time,
        }
        with open(OUTPUT, "w") as f:
            json.dump({"metadata": {"phase":"124","model":MODEL,"seed":SEED},"results":results}, f, indent=2)

    log("\nPhase124 complete.")
    log("Variant comparison (generation accuracy | logit-lens median rank):")
    for name in ["q_only","k_only","v_only","o_only","ffn_only","q_v"]:
        if name in results:
            r = results[name]
            log(f"  {name:12s}: gen {r['base_gen']:.1%}→{r['post_gen']:.1%}  rank {r['base_rank_med']:.0f}→{r['post_rank_med']:.0f}")

if __name__ == "__main__":
    main()
