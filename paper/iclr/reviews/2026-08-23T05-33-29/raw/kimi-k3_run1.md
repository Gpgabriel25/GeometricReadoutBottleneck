# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: ✅ No author-identifying information detected; anonymous author block; no non-anonymous links.
- **AI Use Statement**: ✅ Present (does not count toward page limit).
- **Style files**: ⚠ The file loads `iclr2027_conference`, but the preamble comment reads "% NeurIPS 2026 style — submission mode." The actual package appears correct (stale comment), but I cannot verify from source alone that the official ICLR 2027 style files are unmodified.
- **Page limit**: ⚠ **Cannot verify compiled length from LaTeX source.** The main text contains 2 figures and 5 tables across ~7 sections; it appears close to the 9-page ceiling. The authors should verify the compiled PDF is ≤ 9 pages. Core evidence (Tables 1–5) does live in the main text, which is good.

No hard desk-reject violations identified.

---

## 1) Core Thesis & Significance

**Central contribution**: LLM counting failures are diagnosed as a *geometric readout bottleneck* rather than a representational failure. Linear probes recover counts at R² > 0.99 from residual streams, yet count-encoding directions are near-orthogonal to `lm_head` digit rows (|cos| ≤ 0.032, statistically indistinguishable from random). Two interventions causally localize the failure: a 9-digit-row `lm_head` repair (fixes constrained decoding, fails in generation) and LoRA Q/V (fixes generation, 83.1%).

**Relevance**: Practically relevant — counting failures are a well-documented, embarrassing LLM weakness, and "competence without performance" is a general phenomenon of interest to the interpretability community. The tasks are synthetic but the framing is honest about this.

**Novelty**: Integration-level. Probes, logit lens, and targeted fine-tuning are all standard tools; the contribution is assembling them into a clean, falsifiable mechanistic story with unusually thorough controls. The specific finding — orthogonality between aggregate representations and digit rows, sharpening with scale — is a genuinely new observation, not just a recombination.

**Summarizability**: A reviewer can unambiguously state the contribution. The paper is well-scoped and self-aware about its boundaries (low-vocabulary aggregation tasks only).

## 2) Technical Soundness

The logical chain is sound: (a) information present (probes, with shuffled-label controls at R² = −0.042); (b) readout misaligned (cosine vs. random baseline, permutation test, TOST equivalence, positive control at 3.3× higher alignment); (c) causal localization (9-row repair with shuffled-row and random-position controls degrading to/below baseline); (d) mechanism confirmation (logit-lens rank 55,980 → 1 under LoRA Q/V).

**Issues:**

- **(b) Significant concern — the "why orthogonality" account is thin.** The training-dynamics fixed-point argument is plausible but the supporting experiment is weak: counting fine-tuning raises |cos| only 0.0074 → 0.0280, which is still effectively zero. This shows alignment *doesn't* easily form, which supports stability but doesn't strongly confirm the proposed E[h|y=digit] mechanism. The different starting points across runs (acknowledged) further weaken the contrast.
- **(c) Typical limitation — Hard DPS is partially circular as evidence.** Adding +100 to the probe-predicted digit's logit is essentially probe-round by construction; it confirms the probe is correct, not independently that the bottleneck is geometric. The paper mostly treats it correctly (as a sanity check / upper bound), but the 96.3% (single-seed) vs. 13.2% (multi-seed) soft-DPS discrepancy reveals that soft DPS — the more "interesting" variant — essentially does not work under the harmonized protocol. The appendix explanation (non-digit argmax dominance) is credible and disclosed.
- **(c) Typical limitation — entity-counting repair gap.** 9-row repair reaches 60.7% on entity counting vs. 98–100% on other tasks, with a striking count-magnitude dependence (30.6% at count 7 vs. 100% at count 2). The capacity ablation rules out fitting method and row count, but the residual explanation (norm competition + intra-class variance) is not fully discriminated — acknowledged in limitations.
- **(c) Typical limitation — "generation gap = 0.000 across all seeds"** is an ambiguous and suspiciously perfect statistic; it needs a precise definition (train/test generation delta?) to be evaluable.

No fatal flaws. The core claims are supported by the evidence presented.

## 3) Empirical Rigor

**Strengths:**
- Factorial prompt design explicitly blocking distributional shortcuts (distractors, length, spacing independent of count) — this is better than most probing papers.
- Multi-seed reporting with std for headline numbers; single-seed results clearly relegated/labeled.
- Necessity *and* sufficiency controls (shuffled rows < baseline; random-position rows = baseline).
- Negative controls (MMLU/GSM8K with |cos| = 0.31–0.48) demonstrate the effect is specific, not generic — this is exactly the right scope-discipline experiment.
- Full-`lm_head` fine-tune control (94.2% vs. 9-row 93.8%) shows 9 rows suffice — a genuinely informative comparison.
- Cross-model (3 families + 14B) and cross-task (4+ tasks) coverage.

**Gaps:**
- **No head-to-head CoT numbers under the paper's own protocol in the main text.** CoT is the obvious incumbent solution; the discussion makes a careful scoring-methodology point (final vs. first integer) but then defers the actual comparison to the supplement. This is the most conspicuous missing experiment.
- **No general-capability evaluation after LoRA Q/V.** The intervention is called "deployable," but there is no check that fine-tuning Q/V on counting doesn't degrade MMLU/perplexity. Cheap to run, directly relevant to the deployability claim.
- **Protocol proliferation.** Baselines of 10.3%, 11.3%, 13.7%, 17.0%, 38.6%, and 38.8% for the same underlying model/task pair appear across the paper. The "How to read the numbers" paragraph discloses this honestly, but it places a heavy bookkeeping burden on reviewers and creates surface area for (incorrect) cherry-picking suspicions. A single canonical protocol with all others in the appendix would be stronger.
- LoRA Q/V is trained on the evaluation task family; the claim it works via "routing correction" rather than task memorization is supported (layer-2 probe direction unchanged, logit-lens gains, cross-task transfer), but a LoRA-on-unrelated-task control would close the loop.

**Overclaiming check**: The title and "How to Fix It" phrasing is slightly broad given the fix requires task-specific fine-tuning and the primary diagnostic (9-row) achieves 0.0% in generation — but the body text is consistently careful about scoping ("deployable LoRA," "diagnostic instrument"). No claims clearly exceed the evidence.

## 4) Competitive Realism Check

Relative to accepted ICLR interpretability papers: the verification thoroughness here (controls, equivalence testing, cross-model, negative controls, honest failure reporting) is *above* the accepted-paper median. The novelty is *at* the median — this is a rigorous case study, not a new method or theory. The synthetic-task dominance and the "fix = fine-tune on the task" nature of the deployable intervention are typical limitations, not disqualifying ones. The Pythia-410M repair failure (31.4%) is handled honestly by scoping the claim.

Would two reasonable reviewers score this ≥5? Yes — the diagnosis is crisp and the evidence chain is complete. Would a skeptical reviewer score it ≤4? Plausibly, on "the fix is just fine-tuning" grounds. This places it squarely in the borderline-accept band.

## 5) Weakest Link Analysis

**Weakest link**: The deployable-fix claim rests on LoRA Q/V trained directly on counting-task data. A reviewer can read Table 1's 83.1% generation result as "fine-tuning on counting improves counting," which would deflate contribution (3) of 4 and reframe the paper as diagnosis-only. The mechanistic evidence (routing-specificity: layer-2 direction unchanged, logit-lens 9.3%→71.8%, cross-task transfer) substantially mitigates this, and the missing pieces are **addressable in revision**: (i) CoT baseline under the identical final-integer scorer, (ii) post-LoRA general-capability eval, (iii) an off-task LoRA control. None of these require new methodology. This issue is decision-relevant but unlikely to be fatal given the diagnostic contribution stands independently.

## 6) Convergence Test

**As-is acceptance probability: ~45–55%** — genuinely borderline. The diagnosis is strong enough that some reviewers will score 6 on rigor alone; the fix's task-specificity will pull others to 4.

**Minimal changes to push over the threshold** (all experimental, none editorial):
1. Add CoT accuracy under the paper's own final-integer scorer in the main-text comparison table (one experiment, infrastructure exists).
2. Report MMLU/perplexity after LoRA Q/V to substantiate "deployable."
3. Consolidate to one canonical protocol for headline numbers, moving variants to the appendix.

Items 1–2 are each likely worth more than any amount of prose revision.

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant claim (geometric readout bottleneck). Content classification:

- **(a) Strengthens core**: negative controls (MMLU/GSM8K), necessity/sufficiency row controls, full-`lm_head` comparison, scale-sharpening result (|cos| = 0.011 at 14B).
- **(b) Neutral**: majority-vote and max-extraction extensions — supportive but add little beyond the four main tasks.
- **(c) Attack surface**: the DROP result (+10pp, "partial but incomplete") invites scrutiny without paying off; the multi-digit extension (42.1% fullvocab repair) is weaker than the main story and dilutes it; the proliferation of baselines/protocols (six different baseline numbers) is self-inflicted complexity.

**Recommendation**: Move DROP and the multi-digit extension fully to the appendix with one summarizing sentence in the main text. This removes the weakest numbers from the critical path without weakening any core claim.

## 8) ICLR Formal Scores

- **Soundness (3/4)**: The core diagnostic chain is well-supported with proper controls; the training-dynamics explanation is under-evidenced and some statistics ("generation gap = 0.000") are under-specified.
- **Presentation (3/4)**: Clearly written and unusually honest, but protocol proliferation (six baseline values, DPS discrepancies across tables) imposes real bookkeeping cost on the reader.
- **Contribution (3/4)**: A clean, falsifiable mechanistic diagnosis with causal localization; tools are standard but the specific finding (orthogonality, scale-sharpening, task-family generality) is new knowledge.
- **Significance (3/4)**: The "knows the count but can't say it" framing is memorable and the diagnostic recipe (probe → align → repair) may be reused for other competence-performance gaps; impact is limited by synthetic tasks and a fine-tuning-based fix.
- **Overall (5/10)**: Solid poster-tier work: above-average rigor, average novelty, honest scoping. Sits at the accept/reject boundary; the missing CoT and post-intervention capability checks are what separate it from a comfortable 6.
- **Confidence (4/5)**: Familiar with the probing/logit-lens/model-editing literature; confident in the assessment of the evidence chain, slightly less so on the LoRA mechanism interpretation.

## 9) Final Recommendation

**ICLR: Borderline Accept (5)**

This is a careful, honest piece of mechanistic interpretability that answers a clean question with a complete evidence chain and better controls than most accepted work in this area. It is held back from a clear accept by the deployable-fix claim resting on task-specific fine-tuning without an incumbent-baseline (CoT) or capability-regression check, and by self-inflicted protocol complexity. Both gaps are cheap to close; if the authors add the CoT head-to-head and post-LoRA capability evaluation, this becomes a comfortable poster accept.