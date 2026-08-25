# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: ✅ Pass. Anonymous authors, no self-identifying links, prior work cited in third person.
- **Page limit**: ⚠️ Cannot verify from LaTeX source. Main-text content (Sections 1–7 + figures/tables) appears plausibly within 9 pages, but I cannot confirm the compiled length. Note that some load-bearing evidence (CoT comparison, DPS sensitivity analyses) is deferred to a "supplement" that is not part of the provided material.
- **AI use statement**: ✅ Present.
- **Style files**: ✅ Uses `iclr2027_conference` per the official template pattern. (A stale comment reads "NeurIPS 2026 style" — harmless leftover, but sloppy; also `\author{Anonymous authors\ ...}` contains a `\ `-space typo where a line break was likely intended.)

No desk-reject risks identified beyond the unverifiable page count.

---

## 1) Core Thesis & Significance

The paper asks whether transformer counting failures stem from missing internal representations or from an inability to read those representations out as output tokens. Using linear probes, logit-lens analysis, and three targeted interventions (9-row `lm_head` repair, LoRA on attention Q/V, and "Diagnostic Probe Steering"), the authors argue for a *geometric readout bottleneck*: counts are linearly decodable (R² > 0.99) but the count-encoding directions are nearly orthogonal to the digit rows of the output head (|cos| ≤ 0.032, statistically indistinguishable from random).

The problem is practically relevant (counting failures are well-documented and embarrassing), the contribution is cleanly summarizable, and the causal logic — constrained decoding should be fixed by output-row repair, generation should not, and upstream (Q/V) repair should fix both — is a genuinely falsifiable structure that the paper's experiments largely confirm. Novelty is integration-level (probes, logit lens, LoRA, and ROME-style row edits are all known tools) but the specific finding — that the misalignment is *causally* localized and repairable with 36,864 parameters under constrained decoding — is new and, to my knowledge, not established by prior counting work (Razeghi et al., Stolfo et al.).

## 2) Technical Soundness

**Strengths**: The causal logic is unusually well-instrumented: shuffled-label probes (R² = −0.042), random-direction controls, permutation tests, TOST equivalence testing, necessity/sufficiency controls (shuffled rows degrade below baseline), a locus ablation across Q/K/V/O/MLP, and negative controls on MMLU. Internal arithmetic checks out (9 × 4096 = 36,864; LoRA rank-16 Q/V ≈ 7.66M; 46,080 = 9 × 5120), which suggests genuine care.

**Concerns**:

**(b) Significant — the "knows vs. says" claim conflates three representational loci with very different decodability.** (i) The *entity-mean* aggregate (Table 3): R² ≈ 0.997, but this is a constructed multi-position average, and the reported layer-0 R² = 0.977 is a red flag — for RoPE models with a constant mention token, layer-0 states at mention positions are identical, so the mean cannot encode count unless the construction itself leaks it (e.g., via surface-form variation or position statistics). The factorial design randomizes distractors/length/spacing but does not remove count–position correlations in an averaged representation. (ii) *Last-token early layers*: claimed "R² ≥ 0.99 from layer 2" in one sentence, with no table or figure. (iii) *Last-token final layer* — the state the output head actually reads: its linear decodability is never directly reported, but the 9-row repair *is* a freely-trained linear readout from this state, and it plateaus at 60.7% (67.5% with Adam, no gain with 59 rows). If final-state linear decodability were ~99%, freely-trained rows should approach it; the paper's own "task-level ceiling" admission implies it is not. This means that for the flagship entity-counting task, the failure is *not* purely output-head geometry — count information at the readout position appears substantially degraded (~60–67%), which reframes the clean dichotomy "representation perfect / readout broken" into "partial aggregation loss + geometric misalignment." The dichotomy holds cleanly for character counting, addition, and list length (9-row repair 98–100%); it does not for entity counting, which is nonetheless the headline task. **Required: per-layer probe R² and linear classification accuracy at the last-token position (especially the final layer) for entity counting.**

**(b) Significant — the 0.0% generation result for the 9-row repair is unexplained and internally contradictory as written.** Table 1 reports the 9-row repair at 60.3% *full-vocabulary* next-token accuracy at the answer position, yet greedy generation is exactly 0.0%, and the appendix attributes this to "full-vocabulary argmax at each step is still misaligned" — contradicting Table 1's own 60.3%. A plausible confound the paper never addresses is digit tokenization variants: the 9 repaired rows are presumably bare digit tokens ("3"), while a base model's natural emission after a prompt or template is often " 3" (space-prefixed) — a *different* vocabulary row that was not repaired. The logit-masked control (59.2%) masks to the repaired token set and therefore cannot distinguish "upstream routing failure" from "wrong token variant wins." Since the constrained-vs-generation dissociation is nested Claim 2, the paper owes the reader error traces and an explicit treatment of digit-token variants. Note the repair also scores *below* the unmodified baseline (7.2% generation), which demands explanation.

**(b) Significant — cross-protocol numerical inconsistency.** The same intervention (9-row repair, held-out, Qwen3-8B entity counting) appears as 60.7% (Table 2, "mode-matched primary") and 93.8% (Table 4), and the Discussion summarizes "93–99% held-out accuracy," i.e., quoting the easier protocol while the primary protocol yields 60.7%. The Discussion also cites "LoRA (84%, 4M params)" — a configuration that appears in no table. Baseline entity-counting accuracy takes at least seven distinct values across the paper (7.2%, 10.3%, 11.3%, 13.7%, 14.2%, 17.0%, 38.6/38.8%). Soft DPS flips from 96.3% (Table 6) to 13.2% (Table 1) across protocols with only a partial reconciliation. The protocol-map appendix and "mode-matched" labels show commendable awareness, but the execution leaves the reader unable to reconstruct which number is canonical.

**(c) Typical limitations**: The probing-fallacy caveat (decodable ≠ used) is largely mitigated by the causal interventions, though see the locus issue above. The gradient-dynamics "why orthogonality" argument is a heuristic, not a proof — and the paper's own fine-tuning result (counting data raises |cos| by 3.2×) shows orthogonality is not a stable fixed point under the counting distribution, which is consistent with but weaker than the "stable fixed point" framing. GSM8K is claimed as a negative control in the abstract but no GSM8K numbers appear anywhere in the provided text. The intro's "best models achieve ≤24%" sits awkwardly beside the paper's own 38.8% stratified next-token figure. The 14B result (|cos| = 0.011, "0.57× random baseline") is *below* chance alignment, which would imply active avoidance rather than passive orthogonality — an interpretive distinction the paper glosses over.

## 3) Empirical Rigor

**Sufficient**: The core geometric claims are supported with statistics rare to see at this venue (bootstrap CIs, permutation tests, TOST). Multi-seed reporting (3–5 seeds) for headline numbers. The factorial prompt design is a serious attempt to kill distributional shortcuts. Mode-matched Table 1/Table 2 comparisons are exactly the right discipline. Trade-offs are quantified (parameters vs. accuracy; LoRA vs. CoT inference cost).

**Insufficient**: (1) The CoT comparison — central to the practical "How to Fix It" claim, since CoT requires no fine-tuning — is discussed in the main text with *no numbers* ("also substantially improves entity counting"). (2) GSM8K numbers absent. (3) No error analysis for the 0.0% generation result (see above). (4) The multi-digit claim "each digit position is independently misaligned" is asserted, not measured. (5) Real-benchmark transfer is weak and under-discussed relative to the title: DROP single-digit improves only 20.0% → 30.0%, which honestly tempers the claim that this bottleneck explains real counting failure, yet the abstract does not mention it. (6) Missing the single most decisive probe experiment (last-token final-layer classification accuracy; §2 above).

**Overclaiming check**: The abstract is accurate and appropriately hedged. The title's "How to Fix It" oversells a fix demonstrated on synthetic tasks with an 83.1% ceiling and marginal real-benchmark transfer; the body is more careful ("we are not claiming to beat CoT"). The Discussion's "93–99%" summary is selective relative to the primary protocol.

## 4) Competitive Realistic Check

Compared to typical accepted ICLR mechanistic-interpretability papers, this one is above average in controls (necessity/sufficiency, equivalence testing, locus ablations, negative controls) and in causal design, but below average in numerical hygiene and internal consistency. The memorable finding — correct digit rank dropping 55,980 → 1 under LoRA Q/V, and a 9-row repair causally restoring constrained decoding — is the kind of result reviewers repeat to colleagues. The weaknesses (protocol proliferation, unexplained 0.0%, locus conflation) are the kind that draw one low review but are addressable in rebuttal. At least two reasonable reviewers scoring ≥5: **yes, likely** — this is a plausible 5/6/6/4 review profile.

## 5) Weakest Link Analysis

**Weakest link**: the gap between the "the model knows the count" narrative and what is actually demonstrated *at the readout locus* for entity counting (~60–67% linear decodability implied by the repair ceiling, versus R² > 0.99 only at construction-assisted or early-layer loci), compounded by the unexplained 0.0% generation number. This is **addressable in revision**: it requires one additional probe table (last-token, per-layer, classification accuracy) and error traces for generation, plus a modest reframing ("partial aggregation degradation plus geometric misalignment" for entity counting). It is **not fundamental** — the orthogonality measurement, the DPS/oracle results, and the LoRA mechanism analysis stand independently — and the dissociation logic survives even if the 0.0% turns out to be a tokenization artifact (logit-masked 59.2% vs. LoRA 83.1% still separates output-head-only from upstream repair). Short of that clarification, I would not call this decision-stable; with it, the paper is comfortably acceptable.

## 6) Convergence Test (Minimal-Change Threshold)

As submitted: roughly a coin flip (~50%) — the controls and causal design argue for accept; the inconsistencies and the locus conflation give a skeptical reviewer enough to argue 4.

Minimal changes to clear the bar, in order of importance:
1. **Report last-token per-layer probe R² and final-layer linear classification accuracy for entity counting**, and reframe the "knows vs. says" claim accordingly.
2. **Explain the 0.0% generation result** with error traces and an explicit analysis of digit-token variants ("3" vs. " 3"); reconcile it with the 60.3% full-vocab next-token number.
3. **Harmonize the 9-row repair numbers** (60.7% vs. 93.8%) across Tables 1/2/4 and the Discussion; remove or define the dangling "LoRA (84%, 4M params)".
4. **Put CoT and GSM8K numbers in the main text.**

All four are evidence-based and feasible within a rebuttal cycle.

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant contribution with three nested, falsifiable claims — good structure.

- **(a) Strengthens the core**: mode-matched Tables 1–2, logit-lens section, locus ablation, MMLU negative control, necessity/sufficiency controls.
- **(b) Neutral**: majority vote, max extraction, multi-digit, 14B extensions (these support generality at modest cost).
- **(c) Adds attack surface**: the soft-DPS protocol saga (96.3% vs. 13.2%) is confusing and not load-bearing — demote to the appendix and keep only hard DPS in the main text. The "why orthogonality" gradient paragraph invites theory critique it cannot defend — either formalize or explicitly label it a conjecture. The Discussion's cross-protocol summary sentences ("93–99%", "LoRA 84%") should be rewritten against the primary protocol. The multi-digit "independently misaligned" sentence should be cut or supported. The task-definition example in §3 is ambiguous about whether numerals inside sentences are quantities to be summed or distractors to be ignored ("There are 2 apples…" with the answer defined as "the number of mentions"), which hampers reproduction.

## 8) ICLR Formal Scores

- **Soundness: 3/4.** The causal program (probes → geometry → interventions → controls) is sound and unusually well-instrumented, and most claims are supported. Docked for the locus conflation underlying the headline "knows" claim on entity counting, the unexplained/contradictory 0.0% generation number, and cross-table inconsistencies.
- **Presentation: 2/4.** Prose is clear and the claims-then-evidence structure is good, but the same quantity takes different values across tables and sections, key comparisons (CoT, GSM8K) are discussed without numbers, one task-defining example is ambiguous, and reproduction requires resolving protocol details the main text does not supply.
- **Contribution: 3/4.** A novel causal dissection of a well-documented failure mode: geometric misalignment of count directions with output rows, localized by a 9-row repair, with a deployable upstream fix and reusable diagnostic recipe. Individual tools are known; the finding and its causal validation are new.
- **Significance: 3/4.** The readout-bottleneck framing and the probe-then-measure-alignment-then-repair recipe are likely to be cited and applied to other competence-without-performance failures. Practical impact is limited by synthetic-task scope, an 83.1% generation ceiling, and weak DROP transfer (+10pp).
- **Overall: 6/10.** A clear accept: comfortably above the poster mean on experimental substance and causal design, held below 7 by internal-consistency problems and an over-clean "knows vs. says" narrative that the paper's own 60.7% entity-counting number complicates.
- **Confidence: 4/5.** I read the source closely and checked internal arithmetic, but figures, the supplement, and compiled output were unavailable.

## 9) Final Recommendation

**ICLR: Accept (6).**

This is a genuinely strong mechanistic study whose causal logic — constrained decoding fixed by output-row repair, generation fixed only by upstream Q/V repair, with mechanism confirmed by logit-lens rank shifts — is the kind of clean dissociation ICLR mech-interp reviewers value, and the control suite (necessity/sufficiency, equivalence testing, locus ablation, negative controls) exceeds venue norms. It is held back from a higher score by real but repairable hygiene failures: conflicting numbers for the same intervention across tables, an unexplained 0.0% generation result that contradicts the paper's own Table 1, and a headline framing ("the model knows the count") that the readout-locus evidence for entity counting only partially supports. If the rebuttal supplies the last-token probe measurements, generation error traces, and the missing CoT/GSM8K numbers, I would expect this to settle as a solid poster accept.