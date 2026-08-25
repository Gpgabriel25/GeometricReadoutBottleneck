# Review: "Why Transformers Fail at Counting and How to Fix It"

## 1) Core Thesis & Significance

The paper presents a mechanistic investigation into why transformers fail at trivial counting tasks. The central thesis is that the failure is a *geometric readout bottleneck* — the model encodes counts with near-perfect fidelity internally (probe R² > 0.99), but the count-encoding directions are nearly orthogonal to the output-head digit rows (|cos| ≤ 0.032), preventing readout. This is supported by a clean causal chain: targeted 9-row lm_head repair fixes constrained decoding (60.7–100%), while LoRA Q/V fixes upstream routing for autoregressive generation (83.1% ± 7.2%).

The problem is practically relevant and well-motivated. The novelty is significant — distinguishing encoding failure from readout failure and providing causal localization is a contribution that goes substantially beyond prior work documenting counting failures. The contribution is component-level (geometric diagnosis) with integration-level impact (connecting probes, logit lens, targeted repair, and LoRA interventions into a coherent pipeline). A reviewer can summarize this unambiguously.

## 2) Technical Soundness

The methodology is generally sound and well-controlled, though several points deserve scrutiny:

**Strengths:**
- The probe-to-intervention causal chain is well-designed. The fact that 9-row repair works under constrained decoding but not generation, while LoRA Q/V works in both, is a clean falsifiable prediction that tests the diagnosis.
- Robustness checks are thorough: shuffled-label probes, random-direction baselines, TOST equivalence testing, permutation tests, capacity ablations, and negative controls (MMLU, GSM8K).
- The protocol transparency is notable — different evaluation modes are explicitly mapped, and the authors carefully distinguish headlined numbers by their protocol.

**Concerns:**
- (b) **The orthogonality claim deserves more scrutiny.** The |cos| ≤ 0.032 value is compared to random baselines (0.013 ± 0.011), and the authors claim statistical equivalence (p = 0.79). This is correct for showing no positive alignment, but the paper's framing sometimes implies the orthogonality is "caused by training dynamics" — the gradient analysis in §5 provides a plausible mechanism, but the fine-tuning experiments are suggestive rather than conclusive (the counting fine-tune increases |cos| only from 0.0074 to 0.028, still very small). The story is coherent but the causal claim about training dynamics remains somewhat handwavy.
- (b) **The 9-row repair entity-counting gap (60.7% vs. probe-round 98.7%)** is explained post hoc by norm competition and hidden-state diversity, but these two explanations are not fully disentangled. The capacity ablation helps, but the authors acknowledge this in limitations. This is a significant but not fatal gap.
- (c) **Pythia-410M only reaches 31.4% with 9-row repair**, which the authors note limits the repair claim to mid-size models. This is acknowledged, though it somewhat weakens the "generalizes across model families" claim.

No fatal flaws identified. The theoretical analysis of training dynamics could be stronger.

## 3) Empirical Rigor

**Strengths:**
- Experiments are comprehensive: four tasks (entity counting, character counting, addition, list length), multiple model families, multiple scales (0.4B–14B), multiple evaluation modes, and multiple seeds.
- The unified evaluation table (Table 2) with shared prompts/seeds/scoring is exemplary.
- Negative controls on MMLU and GSM8K (|cos| = 0.31–0.48 vs. ≤ 0.032 for counting) effectively scope the finding.
- The LoRA Q/V generation results include per-seed reporting (71.5%, 89.0%, 86.5%, 81.0%, 87.5%) showing non-trivial variance — this is honest reporting.
- The DPS/digit-row repair are complementary diagnostics that triangulate the same conclusion.

**Concerns:**
- (b) **LoRA Q/V multi-task variance is high** (83.1% ± 7.2%), and the per-seed breakdown reveals entity-only vs. multi-task as an additional factor. The 71.5% seed is concerning — the range spans 71.5–89.0%, which could be unstable in practice. The authors explain this as a "task-mix artifact" citing entity-only per-seed results (97.0%, 96.5%, 94.5%), which is reassuring but still leaves the multi-task claim somewhat fragile.
- (c) **Only Qwen3-8B gets full treatment.** Mistral-7B validation is limited to the 9-row repair (92.0%), and Pythia-410M largely fails. The cross-model claim is qualified but could be stronger with more complete Mistral experiments.
- Overclaiming check: The abstract's claim of "near-perfect accuracy (R² > 0.99)" is well-supported for entity counting but the paper is careful to scope claims to low-vocabulary aggregation tasks. The headline 83.1% generation accuracy is accurately reported. No significant overclaiming detected.

## 4) Competitive Realism Check (Calibrated)

This paper is at **poster accept / strong poster tier**. Comparing to typical ICLR accepted work:

- The mechanistic interpretability contribution (geometric diagnosis + causal interventions) is substantive and novel. The probe → diagnosis → intervention pipeline is cleaner than most similar work.
- The combination of mechanistic analysis with a practical intervention (LoRA Q/V at 83.1% generation) gives both scientific and practical value.
- The scope control is good — negative controls on MMLU/GSM8K, explicit limitation to low-vocabulary aggregation.
- The 9-row repair gap (60.7% on entity counting) and LoRA Q/V variance (±7.2%) are weaknesses, but these are within the variance of accepted work at ICLR.
- At least two reasonable reviewers would likely score this ≥5 (Accept/Poster). The paper is above the poster mean of 5.35 due to clean experimental design, clear causal narrative, and honest scope limitation.

The paper does not reach oral tier (8+) because: (1) the 9-row repair gap and LoRA variance are nontrivial; (2) cross-model validation is thin; (3) the practical impact is limited to a narrow task class (low-vocabulary aggregation).

## 5) Weakest Link Analysis

**The single issue most likely to flip accept/reject:** The 9-row repair achieving only 60.7% on entity counting while claiming to "causally localize" the bottleneck. Two rounds of defense exist: (a) the 9-row repair hits 93.8% under single-seed protocol on held-out data, and (b) the full-vocabulary argmax matches at 60.3%, ruling out a decoding mismatch. However, a skeptical reviewer could argue that 60.7% is too low for a "bottleneck" diagnosis — if the model truly had the count and only the output head was misaligned, why does fixing the output head recover only ~60%? The capacity ablation partially addresses this, but the remaining gap attributed to "hidden-state diversity" is somewhat vague.

This is **addressable in revision** — more detailed analysis of entity-counting failure modes (per-count stratification is already in the appendix, showing highly variable per-count accuracy: 30.6–100%) and a clearer mechanistic account of why entity counting is harder than character counting or list length would strengthen the argument. Decision-stable: this is unlikely to flip the decision alone.

## 6) Convergence Test (Minimal-Change Threshold)

**If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?** Yes, with moderate confidence (~55-60%). The narrative is compelling, the experiments are extensive, and the controls are well-designed.

**Minimal change that would most improve chances:** The analysis of the entity-counting residual gap (60.7% vs. ~100% on other tasks) needs one more layer. Specifically: a fine-grained failure analysis of *which* prompts the 9-row repair fails on for entity counting — are these failures clustered by count value (Table 11 shows extreme variance: 30.6% at count 7 vs. 100% at count 2), by distractor configuration, or by mention spacing? Connecting this failure taxonomy to the "hidden-state diversity" explanation with quantitative evidence would substantially strengthen the diagnosis and is likely the single change with highest acceptance-probability impact.

## 7) Structural Sharpness & Scope Control

The paper is **well-centered on one dominant contribution**: the geometric readout bottleneck diagnosis. Content analysis:

**(a) Strengthens core argument:**
- Probe R² measurements (§4)
- Logit-lens analysis showing 55,980 → 1 rank drop (§5)
- 9-row repair as causal localization (§6)
- LoRA Q/V as deployable fix (§6)
- MMLU/GSM8K negative controls

**(b) Neutral:**
- The background section is adequate but not tightly connected to the contribution.
- The protocol map table and extended robustness checks in the appendix are necessary for reproducibility.

**(c) Introduces attack surface:**
- The gradient analysis of *why* orthogonality arises (§5, "Why is orthogonality there?") is the weakest theoretical section. The proposed mechanism (non-counting digit contexts dominate conditioning) is plausible but the fine-tuning evidence is thin (0.0074 → 0.028 is still very small alignment). A reviewer could question whether the training dynamics explanation is properly supported vs. being an ad hoc narrative.
- The CoT comparison in §7 is interesting but risks being unfocused — the authors correctly note they are not claiming to beat CoT, but the section adds length without closing a loop.

**Scope reduction recommendation:** The gradient training-dynamics explanation could be moved to an appendix or condensed, with the main text focusing on the empirically verified diagnosis. This reduces attack surface without losing the core contribution.

## 8) ICLR Formal Scores

- **Soundness (3):** Methodology is rigorous with extensive controls. The probe→diagnosis→intervention chain is logically sound. Minor gaps in the training dynamics explanation and entity-counting gap explanation.

- **Presentation (3):** Well-organized with clear narrative structure. Table 2 (unified evaluation) is excellent. The protocol explanation paragraph (§4.1) is unusually helpful. Some complexity in tracking multiple numerical results across protocols, but the authors manage this well.

- **Contribution (3):** Novel geometric diagnosis of a well-known failure mode. The combination of interpretability diagnosis + practical intervention is valuable. The bottleneck framing is well-defined and operationally grounded.

- **Significance (3):** Impactful for the mechanistic interpretability community and practitioners debugging counting failures. The diagnostic strategy (probe → alignment check → targeted repair) is generalizable. Limited to low-vocabulary aggregation tasks, which bounds practical impact, but the mechanistic insight is broadly applicable to "competence without performance" failures.

- **Overall (6):** Solid poster accept. Clear contribution with good experimental rigor, honest scope limitation, and a clean causal narrative. Above the poster mean of 5.35, but the entity-counting 60.7% gap and LoRA variance prevent a 7. The paper would be a credible poster at any top ML venue.

- **Confidence (4):** Confident. The experiments are well-documented with sufficient protocol detail for verification. The core claims are well-supported by converging evidence from probes, logit lens, and interventions.

## 9) Final Recommendation

**Accept (Poster).**

This paper makes a clear, well-scoped contribution: identifying counting failure as a geometric readout bottleneck rather than a representational failure. The experimental design is unusually rigorous for mechanistic interpretability work — shared protocols, extensive controls, and honest qualification of claims. The 9-row repair entity-counting gap (60.7%) and LoRA Q/V variance are legitimate weaknesses, but both are within the normal range for accepted ICLR work and are transparently reported. The negative controls on MMLU/GSM8K and the capacity ablations demonstrate scientific maturity. At least two of three likely reviewers would score this ≥5.

---

**⚠ DESK-REJECT RISK items:**
- **Style files:** The paper uses `\usepackage{iclr2027_conference}` — appears correct for ICLR 2027.
- **Anonymity:** `Anonymous authors / Paper under double-blind review` — no violation detected. No GitHub links or author-identifying information found.
- **Page limit:** Not verifiable from the raw LaTeX alone, but the content appears approximately 9 pages for the main text, with a substantial appendix. References and appendices do not count. No violation apparent.
- **AI use statement:** Present ("AI tools were used for editing assistance..."). Compliant.