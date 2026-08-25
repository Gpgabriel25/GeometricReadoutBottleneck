#!/usr/bin/env python3
"""Phase122b: CoT baseline RE-SCORE on CPU.

Reproduces phase122_cot.py conditions (direct / zero-shot CoT / few-shot CoT,
Qwen3-8B greedy) and scores every generation under BOTH extraction rules:
  first-digit  (the original buggy scorer - credits counting seeds)
  final-digit  (corrected scorer - the model's actual emitted answer)
This quantifies exactly how much the paper's original CoT numbers were inflated.
"""
import os, json, time, random, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen3-8B"
SEED, N_TEST, MAX_LENGTH = 42, 200, 256
OUT = Path(__file__).with_name("results_phase122b_dual_scored.json") if False else None
from pathlib import Path
OUT = Path(__file__).parent / "results_phase122b_dual_scored.json"
ENTITIES = ["apple","car","dog","tree","book","chair","lamp","phone","cloud","river",
            "bird","shoe","ball","hat","pen","stone","star","fish","flag","coin"]
def log(m): print(f"[phase122b] {m}", flush=True)

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

def eval_gen(model, tok, prompts, answers, digit_ids, max_new):
    model.eval()
    device = next(model.parameters()).device
    first_correct = last_correct = 0
    gens = []
    with torch.no_grad():
        for i in range(0, len(prompts), 8):
            bp = prompts[i:i+8]; ba = answers[i:i+8]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
            inp = enc["input_ids"].to(device)
            am = enc.get("attention_mask"); am = am.to(device) if am is not None else None
            gen = model.generate(input_ids=inp, attention_mask=am, max_new_tokens=max_new,
                                 do_sample=False, pad_token_id=tok.pad_token_id or tok.eos_token_id)
            new = gen[:, inp.shape[1]:]
            for j, a in enumerate(ba):
                toks = new[j].tolist()
                digits = [t for t in toks if t in digit_ids]
                pred_first = digit_ids.index(digits[0]) + 1 if digits else None
                pred_last = digit_ids.index(digits[-1]) + 1 if digits else None
                if pred_first == int(a): first_correct += 1
                if pred_last == int(a): last_correct += 1
                if len(gens) < 12:
                    gens.append({"target": int(a), "gen": tok.decode(new[j], skip_special_tokens=True)[:120],
                                 "first": pred_first, "last": pred_last})
    n = len(prompts)
    return {"first_digit_acc": round(first_correct/n, 4), "final_digit_acc": round(last_correct/n, 4),
            "n": n}, gens

def main():
    t00 = time.time()
    device = "cpu"
    torch.set_num_threads(24)
    log(f"device={device} threads={torch.get_num_threads()}")
    tok = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True, padding_side="left")
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    digit_ids = [tok.encode(d, add_special_tokens=False)[0] for d in list("123456789")]
    prompts, answers = make_prompts(N_TEST, SEED)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    model.eval()

    results = {"provenance": {"model": MODEL, "device": device, "n": N_TEST, "seed": SEED,
               "note": "dual-scored: first-digit (legacy buggy scorer) vs final-digit (corrected)",
               "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
               "conditions": {}, "samples": {}}

    cot_prompts = [p.replace("Answer with just the number:",
                   "Let's count step by step. The final answer is:") for p in prompts]
    example = ("There are 2 cat near the pond. There are 2 cat near the pond. There are 2 cat near the pond.\n\n"
               "Count how many cat there are. Let's count step by step. The final answer is: 3")
    fs_prompts = [f"{example}\n\n{p}" for p in cot_prompts]

    for name, ps, mn in [("direct", prompts, 10), ("zeroshot_cot", cot_prompts, 50), ("fewshot_cot", fs_prompts, 50)]:
        if name in results["conditions"]:
            log(f"cached {name}"); continue
        t0 = time.time()
        r, gens = eval_gen(model, tok, ps, answers, digit_ids, mn)
        r["minutes"] = round((time.time()-t0)/60, 1)
        results["conditions"][name] = r
        results["samples"][name] = gens
        OUT.write_text(json.dumps(results, indent=1))
        log(f"{name}: first={r['first_digit_acc']:.1%} final={r['final_digit_acc']:.1%} ({r['minutes']} min)")

    c = results["conditions"]
    results["summary"] = {
        "inflation_zeroshot_cot_pp": round((c["zeroshot_cot"]["first_digit_acc"] - c["zeroshot_cot"]["final_digit_acc"]) * 100, 1),
        "inflation_fewshot_cot_pp": round((c["fewshot_cot"]["first_digit_acc"] - c["fewshot_cot"]["final_digit_acc"]) * 100, 1),
        "direct_final": c["direct"]["final_digit_acc"],
        "zeroshot_cot_final": c["zeroshot_cot"]["final_digit_acc"],
        "fewshot_cot_final": c["fewshot_cot"]["final_digit_acc"],
    }
    results["provenance"]["completed_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    OUT.write_text(json.dumps(results, indent=1))
    log("DONE " + json.dumps(results["summary"]))

if __name__ == "__main__":
    main()
