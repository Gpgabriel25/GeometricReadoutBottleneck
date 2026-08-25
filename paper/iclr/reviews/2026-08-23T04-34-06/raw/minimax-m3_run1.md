## Review: "Why Transformers Fail at Counting and How to Fix It"

### ⚠ DESK-REJECT RISK

- **Anonymity**: No author-identifying information detected in main text or appendix. Citations to prior work are in third person ("\citet{...}", "[26]"-style). ✅
- **Page limit**: Main text appears at or near the 9-page limit (the appendix is extensive but does not count). Hard to verify exactly without compiled PDF. Borderline.
- **AI use statement**: Present in main text. ✅
- **Style files**: `\usepackage{iclr2027_conference}` is used. ✅

No desk-reject risk items identified.

---

### 1) Core Thesis & Significance

The paper proposes a mechanistic diagnosis for transformer counting failures: the residual stream encodes the count with high fidelity (probe R² > 0.99), but the count-encoding direction is geometrically orthogonal (|cos| ≤ 0.032, indistinguishable from random) to digit rows of the unembedding matrix. Three nested claims follow: (1) orthogonality is the structural cause; (2) a 9-row repair of the output head causally localizes the bottleneck for constrained decoding; (3) a LoRA Q/V intervention on attention upstream of the output head restores autoregressive generation (83.1% ± 7.2%).

This is a clearly formulated dichotomy (representation vs. readout), and the proposed falsifiable predictions (digit-row repair works under constrained evaluation but not generation; LoRA on routing fixes generation) are exactly what is observed. The problem is practically relevant (counting failures are documented, persistent, and economically meaningful for downstream applications). The novelty is primarily integration-level: combining linear probes, logit-lens, minimal interventions, and negative controls into a coherent mechanistic story with a deployable fix. A reviewer could summarize the contribution unambiguously.

### 2) Technical Soundness

**(a) Fatal flaw**: None identified.

**(b) Significant concerns** (decision-relevant, fixable):

1. **Internal numerical inconsistency in the headline 9-row repair result.** Table 1 (digit-restricted next-token) reports 60.7% ± 3.1%, while Table 4 reports 93.8% held-out for the same nominal intervention. The reader must consult the Appendix capacity ablation to learn that Table 1 is closed-form ridge regression while Table 4 is Adam fine-tuning (300 steps), but this protocol difference is never made explicit in the main text or in the table captions. This 33 pp gap is exactly the kind of mismatch that undermines a clean mechanistic claim, and the paper should clearly label which results use which solver.

2. **Soft vs. Hard DPS discrepancy is hand-waved.** Soft DPS achieves 13.2% (matching baseline) while Hard DPS achieves 98.7% — both using the same probe direction. The explanation (full-vocabulary argmax is dominated by a non-digit token leading by "several logit units" in 600/600 baseline examples) is plausible but should be quantified (what is the typical logit gap between the predicted digit and the leading non-digit token?). Without this, the reader cannot tell whether Hard DPS's success reflects a fundamentally different mechanism than Soft DPS.

3. **Entity-counting 9-row repair ceiling (60.7%) is only partially explained.** The 37 pp gap to probe-round (98.7%) is attributed to "digit-row norm competition and hidden-state diversity (1.5× higher intra-class variance)", but no experiment discriminates the two hypotheses. The "capacity ablation" rules out fitting method and row count, which is informative, but the two stated explanations remain confounded.

**(c) Typical limitations** (common in accepted work):

- Generation-mode evidence for the 9-row repair is partial: only ~83% of DPS errors are "format failures" — the remainder (~17%) are unresolved wrong-digit errors.
- LoRA Q/V variance is substantial (±7.2%, per-seed range 71.5–89.0% in multi-task), and the authors attribute this to "task-mix artifact" rather than treating it as a stability concern.
- The mechanism explanation ("orthogonality is a stable fixed point of training dynamics") is reasonable but the empirical support — a 3.2× vs. 1.1× relative change starting from slightly different baselines (0.0074 vs. 0.0087) — is somewhat fragile. The starting points matter because they are within the bootstrap CI of each other.

### 3) Empirical Rigor

Strengths:
- Multi-model (Pythia, Qwen3, Mistral, four families), multi-scale (0.4B–14B), multi-probe (ridge, LDA, mean-difference, PCA) design.
- Held-out evaluation for repairs; multi-seed (3–5) reporting with means ± SD.
- Factorial prompt design (counts, distractors, lengths, spacings) explicitly rules out distributional shortcuts.
- Negative controls (MMLU, GSM8K) at appropriate strength.
- Shuffled-label, random-direction, TOST equivalence, and positive-control probes.
- Stratified per-count breakdown on entity counting (Table 9) shows the ceiling is count-magnitude-dependent.

Trade-offs quantified: parameter count for interventions (36,864 vs. 7.67M vs. ~622M), vocabulary rank (55,980 → 1).

**Overclaiming check**: The headline framing ("readout bottleneck") is well-supported under the stated scope. The claim that this generalizes to a "diagnostic strategy" for competence-without-performance failures is appropriately hedged as future work. The claim about WHY orthogonality arises is the weakest empirically supported claim and is correctly framed as tentative.

### 4) Competitive Realism Check

This is a well-executed mechanistic interpretability paper with a clean narrative, multiple causal interventions, and a deployable artifact. Compared to typical accepted ICLR mechanistic papers:
- The clean dichotomy and falsifiable predictions are above the median.
- The cross-model and negative-control validation is above the median.
- The reporting inconsistencies are below the median — most accepted papers would not have a 33 pp unreconciled discrepancy in the headline intervention.
- The variance on the deployable fix (±7.2%) is on the high side but not unusual for LoRA interventions.

Two reasonable reviewers could likely score this ≥5; one could push toward 6. The work clearly meets the ICLR poster bar. Whether it clears the strong-accept bar (6+) depends on how much weight the numerical inconsistencies carry.

### 5) Weakest Link Analysis

**The single most decision-relevant issue is the unexplained numerical gap between Table 1 (60.7%) and Table 4 (93.8%) for the nominal "9-row lm_head repair".** A reviewer reading only the main text sees two different "headline" numbers for the same intervention without an explicit protocol reconciliation. This invites suspicion that the authors chose the more favorable number for Table 4 without flagging the comparison.

- Is it addressable in revision? **Yes, easily**: clearly state in both tables and captions which results use ridge vs. Adam, and unify the headline repair number. This is purely a presentation fix, not a methodological change.
- Is it fundamental? **No** — the underlying experiments appear sound; only the reporting is muddled.
- Could it flip the decision? **Maybe**: a clean reconciliation showing Adam > ridge consistently across tasks would actually strengthen the paper (gradient descent independently rediscovers the geometric bottleneck), but the current presentation leaves the impression of inconsistency.

If the weakest link were addressed, the next concern is the high variance (±7.2%) on the LoRA Q/V headline number, but this is typical for LoRA-based fixes and unlikely to flip the decision on its own.

### 6) Convergence Test

- **If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?** Borderline. The mechanistic story is strong enough that a poster accept is plausible, but the reporting inconsistencies and the partially explained 60.7% ceiling on entity counting could just as easily land it in the borderline-reject zone from a strict reviewer. Estimate: ~55–60% accept.

- **Minimal change to push over the threshold**: (1) Reconcile and clearly label the 9-row repair protocol (ridge vs. Adam) across Tables 1 and 4, with a single reconciled headline number per task. (2) Quantify the logit gap between predicted digit and leading non-digit token to justify the Soft vs. Hard DPS distinction. (3) Discriminate the two stated hypotheses for the 37 pp entity-counting ceiling (norm vs. variance) with one targeted experiment. These are all experiments that could be done in a few days.

### 7) Structural Sharpness & Scope Control

The paper is centered on one dominant contribution (geometric readout bottleneck). The scope is well-controlled:

- (a) **Strengthens the core**: Multiple probe types, cross-model validation, negative controls, logit-lens, two interventions (9-row + LoRA), generation-mode evidence — all directly support the central claim.
- (b) **Neutral**: The instruct-mode and natural-language extension are brief and on-topic. The DROP result (+10 pp) is a reasonable scope probe.
- (c) **Introduces new attack surface**: The chain-of-thought comparison in §Discussion is interesting but somewhat tangential. The "broader implications" generalization to a general diagnostic strategy is appropriately hedged but invites reviewer pushback on whether single-token aggregation is a representative test case.

The Discussion section is long; it could lose ~10% of the CoT commentary without weakening the paper.

### 8) ICLR Formal Scores

- **Soundness (1-4)**: **3**. The core methodology is sound and well-controlled. The numerical inconsistencies (Table 1 vs. Table 4 for the same nominal intervention) and the partial explanation of the entity-counting ceiling prevent a 4, but the work is clearly above-average in rigor for mechanistic interpretability.

- **Presentation (1-4)**: **2**. The paper is well-organized at the section level, but the inconsistencies between tables, the unexplained Soft/Hard DPS split, and the high density of metrics (8 tables in the main + appendix, several reporting the same intervention under different protocols) make it hard to extract the headline story. The reviewer had to dig into the appendix capacity ablation to reconcile Tables 1 and 4.

- **Contribution (1-4)**: **3**. A clean mechanistic diagnosis (orthogonality as the cause) with a falsifiable prediction, multiple interventions, and a deployable fix. The mechanistic insight (gradient dynamics → stable orthogonality → readout failure) is original and interesting. Not component-level novel in isolation but a strong integration contribution.

- **Significance (1-4)**: **3**. The finding is memorable and the diagnostic strategy (probe → measure alignment → targeted repair) is genuinely portable. The LoRA Q/V intervention is a deployable artifact. Other groups working on competence-without-performance failures will likely build on this. Not field-shaping but clearly above the poster mean.

- **Overall (1-10)**: **6**. Solid mechanistic contribution that meets the ICLR clear-accept bar. The reporting inconsistencies prevent a 7, but the substance (clean claim, strong evidence, multiple interventions, negative controls, deployable fix) is well above the poster mean.

- **Confidence (1-5)**: **3**. Mechanistic interpretability papers are a substantial fraction of ICLR submissions, and my calibration in this subfield is moderate.

### 9) Final Recommendation

**Borderline Accept / Clear Accept (6).** This is a well-executed mechanistic interpretability paper with a clean falsifiable claim, multiple causal interventions (9-row repair + LoRA Q/V), and appropriate negative controls (MMLU, GSM8K). The proposed diagnostic strategy (probe → alignment → targeted repair) is portable and likely to be used by other groups. The paper loses ground to internal reporting inconsistencies (most notably the unreconciled 60.7% vs. 93.8% for the nominal 9-row repair across Tables 1 and 4) and to the high variance on the headline LoRA Q/V result (±7.2%). Both are addressable in a brief revision, and addressing them would push the paper toward a strong accept. As submitted, it is a clear accept for a poster slot.