## ⚠ Desk-Reject Compliance Check

- **Anonymity**: No obvious anonymity violation. The authors are listed as anonymous, and I do not see author-identifying code links, acknowledgments, or self-revealing prior-work language in the provided text.
- **Page limit**: Cannot be verified from the provided LaTeX source. The authors should ensure that the main text before references/appendix is within the ICLR limit.
- **AI use statement**: Present.
- **Style files**: The manuscript appears to use `iclr2027_conference`, but I cannot verify from the provided text whether it is the exact official ICLR 2027 style.

No clear desk-reject violation is visible from the provided material, but page limit and style compliance should be checked before submission.

---

## 1) Core Thesis & Significance

The paper argues that transformer language models fail at simple counting not because they fail to internally represent the count, but because the internal count representation is geometrically misaligned with the output unembedding rows for digit tokens. The authors support this with linear probes showing near-perfect count decodability, cosine/logit-lens measurements showing weak alignment between count directions and digit rows, and interventions: a minimal 9-row `lm_head` repair that fixes constrained digit prediction, and a LoRA Q/V intervention that improves unconstrained autoregressive generation.

The problem is practically relevant: counting failures in LLMs are well known, embarrassing, and theoretically interesting because the required information is fully present in the context. The novelty is primarily integration-level: the paper combines probing, geometric analysis, logit lens, and targeted interventions into a coherent mechanistic story. The contribution is not a new architecture or a new benchmark, but a diagnosis and causal localization of a specific failure mode.

A reviewer can summarize the contribution unambiguously: “the model internally encodes the count, but the output pathway does not read it out; repairing the readout or upstream routing fixes the behavior.” That is a clean and memorable claim.

---

## 2) Technical Soundness

The paper’s core technical approach is reasonable: probe the residual stream for count information, measure alignment with digit unembedding rows, use logit lens to inspect readout, and then intervene causally. The strongest evidence is the combination of:

1. high probe accuracy,
2. low cosine alignment with digit rows,
3. improved constrained accuracy after repairing only digit rows,
4. improved generation after LoRA Q/V,
5. logit-lens rank changes under the intervention.

However, several issues matter.

### Significant concerns

**(a) Probe decodability is not identical to causal model use.**  
A linear probe reaching \(R^2 > 0.99\) shows that count information is linearly decodable, but it does not by itself prove that the model uses that representation to produce its answer. The authors partially address this through interventions, especially hard DPS and the 9-row repair, but the inference still depends on the probe direction being the relevant causal direction rather than a correlated linear feature. This is a standard limitation of probing studies, but because the paper’s headline claim is “the model knows the count,” the language should be more cautious.

Classification: **significant concern, fixable with more careful framing and/or causal scrubbing/ablation evidence.**

**(b) Cosine alignment may be an oversimplified readout metric.**  
In high-dimensional spaces, many semantically meaningful directions are nearly orthogonal to arbitrary output rows by default. The authors compare to random directions and provide a positive control, which helps. Still, the claim of “orthogonality” rests heavily on a single cosine measurement between a probe direction and digit rows. The readout could involve nonlinear effects, norm effects, combinations of directions, or state-dependent normalization. The paper does discuss RMSNorm and digit-row norm competition, but the central geometric claim would be stronger with additional metrics, e.g., subspace alignment, trained linear readouts to digit logits, causal mediation analysis, or representation similarity measures.

Classification: **significant concern, but not fatal given the converging intervention evidence.**

**(c) Quantitative inconsistencies across tables and claims.**  
This is the most serious presentational/soundness issue in the current manuscript. Several numbers do not line up cleanly:

- Table 4/unified evaluation reports 9-row repair at **60.7%** digit-restricted next-token accuracy and **0.0%** generation for Qwen3-8B entity counting.
- Table 5 reports 9-row repair across four tasks as **60.7–100.0%**, with entity counting specifically at **60.7%**.
- Table 6 reports “9-row `lm_head` (held-out)” for Qwen3-8B at **93.8%**, without clearly stating which task, protocol, or evaluation mode this corresponds to.
- The Discussion says “updating only 9 output rows yields 93–99% held-out accuracy across Qwen3-8B and Mistral-7B, surpassing LoRA (84%, 4M params),” which appears to conflict with the main constrained entity-counting result of 60.7% and with the reported LoRA parameter count of 7.67M.

These inconsistencies do not necessarily invalidate the core claim, but they make it difficult to know exactly which claims are supported under which protocol. In a paper whose contribution is precise mechanistic localization, this level of ambiguity is decision-relevant.

Classification: **significant concern; could become fatal if not clarified in rebuttal/camera-ready.**

**(d) The LoRA Q/V mechanism claim needs stronger main-text evidence.**  
The paper claims LoRA Q/V fixes “upstream routing.” The evidence includes logit-lens improvement, rank reduction, and a locus ablation. However, the main text does not show the full locus ablation numerically. Without seeing the comparison against LoRA on K/O, MLP, or all projections, it is hard to evaluate how specific the Q/V claim is. The claim may still be true, but the current main text relies on a summarized ablation.

Classification: **significant concern, addressable by adding the ablation table to the main text or clearly pointing to the appendix.**

### Typical limitations

**(e) Synthetic task scope.**  
The strongest evidence is on synthetic or low-vocabulary aggregation tasks. This is appropriate for mechanistic analysis, but the generality of the claim should be carefully bounded.

**(f) “Orthogonality as stable fixed point” is heuristic.**  
The training-dynamics explanation is plausible but not formally derived. The empirical fine-tuning check is suggestive, not conclusive.

**(g) Scale and architecture scope.**  
Models up to 14B and three decoder-only families are reasonable for ICLR, but the claim should not be extended to frontier-scale models or non-transformer architectures without further evidence.

Overall, I do not see a fatal flaw in the core idea. The main technical risk is overinterpreting probe/cosine evidence and the presence of inconsistent quantitative reporting.

---

## 3) Empirical Rigor

The empirical effort is substantial. The paper includes:

- multiple model families: Pythia, Mistral, Qwen3;
- multiple scales: 0.4B to 14B;
- multiple tasks: entity counting, character counting, addition, list length, majority vote, max extraction, multi-digit counts;
- multiple evaluation modes: next-token, full-vocabulary next-token, greedy generation, instruct mode;
- controls: random directions, shuffled labels, shuffled rows, random-position controls, capacity ablations, format robustness;
- seeds and variance reporting for several headline results.

This is much stronger than a purely observational probing paper. The intervention component is the main empirical strength.

### Are experiments sufficient to support the core claim?

For the constrained counting setting, mostly yes. The 9-row repair and hard DPS provide compelling evidence that the output head is a bottleneck for constrained digit prediction. The logit-lens rank reduction under LoRA Q/V is also persuasive as evidence that the intervention changes the readout pathway.

However, the evidence for the broader claim — “LoRA Q/V corrects upstream routing” — would be stronger with:

- full numerical locus ablations in the main text;
- comparison with LoRA on all attention projections, MLPs, or a standard LoRA baseline distributed across all layers;
- comparison with chain-of-thought prompting under exactly the same scoring protocol;
- clearer separation between entity-only and multi-task LoRA results.

### Are baselines appropriate and fair?

Mostly, but there are gaps. The paper compares against baseline, DPS, probe-round, 9-row repair, and LoRA Q/V. Missing or under-specified comparisons include:

1. **LoRA baselines at other loci.** The paper says Q/V is best, but the main text does not show the full comparison.
2. **Standard LoRA across all layers or all projections.** This would help assess whether Q/V is special or whether any sufficient fine-tuning fixes the task.
3. **Chain-of-thought.** The Discussion compares conceptually with CoT, but the main empirical comparison is not prominent. Since CoT is a natural zero-shot/few-shot fix for counting, a mode-matched CoT baseline would strengthen the “how to fix it” part of the title.
4. **Fine-tuning on counting data without restricting to digit rows.** The paper has some fine-tuning alignment analysis, but a clearer behavioral baseline would help.

### Are trade-offs quantified?

Partially. The paper reports parameter counts and distinguishes constrained next-token accuracy from generation accuracy. This is useful. But the trade-off between the 9-row repair and LoRA is muddled by inconsistent numbers. The 9-row repair is a beautiful diagnostic, but its failure in unconstrained generation means it is not a deployable fix. The LoRA intervention is deployable but requires fine-tuning and has multi-task variance. The paper should state this trade-off more cleanly.

### Overclaiming check

Several claims should be softened or clarified:

- “The model knows the count” is rhetorically effective but too strong. Better: “a linear probe can recover the count from intermediate representations, and interventions show that this information can be causally routed to the output.”
- “Updating only the digit rows substantially improves constrained next-token digit prediction” is supported for some tasks, but the entity-counting result is only 60.7%, so the range 60.7–100.0% should be presented carefully.
- The Discussion sentence claiming 9-row repair yields “93–99% held-out accuracy” appears inconsistent with the main entity-counting table and should be corrected or explained.
- “Surpassing LoRA” should not be claimed across different evaluation modes or parameter budgets without a mode-matched comparison.
- The 14B result is described as “targeted repair recovers 90.3%,” but Table 6 lists “9-row + DPS,” which is not the same as 9-row repair alone. This should be clarified.
- MMLU/GSM8K as negative controls are interesting, but the tasks are not directly comparable to single-digit counting. The paper should frame them as exploratory scope checks rather than strong negative controls.

---

## 4) Competitive Realism Check (Calibrated)

Compared to typical accepted ICLR papers, this manuscript has several strengths that are common in accepted mechanistic-interpretability work:

- a clearly stated mechanism;
- a controlled synthetic benchmark;
- multiple models and scales;
- causal interventions rather than only correlational probing;
- ablations and controls;
- a memorable diagnostic narrative.

The weaknesses are also common in this literature:

- reliance on synthetic tasks;
- potential gap between probe decodability and causal representation;
- limited scale relative to frontier models;
- somewhat overstrong “model knows” language.

The non-standard problem is the internal inconsistency in the reported numbers. That is more concerning than the usual limitations because it affects trust in the headline claims. Still, the inconsistency appears fixable rather than fundamental.

Would at least two reasonable reviewers likely score this ≥5? Probably yes, if the table inconsistencies are clarified. As currently presented, one reviewer may focus on the conflicting 9-row numbers and downgrade the paper to borderline reject. Another reviewer may value the mechanistic diagnosis and interventions enough to score it accept. So the paper is within acceptance variance, but not decision-stable as written.

---

## 5) Weakest Link Analysis

The single issue most likely to flip accept/reject is **the inconsistent reporting of the 9-row repair and LoRA results across tables and prose**.

Specifically, the reader cannot easily reconcile:

- 60.7% entity-counting 9-row repair in the unified/mode-matched tables;
- 93.8% “9-row `lm_head` (held-out)” in the intervention comparison table;
- “93–99% held-out accuracy” in the Discussion;
- 0.0% generation for 9-row repair;
- LoRA parameter count and accuracy comparisons across modes.

This is **addressable in revision**, but it must be addressed decisively. The authors need one canonical table that states, for each method and each task, the exact evaluation mode, argmax scope, prompt set, seed set, and scoring rule. Claims in the abstract/introduction/discussion should then be tied only to that canonical table.

If the inconsistency is merely a labeling error, it is fixable. If it reflects unresolved protocol confusion, it would become a more serious methodological issue.

---

## 6) Convergence Test (Minimal-Change Threshold)

**If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?**

As presented, I would say **borderline, slightly below a comfortable 50%**. The core contribution is strong enough that some reviewers would accept it, but the inconsistent quantitative reporting creates unnecessary risk. A reviewer who notices the conflicting 9-row numbers may reasonably question whether the headline claims are stable.

**Minimal change that would push it over the threshold:**

The most important change is not prose polish but evidence organization:

1. Add a single canonical table for the primary entity-counting task, with rows for:
   - baseline;
   - probe-round;
   - hard DPS;
   - 9-row repair;
   - full `lm_head` repair;
   - LoRA Q/V;
   - LoRA other loci or all projections;
   - CoT prompting, if available.

   Columns should be:
   - digit-restricted next-token accuracy;
   - full-vocabulary next-token accuracy;
   - greedy generation accuracy;
   - parameter count;
   - number of seeds and variance.

2. Remove or clearly footnote any table entry that uses a different protocol. Table 6 in particular needs explicit task/mode labels.

3. Align all abstract/introduction/discussion claims with that table. If the 9-row repair achieves 60.7% on entity counting, the Discussion should not say “93–99%” without specifying that this refers to other tasks or another protocol.

4. Move secondary tasks to a clearly labeled extension section or appendix, so the main story is not diluted.

This minimal evidence-based revision would substantially increase decision stability.

---

## 7) Structural Sharpness & Scope Control

The paper is centered on one dominant contribution: **counting failure as a geometric readout bottleneck**. That is a strong central thesis.

### Content that strengthens the core argument

- Probe \(R^2\) results.
- Cosine alignment with digit rows.
- Logit-lens analysis.
- 9-row `lm_head` repair.
- Hard DPS bypass.
- LoRA Q/V generation results.
- Mode-matched comparison between constrained and generation evaluation.

### Neutral content

- Background on mechanistic interpretability and activation steering is fine but standard.
- General discussion of superposition is plausible but not essential.

### Content that introduces new attack surface

- MMLU/GSM8K negative controls. These are interesting but not perfectly comparable to counting tasks and may invite objections about task mismatch.
- Majority vote, max extraction, and multi-digit results. These support generality but expand the scope beyond the cleanest single-digit counting case.
- The CoT discussion. Without a strong mode-matched CoT baseline, this invites comparison to a natural method that the paper does not fully benchmark.
- Table 6 as currently written. It creates more confusion than clarity.

### Recommended scope reduction

The paper would be stronger if the main text focused primarily on entity counting as the canonical case, with character counting/addition/list length presented as supporting extensions. MMLU/GSM8K, majority vote, max extraction, and multi-digit results could be moved to a clearly labeled broader-evaluation appendix. The title says “How to Fix It,” so the main text should also make the fix story cleaner: one diagnostic fix, one deployable fix, one comparison baseline.

---

## 8) ICLR Formal Scores

### Soundness: **3**

The core methodology is sound, and the intervention evidence is stronger than typical probing work. However, the probe-to-causality gap, reliance on cosine geometry, and especially the inconsistent table reporting prevent a higher score.

### Presentation: **2**

The writing is generally clear and the narrative is compelling, but the manuscript currently suffers from protocol ambiguity and conflicting numbers. For a paper whose contribution is precise mechanistic localization, this is a meaningful weakness.

### Contribution: **3**

The paper provides a useful mechanistic diagnosis and a clean set of interventions. The novelty is mostly in the integration of probing, geometric analysis, and targeted repair, rather than in a fundamentally new method.

### Significance: **3**

The finding is memorable and likely to be cited in interpretability and evaluation discussions: models can internally represent a count while failing to emit it due to output-pathway misalignment. The practical impact is more limited because the strongest fixes are task-specific and require intervention, but the conceptual contribution is solid.

### Overall: **5**

This is a solid, poster-level ICLR paper with an interesting mechanism and meaningful interventions. It is held back from a clear accept by avoidable reporting inconsistencies and some overbroad claims. With a clean canonical evaluation table and tightened claims, it would likely become a clear accept.

### Confidence: **3**

I am fairly confident in this assessment based on the provided manuscript, but I cannot verify all appendix details, figures, code, or full experimental configurations.

---

## 9) Final Recommendation (Venue-Calibrated)

**ICLR recommendation: Borderline Accept (5).**

The paper presents a clear and memorable mechanistic claim: counting failures can arise from a readout bottleneck rather than from absent internal count information. The combination of probes, logit lens, 9-row repair, DPS, and LoRA Q/V is stronger than standard correlational interpretability work. However, the current manuscript contains inconsistent quantitative reporting and some overclaims that make the acceptance decision less stable than the underlying evidence warrants. If the authors reconcile the tables, clarify the evaluation protocols, and add mode-matched baselines for the main claims, this should become a reliable ICLR poster.