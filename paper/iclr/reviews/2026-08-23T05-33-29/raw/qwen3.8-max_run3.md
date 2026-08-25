⚠ **DESK-REJECT RISK**

- **Anonymity:** No obvious anonymity violation in the provided manuscript. Authors are listed as anonymous, and I do not see self-identifying repository links, acknowledgments, or explicit “our prior work” phrasing.
- **Page limit:** Cannot be verified from the provided LaTeX source. The main text plus multiple tables may be close to or beyond the 9-page main-text limit once compiled. Authors should ensure that all core evidence is in the main text and that the main PDF satisfies the page limit.
- **AI use statement:** Present.
- **Style file:** The source uses `\usepackage{iclr2027_conference}`, which appears consistent with the requirement, but I cannot verify from the provided material whether this is the official ICLR 2027 template. The source comment says “NeurIPS 2026 style,” which should be removed to avoid confusion.

---

## 1) Core Thesis & Significance

The paper argues that transformer language models often fail at simple counting tasks not because they lack an internal representation of the count, but because the internal count representation is geometrically misaligned with the output embedding rows corresponding to digit tokens. Using linear probes, the authors claim that counts are nearly perfectly decodable from hidden states, while the probe directions have near-zero cosine similarity with the `lm_head` digit rows. They then intervene by repairing only the digit rows, by bypassing the output head with probe-based logit steering, and by applying LoRA to attention Q/V weights. The main empirical conclusion is that a localized readout bottleneck explains constrained counting failures, while unconstrained generation also requires upstream routing corrections.

The problem is practically relevant and scientifically interesting. Counting is a simple, transparent capability, and failures on it are easy to demonstrate and interpret. The paper’s framing — “the model knows the count but cannot read it out through the digit tokens” — is clear, memorable, and likely to attract attention from the interpretability and model-editing communities.

The novelty is primarily integration-level rather than method-level. Linear probing, logit lens, logit steering, and LoRA are all existing tools. The contribution is the way these tools are combined to produce a causal story: probe evidence shows internal information, cosine/logit-lens evidence shows poor output alignment, and targeted repairs show that intervening at the output head or upstream routing changes behavior. A reviewer can summarize the contribution unambiguously: counting failure is diagnosed as a geometric readout bottleneck and partially repaired by targeted interventions.

---

## 2) Technical Soundness

The paper is technically ambitious and presents a relatively coherent mechanistic narrative. However, several issues affect confidence in the central claims.

### Strengths

- The paper does not rely on a single diagnostic. It combines probes, cosine alignment, logit lens, hard/soft logit steering, output-row repair, and LoRA.
- It includes controls such as random directions, shuffled rows, equivalence testing, and negative-control benchmarks.
- The distinction between constrained next-token evaluation and autoregressive generation is important and, for the most part, carefully handled.
- The observation that a tiny output-head repair can fix constrained decoding but not free generation is a useful causal finding.

### Significant concerns

#### (b) Probe-weight cosine may not establish the intended geometric claim

The central geometric evidence is that the linear probe direction for count is nearly orthogonal to digit rows in `lm_head`. This is intuitively appealing, but probe weight vectors are not necessarily the unique or most meaningful representation of a concept in hidden space. In high-dimensional residual streams, many different linear probes can achieve similar decoding performance, especially when the relevant signal lies in a low-dimensional subspace or when covariance structure is nontrivial. The weight vector of a ridge probe, LDA, or PCA-based probe can depend strongly on regularization, class frequencies, and covariance.

Therefore, near-zero cosine between a probe weight vector and digit rows does not automatically prove that the model’s count representation is unavailable to the output head. A more robust test would examine alignment with the **digit-row subspace** rather than with individual digit rows. For example:

- project the count direction onto the span of the digit rows and measure retained decodability;
- compare against random subspaces of matched dimensionality;
- use canonical correlation or centered kernel alignment between the count-decoding subspace and the digit-row subspace;
- construct count-discriminating directions from pairwise digit-row contrasts rather than individual row cosines.

The paper does mention multiple probe types, but the core claim would be much stronger if it were formulated at the subspace level rather than through individual cosine similarities.

#### (b) The readout position matters: entity-mean vs. last-token

The output head reads from the final token position at generation time, but many probe results are reported at the “entity-mean” position. The paper does discuss last-token logit-lens behavior, but the evidence would be stronger if it systematically reported:

- probe accuracy at the final answer token position;
- count-direction alignment with digit rows at that same position;
- how count information moves from entity positions to the final token position;
- whether LoRA Q/V specifically improves this transfer.

As written, the story oscillates between “the output head cannot read the count” and “upstream routing fails to bring the count into an output-readable position.” These are related but distinct failures. If the final-token hidden state does not contain a clean count representation, then the bottleneck is not purely at the output head. The LoRA Q/V result actually suggests that upstream routing is a major part of the problem. The paper acknowledges this, but the core “output-head bottleneck” framing could be tightened.

#### (b) The causal role of orthogonality is plausible but not fully proven

The paper offers a training-dynamics explanation: digit rows are trained mostly on non-counting contexts, so they become orthogonal to count directions, and orthogonality becomes a stable fixed point because gradients along the count direction vanish. This is a reasonable hypothesis, but the evidence is mostly correlational. The fine-tuning experiment showing a 3.2× increase in cosine after counting fine-tuning is suggestive, but the absolute cosine remains small, and the causal chain is not fully isolated. A stronger version would manipulate the training distribution of digit tokens and show predictable changes in alignment and behavior.

#### (b) Protocol heterogeneity weakens the inferential clarity

The paper is unusually transparent about protocol differences, but the number of distinct evaluation regimes is high. For example, the 9-row repair appears as 60.7%, 93.8%, and 99.9% depending on protocol. The authors explain that these correspond to different modes, seeds, templates, and scoring rules, but this makes it difficult to form a stable impression of the method’s robustness. A reader must constantly check which protocol supports which claim. This is not necessarily fatal, but it increases the chance that a reviewer will interpret the results as fragile or selectively reported.

### Classification of issues

- **Fatal flaw:** None that alone clearly invalidates the paper.
- **Significant concerns:** Probe-direction geometry, final-token readout analysis, protocol heterogeneity, and incomplete isolation of LoRA’s mechanism.
- **Typical limitations:** Synthetic task emphasis, limited scale range, imperfect generation-mode repair, and narrow task scope.

---

## 3) Empirical Rigor

The empirical work is substantial. The paper evaluates multiple models, multiple tasks, multiple intervention types, and multiple evaluation modes. It also includes useful negative controls. That said, some empirical choices limit confidence.

### Are the experiments sufficient to support the core claim?

Mostly, but not completely. The evidence is strongest for the following chain:

1. Counts are decodable from hidden states.
2. The model’s natural digit-token output is poor.
3. Repairing digit rows helps constrained next-token prediction.
4. LoRA Q/V helps autoregressive generation.
5. Logit-lens rank improves after intervention.

This is a persuasive pattern. However, the core claim that the failure is specifically a **geometric readout bottleneck** would benefit from more direct geometric measurements at the actual generation readout position and from subspace-level alignment tests.

### Are baselines appropriate and fair?

The internal baselines are generally appropriate: unrepaired model, probe-round upper bound, hard DPS, soft DPS, digit-row repair, full-vocabulary repair, and LoRA. The paper also includes random-direction and shuffled-row controls.

However, several useful comparisons are missing or underdeveloped:

- A chain-of-thought or scratchpad baseline under the exact same final-integer scoring protocol is discussed but not presented with the same rigor as the main interventions.
- LoRA ablations across Q/K/V/O and MLP are mentioned, but the main text would be more convincing with a compact table showing those comparisons.
- A parameter-matched control for LoRA Q/V would help. For example, applying the same rank and parameter budget to other projections or to a non-targeted subset of layers.
- The paper would benefit from a simple baseline that combines digit-row repair with logit masking or constrained decoding, since that appears to be the most practical low-cost fix.

### Are trade-offs quantified?

Partially. The paper distinguishes constrained decoding from generation and notes that 9-row repair is cheap but does not fix free generation. It also notes that LoRA requires fine-tuning but adds no inference-time cost. The parameter counts are given. However, the practical trade-off is still somewhat unclear:

- 9-row repair: very small, but only works under constrained decoding.
- Hard DPS: diagnostic, not deployable.
- LoRA Q/V: deployable but requires fine-tuning and still does not reach the probe-round ceiling.
- CoT: likely no fine-tuning but increases inference cost; not quantitatively centralized.

A clearer table mapping intervention → parameters → training required → inference overhead → constrained accuracy → generation accuracy would improve the paper.

### Overclaiming check

There are a few places where the language is stronger than the evidence:

- The title, “Why Transformers Fail at Counting and How to Fix It,” is broad. The evidence is mostly about decoder-only transformers in the 0.4B–14B range on low-vocabulary aggregation tasks, often synthetic.
- “The model knows the count” is a useful shorthand, but it risks overstating the result if the clean count representation is not always available at the final generation position.
- Claims about generalization across tasks are promising but rest on a small set of related aggregation tasks. Addition, list length, character counting, and entity counting share a low-vocabulary aggregate-answer structure.
- The negative-control conclusion for MMLU and GSM8K is interesting, but the evidence is not as deep as for counting. It should be framed as suggestive rather than definitive.

These are not fatal, but they should be softened.

---

## 4) Competitive Realism Check

Compared with typical ICLR-accepted interpretability papers, this manuscript has several favorable features:

- a clear behavioral failure;
- a mechanistic hypothesis;
- multiple diagnostic methods;
- intervention-based validation;
- cross-model evidence;
- negative controls;
- a memorable conceptual framing.

These are qualities that often lead to acceptance. The paper is not merely a probing paper; it attempts causal localization and repair. That is valuable.

However, the paper also has vulnerabilities that are common in interpretability work:

- reliance on probe geometry that may not be uniquely defined;
- possible conflation of representation, routing, and formatting failures;
- heavy dependence on synthetic tasks;
- multiple evaluation protocols that make headline numbers harder to interpret.

Are these weaknesses worse than average? I do not think they are clearly worse than the weaknesses of many accepted mechanistic-interpretability papers. But they are significant enough that the paper is not a clean accept as written. A reviewer sympathetic to mechanistic interpretability may score it 6; a reviewer focused on probing validity and protocol consistency may score it 4. Thus, the paper is in the acceptance variance zone.

Would at least two reasonable reviewers likely score this ≥5? Yes, I think that is plausible. One reviewer may value the diagnostic story and interventions highly. Another may worry about the probe-geometry inference and the fragmented protocol. The outcome would likely depend on rebuttal quality.

---

## 5) Weakest Link Analysis

The single issue most likely to flip accept/reject is the **inferential bridge from probe decodability to output-head orthogonality**.

The paper’s central claim is not merely that probes can decode counts. It is that the model’s count representation is present but geometrically inaccessible to digit-token output rows. The main evidence for that claim is cosine similarity between probe directions and digit rows. If a reviewer believes that probe weight vectors are not valid stand-ins for the model’s internal count direction, the central story weakens substantially.

This issue is:

- **decision-relevant**, because it concerns the core mechanism;
- **addressable in revision**, because the authors can add subspace alignment analyses, final-token probes, contrast-direction analyses, and additional causal checks;
- **not obviously fundamental**, because the intervention results still provide meaningful evidence even if the cosine argument is weakened.

If the authors can show that count information is decodable at the final token position, that the count-decoding subspace has low projection into the digit-row span, and that repairing or routing into that span improves behavior, the paper would be much stronger.

---

## 6) Convergence Test

If the authors made no further changes, I would estimate the acceptance chance as borderline, roughly in the 45–55% range. It is not clearly below the ICLR bar, but it is also not robustly above the bar. The paper could be accepted if assigned to reviewers who value the mechanistic narrative and intervention evidence, but it could also be rejected if reviewers focus on probe validity and protocol fragmentation.

The minimal change most likely to push it over the threshold is not editorial but evidential:

1. Add a dedicated geometric-validation analysis that measures alignment between the count-decoding subspace and the digit-row subspace, not only individual cosine similarities.
2. Report probe accuracy and alignment at the actual final-token generation position, with a clear account of how count information is transferred there.
3. Consolidate the headline results around one primary protocol, with other protocols moved to the appendix and explicitly labeled as secondary.
4. Include a compact LoRA ablation table in the main text comparing Q/V with K/O, MLP, and parameter-matched controls.

Those changes would directly address the most likely reviewer objections and would make the central causal claim much harder to dismiss.

---

## 7) Structural Sharpness & Scope Control

The paper is centered on one dominant contribution: counting failure as a geometric readout bottleneck. This is good. The narrative is not diffuse in its core objective.

### Content that strengthens the paper

- Probe evidence showing near-perfect count decodability.
- Cosine and logit-lens evidence connecting internal representations to output behavior.
- The 9-row `lm_head` repair as a minimal causal diagnostic.
- The contrast between constrained next-token success and free-generation failure.
- The LoRA Q/V intervention showing that generation can be improved.
- Negative controls on MMLU/GSM8K, if framed cautiously.

### Neutral content

- Some of the extended appendix protocol details are necessary but do not directly strengthen the main argument.
- The discussion of soft DPS under different protocols is technically informative but may confuse readers because the result changes dramatically across settings.

### Content that introduces attack surface

- Broad claims about “Transformers” in the title.
- Claims of generalization across tasks and scales when the strongest evidence is concentrated in a few models and synthetic tasks.
- The comparison to chain-of-thought without a fully harmonized table.
- The large differences between 9-row repair results under different protocols.
- The use of “bottleneck” for a phenomenon that partly involves upstream routing and formatting.

### Recommended scope reductions

The paper would be sharper if it explicitly framed the contribution as:

> In several decoder-only transformer families, low-vocabulary counting failures are partly caused by a geometric mismatch between internal count representations and digit-token output rows; fixing the output rows repairs constrained decoding, while repairing free generation also requires upstream routing changes.

That version of the claim is more defensible than a broad “Transformers fail at counting and we fix it” claim.

I would also recommend:

- making entity counting the primary task and treating other tasks as extensions;
- presenting the 9-row repair primarily as a diagnostic tool, not as a practical fix;
- moving the single-seed soft DPS result to the appendix and clearly separating it from the unified multi-seed results;
- reducing rhetorical emphasis on “orthogonality” unless supported by subspace-level analyses.

---

## 8) ICLR Formal Scores

**Soundness: 3**  
The paper presents a plausible and empirically supported mechanism, but the central geometric claim depends on probe-direction interpretations that are not fully robust, and the distinction between output-head misalignment, upstream routing, and formatting failure could be sharper.

**Presentation: 3**  
The paper is generally clear and well organized, and the authors are commendably explicit about protocols. However, the multiplicity of evaluation regimes and the large differences between similarly named results make the paper harder to assess than it needs to be.

**Contribution: 3**  
The readout-bottleneck diagnosis is a useful conceptual contribution, and the targeted repairs are interesting. The methods themselves are mostly existing tools, but their combination is meaningful.

**Significance: 3**  
The finding is likely to interest interpretability and model-editing researchers. Practical impact is currently limited to constrained low-vocabulary tasks and imperfect generation-mode repairs, but the diagnostic framework could be influential if generalized.

**Overall: 5**  
This is a borderline-accept paper. It has a clear idea, substantial experiments, and a memorable mechanistic claim, but it also has meaningful soundness concerns that prevent a confident accept. With stronger geometric validation and cleaner protocol consolidation, it would be a clearer poster.

**Confidence: 3**  
I am fairly confident in the assessment of the methodology and the venue fit, but I did not rerun the experiments or inspect the full supplementary code and data.

---

## 9) Final Recommendation

**ICLR: Borderline Accept**

The paper presents an interesting and well-developed mechanistic account of counting failures: models may internally represent counts but fail to express them because the relevant representation is poorly aligned with digit-token output rows. The combination of probing, logit-lens analysis, targeted output-head repair, and LoRA-based routing correction makes the paper stronger than a purely observational interpretability paper. However, the central geometric evidence relies heavily on probe-direction cosines, the final-token readout story could be more direct, and the multiple evaluation protocols make the results appear less stable than they may actually be. As written, the paper is acceptable only borderline; a revision adding subspace-level geometric validation, final-token analysis, and a unified primary evaluation would substantially improve its chances.