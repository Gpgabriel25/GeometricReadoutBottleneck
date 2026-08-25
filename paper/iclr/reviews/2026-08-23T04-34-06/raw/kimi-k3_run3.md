## Desk-Reject Compliance Check

- **Anonymity:** No obvious author-identifying information, acknowledgments, or non-anonymous repository links appear in the provided source.
- **Page limit:** Cannot be verified without the compiled PDF. There is no obvious source-level violation, but the exact main-text length and float placement need checking.
- **Required AI use statement:** Present.
- **Style files:** The source uses `iclr2027_conference`; the stale preamble comment mentioning “NeurIPS 2026 style” is not typeset and should not itself be a compliance issue. I cannot verify that the referenced style file is the unmodified official file.
- **Other verification limits:** The bibliography database and figure PDFs were not included, so citation rendering and figure content cannot be inspected.

No definite **⚠ DESK-REJECT RISK** is identifiable from the provided material.

## 1) Core Thesis & Significance

The paper argues that counting failures are not primarily failures to represent the count: linear probes recover counts with \(R^2>0.99\), while the count-encoding directions are nearly orthogonal to digit-token rows of the output head. It supports this diagnosis with logit-lens measurements, a minimal nine-row output-head repair, DPS interventions, and a LoRA Q/V intervention that improves greedy generation.

The problem is scientifically relevant as a clean instance of “competence without performance,” although the immediate practical significance is narrower than the title suggests: the strongest evidence concerns synthetic, low-vocabulary aggregation tasks on open decoder-only models up to 14B. The novelty is primarily integration-level—combining probing, output-head geometry, logit lens, and targeted adaptation—but the geometric framing and minimal-row localization could be a useful contribution if the evidence is reliable.

A reviewer can summarize the thesis unambiguously: **the count is represented, but the output pathway cannot normally read it out.** However, the many incompatible-looking numerical results make it difficult to determine exactly which protocol supports each version of that thesis.

## 2) Technical Soundness

### (a) Fatal or potentially fatal flaw

**The protocol and numerical provenance of the headline results are not auditable as presented.** This is decision-blocking unless it can be fully reconciled.

Examples include:

- The unified entity-counting baseline is **13.7%** in Table 1 and **11.3%** in Table 4, while Figure 2 refers to **38.8%/38.6%** next-token digit accuracy under allegedly related sampling protocols.
- The nine-row entity-counting repair is **60.7%** in the mode-matched table but **93.8% held-out** in Table 4; the Discussion subsequently describes 93–99% held-out accuracy across Qwen3-8B and Mistral-7B. These may come from different protocols, but the tables do not provide enough information to establish that.
- Soft DPS is listed at **13.2% under digit-restricted next-token evaluation**, yet the appendix explains its failure by saying that a non-digit token wins the full-vocabulary argmax. A non-digit winner should be irrelevant under a genuinely digit-restricted argmax. Either the column label, the evaluation, or the explanation is wrong.
- Single-seed soft DPS is reported at 96.3%, while the purportedly corresponding multi-seed result is 13.2%. The stated single-versus-multi-seed explanation is not sufficient to explain an 83-point difference.
- Qwen3-14B is said to show that “targeted repair” recovers 90.3%, but the table evaluates **nine-row repair plus DPS**, not the nine-row repair alone.

These discrepancies do not prove the underlying phenomenon is false, but they prevent verification of the central quantitative claims. A complete result registry—prompt set, model checkpoint, probe layer, intervention, argmax scope, decoding mode, train/test split, scorer, and seed set for every number—is necessary.

### (b) Significant concerns

1. **Entity-mean probing does not by itself establish a count representation at the model’s decision point.**  
   Constructing an “entity-mean” representation gives the probe access to all target-mention positions and may allow it to integrate evidence that is distributed across tokens, even if no individual hidden state usable by the model contains an aggregate count. The last-token row of the logit-lens table leaves probe \(R^2\) blank. Direct last-token probe accuracy, MAE, confusion matrices, and causal ablation of the probed direction are needed to support the claim that “the model stores the count.”

2. **Raw cosine orthogonality is not, by itself, the relevant readout geometry.**  
   A probe weight from an intermediate layer lives in a different representational coordinate system from the rows of the final output head. Downstream attention, MLPs, and normalization can rotate or transform the count direction. The logit-lens evidence helps, but the paper should measure alignment of the actual count component at the output-read position, ideally through path-specific causal interventions rather than only comparing raw parameter vectors.

3. **Hard DPS and probe-round are largely tautological.**  
   Hard DPS adds a large constant to the digit predicted by the probe; matching probe-round therefore does not independently verify the geometric diagnosis. It confirms that the probe prediction is accurate when forcibly emitted, not that the diagnosed output-head geometry uniquely explains the original failure.

4. **The causal interpretation of the nine-row repair is overextended.**  
   Fine-tuning nine rows on counting prompts shows that a low-dimensional output-head adaptation can learn the task mapping. It does not, without more controls, prove that the original failure was uniquely caused by those rows. The shuffled-row and random-position controls are useful, but the paper should also compare same-budget adaptations at non-output loci, a separately trained linear readout, and alternative rows under identical data and optimization.

5. **“Necessary and sufficient” is stronger than the controls establish.**  
   The experiments support necessity and sufficiency only within a particular synthetic constrained-decoding regime and a limited intervention family. They do not establish universal necessity or sufficiency, particularly because Pythia exhibits the geometric signature but only reaches 31.4% after repair.

6. **The LoRA mechanism and deployability claims need more evidence.**  
   The claimed locus ablation is not presented with full results. More importantly, Q/V LoRA could damage general behavior, yet no post-intervention perplexity, MMLU, or general-generation evaluation is reported. “Deployable” is not supported by task-specific synthetic gains alone.

7. **The training-dynamics explanation is speculative.**  
   The argument that orthogonality is a stable fixed point of gradient training is plausible but not rigorously established. Two fine-tuning runs starting from different checkpoints and showing movement between very small cosine values do not strongly validate the proposed fixed-point mechanism.

### (c) Typical limitations

- Restriction to decoder-only transformers and models no larger than 14B.
- Heavy reliance on synthetic tasks.
- Lack of frontier-model evidence.
- Task-specific fine-tuning rather than a general counting fix.
- Limited natural-language and out-of-distribution evaluation.

These limitations would be acceptable in an otherwise well-audited ICLR paper.

## 3) Empirical Rigor

### Strengths

- Three model families and an additional 14B checkpoint are examined.
- The factorial prompt design varies count, distractors, passage length, and spacing independently.
- Several probe types, shuffled-label controls, random-direction baselines, permutation testing, and TOST are used.
- The study combines constrained decoding, full-vocabulary decoding, greedy generation, logit lens, and multiple interventions.
- The median vocabulary-rank improvement from 55,980 to 1 is a memorable and potentially strong mechanistic measurement.
- Negative controls and per-count breakdowns are included, at least in summarized form.

### Major gaps

1. **Baselines are incomplete.**  
   The paper should report, under identical training data and compute:
   - Full-model fine-tuning.
   - LoRA at Q/K/V/O, MLP, and multiple ranks, with full numerical results rather than a summary claim.
   - A trainable linear classifier from the final hidden state.
   - Standard prompting and CoT under the same final-answer scorer.
   - A format-constrained decoding baseline where applicable.

2. **Important training and evaluation details are missing.**  
   The source does not specify probe regularization, normalization, LoRA \(\alpha\), learning rates, batch sizes, optimizer settings, training-prompt composition, deduplication, template disjointness, or whether entities and templates overlap between train and test. No code or configuration repository is provided.

3. **Uncertainty reporting is inconsistent.**  
   Some results use three or five seeds, while many geometric and cross-task results are point estimates. The main LoRA result has a large spread, \(83.1\%\pm7.2\%\). Reporting entity-only results from separate runs does not establish that the multi-task variance is merely a “task-mix artifact.”

4. **Probe evaluation should go beyond \(R^2\).**  
   \(R^2\) can look high when the target range is wide even if count classification is imperfect. MAE, rounded-count accuracy, per-count confusion, and calibration should accompany \(R^2\). The paper sometimes calls \(R^2\) “near-perfect accuracy,” which is imprecise.

5. **General-capability trade-offs are not quantified.**  
   A LoRA intervention on attention Q/V weights is global. Its effects on unrelated tasks, calibration, perplexity, and long-form generation are essential before describing it as a deployable fix.

### Overclaiming check

The following claims clearly exceed the evidence presented:

- **“Probe-round upper-bounds what any output-side intervention can reach.”** A particular linear probe is not a theoretical upper bound on all possible output-side interventions; it is only an operational reference decoder.
- **“Absent from GSM8K.”** No GSM8K results are actually reported in the supplied manuscript.
- **“Scale strengthens the thesis.”** One 14B result, using a combined nine-row-plus-DPS intervention, is insufficient for a broad scaling claim—especially when Pythia shows the same signature but limited repair.
- **“Necessary and sufficient.”** This is only demonstrated within a narrow intervention and evaluation family.
- **“Deployable LoRA intervention.”** General-capability and robustness costs are not measured.
- **“24× residual amplification.”** Raising \(R^2\) from 0.974 to 0.998 corresponds to roughly a 13× reduction in unexplained variance, not “24× residual amplification,” absent additional unstated calculations.

## 4) Competitive Realism Check

Relative to accepted ICLR interpretability papers, the study has above-average breadth: multiple model families, controlled prompt generation, probing, geometric analysis, logit lens, targeted adaptation, generation evaluation, and several controls. A clean version could plausibly meet the poster bar without needing frontier-model dominance or universal SOTA.

The central weaknesses, however, are worse than typical accepted-paper limitations. Accepted papers can be synthetic, narrow, or incomplete, but their headline tables usually have traceable protocols and internally consistent numbers. Here, the reader cannot reliably determine which baseline, repair result, DPS result, or decoding mode supports the abstract’s claims.

Two reviewers could plausibly score the paper at 5 or higher because the phenomenon is interesting and the experimental program is broad. Two other reviewers could just as reasonably score it 3–4 because the evidence cannot presently be audited. This is therefore not decision-stable in its current form.

## 5) Weakest Link Analysis

**Weakest link:** the inability to reconcile the headline results with their evaluation protocols.

This issue is most likely to flip the decision because it affects the central empirical claims rather than a peripheral extension. The paper may contain a real and interesting effect, but the supplied tables do not yet establish which numbers correspond to the claimed phenomenon.

- **Addressable in revision:** Yes, if the authors have preserved raw logs and configurations.
- **Fundamental:** Not currently demonstrable; the underlying hypothesis may survive.
- **Unlikely to change the outcome:** No. Without reconciliation and reproducibility details, rejection is substantially more likely than acceptance.

## 6) Convergence Test

**If the authors made no further changes, would this have at least a 50% acceptance chance at ICLR? No.** I would estimate its current acceptance probability below 50%, primarily because the core quantitative results are not internally traceable.

The minimal evidence-based changes most likely to move it above the threshold are:

1. **Perform a complete numerical audit.**  
   Give every headline result a unique configuration identifier covering prompts, model checkpoint, probe layer, intervention, argmax scope, decoding mode, scorer, train/test split, and seeds. Reconcile the 13.7/11.3/38.8 baseline values, the 60.7/93.8 repair values, and the 13.2/96.3 soft-DPS values.

2. **Establish the representation at the output-read position.**  
   Report direct last-token probe \(R^2\), MAE, rounded accuracy, and per-count errors; add a causal ablation or activation intervention showing that this representation influences the count computation.

3. **Make the causal controls comparable.**  
   Evaluate nine-row repair, alternative-row repair, LoRA loci, a final-layer linear head, full fine-tuning, and DPS under one primary protocol with identical data and seeds.

4. **Report LoRA’s trade-offs.**  
   Include post-intervention general-capability measurements and per-task generation results, with confidence intervals.

5. **Remove or substantiate unsupported claims.**  
   Either provide GSM8K, CoT, full locus-ablation, and scaling data or narrow the corresponding claims.

If these changes validate the current qualitative story, the paper could plausibly rise to a 5–6.

## 7) Structural Sharpness & Scope Control

The paper is nominally centered on one contribution—the representation–output gap—but it accumulates several secondary claims that introduce avoidable attack surfaces.

### Strengthens the core argument

- Factorial synthetic entity-counting design.
- Probe versus logit-lens comparison.
- Nine-row repair with shuffled-row and random-position controls.
- Direct generation-mode evaluation.
- Full-vocabulary versus digit-restricted decoding.
- Vocabulary-rank measurements.
- Replication across Qwen, Mistral, and Pythia.
- MMLU as a preliminary negative control.

### Neutral or secondary

- DPS is useful as a diagnostic but should not be treated as independent causal confirmation of probe-round.
- Character counting, addition, and list length are useful transfers, although addition’s 93.3% baseline makes it a weak example of a failure.
- Instruct-mode and natural-language extensions are potentially valuable but need fuller methods.

### Introduces new attack surface

- The gradient fixed-point explanation.
- The broad “how to fix it” framing.
- The “deployable” LoRA claim.
- The GSM8K claim without reported results.
- The CoT discussion without a directly reported controlled comparison.
- The 14B scaling conclusion based on a combined intervention.
- Majority vote, max extraction, DROP, and multi-digit counting without enough detail to independently assess each.
- The claim that entity-only runs prove the LoRA variance is a task-mix artifact.

### Recommended scope reduction

Make synthetic entity counting plus one or two fully audited transfer tasks the main paper. Move majority vote, max extraction, DROP, multi-digit counting, and possibly instruct-mode results to an appendix unless each receives the same protocol detail as the primary task. Remove the theoretical fixed-point and deployment language unless substantially stronger evidence is added. This would concentrate reviewer attention on the strongest mechanistic evidence rather than on peripheral claims.

## 8) ICLR Formal Scores

- **Soundness: 2/4** — The general methodology is plausible and includes useful controls, but internally inconsistent headline numbers, incomplete probe localization, and causal overreach prevent the central claims from being fully supported.

- **Presentation: 2/4** — The high-level narrative is clear and the paper is well organized, but the proliferation of incomparable protocols, missing training details, and conflicting table labels make the results difficult to audit or reproduce.

- **Contribution: 3/4** — The geometric readout framing and minimal output-row localization are a worthwhile combination of known interpretability tools, though the individual methods are not new.

- **Significance: 3/4** — If validated, the finding would be memorable and useful for diagnosing competence–performance gaps, but its present impact is bounded by synthetic tasks, task-specific training, and unresolved evidence concerns.

- **Overall: 4/10** — **Borderline reject.** The paper has a promising mechanistic thesis and substantial experimental breadth, but the core quantitative evidence is not currently reliable enough for acceptance.

- **Confidence: 3/5** — I am fairly confident in the main concerns. Confidence is limited because the figure files, bibliography, training configurations, and raw result logs were not available.

## 9) Final Recommendation

**ICLR: Borderline Reject (4/10).**

This is a promising and potentially publishable mechanistic study with a clear hypothesis and several strong forms of evidence. In its current form, however, incompatible headline numbers and opaque evaluation protocols prevent reviewers from verifying the central representation–readout claim. A rigorous numerical audit and a smaller set of fully comparable causal experiments could make this a credible poster, but the present version is more likely than not to be rejected.