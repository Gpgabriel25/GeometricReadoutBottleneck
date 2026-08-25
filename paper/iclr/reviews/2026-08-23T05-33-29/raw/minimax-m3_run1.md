# Review of "Why Transformers Fail at Counting and How to Fix It"

## ⚠ DESK-REJECT RISK CHECK

- **Anonymity**: Authors listed as "Anonymous authors / Paper under double-blind review". No author-identifying information detected in main text or appendix. Citations appear in third person. **PASS.**
- **Page limit**: Main text (Sections 1–8 + bibliography) appears tight against the 9-page submission limit given the number of tables and figures. Cannot verify exactly without typesetting; flag for chairs to confirm.
- **AI use statement**: Present immediately after Conclusion. **PASS.**
- **Style files**: Uses `iclr2027_conference` style. **PASS.**

No desk-reject violations detected, with the page-limit caveat noted.

---

## 1) Core Thesis & Significance

The paper claims that transformer counting failures are **not** caused by absent internal representations of the count, but by a **geometric readout bottleneck**: count-encoding directions in the residual stream are orthogonal (|cos| ≤ 0.032) to the digit rows of `lm_head`, and this misalignment is a stable fixed point of training dynamics. The thesis is operationally precise: probes recover counts at R² > 0.99, three independent interventions localize the failure, and the prediction is empirically falsified (and confirmed) under controlled tests across four tasks and four model families.

The contribution is **integration-level**: the individual tools (linear probes, logit-lens, output-head editing, LoRA) are well-established, but the synthesis — a single geometric explanation that predicts and reproduces a specific behavioral failure mode — is novel and would be unambiguous in a summary.

The practical relevance is moderate: counting failures are well-documented but represent a narrow slice of LLM competence. The proposed diagnostic strategy (probe → measure alignment → targeted repair) is more broadly applicable than counting per se.

---

## 2) Technical Soundness

**Strengths:**
- Probe methodology is standard (ridge regression) and well-controlled (shuffled-label probes yield R² = −0.042; positive control on predicted continuation yields |cos| = 0.115, 3.3× the count-probe alignment).
- The orthogonality claim is unusually well-supported: permutation test (p = 0.79), TOST equivalence, four probe types (ridge, LDA, mean-difference, PCA), three model families, bootstrap CIs on per-layer |cos|.
- The mechanistic story (orthogonality as stable fixed point of gradient dynamics) is supported by a controlled comparison: counting fine-tuning raises |cos| by 3.2× while arithmetic fine-tuning does not (1.1×).
- Necessary-and-sufficient controls (shuffled-digit rows degrade below baseline; trained rows at random positions match baseline) correctly frame the diagnostic.

**Concerns (categorized):**

(b) **Significant concern — multiple evaluation protocols with different headline numbers.** The same intervention (9-row repair) is reported as 60.7% (unified multi-seed), 93.8% (single-seed train/held-out), and 99.9% (instruct mode). The paper explicitly acknowledges this in §4 ("How to read the numbers") and §3.4.4 of the appendix, but the protocol-driven variation is large enough that a reader cannot easily verify which result supports which headline claim. The honesty is appreciated but the headline story is harder to defend than a single-protocol headline would be.

(b) **Significant concern — entity counting ceiling of 60.7%.** The 37-pp gap between probe-round (98.7%) and 9-row repair (60.7%) on the headline task is partially explained (norm competition, intra-class variance) but not closed. The capacity ablation rules out two explanations but not a third — e.g., that digit-row geometric structure simply does not match the entity-count subspace for higher counts (the per-count table shows 51.3% at count 4 and 30.6% at count 7, suggesting a non-trivial interaction). This means the "digit-row repair" is *diagnostic* rather than a deployable intervention for entity counting specifically.

(c) **Typical limitation — Pythia-410M transferability.** The 9-row repair only reaches 31.4% on Pythia-410M despite the geometric signature appearing. The authors scope the claim appropriately, but this limits the universality of the diagnosis.

(c) **Typical limitation — soft DPS behavior depends heavily on protocol.** Soft DPS achieves 96.3% in single-seed (Table 4 in appendix) but 13.2% in unified multi-seed (Table 1). The paper explains this is because non-digit tokens dominate the full-vocabulary argmax for every baseline prompt, but the implication that "soft DPS works" requires a constrained decoding setting is understated.

(c) **Typical limitation — generation-mode DPS at 72.4%.** The 83.5% format-failure caveat is honest but reduces the headline.

---

## 3) Empirical Rigor

**Strengths:**
- Multi-seed reporting for headline numbers (3 seeds × 200 prompts for Table 1; 5 seeds for LoRA Q/V).
- Per-seed values reported alongside means for the LoRA Q/V result (71.5%, 89.0%, 86.5%, 81.0%, 87.5%).
- Multiple cross-validation axes: 4 probe types, 3 model families, 4 tasks, 4 model scales (0.4B–14B), 4 prompt formats.
- Negative controls on MMLU and GSM8K (|cos| = 0.31–0.48 vs. ≤0.032 for counting) — these strengthen the specificity argument substantially.

**Concerns:**
- The LoRA Q/V "generation gap = 0.000 across all 5 seeds" is reported but the meaning is unclear (gap between what and what?). This needs clarification.
- DROP shows only partial improvement (20.0% → 30.0%, +10pp), suggesting the diagnosis doesn't fully generalize to less-controlled contexts. The paper notes this but doesn't develop the implication.
- The instruction-mode result (22% first-token, 99.9% after 9-row repair) is striking but not benchmarked across model families.

**Overclaiming check:**
- The abstract's claim of "the model knows the count but the output pathway is geometrically misaligned" is well-supported by the evidence.
- "Substantial improvement" for 9-row repair is fair — 60.7% on entity counting is meaningful but not dominant.
- The LoRA Q/V "achieves 83.1% generation" is accurate given the multi-seed protocol.
- No factual errors detected; confident framing is appropriate to the evidence.

---

## 4) Competitive Realism Check

Compared to typical accepted ICLR mechanistic interpretability papers:
- Stronger than average: the geometric quantification and cross-model validation are unusually thorough.
- Weaker than average: the headline intervention (9-row repair) does not solve entity counting under the most stringent protocol.
- Comparable to typical posters: multiple interventions, multiple controls, clear mechanism.

Would at least two reasonable reviewers likely score this ≥5? **Yes.** The mechanistic story is compelling and the evidence is substantial, even if some headline numbers are not dominant SOTA.

---

## 5) Weakest Link Analysis

**Single issue most likely to flip accept/reject:** The 60.7% on entity counting for the primary intervention under the unified multi-seed protocol. This number is the headline for the 9-row repair claim, and it is 37 percentage points below the probe-round ceiling. While the authors provide partial explanations (norm competition, intra-class variance), the gap leaves the diagnosis feeling incomplete: the bottleneck is real, but the most parsimonious intervention doesn't fully solve the primary task.

- **Addressable in revision:** Yes. A single additional ablation varying prompt diversity at fixed count values (already flagged in the limitations as future work) could clarify the 60.7% ceiling. Alternatively, a more thorough intervention design that combines digit-row repair with norm rescaling could close more of the gap.
- **Fundamental:** No — the mechanism is well-characterized; the 60.7% reflects a sub-optimal intervention, not a flaw in the diagnosis.
- **Unlikely to change the outcome:** The LoRA Q/V result at 83.1%±7.2% is the deployable solution and is solid enough to support the paper's claims regardless.

---

## 6) Convergence Test (Minimal-Change Threshold)

**If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?**

**Yes, but borderline.** This is a solid mechanistic interpretability paper with clear findings, multiple cross-validations, and a deployable intervention. The acceptance probability is probably 50–60% as written.

**Minimal change that would push it over the threshold:**
1. **Single, primary protocol for all headline numbers.** Reporting the 9-row repair as 60.7%, 93.8%, AND 99.9% under three different protocols is honest but reduces credibility. Commit to one protocol and report all numbers under that protocol. (High-leverage change; primarily editorial.)
2. **Close the 60.7% ceiling on entity counting.** Either (a) identify the source of intra-class variance and design an intervention that handles it, or (b) explicitly scope the 9-row repair claim to "diagnostic only" and elevate LoRA Q/V as the headline. (Experimental change.)
3. **Clarify the "generation gap = 0.000" definition.** This number is reported without definition and is confusing. (Editorial.)

---

## 7) Structural Sharpness & Scope Control

**Content that strengthens the core argument:**
- Probe R² > 0.99 (Table 2)
- Per-layer |cos| with bootstrap CIs
- Mechanism explanation (orthogonality as fixed point)
- Negative controls on MMLU/GSM8K
- 14B result showing the bottleneck sharpens with scale
- Format robustness across 4 prompt styles

**Content that is neutral:**
- Cross-task validation on character counting, addition, list length (these support the generality claim but are somewhat redundant with entity counting)
- Max extraction and majority vote (these extend the scope but aren't central to the counting thesis)

**Content that introduces new attack surface:**
- The CoT comparison (§7) is risky: the paper acknowledges it doesn't beat CoT on accuracy, which is honest but draws attention to the limits of the contribution.
- The DROP result (20% → 30%) is honest but invites the question of whether the diagnosis generalizes beyond the synthetic setting.

**Scope reduction recommendation:** Move the max-extraction and majority-vote subsections to appendix. They extend the generality claim but add page count and complexity without strengthening the core counting story. The CoT comparison is appropriate in the main text but could be tightened.

---

## 8) ICLR Formal Scores

- **Soundness (3/4)**: Methodology is sound and well-controlled, but the multiple-protocol reporting on the 9-row repair headline (60.7% / 93.8% / 99.9%) muddies the strongest evidence for the central claim.

- **Presentation (3/4)**: Well-organized with clear tables and figures. The protocol-labelling issue is the main weakness; the writing is otherwise clear and the figures are effective.

- **Contribution (3/4)**: The geometric diagnosis, DPS diagnostic tool, and deployable LoRA Q/V intervention are a coherent and novel synthesis. Not field-shaping, but well above incremental.

- **Significance (3/4)**: The proposed diagnostic strategy (probe → measure alignment → targeted repair) could be applied to other "competence without performance" failures. Moderate practical and methodological impact.

- **Overall (5/10)**: Solid mechanistic interpretability contribution that meets the ICLR acceptance bar. The 60.7% entity-counting ceiling and protocol variability hold it back from clear accept territory, but the depth of evidence and the deployable intervention keep it above borderline reject.

- **Confidence (4/5)**: Confident in the assessment. The core findings are clear; the question is whether the headline numbers meet the bar for stronger acceptance.

---

## 9) Final Recommendation

**Borderline Accept (5)**

This is a substantial mechanistic interpretability study with a clear, falsifiable geometric diagnosis of transformer counting failures. The evidence is unusually thorough — multiple probe types, model families, tasks, and scales, plus negative controls on MMLU/GSM8K that strengthen the specificity argument. The proposed interventions (9-row repair for diagnosis, LoRA Q/V for deployment) are well-motivated and reasonably effective.

However, the paper's strongest evidence is undercut by two issues: (1) the 9-row repair achieves only 60.7% on the headline entity-counting task under the unified multi-seed protocol, leaving a 37-pp gap to the probe-round ceiling that is partially but not fully explained; and (2) the same intervention is reported under three different protocols with three different headline numbers (60.7% / 93.8% / 99.9%), which is honest but reduces the strength of any single claim. The LoRA Q/V result (83.1%±7.2% generation) is solid and provides a deployable solution, but the high variance suggests the intervention is not yet mature for production use.

The paper is a clear poster-tier contribution. The acceptance probability is probably 50–60% as written; tightening the protocol reporting and clarifying the entity-counting ceiling would push this comfortably into accept territory.