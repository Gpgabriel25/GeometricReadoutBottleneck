# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: Compliant as far as visible. Authors are anonymized; no repo links, no acknowledgments, no self-revealing phrasing. (The LaTeX comment `% NeurIPS 2026 style` is invisible in the compiled PDF and not a violation, though it should be cleaned up.)
- **Page limit**: **Cannot verify from source.** The main-text density (8 sections, 7+ tables, 3 figures) is at real risk of exceeding 9 pages; authors should verify. Core evidence does appear to live in the main text.
- **AI use statement**: Present and appropriately scoped. ✓
- **Style files**: `iclr2027_conference` package with `article` class — the standard ICLR pattern. ✓

No desk-reject flags, subject to page-count verification.

---

## 1) Core Thesis & Significance

The paper argues that transformer counting failure is a **geometric readout bottleneck**: counts are linearly encoded in the residual stream (probe R² > 0.99) but the encoding directions are statistically indistinguishable from orthogonal to the `lm_head` digit rows (|cos| ≤ 0.032, matching a random-direction baseline). Three interventions triangulate the claim: a 9-row `lm_head` repair (36,864 params) fixes constrained decoding but not generation; probe-based steering (DPS) bypasses the head analytically; LoRA on attention Q/V (7.67M params) corrects upstream routing and reaches 83.1% ± 7.2% in true greedy generation, with logit-lens rank of the correct digit dropping from 55,980 to 1.

The problem is practically relevant (counting failures are a widely discussed LLM pathology) and the contribution is a clean, falsifiable mechanistic diagnosis with causal verification — the kind of contribution a reviewer can summarize unambiguously. Novelty is component-level (probes, logit lens, targeted fine-tuning are standard tools) but the integration — quantifying encoding-vs-readout geometry and repairing at three distinct loci — is genuinely insightful and goes beyond prior counting work (Razeghi et al., Stolfo et al.), which localized failures without identifying the geometric cause.

## 2) Technical Soundness

The core claims are unusually well-supported. The factorial prompt design independently randomizes count, distractors, length, and spacing, closing the distributional-shortcut loophole for probes. Controls are above venue standard: shuffled-label probes (R² ≈ 0), random-direction cosine baselines with permutation tests and TOST equivalence, a positive control (continuation-token probe achieves |cos| = 0.115, 3.3× the count probe), shuffled-row and random-position necessity controls, negative controls on MMLU/GSM8K, locus ablations for LoRA, and capacity ablations for the row repair.

**Issue classification:**

- **(a) Fatal flaws**: None.
- **(b) Significant concerns (decision-relevant, fixable):**
  1. **Cross-table protocol inconsistency for the same intervention.** The 9-row repair appears as 60.7% ± 3.1% (unified table, entity counting), 93.8% held-out (Table 5), and 99.9% (instruct mode) — with no in-text reconciliation. Baseline appears as 13.7%, 11.3%, and 17.0% (appendix). The paper's protocol map is commendable, but a reader cannot currently determine which number is canonical for the row repair. This invites cherry-picking suspicion the paper probably doesn't deserve (the headline claims use the *conservative* multi-seed numbers), but it must be fixed.
  2. **The flagship-task repair ceiling (60.7%) is labeled, not explained.** "Task-level ceiling" is a restatement. The stratified table (30.6% at count 7, 100% at count 2, 71.9% at count 9) shows non-monotonic, unstable decision boundaries between adjacent digits — under-analyzed.
  3. **A numeric inconsistency at 14B**: |cos| = 0.011 claimed as "0.57× random baseline" implies a baseline of ~0.019, but for 5120-dim hidden states the expected E[|cos|] for random directions is ≈ 0.011 (and the paper's own 8B measurement, 0.013 ± 0.011 in 4096 dims, matches theory). The "scale sharpens the bottleneck" claim needs this arithmetic checked.
  4. **Minor text–table mismatch**: "Probe R² exceeds 0.99 at every layer" vs. layer 0 = 0.977 in Table 2.
- **(c) Typical limitations**: probe-direction ≠ unique encoding direction (mitigated by four probe types and the causal DPS result); Pythia-410M repair transfer failure (honestly scoped); scale capped at 14B; the orthogonality-as-fixed-point argument is a verbal model with supportive but not rigorous evidence.

## 3) Empirical Rigor

Broadly sufficient and above average. Multi-model (4 models, 3 families, 0.4B–14B), multi-task (4 primary + 3 extension tasks), multi-seed with reported per-seed values, and a genuinely unified evaluation table. The logit-masked generation control (59.2%, matching constrained accuracy) is an elegant confirmation that the row repair encodes the right answer and the generation failure is routing. The LoRA mechanism analysis (probe direction unchanged at layer 2; final-layer R² 0.974 → 0.998; logit-lens 9.3% → 71.8%) directly supports the routing interpretation.

**Gaps:**

- **CoT accuracy is never reported in the main text** under the paper's own corrected final-integer scorer, despite CoT being invoked as a comparable intervention. For a paper whose deployable fix scores 83.1%, this number belongs in the main text. "Substantially improves" is not evidence.
- **Addition is weak evidence for generality**: baseline is already 93.3%, so the "bottleneck" there is worth ≤ 7 pp. Including it in the abstract's generality claim is a stretch.
- **External validity is thinner than the title suggests.** On DROP the probe-round improvement is +10 pp (20% → 30%); on natural-language counting the baseline is already 88.7%. The bottleneck is large and well-characterized on the *synthetic* distribution the authors designed, and much smaller on natural text. The title "Why Transformers Fail at Counting" is broader than the demonstrated effect; the paper's own scope statements are more honest than its title.
- Reproduction details (learning rates, batch sizes, LoRA data mixture, the 200/300 training steps) are not in the main text.

**Overclaiming check**: confined to the title/framing and the two flagged numeric statements. The body's claims are carefully scoped and mode-labeled — notably the candid admission that the 9-row repair achieves 0.0% in generation.

## 4) Competitive Realism Check

Compared to typical accepted ICLR mechanistic-interpretability papers, this one has *more* controls than most (negative controls on standard benchmarks are rare; necessity/sufficiency controls are rare; mode-matched protocol harmonization is rare). The weaknesses — synthetic-task focus, protocol sprawl, a partially unexplained flagship gap — are within acceptance variance. The "knows the count but can't say it" dissociation, quantified geometrically and verified causally at three loci, is a memorable finding that the interpretability community will cite. I would expect at least two reasonable reviewers to score ≥ 5, with clustering around 5–7.

## 5) Weakest Link Analysis

The **single most decision-relevant issue is the cross-table protocol inconsistency** (60.7% vs. 93.8% vs. 99.9% for the 9-row repair; multiple baselines). A careful reviewer reading Table 5 next to Table 1 cannot tell which measurement is authoritative, and this is exactly the pattern that triggers a downgrade from "solid" to "suspicious." It is **addressable in revision** (annotate every table row with its protocol; add one reconciliation paragraph) and **unlikely to be fundamental** — the conservative numbers already support the headline claims. Secondary: missing CoT number in the main text (addressable).

## 6) Convergence Test

- **With no further changes**: I estimate a ~50–60% acceptance chance — the empirical substance is above the poster bar, but the protocol ambiguity and missing CoT baseline give a skeptical reviewer room to push to 4–5.
- **Minimal change to clear the threshold**: (i) a protocol reconciliation pass making every accuracy number's mode/N/seeds explicit at point of use (one table or per-row annotations); (ii) the CoT baseline number under the final-integer scorer in the main text; (iii) one paragraph explaining or explicitly flagging the instruct-mode 99.9% vs. base-mode 60.7% repair discrepancy, and correcting the 14B "0.57×" arithmetic. These are evidence-presentation changes, not new experiments, and would make this a comfortable accept.

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant contribution: the geometric readout bottleneck, diagnosed and causally verified.

- **(a) Strengthens**: unified evaluation table; necessity/sufficiency controls; logit-masked generation control; LoRA mechanism measurements; MMLU/GSM8K negative controls (rare and valuable for scoping); multi-digit extension (tests the token-level claim).
- **(b) Neutral**: majority vote and max extraction (generality evidence; could be compressed to one paragraph each).
- **(c) Attack surface**: the single-seed soft-DPS pilot (96.3%) that collapses to 13.2% under the harmonized protocol. The appendix discloses this honestly, but the narrative would be tighter — and less vulnerable — if presented as "pilot experiment that motivated protocol harmonization" rather than a headline result requiring an explanatory footnote. The title is also mild attack surface relative to the DROP/NL evidence; consider scoping it ("A Geometric Readout Bottleneck in Transformer Counting").

## 8) ICLR Formal Scores

- **Soundness (3/4)**: Claims are supported by an unusually strong control suite (permutation tests, TOST, shuffled controls, negative controls, causal interventions). Held below 4 by unreconciled cross-table numbers, the unexplained 60.7% flagship ceiling, and two checkable numeric inconsistencies (14B baseline ratio; layer-0 R²).
- **Presentation (3/4)**: Dense but organized, with numbered claims, mode labels, and a protocol map. Docked for protocol sprawl that forces the reader to reconstruct which measurement supports which claim, and for the unexplained instruct/base repair discrepancy.
- **Contribution (3/4)**: A crisp, novel-in-combination diagnosis — orthogonal-to-unembedding encoding with causal repair at three loci — that advances beyond prior counting localization work. Tools are standard; the insight is not.
- **Significance (3/4)**: Addresses a widely recognized failure mode with a memorable, quotable finding and a generalizable diagnostic recipe (probe → measure alignment → targeted repair). Practical deployment impact is moderate (CoT already fixes counting at inference cost), but the mechanistic clarification of *why* CoT helps is valuable.
- **Overall (6/10)**: Clear accept. Comfortably above the poster mean (5.35) on experimental substance; not at 7 because external validity on natural text is materially weaker than the synthetic evidence and the flagship-task repair result remains partially unexplained; not at 5 because the control rigor and causal completeness exceed the typical accepted mech-interp paper.
- **Confidence (4/5)**: The analysis is self-contained and I checked internal consistency of the headline numbers (they reconcile, with the flagged exceptions); I could not inspect figures or the referenced supplement.

## 9) Final Recommendation

**Accept (6).**

This is a well-controlled mechanistic study with a clean causal story and a memorable finding; its weaknesses (protocol sprawl, synthetic-task concentration, a partially explained repair ceiling) are the kind that accepted ICLR papers routinely carry and that a rebuttal can largely neutralize. With protocol reconciliation and the CoT number in the main text, I would not be surprised to see this score 7 from other reviewers; as submitted, 6 is the defensible calibrated rating.