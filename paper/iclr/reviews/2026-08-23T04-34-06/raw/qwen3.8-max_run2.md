## ⚠ DESK-REJECT RISK

- **Anonymity**: No obvious anonymity violations in the provided manuscript. The author block is anonymous, and I see no acknowledgments, GitHub links, or self-identifying citations in the main text.
- **Page limit**: Cannot be verified from the provided source alone. The main text contains multiple tables, figures, and dense methodological/result sections. Authors should ensure that the main text, excluding references and appendices, fits within the ICLR 9-page submission limit.
- **Required AI use statement**: Present.
- **Style files**: The manuscript uses `\usepackage{iclr2027_conference}`, but the source comment says “NeurIPS 2026 style.” I cannot verify whether the style file is the official ICLR 2027 file. This should be checked before submission.

---

# 1) Core Thesis & Significance

The paper investigates why transformer language models fail at simple counting tasks even when the items to be counted are explicitly present in the context. Its central claim is that the failure is not primarily due to absent internal count information. Instead, the paper argues that models internally encode counts accurately, but the count-encoding direction is geometrically misaligned with the output-head rows corresponding to digit tokens. The authors support this with linear probes, cosine alignment measurements, logit-lens analysis, and interventions: a minimal 9-row `lm_head` repair, a probe-based logit injection method, and LoRA fine-tuning on attention Q/V projections.

The problem is practically relevant and scientifically interesting. Counting failures in LLMs are well known, and a mechanistic explanation would be valuable. The paper’s framing — “the model knows the count but cannot read it out” — is clear and memorable. The contribution is mostly integration-level: linear probes, logit lens, targeted output-head edits, and LoRA are known tools, but their combination into a causal diagnosis of counting failure is potentially useful.

A reviewer can summarize the contribution fairly unambiguously: the paper claims that counting failures arise from a readout bottleneck between an internal count representation and digit-token output rows. However, the manuscript currently overextends in several places and presents multiple numerical inconsistencies that weaken confidence in the exact claims.

---

# 2) Technical Soundness

The conceptual distinction between two failure modes — absent internal representation versus failed readout — is a good one. The paper’s diagnostic logic is attractive:

1. Probe the residual stream for count information.
2. Measure alignment between the probe direction and digit rows of the unembedding matrix.
3. Intervene on the output head or upstream routing.
4. Check whether constrained next-token prediction and autoregressive generation improve.

However, several technical concerns are significant.

## Major concern 1: Probe evidence may not establish that the model “knows” the count

The paper repeatedly states that probes show the model “knows” the count. This is too strong. A linear probe can recover information that is only weakly used by the model’s computation or that is made available by the probe’s own preprocessing.

In particular, the paper emphasizes probes at the “entity-mean” position. If this means averaging hidden states over target-entity mentions, then the probe construction itself may depend on knowing where and how many target mentions exist. That can introduce a form of leakage: the probe may not be reading out an internally aggregated count, but rather exploiting the fact that the probe input was constructed from a variable number of entity positions.

This does not make the result meaningless, but it weakens the claim that the model has formed a causally relevant count representation. To support the stronger “model knows the count” claim, the paper should show that the count is decodable from a fixed, causally relevant output position, e.g. the final token position immediately before the answer, without using the number of target mentions in the probe input construction.

The manuscript mentions last-token logit-lens accuracy but does not provide a clear last-token probe \(R^2\) table comparable to the entity-mean probe table. This is a gap.

**Classification**: significant concern; potentially fatal if the only near-perfect probe evidence relies on an entity-mean construction that leaks count information.

## Major concern 2: Cosine alignment between a probe direction and digit rows is suggestive but not decisive

The paper’s core geometric claim is that the count-probe direction is nearly orthogonal to the digit rows of `lm_head`. This is intuitively appealing, but the metric is not sufficient on its own.

First, the output logit for digit token \(t\) is not determined only by cosine alignment. It depends on the row norm, hidden-state norm, and any bias term:

\[
z_t = w_t^\top h + b_t.
\]

A small cosine value may still produce a meaningful logit if row norms or hidden-state projections are favorable, and conversely a larger cosine may not matter if row norms are small. The paper partially addresses this by discussing digit-row norm competition and norm rescaling, but the main narrative still leans heavily on cosine.

Second, a single probe direction may not be the right object. Count information could be represented in a multidimensional subspace, in class-dependent directions, or in a way that is linearly separable but not aligned with any one “count direction.” The paper says the result holds across ridge, LDA, mean-difference, and PCA probes, which helps, but the analysis would be stronger with subspace-level measurements, e.g. canonical correlation, class-centroid alignment, or direct logit decomposition.

Third, random directions in high-dimensional spaces naturally have small absolute cosine values. The paper compares against a random baseline and uses equivalence testing, which is good, but the conclusion that the model has a specifically “orthogonal” count representation should be stated more carefully. The evidence shows weak alignment, not necessarily an actively enforced orthogonal code.

**Classification**: significant concern.

## Major concern 3: The 9-row repair is a good diagnostic, but its interpretation is complicated by generation-mode failure

The 9-row repair is one of the paper’s strongest causal interventions. Updating only the digit rows improves constrained digit prediction, which supports the claim that part of the bottleneck lies in the output head.

However, the same repair reportedly gives 0.0% accuracy under unconstrained autoregressive generation. This is surprising and not fully resolved by the paper’s explanation. If the repaired rows produce the correct digit under full-vocabulary next-token evaluation, why does greedy generation fail completely? The paper attributes this to routing and format failures, but the manuscript does not make the generation protocol sufficiently transparent.

Key questions include:

- What exactly is the “answer position” in next-token evaluation?
- Is the generation prompt identical to the next-token prompt?
- Is the model allowed to emit non-digit tokens before the answer?
- Does greedy generation begin from the same hidden state used for next-token evaluation?
- Why does full-vocabulary next-token accuracy remain high while generation collapses to 0%?
- What fraction of generation failures are due to emitting a non-digit first token versus emitting the wrong digit later?

The appendix says that 83.5% of hard-DPS generation errors are format failures, which is useful, but the 9-row repair’s complete generation failure needs a clearer causal explanation.

**Classification**: significant concern.

## Major concern 4: Inconsistent numerical reporting

The manuscript contains multiple numerical discrepancies that are difficult to reconcile.

Examples:

- Abstract and main table: 9-row repair on entity counting achieves **60.7%** constrained next-token accuracy.
- Later intervention table: 9-row `lm_head` repair on Qwen3-8B achieves **93.8%** held-out accuracy.
- Discussion: “updating only 9 output rows yields 93–99% held-out accuracy across Qwen3-8B and Mistral-7B.”
- Unified evaluation table: baseline digit-restricted next-token accuracy is **13.7%**.
- Figure caption: next-token digit accuracy is reported as **38.8%** under stratified sampling and **38.6%** under unified-evaluation sampling.
- Intervention comparison table: Qwen3-8B baseline is **11.3%**.
- Soft DPS is **13.2%** in the unified table but **96.3%** in the appendix single-seed table.
- The abstract says LoRA Q/V has **7.67M** parameters; the discussion later refers to “LoRA (84%, 4M params).”

These inconsistencies are serious. They may reflect different protocols, sampling schemes, tasks, or evaluation modes, but the manuscript does not make the mapping sufficiently clear. In a paper whose main contribution is precise mechanistic diagnosis, this level of protocol ambiguity is decision-relevant.

**Classification**: significant concern; if the discrepancies cannot be reconciled, they could become fatal.

## Major concern 5: The claim that orthogonality is a stable fixed point is under-supported

The paper offers a training-dynamics story: digit rows are trained mostly on non-counting contexts, so they become orthogonal to the count direction; once orthogonal, gradient signal along the count direction is near zero.

This is plausible as a hypothesis, but the empirical support is thin. The paper reports that fine-tuning on counting data raises \(|\cos|\) from 0.0074 to 0.0280, while arithmetic fine-tuning does not. However:

- The absolute alignment remains small.
- The paper does not show whether this increased alignment is necessary for behavioral improvement.
- There is no direct gradient analysis across training checkpoints.
- The comparison uses different starting points, making the contrast less clean.
- The “stable fixed point” language is stronger than the evidence warrants.

**Classification**: typical limitation if framed as a hypothesis; significant concern if presented as an established mechanism.

## Other technical issues

- The paper claims “the correct digit’s vocabulary rank drops from 55,980 to 1.” This is striking, but the paper should specify whether this is median, mean, or per-example behavior, and how often rank 1 is achieved.
- The claim that the bottleneck is “absent” from MMLU and GSM8K is too broad given the limited evidence shown.
- The term “bottleneck” is defended operationally, but the paper sometimes uses it more broadly than the evidence supports.
- The causal role of attention Q/V LoRA is plausible, but the paper needs stronger controls against simple task-specific fine-tuning effects.

---

# 3) Empirical Rigor

The empirical scope is ambitious. The paper evaluates multiple models, multiple tasks, multiple intervention types, and several negative controls. This is one of the paper’s strengths.

## Strengths

- Multiple model families: Pythia, Qwen3, Mistral.
- Scale range from 0.4B to 14B.
- Multiple tasks: entity counting, character counting, addition, list length.
- Multiple evaluation modes: next-token, generation, instruct mode.
- Intervention ladder: probes, DPS, 9-row repair, LoRA Q/V.
- Some negative controls: MMLU, GSM8K, DROP subset.
- Some robustness checks: shuffled-label probes, random directions, format robustness, shuffled-row controls.

## Weaknesses

### Baselines and comparisons are incomplete

The paper compares against internal mechanistic interventions but lacks several natural baselines:

- Chain-of-thought prompting is discussed but not given a rigorous table in the main text.
- There is no clear comparison to standard supervised fine-tuning of the full model or a larger adapter.
- There is no parameter-matched LoRA baseline on all projections with identical training data.
- There is no random-label LoRA control to show that the improvement is not simply due to task-specific memorization.
- There is no clear comparison to constrained decoding or simple digit masking without weight edits.
- The paper does not compare against retrieval-style counting, external tools, or explicit counting algorithms, though those are less central to the mechanistic claim.

### Evaluation protocols are too heterogeneous

The paper includes several tables with different protocols: digit-restricted next-token, full-vocabulary next-token, greedy generation, probe-round, hard DPS, soft DPS, single-seed, multi-seed, train vs held-out, entity-only vs multi-task. This would be acceptable if the manuscript maintained a very strict protocol map, but the current presentation is confusing.

The most important problem is that the headline numbers are not stable across tables. A reader should not have to infer whether a 9-row repair number is 60.7%, 93.8%, or somewhere else depending on an unspecified protocol difference.

### Synthetic tasks limit generality

The main tasks are synthetic and low-vocabulary. The paper acknowledges this, but the title and abstract suggest a broader fix for counting failures. The evidence is strongest for artificial counting prompts where the answer is a single digit from 1 to 9. Generalization to natural-language counting, multi-digit answers, and broader reasoning tasks is much weaker.

### Overclaiming check

Several claims exceed the evidence as presented:

- “How to Fix It” in the title is too strong. The 9-row repair does not fix autoregressive generation, and LoRA Q/V gives variable multi-task generation accuracy.
- “The model knows the count” is too strong unless the probe evidence is shown at causally relevant output positions without leakage.
- “Absent from broader multi-step reasoning benchmarks” is too broad without full GSM8K results and a more careful benchmark protocol.
- “Scale strengthens, not refutes, the readout-bottleneck thesis” is plausible, but the 14B evidence is limited.
- “Correcting upstream routing restores generation” is promising, but the multi-task generation variance and unclear training protocol weaken the claim.

---

# 4) Competitive Realism Check

Compared to typical accepted ICLR papers in mechanistic interpretability, this manuscript has a compelling central question and an attractive diagnostic narrative. The combination of probing, geometric analysis, and targeted intervention is the kind of work that can attract interest at ICLR.

However, accepted interpretability papers usually require a high standard of causal clarity and protocol transparency. This manuscript currently falls below that standard in several ways:

- The probe evidence may be partly leaky or insufficiently localized.
- The core geometric metric is suggestive but not decisive.
- The generation-mode results are not fully coherent.
- The tables contain conflicting numbers.
- The paper makes broader claims than the experiments comfortably support.

Would at least two reasonable reviewers score this ≥5 as currently written? Possibly one reviewer would be attracted by the diagnosis and intervention story. Another reviewer would likely focus on inconsistencies and probe leakage. As written, I do not think two stable accept-level reviews are likely without revision.

The weaknesses are not obviously fatal, but they are worse than the typical limitations present in accepted work. The paper is not far from the acceptance threshold, but it needs substantial tightening.

---

# 5) Weakest Link Analysis

The single issue most likely to flip accept/reject is **inconsistent reporting and protocol ambiguity**, especially around the 9-row repair, baseline accuracies, and generation-mode evaluation.

This issue is decision-relevant because the paper’s causal story depends on precise comparisons between constrained next-token prediction, full-vocabulary prediction, and autoregressive generation. If the reader cannot determine which numbers belong to which protocol, the central mechanistic claim becomes hard to trust.

Status of this weakest link:

- **Addressable in revision?** Yes, if the underlying experiments are consistent and the authors can produce a unified evaluation table.
- **Fundamental?** Not necessarily fundamental, but if the discrepancies reflect unstable results rather than presentation errors, it becomes fundamental.
- **Unlikely to change the outcome?** No. If fixed cleanly, the paper could become acceptable.

A secondary weak link is the probe construction, especially the entity-mean probe. If that probe leaks count information through the number of selected entity positions, the “internal representation” claim would be substantially weakened. This is also addressable by adding leak-controlled probes at fixed final-token positions.

---

# 6) Convergence Test (Minimal-Change Threshold)

If the authors made no further changes, I would not assign this manuscript a ≥50% acceptance chance at ICLR. The central idea is interesting, but the current version has too many inconsistent numbers and ambiguous protocols.

The minimal change that would push it closer to acceptance is not merely editorial. The authors should produce a single authoritative evaluation table for the primary claim, with all of the following fixed and explicitly stated:

1. One model, e.g. Qwen3-8B.
2. One primary task, e.g. entity counting with counts 1–9.
3. One held-out test set with templates/entities not used in training.
4. Three seeds minimum.
5. Two evaluation modes:
   - digit-restricted next-token at the answer position;
   - unconstrained greedy generation scored by final emitted integer.
6. Methods:
   - baseline;
   - probe-round;
   - hard DPS;
   - 9-row repair;
   - full `lm_head` repair;
   - LoRA Q/V;
   - LoRA control on another locus or random labels.
7. Explicit parameter counts.
8. Explicit train/validation/test split.
9. Explicit statement of whether numbers are entity-only or multi-task.
10. Confidence intervals or seed-level standard deviations for all headline numbers.

Additionally, the authors should add one decisive probe-control experiment:

- Show count decodability from the final answer-position hidden state without using the number of entity mentions in the probe input.
- If entity-mean probing is retained, include a leak-controlled version and discuss the distinction clearly.

If those changes were made and the numbers remained stable, the paper could plausibly move into the 5–6 range.

---

# 7) Structural Sharpness & Scope Control

The paper is centered on one dominant contribution: counting failure as a geometric readout bottleneck. That core is clear.

However, the manuscript currently includes too many secondary claims, several of which introduce new attack surface.

## Content that strengthens the core argument

- Probe \(R^2\) versus output accuracy gap.
- Cosine/logit-lens analysis of digit-row misalignment.
- 9-row `lm_head` repair under constrained decoding.
- Hard DPS as an analytic bypass.
- LoRA Q/V improvement in logit-lens rank.
- Shuffled-row and random-direction controls.

## Content that is mostly neutral

- Additional tasks such as character counting, addition, and list length, provided they are clearly secondary.
- Instruct-mode first-token results.
- Natural-language counting extension.
- Multi-digit extension.

## Content that introduces new attack surface

- Broad claims about MMLU and GSM8K negative controls without full benchmark details.
- The claim that the bottleneck is absent from broader multi-step reasoning.
- The comparison to chain-of-thought without a rigorous main-text table.
- The 14B “sharpening” claim with limited detail.
- The “How to Fix It” framing when the generation-mode fix is partial.
- The appendix soft-DPS result, which conflicts with the main-table soft-DPS result.

## Recommended scope reduction

To increase acceptance probability, I would recommend the following:

1. Make entity counting the primary task.
2. Keep one or two generalization tasks, e.g. list length and character counting, but do not present them as equally central.
3. Move MMLU/GSM8K/DROP analyses to a clearly labeled secondary section or appendix unless they are fully powered and unambiguous.
4. Reduce the title’s “How to Fix It” framing or qualify it: the paper diagnoses a bottleneck and provides partial targeted repairs, not a complete fix.
5. Remove or reconcile all conflicting single-seed versus multi-seed results.
6. Focus the main text on the cleanest causal chain: probe → geometric misalignment → output-row repair → upstream routing repair.

---

# 8) ICLR Formal Scores

### Soundness: 2

The paper has an interesting diagnostic logic and several useful interventions, but the evidence is weakened by inconsistent tables, ambiguous evaluation protocols, possible probe leakage, and an under-supported training-dynamics claim.

### Presentation: 2

The writing is often clear and the narrative is attractive, but the manuscript presents conflicting numbers across tables and does not sufficiently disambiguate evaluation modes. This materially harms reproducibility and trust.

### Contribution: 3

The central framing — counting failure as a readout bottleneck rather than absent representation — is novel and potentially useful. The combination of probing, geometric diagnosis, and targeted repair is a meaningful contribution if substantiated.

### Significance: 3

If the claims are robust, the paper could influence mechanistic interpretability work on competence-versus-performance failures and targeted model editing. However, the current scope is mostly synthetic, and the practical fix is partial.

### Overall: 4

This is a borderline-reject paper in its current form. The core idea is strong enough to be publishable after substantial revision, but the current manuscript has too many reliability and clarity problems to support acceptance as is.

### Confidence: 4

I am fairly confident in this assessment. The main uncertainties are whether the numerical inconsistencies are merely presentation issues and whether the entity-mean probe construction leaks count information.

---

# 9) Final Recommendation

**ICLR: Borderline Reject (4)**

The manuscript proposes a compelling mechanistic explanation for counting failures: models encode counts internally but fail to read them out through digit-token output rows. The diagnostic framework is interesting, and the intervention ladder is a strength. However, the current version contains conflicting numerical results, ambiguous protocols, possible probe leakage, and overbroad claims relative to the evidence. A revised version with unified evaluation, leak-controlled probes, and tighter scope could become a credible ICLR submission, but as presented the reasons to reject outweigh the reasons to accept.