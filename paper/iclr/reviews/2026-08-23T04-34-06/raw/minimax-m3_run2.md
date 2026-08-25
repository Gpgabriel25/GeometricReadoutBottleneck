# Review of "Why Transformers Fail at Counting and How to Fix It"

## ⚠ DESK-REJECT COMPLIANCE CHECK

- **Anonymity**: ✅ Pass — author block is anonymized; no self-revealing phrasing detected in the text I can read. Code/repo links are not visible in the main text.
- **Page limit**: ✅ Pass (cannot render, but main text appears within 9 pages; references and appendix separate).
- **AI use statement**: ✅ Present, in proper section.
- **Style files**: ✅ Uses `iclr2027_conference`.

No desk-reject risk items.

---

## 1) Core Thesis & Significance

The paper argues that transformer counting failures arise from a **geometric readout bottleneck**: counts are linearly encoded in the residual stream ($R^2 > 0.99$ via ridge probes) but in directions nearly orthogonal to digit rows of `lm_head` ($|\cos| \leq 0.032$). It localizes this causally by repairing only the 9 digit rows (60.7–100.0% across four tasks under constrained decoding) and shows that correcting upstream routing via LoRA Q/V (7.67M params) achieves 83.1% ± 7.2% in true autoregressive generation.

The problem is practically relevant: counting is a transparent test case for competence-without-performance failures. The novelty is **integration-level** — combining linear-probe evidence, geometric alignment, logit-lens, and minimal causal intervention into a coherent diagnostic pipeline. The contribution can be summarized unambiguously: "the model knows the count, but the output pathway is misaligned."

---

## 2) Technical Soundness

**Strong aspects:**
- The geometric claim (cosine orthogonality ≈ random baseline, $p = 0.79$; TOST equivalence) is well-supported across 3 model families and 4 probe types.
- The 9-row repair as a **minimal causal probe** is a methodologically clean design — locality of intervention causally links the bottleneck to digit rows under constrained decoding.
- Negative controls (MMLU: $|\cos| = 0.31$–$0.48$; no bottleneck observed) effectively bound the scope.

**Concerns:**
- **(b) Significant concern — Soft DPS vs. Hard DPS inconsistency.** Soft DPS fails (13.2%, ≈ baseline) while Hard DPS achieves 98.7% on the same task. The explanation (non-digit tokens always win full-vocab argmax by several logit units) actually reveals that the bottleneck is not purely geometric — there's a routing/format layer that the 9-row repair doesn't address. This is acknowledged but deserves more emphasis.
- **(b) Significant concern — Numerical inconsistency between tables.** Table 1 (`tab:unified_evaluation`) and Table 2 (`tab:mode_matched_extval`) report 9-row repair at 60.7% on entity counting, but Table 3 (`tab:intervention_comparison`) reports "9-row lm_head (held-out)" at 93.8% on Qwen3-8B. Even if explained by averaging across tasks or training steps, the lack of explicit reconciliation is a presentation problem that erodes trust in the numerical claims.
- **(c) Typical limitation — 38 pp gap on entity counting.** Probe-round reaches 98.7% but 9-row repair only 60.7%. The proposed explanations ("vocabulary competition" + "intra-class hidden-state diversity") are plausible but post-hoc; discriminating them requires experiments varying prompt diversity at fixed count values, which is acknowledged as future work.
- **(c) Typical limitation — "Stable fixed point" argument.** The theoretical claim that orthogonality is a stable fixed point of training dynamics is intuitive but only empirically supported by one fine-tuning contrast (counting vs. arithmetic fine-tuning). This is suggestive, not conclusive.
- **(c) Typical limitation — "Generation gap = 0.000."** This claim appears alongside ±7.2% across-seed variance. The "generation gap" must refer to train-test gap rather than variability, but the phrasing is ambiguous.

No fatal flaws.

---

## 3) Empirical Rigor

**Strengths:**
- Multiple model families (Pythia-410M, Mistral-7B, Qwen3-8B, Qwen3-14B).
- Probe robustness checks: shuffled-label ($R^2 = -0.042$), random-direction baseline, TOST equivalence, positive control ($|\cos| = 0.115$ for predicted continuation).
- Necessity/sufficiency controls: shuffled-digit rows (14.0% < 17.0% baseline), random non-digit positions (matches baseline).
- Stratified analysis by count magnitude, difficulty, format.
- Negative controls on MMLU, GSM8K, and partial DROP analysis.

**Gaps:**
- Pythia-410M repair only reaches 31.4% — the geometric signature appears but the repair is limited. The paper correctly scopes this to "mid-size and larger models," but the practical utility of the intervention at frontier scale (≥70B) is left untested.
- The DROP result (+10 pp from probe-round) is mentioned in passing without systematic analysis — it neither confirms nor refutes the story cleanly.
- CoT comparison acknowledges that scoring conventions differ; a head-to-head under identical final-integer scoring would strengthen the mechanistic argument.
- The soft DPS failure mode (full-vocab argmax dominated by non-digit tokens) deserves a dedicated analysis — what proportion of failures are format vs. wrong-digit?

---

## 4) Competitive Realism Check

The paper would likely fare as a poster at ICLR. The geometric diagnosis is well-isolated and falsifiable, the multi-model evidence is broad enough, and the practical intervention (LoRA Q/V) achieves respectable performance (83.1% generation accuracy). The 9-row repair result is methodologically interesting but partial. The paper does not claim SOTA on broad benchmarks (it explicitly disclaims CoT comparison), which is appropriate given the narrow task scope.

The numerical inconsistencies and the soft-vs-hard DPS explanation issue would likely surface in reviewer discussion, but they appear addressable in revision. At least two reasonable reviewers would likely score this ≥ 5.

---

## 5) Weakest Link Analysis

**Weakest link: the 38 pp gap on entity counting (probe-round 98.7% vs. 9-row repair 60.7%).**

If a reviewer pushes on this gap, the post-hoc explanation (norm competition + intra-class variance) is not fully demonstrated. The paper itself acknowledges the limitation and proposes discriminating experiments as future work, which is honest but leaves the diagnostic story partially incomplete.

This is **addressable in revision**: targeted experiments varying prompt diversity at fixed count values, and a fuller decomposition of the 38 pp gap. However, the paper can stand without full resolution.

**Decision-stable** on the headline claim (geometric readout bottleneck exists), but vulnerable on the strength of the intervention story.

---

## 6) Convergence Test (Minimal-Change Threshold)

- **≥50% acceptance chance as-is?** Borderline — likely 40-55%. The contribution is real and the methodology is sound, but numerical inconsistencies and the soft DPS explanation would generate reviewer discussion.
- **Minimal change to push over threshold:**
  1. Reconcile the 60.7% vs. 93.8% numbers across tables with explicit protocol annotation.
  2. Add a 1-paragraph analysis explaining why soft DPS fails (the answer is in the appendix but needs to be in the main text to preempt reviewer confusion).
  3. Add one experiment decomposing the 38 pp entity-counting gap (e.g., controlled prompt diversity).

---

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant contribution (the geometric readout bottleneck diagnosis). Content that strengthens the core: probes, logit-lens, 9-row repair, LoRA Q/V mechanism, negative controls. Content that is neutral but lengthens the paper: majority vote, max extraction, multi-digit extension — useful but could be condensed. No new attack surfaces that seriously undermine the core argument.

The CoT comparison section is well-scoped (acknowledges "not trying to beat CoT") and adds mechanistic value. The Discussion's "broader implications" — proposing a general probe-align-repair diagnostic — is appropriately framed as future work.

**Possible scope reductions:** The DROP analysis could be removed or expanded; currently it neither confirms nor refutes the story cleanly. The max-extraction and majority-vote sections could be condensed to a single paragraph each.

---

## 8) ICLR Formal Scores

- **Soundness (1-4)**: **3** — The geometric claims and probe-based evidence are well-supported. The soft-vs-hard DPS asymmetry and the 60.7% vs. 93.8% inconsistency are concerns but not fatal. The 38 pp gap explanation is incomplete but honestly acknowledged.

- **Presentation (1-4)**: **3** — Well-organized with clear sections, useful cross-references, and a logical narrative arc. Tables are dense but readable. The numerical inconsistencies and the appendix-buried soft DPS explanation hurt clarity. The DPS acronym collides with the standard RLHF usage (Direct Preference Optimization is sometimes called DPO, but DPS may also be confused with other techniques).

- **Contribution (1-4)**: **3** — Genuinely novel integration: combining linear probes, geometric alignment measurement, minimal causal intervention (9-row repair), and a deployable fix (LoRA Q/V) into a coherent diagnostic. The general probe→align→repair strategy is a useful methodological contribution beyond the specific counting result.

- **Significance (1-4)**: **3** — The diagnosis is memorable and falsifiable. The 9-row repair is a clever experimental technique that others will likely adopt. Practical impact is limited (LoRA Q/V requires fine-tuning, scope is single-token low-vocabulary aggregation), but the diagnostic framework has broader applicability to "competence without performance" failures.

- **Overall (1-10)**: **6** — Clear accept. Solid mechanistic insight with multiple-model validation and clean negative controls. The numerical inconsistencies and the soft DPS explanation prevent a 7, but the contribution comfortably exceeds the poster mean.

- **Confidence (1-5)**: **3** — Fairly confident on the overall assessment. The numerical inconsistencies might be reconcilable with more careful reading, which would push toward 6-7. Confident the paper meets the ICLR poster bar; less certain whether it clears the strong-accept threshold.

---

## 9) Final Recommendation

**Recommendation: Accept (6) — Borderline Accept / Clear Accept**

This paper makes a clean, falsifiable mechanistic claim that is well-supported across model families, provides a creative minimal causal probe (9-row repair) that localizes the bottleneck, and validates the diagnosis through multiple intervention strategies with informative negative controls. The contribution to the mechanistic interpretability literature is real and the proposed diagnostic framework (probe → measure alignment → targeted repair) has broader methodological value.

The main weaknesses — the numerical inconsistencies between tables, the soft DPS failure explanation buried in the appendix, and the incomplete accounting of the 38 pp entity-counting gap — are addressable in revision but currently create reviewer discussion surface that prevents a stronger score. The practical impact is limited to single-token low-vocabulary aggregation tasks at mid-scale, but this is honestly scoped.

This is a poster-tier paper that the ICLR community will cite for the 9-row repair methodology and the geometric framing of output-head bottlenecks, even if the practical intervention (LoRA Q/V) has narrow applicability.