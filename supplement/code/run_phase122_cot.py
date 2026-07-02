#!/usr/bin/env python3
"""
Phase122: Quick CoT baseline pilot for entity counting.
Minimal: 1 seed, N=200 test, compare direct vs CoT prompt.
"""
import os, random, time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

HF_CACHE = os.environ.get("HF_CACHE", "/home/gpgabriel25/hf_cache")
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE; os.environ["HF_HOME"] = HF_CACHE

MODEL = "Qwen/Qwen3-8B"
SEED, N_TEST, MAX_LENGTH = 42, 200, 256
ENTITIES = ["apple","car","dog","tree","book","chair","lamp","phone","cloud","river",
            "bird","shoe","ball","hat","pen","stone","star","fish","flag","coin"]

def log(msg): print(f"[phase122] {msg}", flush=True)

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

def eval_gen(model, tok, prompts, answers, digit_ids, max_new=10):
    model.eval()
    device = next(model.parameters()).device
    correct = 0
    with torch.no_grad():
        for i in range(0, len(prompts), 4):
            bp = prompts[i:i+4]; ba = answers[i:i+4]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
            inp = enc["input_ids"].to(device)
            am = enc.get("attention_mask")
            if am is not None: am = am.to(device)
            gen = model.generate(input_ids=inp, attention_mask=am, max_new_tokens=max_new,
                                 do_sample=False, pad_token_id=tok.pad_token_id or tok.eos_token_id)
            new = gen[:, inp.shape[1]:]
            for j, a in enumerate(ba):
                # Extract first digit token from generation
                tokens = new[j].tolist()
                found = False
                for tid in tokens:
                    if tid in digit_ids:
                        if tid == digit_ids[int(a)-1]: correct += 1
                        found = True
                        break
                if not found and len(tokens) > 0:
                    # Check if first token is the digit
                    if int(tokens[0]) == digit_ids[int(a)-1]: correct += 1
    return correct / len(prompts)

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Phase122: CoT baseline pilot. device={device}")

    tok = AutoTokenizer.from_pretrained(MODEL, cache_dir=HF_CACHE, trust_remote_code=True, padding_side="left")
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    digit_ids = [tok.encode(d, add_special_tokens=False)[0] for d in ["1","2","3","4","5","6","7","8","9"]]

    prompts, answers = make_prompts(N_TEST, seed=SEED)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL, cache_dir=HF_CACHE, trust_remote_code=True,
        torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    model.eval()

    # 1) Direct generation (no CoT) — max_new_tokens=10, extract first digit
    t0 = time.time()
    direct_acc = eval_gen(model, tok, prompts, answers, digit_ids, max_new=10)
    log(f"  Direct gen (max_new=10): {direct_acc:.1%} ({time.time()-t0:.0f}s)")

    # 2) CoT prompt
    cot_prompts = [p.replace("Answer with just the number:", 
                              "Let's count step by step. The final answer is:") 
                   for p in prompts]
    t0 = time.time()
    cot_acc = eval_gen(model, tok, cot_prompts, answers, digit_ids, max_new=50)
    log(f"  CoT gen (max_new=50): {cot_acc:.1%} ({time.time()-t0:.0f}s)")

    # 3) Few-shot CoT (1 example)
    example = "There are 2 cat near the pond. There are 2 cat near the pond. There are 2 cat near the pond.\n\nCount how many cat there are. Let's count step by step. The final answer is:"
    example_answer = "3"
    fewshot_prompts = [f"{example} {example_answer}\n\n{p}" for p in cot_prompts]
    t0 = time.time()
    fs_acc = eval_gen(model, tok, fewshot_prompts, answers, digit_ids, max_new=50)
    log(f"  Few-shot CoT gen: {fs_acc:.1%} ({time.time()-t0:.0f}s)")

    log(f"\nPhase122 complete.")
    log(f"  Direct: {direct_acc:.1%}")
    log(f"  Zero-shot CoT: {cot_acc:.1%}")
    log(f"  Few-shot CoT: {fs_acc:.1%}")

    import json
    with open("/tmp/results_phase122_cot.json","w") as f:
        json.dump({"direct": direct_acc, "zeroshot_cot": cot_acc, "fewshot_cot": fs_acc}, f, indent=2)

if __name__ == "__main__":
    main()
