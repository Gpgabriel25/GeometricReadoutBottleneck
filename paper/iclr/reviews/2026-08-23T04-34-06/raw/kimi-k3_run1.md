# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: No author-identifying information visible in the provided source. ✅ (Cannot verify supplementary/repo links — none provided.)
- **Style files**: Uses `iclr2027_conference.sty` and matching bibliographystyle. ✅ (The stale comment "% NeurIPS 2026 style" in the preamble is editorially sloppy but not a violation.)
- **AI use statement**: Present. ✅
- **Page limit**: Cannot be verified from uncompiled LaTeX source. Main text (Intro through Conclusion) appears dense but plausibly within 9 pages; the volume of floated tables/figures makes this uncertain — authors should verify. Core evidence (Tables 1–4, logit-lens figure) does live in the main text. ⚠ Unverifiable.

No desk-reject risk identified from the material provided.

---

## 1) Core Thesis & Significance

**Thesis**: LLMs fail at counting not because they don't represent counts internally (linear probes recover counts at R² > 0.99), but because the count-encoding direction is geometrically misaligned with the `lm_head` digit rows (|cos| ≤ 0.032, statistically indistinguishable from random directions). The paper supports this with logit-lens analysis, a minimal 9-row output-head repair (fixes constrained decoding), and a LoRA Q/V intervention (fixes autoregressive generation, 83.1%).

**Relevance**: Practically relevant — counting/aggregation failures are well-documented and embarrassing for deployed LLMs, and a mechanistic account of *why* has been missing. The problem is real, though the "low-vocabulary aggregation" scope is narrower than the title implies.

**Novelty**: The framing is component-level novel: prior work documented failures (Razeghi et al.) and localized heads (Stolfo et al.), but the explicit *representation–readout geometric gap* — quantified via probe-vs-logit-lens divergence on the *same* hidden states, with a random-direction equivalence test — is a genuinely new and crisply stated claim. The "linearly encoded but not output-promoted" observation is a nice complement to Geva et al.'s FFN-promotion story.

**Summarizability**: A reviewer can unambiguously state the contribution: "counts are linearly decodable but orthogonal to digit unembedding rows; this is causally the bottleneck; it is repairable." That clarity is a strength.

## 2) Technical Soundness

**Well-supported claims**:
- The orthogonality claim is handled with unusual statistical care: random-direction baselines, permutation tests, TOST equivalence, four probe types, three model families, shuffled-label probes, and a positive control (predicted-token probe achieves 3.3× higher alignment). This is better than most accepted interpretability work.
- The "why is orthogonality stable" gradient fixed-point argument is assumption-light and receives direct empirical support (counting FT raises |cos| 3.2×; arithmetic FT 1.1×).
- Necessity/sufficiency controls (shuffled rows below baseline; trained rows at random positions at baseline) properly earn the causal "bottleneck" language.

**Concerns**:

- **(b) Significant concern — internally inconsistent headline numbers across tables.** The 9-row repair on Qwen3-8B entity counting is reported as 60.7% (Tables 1–2), 93.8% "held-out" (Table `intervention_comparison`), and 56.7% as the "ridge baseline in the ablation replication" (Appendix capacity ablation). Baseline digit-restricted accuracy appears as 13.7%, 11.3%, 17.0%, and 38.8% in different places. The paper gestures at protocol differences and provides a protocol map, but the largest gap (60.7 vs. 93.8, same model, same task, both "held-out") is never reconciled in text. Even if each number is individually honest, this invites the suspicion of protocol shopping and must be fixed with an explicit reconciliation.
- **(b) Significant concern — soft DPS fragility.** Soft DPS goes from 96.3% (single-seed protocol) to 13.2% ≈ baseline (multi-seed protocol), attributed to full-vocabulary argmax being dominated by non-digit tokens. But the appendix states the *single-seed* protocol also used "argmax over all tokens," so the explanation given does not actually account for the discrepancy ("single-seed vs. diverse templates" is not a mechanism). Hard DPS (+100 to a logit) is answer-forcing, not an intervention — fine as a probe-correctness check, but it should not be presented alongside repairs.
- **(c) Typical limitation — the "fixes" are task-specific fine-tuning.** Both the 9-row repair and LoRA Q/V are trained on counting data. "Fine-tuning on task X improves task X" is not surprising; the scientific value is the *localization* (9 rows suffice; Q/V locus beats alternatives), which the paper does establish via the locus ablation. But the title's "How to Fix It" leans on the weaker half of the contribution.
- **(c) Typical limitation — unexplained non-monotonic per-count pattern.** The 9-row repair collapses at counts 4–7 (30–51%) but recovers at 8–9 (49–72%). This striking pattern gets no mechanistic comment.

No fatal flaws: the core geometric claim survives all stated controls.

## 3) Empirical Rigor

**Strengths**:
- Factorial prompt design (count ⊥ distractors ⊥ length ⊥ spacing) properly defends against probe shortcuts — this is the right way to run probing studies and is frequently skipped in accepted papers.
- Three evaluation modes explicitly labeled; generation scored by final integer with an explicit warning about first-integer scoring inflation.
- Negative controls (MMLU/GSM8K: |cos| = 0.31–0.48, no bottleneck, repair *hurts*) correctly bound the claim's scope.
- Multi-seed reporting with per-seed values disclosed (LoRA: 71.5–89.0% multi-task; 94.5–97.0% entity-only).

**Gaps**:
- **No reported CoT baseline number.** The Discussion claims CoT "places alongside LoRA Q/V" but presents no CoT accuracy under the paper's own final-integer scorer (it is mentioned as "available in the supplement," not provided here). Since CoT is the zero-training-cost competitor for the deployable fix, this head-to-head belongs in the main text. This is the most conspicuous missing baseline.
- **No full fine-tuning baseline for generation.** LoRA Q/V is compared only against the paper's own interventions; full-FT generation accuracy would calibrate whether 83.1% reflects routing-specific repair or generic task learning. The locus ablation partially substitutes for this but not fully.
- High-variance headline: 83.1% ± 7.2% across 5 seeds is a wide band for the paper's flagship deployable number; the entity-only numbers (94.5–97.0%) suggest the multi-task mix drives the variance, which is fine but should temper the abstract's presentation.
- Trade-offs are quantified honestly (inference-cost vs. training-cost framing vs. CoT; parameter counts for each intervention).

**Overclaiming check**: The abstract and claims are mostly well-calibrated — the paper explicitly scopes the 9-row repair to constrained decoding and discloses its 0.0% generation result prominently. Two exceptions: (i) the title promises a "fix" that the paper itself shows fails in the deployment mode (0.0% generation for the minimal repair; the working fix is plain LoRA fine-tuning); (ii) "the bottleneck generalizes" leans on addition, where the constrained baseline is already 93.3%, leaving little bottleneck to explain.

## 4) Competitive Realism Check (Calibrated)

Against the ICLR 2026 population (poster accept mean ≈ 5.35): this paper's *diagnostic* half — clean falsifiable claim, four probe types, equivalence testing, necessity/sufficiency controls, negative controls, cross-model replication — is comfortably above the accepted-paper bar for mechanistic interpretability work. Many accepted interpretability papers rely on a single probing analysis with none of these controls.

The *intervention* half is where accepted-paper variance bites: the number inconsistencies across tables and the absent CoT number are the kind of thing that produces one frustrated 3–4 score in an otherwise positive review pool. Would at least two reasonable reviewers score ≥5? **Yes**, plausibly three — the core finding is memorable and the evidence for it is strong even if one discounts every intervention number entirely. The weaknesses are within acceptance variance, not below it.

## 5) Weakest Link Analysis

**Weakest link**: the unreconciled cross-table number discrepancies for the same model/task (60.7% vs. 93.8% vs. 56.7% for 9-row repair; 96.3% vs. 13.2% for soft DPS under two protocols whose stated difference doesn't mechanistically explain the gap).

**Classification**: *Addressable in revision* — a single reconciliation table (rows = each reported number, columns = exact protocol: split, argmax scope, template set, seed count) plus one paragraph explaining the soft-DPS discrepancy would resolve it. It is not fundamental to the geometric claim, but left unfixed it is decision-relevant because it converts the paper's laudable protocol-transparency effort into a credibility liability. This is the issue most likely to flip a borderline reviewer.

## 6) Convergence Test (Minimal-Change Threshold)

- **As-is, ≥50% acceptance chance?** Roughly at the threshold — I estimate ~45–55%, driven by review-pool variance on the number-consistency issue and title-oversell reaction. Not safely above.
- **Minimal changes to push over** (evidence-based, not editorial):
  1. A reconciliation table/appendix mapping every reported accuracy to its exact protocol, with an explicit explanation of the 60.7 vs. 93.8 gap and a mechanistic (not just "different templates") account of the soft-DPS discrepancy.
  2. Report the CoT baseline under the paper's own final-integer scorer in the main text alongside LoRA Q/V.
  3. Retitle or subtitle to scope the "fix" claim (e.g., "...: A Geometric Readout Bottleneck"), or move the deployable-fix framing behind the diagnosis framing.

Items 1–2 are small experiments/tables, not new research programs.

## 7) Structural Sharpness & Scope Control

The paper is centered on one dominant contribution (the geometric readout bottleneck) and most material serves it:

- **(a) Strengthens core**: probes + orthogonality statistics, logit-lens two-phase analysis, necessity/sufficiency controls, negative controls, gradient fixed-point explanation, scale sharpening at 14B.
- **(b) Neutral**: majority-vote and max-extraction extensions (nice but the counting story stands without them); DROP +10pp partial result.
- **(c) Introduces attack surface**: (i) the soft-DPS single-seed result (96.3%) presented at all, given its fragility — the hard-DPS/probe-round equivalence already makes the diagnostic point; (ii) the "intervention comparison" table mixing protocols in one view invites the confusion flagged in §5; (iii) the per-count stratified table exposes an unexplained non-monotonicity that reviewers will poke.

**Recommended scope reduction**: drop or fully quarantine the single-seed soft-DPS result and merge all intervention numbers into one protocol-locked table. This removes two attack surfaces at zero cost to the thesis.

## 8) ICLR Formal Scores

- **Soundness: 3/4** — The core geometric claim is supported by an unusually complete control battery; however, unexplained cross-table numeric inconsistencies and the under-explained soft-DPS protocol sensitivity prevent a 4.
- **Presentation: 3/4** — Well-organized, honest scope labeling, explicit protocol map; but the proliferation of unreconciled numbers across tables undermines the clarity the structure otherwise achieves.
- **Contribution: 3/4** — A genuinely new, crisply falsifiable mechanistic claim (encoded-but-orthogonal-to-readout) plus causal localization; the repair side is closer to informed fine-tuning than to a novel fix.
- **Significance: 3/4** — Memorable finding with a reusable diagnostic recipe (probe → align → targeted repair) applicable to other competence/performance gaps; impact bounded by the low-vocabulary-aggregation scope and sub-frontier model scales.
- **Overall: 6/10** — Clear accept: a well-controlled, memorable mechanistic diagnosis comfortably above the poster mean, held back from 7 by number-consistency issues, the absent CoT head-to-head, and an intervention story weaker than the diagnosis.
- **Confidence: 4/5** — Confident in the assessment of the probing/geometry evidence and the review dynamics; residual uncertainty on whether the cross-table discrepancies have a benign explanation the authors could trivially supply.

## 9) Final Recommendation (Venue-Calibrated)

**ICLR: Accept (6/10)**.

The paper delivers a clean, falsifiable, and well-controlled mechanistic answer to a widely observed failure — counts are linearly represented but geometrically inaccessible to the output head — with controls (equivalence testing, shuffled rows, negative benchmarks) that exceed typical accepted interpretability work. Its liabilities — unreconciled numbers across protocols, no reported CoT comparison for the generation-mode fix, and a title that oversells a fine-tuning intervention — are real but addressable and fall within the variance of accepted ICLR papers. In a typical review pool this lands as a solid poster with a plausible path to stronger scores after revision.