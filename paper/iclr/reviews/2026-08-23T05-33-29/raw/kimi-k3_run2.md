# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: ✅ Author block is anonymized; no identifying links, acknowledgments, or self-revealing citations detected in the provided source.
- **Page limit**: ⚠ **Cannot verify precisely from LaTeX source.** The main text is dense — 8 sections plus 6 substantial floats (2 figures, 4 tables) before the references. This plausibly lands at 9–10 pages compiled. The authors must verify the compiled main text is ≤ 9 pages; if it is at the boundary, this is a genuine risk item.
- **AI use statement**: ✅ Present ("AI Use Statement").
- **Style files**: ✅ Uses `iclr2027_conference` package. (Minor: the header comment says "NeurIPS 2026 style" — a leftover, scientifically irrelevant, but worth cleaning.)

No confirmed desk-reject violations; page count needs author verification.

---

## 1) Core Thesis & Significance

The paper argues that transformer counting failure is a **geometric readout bottleneck**, not a representational failure: counts are linearly decodable from the residual stream at $R^2 > 0.99$, but the count-encoding direction is nearly orthogonal to the digit rows of `lm_head` ($|\cos| \leq 0.032$ ≈ random). Three interventions triangulate the claim: a 9-row `lm_head` repair fixes constrained next-token prediction but not generation; LoRA Q/V fixes generation (83.1%); Diagnostic Probe Steering (DPS) bypasses the head analytically.

- **Practical relevance**: Counting failure is a well-known, genuinely puzzling LLM weakness; a crisp mechanistic account is of interest to the interpretability and LLM-reliability communities.
- **Novelty type**: Component-level novelty is moderate — "models encode more than they can express" is established (logit lens, tuned lens, probing literature, all cited). The novel elements are: (i) quantifying the gap as *orthogonality to specific unembedding rows* with refit probes at the final layer; (ii) causal localization via a minimal 9-row intervention; (iii) an informal but empirically tested "orthogonality as fixed point of training dynamics" explanation (counting fine-tune raises $|\cos|$ 3.2×, arithmetic fine-tune does not). This is a solid integration-and-measurement contribution, not a conceptual breakthrough.
- **Summarizability**: A reviewer can state the contribution unambiguously — that is a strength. "9 rows of `lm_head`" is a memorable, shareable hook.

## 2) Technical Soundness

**(a) Fatal flaws**: None identified in the core chain (probe → orthogonality → causal repair).

**(b) Significant concerns**:

1. **Soft-DPS internal inconsistency.** Table 1 reports Soft DPS at 13.2% (≈ baseline) under **digit-restricted** next-token argmax. The appendix explains soft-DPS failure by non-digit tokens winning the *full-vocabulary* argmax. That explanation cannot apply under digit-restricted argmax — if only digits compete, a Gaussian boost on the predicted digit's logit should work. Either the table column is mislabeled, or the explanation is wrong. Compounding this: single-seed soft DPS achieves 96.3% while the multi-seed/diverse-template protocol gives ≈13% — a near-total reversal that suggests soft DPS is extremely fragile to prompt distribution. DPS is auxiliary to the core claims, but this discrepancy raises hygiene questions about the many protocols in the paper and must be reconciled.

2. **Mid-layer orthogonality is partially expected.** That a mid-layer probe direction is not aligned with `lm_head` is, to a first approximation, what the tuned-lens literature (cited) already tells us — intermediate states are not natively read by the unembedding. The load-bearing version of the claim is the **final-layer, refit-probe** orthogonality (last-token $|\cos| \leq 0.014$) plus the causal repairs. The paper would be stronger if the headline framing foregrounded the final-layer result rather than the across-layers mean ($|\cos| = 0.016$), which mixes trivially-expected mid-layer misalignment with the meaningful final-layer result.

**(c) Typical limitations** (common in accepted work):

- The "fixed point of training dynamics" argument is informal; the two fine-tuning runs start from different checkpoints (0.0074 vs 0.0087 baseline alignment), which the authors acknowledge. The relative-change contrast (3.2× vs 1.1×) is still informative.
- The "scale sharpens the bottleneck" claim rests on one model per scale point (8B vs 14B); thin as a scaling law, fine as an observation.
- The entity-mean probe position is an engineered representation (mean-pooling over mention positions); the factorial randomization over length/spacing/distractors adequately defends against shortcut readings.
- The entity-counting repair ceiling (~60%) is partially unexplained; the capacity ablation (59 rows, Adam vs ridge) is a good-faith attempt.

## 3) Empirical Rigor

This is the paper's strongest dimension.

- **Controls**: shuffled-label probes ($R^2 = -0.042$), random-direction cosine baselines with permutation test and TOST equivalence, four probe types, shuffled-row and random-position necessity/sufficiency controls for the repair, format robustness across 4 templates, positive control (predicted-token probe at $|\cos|=0.115$). This is a more complete control battery than most accepted interpretability papers.
- **Multi-model/multi-task**: three families (Pythia-410M, Mistral-7B, Qwen3-8B/14B), four-plus tasks (entity/character counting, addition, list length, majority vote, max extraction, multi-digit), negative controls on MMLU/GSM8K with the predicted *absence* of the effect ($|\cos| = 0.31$–$0.48$) — the negative controls are genuinely falsifying and well-chosen.
- **Baselines**: The locus ablation (LoRA on Q/K/V/O/MLP) is reported only in prose without a table; a **full fine-tuning baseline for generation is missing**, which matters because the "deployable fix" (LoRA Q/V, 83.1%) is task-specific fine-tuning — readers will want to know what full FT or larger-rank LoRA achieves.
- **Trade-offs quantified**: constrained vs. generation mode, param counts (36,864 vs 7.67M), per-count stratification showing the repair degrades with count magnitude. Good.
- **Overclaiming check**: The prose is unusually careful (protocol map, "how to read the numbers," explicit limitations). Two exceptions: (i) the title's "**How to Fix It**" overpromises — the generation-mode fix is standard task-specific LoRA fine-tuning, and the 9-row repair is explicitly a diagnostic; (ii) the high variance of the headline generation number (71.5–89.0% across seeds; ±7.2%) is reported honestly but the abstract's "83.1%" is the multi-task mean while entity-only is 94–97% — both are disclosed, so this is presentation rather than misrepresentation.
- **Number sprawl**: The same intervention appears as 60.7% / 93.8% / 99.9% under different protocols. The authors handle this transparently, but three values for one intervention is a symptom of an evaluation assembled in layers; consolidation would improve credibility more than additional experiments would.

## 4) Competitive Realism Check (Calibrated)

Relative to accepted ICLR interpretability/mechanistics posters, this paper's experimental substance is **above average**: multi-seed, multi-model, causal interventions, necessity/sufficiency controls, and negative controls are more than the typical accepted poster provides. The conceptual novelty (representation–readout gap) is moderate and the finding is an especially clean instance rather than a new phenomenon. The weaknesses — the soft-DPS inconsistency, protocol sprawl, missing full-FT baseline — are **within acceptance variance** for the poster tier, not worse than average. Would at least two reasonable reviewers score ≥5? **Yes**, plausibly three, with scores likely spread 4–6 depending on how much weight each places on the DPS inconsistency and the incremental framing.

## 5) Weakest Link Analysis

The single most decision-relevant issue is the **soft-DPS contradiction (96.3% single-seed vs. 13.2% under digit-restricted argmax, with an explanation that cannot apply to digit-restricted argmax)**. It is the one place where a careful reviewer cannot make the paper's own numbers mutually consistent, and it casts a shadow over the otherwise strong protocol hygiene.

- **Addressable in revision**: Yes — almost certainly a labeling/protocol bookkeeping error or a missing detail about how soft DPS was scored in the unified table. Fixable with a corrected table and one paragraph.
- **Decision impact**: Unlikely to flip the decision by itself, because DPS is corroborating rather than load-bearing (the core claims rest on probes, refit-probe orthogonality, 9-row repair, and LoRA Q/V, all with multi-seed support). But if a reviewer discovers it unaided, it disproportionately damages trust in the many other numbers.

## 6) Convergence Test (Minimal-Change Threshold)

- **As-is acceptance probability: ~40–50%.** The paper sits at the accept/reject boundary: poster-quality experimental rigor, moderate novelty, one unresolved internal inconsistency.
- **Minimal changes to cross the threshold** (evidence-based, not editorial):
  1. Reconcile the soft-DPS numbers and the digit-restricted vs. full-vocab explanation (correct the table or the explanation).
  2. Add a **full fine-tuning generation baseline** at matched data (to contextualize the 83.1% LoRA claim).
  3. Reframe the headline orthogonality around the **final-layer refit-probe** result ($|\cos| \leq 0.014$ at last-token), explicitly preempting the "mid-layer states are never lm_head-aligned anyway" objection.
  4. Optionally, cut or demote DPS to the appendix — it adds attack surface (see §7) without carrying weight.

With (1)–(3), I would expect acceptance probability to rise to ~65–75%.

## 7) Structural Sharpness & Scope Control

The paper is centered on one dominant claim (geometric readout bottleneck), and most content serves it:

- **(a) Strengthens core**: probes + controls, refit-probe orthogonality, 9-row repair + necessity/sufficiency, LoRA Q/V mechanism analysis (logit-lens rank 55,980→1, probe $R^2$ unchanged at layer 2), MMLU/GSM8K negative controls, norm-competition analysis, fine-tuning fixed-point test.
- **(b) Neutral**: majority-vote and max-extraction extensions (nice-to-have generalization, low risk), multi-digit extension, instruct-mode check.
- **(c) Introduces attack surface**: **DPS** (the hard/soft distinction, the 96.3%↔13.2% reversal, and the "bypasses the output head" framing — it is a decoding oracle, not a model property); the **14B scaling claim** (n=1 per scale); the **generation-mode battery** (five variants, several landing at 0.0% or relying on logit masking) which adds tables without adding information beyond "routing is upstream."

**Recommendation**: demote DPS to an appendix diagnostic, drop or heavily hedge the scaling sentence, and merge the generation-mode variants into one table. These cuts remove the most attackable material while leaving every core claim intact.

## 8) ICLR Formal Scores

- **Soundness: 3 (good)** — Core causal chain is well-supported with strong controls; the unreconciled soft-DPS inconsistency and the mid-layer-vs-final-layer framing prevent a 4.
- **Presentation: 3 (good)** — Organized, transparent about protocols (the protocol map and "how to read the numbers" are commendable), but dense and number-sprawled; the same intervention appearing under 3–4 values taxes the reader.
- **Contribution: 3 (good)** — A clean, well-localized instance of a known phenomenon plus a genuinely new minimal-intervention diagnostic and a tested training-dynamics explanation; not a new conceptual framework.
- **Significance: 3 (good)** — "Counts are perfectly encoded but orthogonal to the digit unembedding; 9 rows suffice for constrained readout" is a memorable, citable mechanistic fact; impact is bounded by the task's narrowness (single-token, low-vocabulary aggregation) and the fix being standard fine-tuning.
- **Overall: 5 (borderline accept / poster)** — Sits at the poster-tier bar (pool anchor 5.35): rigorous, honest, useful, but incrementally novel with one unresolved internal inconsistency. Reviewer spread plausibly 4–6.
- **Confidence: 4** — I have read the full source carefully; I cannot verify the figures, compiled page count, or rerun the experiments.

## 9) Final Recommendation (Venue-Calibrated)

**ICLR: Borderline Accept (5).**

This is a careful, control-rich mechanistic case study whose central claim — counting failure as geometric readout misalignment, causally localized to nine unembedding rows — is well-supported and more rigorously tested than the average accepted poster. It falls short of a clear accept because the representation–readout gap is a known phenomenon (the novelty is in the clean instance and localization, not the concept), the "fix" is task-specific fine-tuning, and the soft-DPS contradiction needs reconciliation before the numbers can be fully trusted. Fixing that inconsistency, adding a full-FT generation baseline, and foregrounding the final-layer orthogonality result would likely push this into comfortable poster acceptance.

Stop.