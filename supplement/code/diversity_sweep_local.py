#!/usr/bin/env python3
"""GRB diversity-controlled repair-ceiling sweep (local CPU/iGPU version).

Question (paper Limitation #4): why does 9-row lm_head repair cap at ~60% on
entity counting while other tasks reach ~100%?

Hypotheses:
  H1 norm competition      -> accuracy roughly independent of prompt diversity
  H2 intra-class diversity -> accuracy rises as prompt diversity shrinks

Design: fix the count distribution (uniform 1..9) and vary ONLY surface
diversity across four controlled levels (entity-pool size, template variety,
distractor load). Per level: extract last-position hidden states, fit a ridge
probe, train the 9-row margin repair against the full-vocabulary competitor,
evaluate digit-restricted + full-vocab accuracy in-domain and cross-level.
"""
import os, sys, json, time, random
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = os.environ.get("GRB_MODEL", "Qwen/Qwen3-8B")
OUT = Path(__file__).parent / "results_diversity_sweep.json"
DEVICE = os.environ.get("SWEEP_DEVICE", "cpu")
N_TRAIN, N_TEST = int(os.environ.get("SWEEP_TRAIN", "240")), int(os.environ.get("SWEEP_TEST", "160"))
SEED = 42
MARGIN, REPAIR_ITERS, LR = 2.0, 400, 0.05

ENTITIES = ["apple","car","dog","tree","book","chair","lamp","phone","cloud","river",
            "bird","shoe","ball","hat","pen","stone","star","fish","flag","coin"]
TEMPLATES = [
    "There are {k} {e} near the pond.",
    "I can see {k} {e} in the garden.",
    "The photo shows {k} {e} on the table.",
    "She counted {k} {e} this morning.",
]
LEVELS = {
    "D0_minimal":  dict(pool=1,  tmpl=1, dist_max=0),
    "D1_low":      dict(pool=3,  tmpl=2, dist_max=0),
    "D2_medium":   dict(pool=8,  tmpl=3, dist_max=2),
    "D3_original": dict(pool=20, tmpl=4, dist_max=4),
}

def log(m): print(f"[sweep] {m}", flush=True)

def make_prompts(level, n, rng):
    cfg = LEVELS[level]
    pool = rng.sample(ENTITIES, cfg["pool"])
    others = [e for e in ENTITIES if e not in pool]
    out = []
    for _ in range(n):
        e = rng.choice(pool)
        c = rng.randint(1, 9)
        sents = []
        tmpl = TEMPLATES[:cfg["tmpl"]]
        for _ in range(c):
            sents.append(rng.choice(tmpl).format(k=rng.randint(1, 3), e=e))
        nd = rng.randint(0, cfg["dist_max"])
        for d in rng.sample(others, min(nd, len(others))):
            dn = rng.randint(1, 4)
            sents.append(f"There are {dn} {d} in the area.")
        rng.shuffle(sents)
        text = " ".join(sents)
        out.append({"prompt": f"{text}\n\nCount how many {e} there are. Answer with just the number: ",
                    "answer": c})
    return out

@torch.inference_mode()
def extract(model, tok, prompts, bs=64):
    """Return (hiddens[N,D] float32 post-final-norm, answers[N]).
    Optimized path: length-sorted batches, backbone-only forward (skips the
    152K-vocab lm_head GEMM), no KV cache. Measured 2.42 vs 2.17 prompts/s on
    the 890M iGPU; the transformer body dominates, so gains are modest."""
    hs, ys = [], []
    dev = next(model.parameters()).device
    norm = model.model.norm
    order = sorted(range(len(prompts)), key=lambda i: len(prompts[i]["prompt"]))
    done = 0
    for i in range(0, len(order), bs):
        idx = order[i:i+bs]
        chunk = [prompts[j] for j in idx]
        enc = tok([p["prompt"] for p in chunk], return_tensors="pt",
                  padding=True, truncation=True, max_length=512, padding_side="left")
        inp = enc["input_ids"].to(dev)
        am = enc["attention_mask"].to(dev)
        out = model.model(input_ids=inp, attention_mask=am, use_cache=False)
        h_last = out.last_hidden_state[:, -1, :]           # left padding -> last pos is real
        h = norm(h_last).float().cpu().numpy()
        hs.append(h)
        ys.extend(int(p["answer"]) for p in chunk)
        done += len(chunk)
        if (done // 80) != ((done - len(chunk)) // 80):
            log(f"  extracted {done}/{len(prompts)}")
    H = np.concatenate(hs)
    # unsort back to original prompt order
    inv = np.empty_like(order)
    for rank, orig_idx in enumerate(order): inv[orig_idx] = rank
    return H[inv], np.array(ys)

def ridge_probe(H, y, lam=1.0):
    """Closed-form ridge regression to integer count; returns predict fn."""
    mu, sd = H.mean(0), H.std(0) + 1e-6
    X = (H - mu) / sd
    A = X.T @ X + lam * np.eye(X.shape[1])
    b = X.T @ y.astype(np.float64)
    w = np.linalg.solve(A, b)
    return lambda Z: ((Z - mu) / sd) @ w

def digit_ids(tok):
    ids = []
    for d in range(1, 10):
        t = tok.encode(str(d), add_special_tokens=False)
        ids.append(t[0] if len(t) == 1 else next(x for x in t if tok.decode([x]).strip() == str(d)))
    return ids

def train_repair(model, H, y, dids):
    """Margin-train the 9 digit rows against the full-vocab competitor."""
    W = model.lm_head.weight.detach().float().cpu().clone()
    rows = torch.tensor(dids, dtype=torch.long)
    Ht = torch.tensor(H)
    yt = torch.tensor(y - 1)
    with torch.no_grad():
        base_logits = Ht @ W.T                              # [N, V]
        mask = torch.ones(W.shape[0], dtype=torch.bool)
        mask[rows] = False
        competitor = base_logits[:, mask].max(dim=1).values  # max non-digit logit
    R = W[rows].clone().requires_grad_(True)
    opt = torch.optim.Adam([R], lr=LR)
    for it in range(REPAIR_ITERS):
        z = Ht @ R.T                                        # [N, 9]
        true_z = z.gather(1, yt.view(-1, 1)).squeeze(1)
        loss = torch.clamp(MARGIN + competitor - true_z, min=0).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    W[rows] = R.detach()
    return W

@torch.no_grad()
def eval_head(model, tok_cpu_W, H, y, dids, digit_restricted):
    """Digit-restricted or full-vocab argmax accuracy using a (possibly repaired) lm_head on CPU."""
    W = tok_cpu_W
    logits = torch.tensor(H) @ W.T
    if digit_restricted:
        dlogits = logits[:, dids]
        pred = dlogits.argmax(dim=1) + 1
    else:
        pred = logits.argmax(dim=1) + 1
    pred = torch.clamp(pred, 1, 9)
    return float((pred == torch.tensor(y)).float().mean())

def main():
    t00 = time.time()
    rng = random.Random(SEED)
    log(f"device={DEVICE} model={MODEL}")
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, dtype=torch.bfloat16, low_cpu_mem_usage=True).to(DEVICE)
    model.eval()
    torch.set_num_threads(24)
    dids = digit_ids(tok)

    data = {}
    for lvl in LEVELS:
        tr = make_prompts(lvl, N_TRAIN, rng)
        te = make_prompts(lvl, N_TEST, rng)
        log(f"{lvl}: extracting train ({len(tr)})...")
        Htr, ytr = extract(model, tok, tr)
        log(f"{lvl}: extracting test ({len(te)})...")
        Hte, yte = extract(model, tok, te)
        data[lvl] = {"Htr": Htr, "ytr": ytr, "Hte": Hte, "yte": yte}

    results = {"provenance": {
        "model": MODEL, "device": DEVICE, "seed": SEED,
        "n_train_per_level": N_TRAIN, "n_test_per_level": N_TEST,
        "repair": f"9-row margin {MARGIN} vs full-vocab competitor, Adam lr={LR}, iters={REPAIR_ITERS}",
        "hidden": "last-position post-final-norm, bf16 model, float32 numpy",
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, "in_domain": {}, "probe_r2": {}, "cross_level": {}}

    baseline_W = model.lm_head.weight.detach().float().cpu().clone()

    for lvl in LEVELS:
        d = data[lvl]
        probe = ridge_probe(d["Htr"], d["ytr"])
        pr = probe(d["Hte"])
        r2 = 1 - ((pr - d["yte"]) ** 2).sum() / ((d["yte"] - d["yte"].mean()) ** 2).sum()
        results["probe_r2"][lvl] = round(float(r2), 4)

        b_dr = eval_head(model, baseline_W.numpy(), d["Hte"], d["yte"], dids, True)
        repW = train_repair(model, d["Htr"], d["ytr"], dids)
        r_dr = eval_head(model, repW.numpy(), d["Hte"], d["yte"], dids, True)
        r_fv = eval_head(model, repW.numpy(), d["Hte"], d["yte"], dids, False)
        results["in_domain"][lvl] = {
            "baseline_digit_restricted": round(b_dr, 4),
            "repair_digit_restricted": round(r_dr, 4),
            "repair_fullvocab": round(r_fv, 4),
            "probe_r2": results["probe_r2"][lvl],
        }
        OUT.write_text(json.dumps(results, indent=1))
        log(f"{lvl}: probeR2={r2:.3f} base={b_dr:.3f} repair_dr={r_dr:.3f} repair_fv={r_fv:.3f}")

    log("cross-level: train D0_minimal -> test each level")
    d0 = data["D0_minimal"]
    repW0 = train_repair(model, d0["Htr"], d0["ytr"], dids)
    for lvl in LEVELS:
        acc = eval_head(model, repW0.numpy(), data[lvl]["Hte"], data[lvl]["yte"], dids, True)
        results["cross_level"][f"D0_to_{lvl}"] = round(acc, 4)
    log("cross-level done")

    idm = results["in_domain"]
    results["summary"] = {
        "diversity_gradient_repair": {l: idm[l]["repair_digit_restricted"] for l in LEVELS},
        "interpretation_hint": (
            "monotonic decline with diversity supports H2 intra-class diversity; "
            "flat profile supports H1 norm competition"),
    }
    OUT.write_text(json.dumps(results, indent=1))
    log("DONE " + json.dumps(results["summary"]))
    log(f"total {round((time.time()-t00)/60,1)} min")

if __name__ == "__main__":
    main()
