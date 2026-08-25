## Review: *Why Transformers Fail at Counting and How to Fix It*

Below is a detailed review of the provided LaTeX manuscript. I evaluate both the scientific content and the manuscript preparation issues. Because the figures and `references.bib` are not included, I cannot fully verify compilation, citation correctness, or the visual evidence.

---

# 1. Summary

The paper studies why large language models fail at simple counting tasks even when the items to be counted are explicitly present in the prompt. The authors propose a two-stage explanation: either models do not internally represent the count, or they represent it but fail to map that representation to the correct output token. Using linear probes, logit lens, cosine-alignment analysis, and targeted interventions, the paper argues that the failure is primarily a *geometric readout bottleneck*: count information is linearly decodable from hidden states, but the corresponding direction is nearly orthogonal to the language-model head rows for digit tokens.

The main empirical claims are:

1. Linear probes recover counts from intermediate hidden states with very high accuracy, often \(R^2 > 0.99\).
2. The count-encoding direction is nearly orthogonal to the unembedding rows for digit tokens, with small cosine similarity.
3. Repairing only the digit rows of the LM head improves constrained next-token digit prediction but does not fix unconstrained autoregressive generation.
4. A LoRA intervention on attention Q/V weights improves generation accuracy, which the authors interpret as correcting upstream routing.
5. The phenomenon generalizes across several low-vocabulary aggregation tasks, but not to broader multi-step benchmarks such as MMLU and GSM8K.

The paper is ambitious, mechanistically motivated, and addresses an important failure mode of LLMs. However, the current manuscript suffers from substantial protocol inconsistencies, unclear evaluation definitions, missing methodological details, and several overclaimed causal interpretations. In its present form, I would classify it as a **major revision / borderline reject**. The core idea is strong enough that a carefully revised version could become a solid submission.

---

# 2. Overall Assessment

The central scientific question is compelling: *Do transformers fail to count because they lack the internal count, or because they cannot express it?* This is a clean and useful decomposition. The paper brings an impressive battery of methods to bear on the question: probing, logit lens, geometric alignment, targeted output-head repair, logit steering, and LoRA-based intervention. The combination of observational and interventional evidence is the paper’s strongest feature.

However, the execution is currently undermined by several serious issues:

1. **Multiple inconsistent evaluation protocols and numbers.**  
   The paper reports many different baseline and repair accuracies for the same model and task under slightly different protocols. While the authors include a “How to read the numbers” paragraph, the current presentation is still confusing and creates the impression of selective reporting.

2. **Unclear generation scoring.**  
   The claim that the 9-row repair achieves 0.0% in generation is difficult to reconcile with the reported full-vocabulary next-token accuracy of 60.3%. This suggests that the generation scoring protocol may be penalizing correct direct answers because of continuation tokens, stopping behavior, or final-integer extraction. This needs to be clarified and possibly re-scored.

3. **Probe interpretation is too strong.**  
   The phrase “the model knows the count” is too anthropomorphic and too strong given the evidence. A linear probe can decode information that may not be causally used by the model, especially on synthetic distributions. More controls are needed to rule out surface shortcuts.

4. **The geometric claim relies heavily on cosine alignment.**  
   Cosine similarity between a single probe direction and digit-token rows is suggestive but not sufficient to establish a readout bottleneck. The paper should analyze digit-row differences, low-dimensional count subspaces, and the effect of moving hidden states along count directions.

5. **The LoRA Q/V intervention is not sufficiently isolated.**  
   LoRA may improve instruction following, stopping behavior, formatting, attention aggregation, or general routing. The paper needs stronger controls to show that the improvement is specifically due to correcting the geometric bottleneck rather than improving format compliance.

6. **Missing implementation details.**  
   The manuscript lacks enough detail to reproduce the benchmark, probes, DPS, 9-row repair, and LoRA intervention. Hyperparameters, prompt templates, tokenizer behavior, stopping criteria, and scoring regexes are not fully specified.

7. **The title and abstract overgeneralize.**  
   The evidence is strongest for synthetic or semi-synthetic low-vocabulary aggregation tasks with single-digit answers. The title “Why Transformers Fail at Counting” is too broad unless the authors substantially qualify the scope.

The paper has a valuable core contribution, but the current version is not yet robust enough for acceptance at a top venue.

---

# 3. Strengths

## 3.1 Clear and useful mechanistic hypothesis

The paper’s main conceptual contribution is the distinction between:

- **Representation failure:** the model does not encode the count internally.
- **Readout failure:** the model encodes the count but cannot map it to the correct output token.

This is a clean, testable decomposition. It is also relevant to broader questions in interpretability, such as “competence without performance” and hidden capabilities that are not expressed in greedy decoding.

## 3.2 Multi-method evidence

The paper does not rely on a single diagnostic. It combines:

- linear probing,
- logit lens,
- cosine alignment with LM head rows,
- targeted LM-head repair,
- logit steering,
- LoRA intervention,
- negative controls on MMLU/GSM8K,
- cross-task and cross-model checks.

This multi-pronged approach is appropriate for a mechanistic claim.

## 3.3 Causal interventions

The inclusion of interventions is a major strength. Observational probing alone would not be enough. The 9-row LM-head repair, hard DPS, and LoRA Q/V intervention provide causal evidence at different levels of the computation graph.

The 9-row repair is especially interesting because it is a minimal intervention: changing only the output rows corresponding to digits. If it works under constrained decoding, that is meaningful evidence that part of the failure lies at the readout stage.

## 3.4 Useful negative-control intuition

The paper correctly identifies that the proposed bottleneck should be specific to tasks where an internal aggregate must be mapped to a small set of output tokens. Testing MMLU and GSM8K as negative controls is a good idea.

## 3.5 Practical relevance

Counting failures are practically important for agentic systems, retrieval-augmented generation, code generation, tool use, and structured output generation. Even if the tasks studied here are synthetic, the underlying issue — models possessing information but failing to emit it in the required format — is broadly relevant.

---

# 4. Major Concerns

## 4.1 Inconsistent evaluation protocols and confusing numbers

This is the most serious presentation and soundness issue.

The manuscript reports many different numbers for what appears to be the same basic setting: Qwen3-8B entity counting. Examples:

### Baseline differences

The paper reports baseline entity-counting accuracies including:

- 13.7% in Table 1, digit-restricted next-token.
- 11.3% in Table 4, intervention comparison.
- 10.3% in Appendix Table 6, single-seed DPS protocol.
- 38.8% / 38.6% in the caption of Figure 3.

Even allowing for different seeds, templates, and modes, this is difficult to follow. The reader cannot easily tell which baseline should be considered the primary one.

### 9-row repair differences

The 9-row repair appears with several different values:

- 60.7% in Table 1, unified multi-seed digit-restricted next-token.
- 93.8% in Table 4, described as single-seed train/held-out split.
- 99.9% in instruct mode.
- “93–99% held-out” in the Discussion.

The explanation that these correspond to different protocols is present, but the paper still gives the impression of cherry-picking favorable numbers. The headline claim in the abstract is “60.7–100.0% across four tasks,” but later the discussion emphasizes 93–99%. This is confusing.

### Full-vocabulary next-token versus generation

Table 1 reports:

- 9-row repair, full-vocabulary next-token: 60.3%.
- 9-row repair, greedy generation: 0.0%.

This is a major inconsistency. If the repaired model chooses the correct digit under full-vocabulary next-token prediction 60.3% of the time, why is greedy generation accuracy exactly 0.0%? The most likely explanation is that the generation scoring penalizes outputs that begin correctly but continue with additional tokens, or that stopping behavior is not handled properly. This must be clarified.

### Recommendation

The paper needs a single primary evaluation protocol for each claim. I recommend:

1. Choose one unified protocol for entity counting.
2. Use the same prompts, seeds, tokenizer, stopping criteria, and scorer.
3. Report all main methods under that protocol in one table.
4. Move alternative protocols to the appendix and label them clearly as secondary.
5. Avoid quoting different numbers for the same method in the abstract, main text, and discussion unless the protocol is explicitly stated each time.

Without this consolidation, the empirical claims are hard to evaluate.

---

## 4.2 Generation scoring may conflate counting failure with formatting failure

The paper emphasizes “true greedy autoregressive generation” and scores the **final integer emitted**. This is understandable for chain-of-thought outputs, where scoring the first integer can inflate accuracy. However, for direct-answer interventions, scoring only the final integer can be excessively harsh.

Consider a model that outputs:

```text
3
```

This should be correct.

But if it outputs:

```text
3.
```

or

```text
3 apples
```

or

```text
3, as requested
```

and there is another integer later, scoring the final integer may mark it wrong even though the model produced the correct count immediately.

Given that the 9-row repair achieves 60.3% full-vocabulary next-token accuracy but 0.0% generation accuracy, it is likely that the model often produces the correct digit initially but then continues with additional tokens. If so, the 0.0% number may not reflect a counting failure or even a readout failure, but a **stopping/formatting failure**.

This matters because the paper’s second core claim is that repairing the digit rows fixes constrained decoding but not generation. That claim would be much stronger if the authors separated:

- **first-token digit accuracy**,
- **exact-match accuracy after trimming**,
- **accuracy when generation is stopped after the first digit**,
- **accuracy when a digit is produced anywhere in the response**,
- **final-integer accuracy**,
- **format failure rate**.

The current presentation conflates these.

### Recommendation

For generation, report at least:

| Metric | Definition |
|---|---|
| First-token digit accuracy | First generated token is the correct digit. |
| First-integer accuracy | First integer extracted from the response is correct. |
| Final-integer accuracy | Final integer extracted is correct. |
| Exact-match accuracy | Response after whitespace/punctuation stripping exactly matches the answer. |
| Any-digit accuracy | Any integer token in the response matches the answer. |
| Format failure rate | No integer produced, too many tokens, or invalid format. |

Then the paper can distinguish whether an intervention fixes counting but not formatting, or fixes both.

This is essential for the claim that the 9-row repair fails in generation.

---

## 4.3 Linear probes may overstate that the model “knows” the count

The paper repeatedly says that the model “knows” the count. The evidence is that linear probes achieve high \(R^2\). This is suggestive, but the claim is too strong.

A linear probe can decode information that is:

- present but not used by the model,
- correlated with surface features,
- artifactually introduced by the synthetic template,
- accessible only because of the probe’s access to multiple token positions or averaging,
- present in a subspace not aligned with the model’s actual computation.

The paper includes shuffled-label probes and random-direction controls, which is good. But more controls are needed.

### Specific concerns

#### Layer 0 probe accuracy is suspiciously high

Table 2 reports layer 0 \(R^2 = 0.977\). If the count is not yet computed at layer 0, how is the probe recovering it?

Possible explanations:

- the probe is reading the number of entity token embeddings,
- the prompt template encodes count information lexically,
- the entity-mean position is constructed in a way that makes counting trivial,
- the probe uses positional or delimiter statistics,
- the synthetic benchmark has residual correlations.

The paper should explain what information is available at layer 0.

#### “Entity-mean position” is not clearly defined

The phrase “entity-mean position” appears repeatedly, but the exact definition is not clear.

Is it:

- the mean of hidden states at entity mention positions?
- the hidden state at the final entity mention?
- a special aggregated position?
- the last token of the prompt?
- an average over all target-entity tokens?

This is crucial. If the probe averages over entity mentions, then the count may be trivially recoverable from the number of vectors being averaged, depending on implementation.

#### Probe direction may not correspond to a causally used representation

A high-accuracy probe does not prove that the model uses that representation for its next-token prediction. The paper partially addresses this with interventions, but the probing claim itself should be stated more cautiously.

### Recommendation

The paper should include:

1. A precise definition of the probe input representation.
2. A description of which token positions are used.
3. Controls where entity mentions are replaced, shuffled, or masked.
4. Held-out entity types and templates, with separate results.
5. A layer-0 analysis explaining what information is available before computation.
6. A probe trained to predict the model’s own output token, not only the ground-truth count.
7. A comparison between probe direction and causal activation-patching directions.

The phrase “the model knows the count” should be softened to something like:

> A linear probe can recover the count from intermediate hidden states with high accuracy.

---

## 4.4 Cosine alignment with digit rows is not sufficient to establish a readout bottleneck

The paper’s geometric claim is that the count direction is nearly orthogonal to the LM-head rows for digit tokens. This is an interesting observation, but the inference from low cosine to “readout bottleneck” requires more support.

### Issues

#### 1. The LM head reads out differences between rows

For a linear unembedding, the logit for token \(t\) is roughly:

\[
z_t = w_t^\top h
\]

The decision between digit tokens depends on differences such as:

\[
z_i - z_j = (w_i - w_j)^\top h
\]

Therefore, the relevant question is not only whether the count direction aligns with individual digit rows, but whether it aligns with the **subspace spanned by differences between digit rows**.

A count direction could have low cosine with each individual row but still be decodable from pairwise row differences. Conversely, a direction could align moderately with rows but not produce useful digit discrimination.

The paper should analyze:

- alignment with \(w_i - w_j\),
- alignment with the subspace spanned by digit rows,
- alignment with the subspace spanned by digit-row differences,
- canonical correlation between the count subspace and digit-token subspace,
- linear separability of counts after projection through the LM head.

#### 2. The probe direction may not be the relevant count subspace

The probe direction is the weight vector of a ridge regression probe. But the count representation might be multidimensional. A single direction may not capture the full geometry.

The paper mentions four probe types, which is helpful, but it would be stronger to define a count subspace using multiple class-mean directions or principal components.

#### 3. Low cosine may be expected in high dimensions

In a 4096-dimensional space, random unit vectors often have cosine magnitude around \(1/\sqrt{d}\), which is approximately 0.0156. The reported mean cosine of 0.016 is therefore close to random. This supports the orthogonality claim, but the paper should explicitly compare against the theoretical high-dimensional random baseline, not only sampled random vectors.

#### 4. Causal manipulation along the count direction is needed

A stronger test would be:

- take a hidden state,
- add or subtract the probe direction,
- observe the change in digit logits,
- check whether the change matches the predicted count change.

If the count direction is causally irrelevant to digit logits, moving along it should not change digit logits. If it does change digit logits after repair, that would support the bottleneck story.

### Recommendation

Add a dedicated subsection titled something like:

> Geometric relationship between count subspace and digit-token unembedding subspace

and report:

1. Cosine with individual digit rows.
2. Cosine with digit-row differences.
3. Projection variance into the digit-row subspace.
4. CKA or linear decoding accuracy from LM-head logits.
5. Logit changes when adding the count direction to hidden states.
6. Results before and after 9-row repair.

This would make the geometric claim much more convincing.

---

## 4.5 The 9-row repair is a useful diagnostic but its interpretation is not fully clean

The 9-row repair is one of the paper’s most interesting interventions. However, its interpretation is complicated.

### Concern 1: Fine-tuning the digit rows may learn a new shortcut

Updating the digit rows on counting prompts may not simply “align” them to a pre-existing count direction. It may learn a new mapping that exploits prompt-specific features. This is not necessarily bad, but it weakens the claim that the repair merely fixes a geometric misalignment.

### Concern 2: The repair works well under constrained decoding but not generation

This could mean:

- the output head is fixed but upstream computation is not,
- the repair does not fix formatting or stopping,
- the generation scorer is too strict,
- the repaired rows are still dominated by non-digit tokens in full autoregressive contexts,
- the hidden state distribution shifts after the first generated token.

The paper should distinguish these possibilities.

### Concern 3: The 60.7% versus 93.8% gap is not adequately explained

The unified protocol gives 60.7%, while the single-seed train/held-out split gives 93.8%. This is a very large difference. The paper attributes it to protocol differences, but this needs a more careful explanation.

Possible causes:

- different prompt templates,
- different answer positions,
- different digit-restriction rules,
- different train/test splits,
- seed variance,
- overfitting,
- evaluation on easier held-out prompts.

The paper should provide a table that directly compares these protocols on the same prompts.

### Concern 4: Full LM-head fine-tuning performs similarly

Table 4 shows full LM-head held-out accuracy of 94.2%, close to the 9-row repair’s 93.8% under that protocol. This weakens the claim that the 9-row repair uniquely localizes the bottleneck. The paper should discuss this more honestly.

### Recommendation

The 9-row repair should be framed as a **minimal diagnostic intervention**, not as definitive proof that the entire failure is localized to the output head. The paper should say:

> Repairing digit rows substantially improves constrained digit prediction, showing that output-side misalignment is sufficient to explain part of the failure. However, unconstrained generation also depends on upstream routing and formatting.

This is close to what the paper already says, but the abstract and introduction should be adjusted to avoid overclaiming.

---

## 4.6 The LoRA Q/V intervention needs stronger controls

The LoRA Q/V result is potentially the most practically important contribution. However, the interpretation that LoRA “corrects upstream routing” is not yet sufficiently supported.

### Possible confounds

#### 1. Instruction-following improvement

LoRA may improve the model’s tendency to answer with a digit rather than produce preamble. This would improve generation accuracy without specifically fixing count routing.

#### 2. Stopping behavior

If the fine-tuned model stops after producing the answer, final-integer accuracy may improve. This is a formatting improvement, not necessarily a counting improvement.

#### 3. General attention changes

LoRA on Q/V may change attention patterns broadly. The improvement may come from better aggregation of entity mentions, better instruction adherence, or reduced distraction.

#### 4. Overfitting to the training distribution

The intervention is trained on counting tasks. It may simply memorize the task family. The paper reports held-out prompts, but more out-of-distribution tests are needed.

#### 5. Catastrophic forgetting

The paper does not sufficiently evaluate whether LoRA Q/V harms general abilities. MMLU and GSM8K are used as negative controls for the bottleneck, but the paper should also report post-LoRA performance on these benchmarks.

### Missing baselines

The paper should compare LoRA Q/V against:

1. LoRA on K/O projections.
2. LoRA on MLPs.
3. LoRA on all projections.
4. Randomly initialized LoRA with the same training budget.
5. Fine-tuning only on formatting, not counting.
6. Digit-logit bias at inference time.
7. Constrained decoding.
8. Chain-of-thought prompting.
9. Self-consistency.
10. Direct fine-tuning of the LM head plus norm adjustment.

The paper mentions a locus ablation, but the main text does not present enough detail. A table with all LoRA variants and their generation accuracies would be very useful.

### Recommendation

The LoRA section should include:

- per-task generation results,
- per-seed results,
- first-token and final-token metrics,
- post-intervention MMLU/GSM8K/DROP results,
- a comparison with CoT,
- a comparison with digit-logit bias,
- an analysis of whether LoRA changes stopping behavior.

Without these, the claim that LoRA Q/V specifically fixes the geometric bottleneck is too strong.

---

## 4.7 The paper lacks sufficient baseline comparisons for “fixing” counting

The title says “How to Fix It,” but the paper does not compare against several simple fixes.

### Needed baselines

#### Constrained decoding

If the task requires a digit, restricting the vocabulary to digits is an obvious baseline. The paper includes digit-restricted next-token evaluation, but it should also include constrained autoregressive generation.

#### Logit bias

Adding a fixed positive bias to digit tokens may be a simple and deployable fix. The paper explores norm rescaling, but a full logit-bias baseline would be useful.

#### Chain-of-thought

The paper discusses CoT but does not provide clear main-table numbers. Since CoT is a standard way to improve counting, it should appear in the main results table.

#### Self-consistency

Sampling multiple CoT traces and majority-voting may further improve accuracy.

#### External tool use

For counting explicitly present items, a regex or external counter is trivial. The paper is not expected to solve practical counting with tools, but mentioning the tool-use baseline would help situate the contribution.

#### Instruction tuning on formatting

If generation failure is partly due to formatting, a small fine-tuning dataset that only teaches “answer with a single digit” could be a strong baseline.

### Recommendation

Add a table like:

| Method | Constrained next-token | Unconstrained generation | Inference overhead | Training required |
|---|---:|---:|---:|---:|
| Baseline | ... | ... | none | no |
| Digit-only decoding | ... | ... | none | no |
| Digit logit bias | ... | ... | none | no |
| CoT | ... | ... | high | no |
| Self-consistency | ... | ... | very high | no |
| 9-row repair | ... | ... | none | yes |
| LoRA Q/V | ... | ... | none | yes |

This would make the practical contribution much clearer.

---

## 4.8 The synthetic benchmark may not generalize to natural counting

The benchmark is carefully constructed, but it is synthetic and low-vocabulary. The paper does test natural-language templates, instruct mode, DROP, majority vote, and max extraction, which is good. However, the strongest results remain on synthetic tasks.

### Concerns

#### Counts are mostly 1–9

This avoids tokenization complications but limits realism. Real counting tasks may involve larger numbers, multi-digit outputs, and non-uniform distributions.

#### Prompts are templated

Even with randomization, templates can create exploitable regularities.

#### The model may not need to perform robust counting

The task may be solvable by shallow pattern matching over entity mentions.

#### DROP improvement is weak

The paper reports that on a single-digit DROP subset, probe-round improves from 20.0% to 30.0%. This is a very small improvement and suggests that the proposed bottleneck does not strongly explain failures on realistic reading-comprehension counting.

### Recommendation

The paper should temper claims about “counting” in general and emphasize:

> low-vocabulary aggregation tasks where the answer is a single digit or small token set.

The abstract and title should reflect this scope.

---

## 4.9 The negative controls are useful but incomplete

The paper uses MMLU and GSM8K as negative controls. This is a good idea, but the evidence is incomplete.

### MMLU

The paper reports:

- baseline MMLU: 70.2%,
- output-row adaptation degrades to 55.6%,
- cosine alignment: 0.31–0.48.

This is informative, but the paper should specify:

- which MMLU subsets were used,
- how answer directions were defined,
- whether answers are single tokens,
- how many examples were used,
- whether the output-row adaptation was trained on MMLU or counting data.

The degradation after output-row adaptation is interesting but could also simply mean that modifying the LM head harms general outputs. It does not by itself prove the absence of a counting-specific bottleneck.

### GSM8K

The abstract says the bottleneck is absent from GSM8K, but the main text provides almost no GSM8K numbers. This should be fixed.

GSM8K answers are often multi-step and multi-digit, so the geometric analysis may not apply cleanly. The paper should explain how GSM8K was used as a control.

### Recommendation

Add a table:

| Benchmark | Probe \(R^2\) or answer decoding | Cosine with answer rows | Effect of output-head repair | Interpretation |
|---|---:|---:|---:|---|
| Entity counting | high | low | improves constrained decoding | bottleneck present |
| MMLU | ... | ... | harms or no improvement | no bottleneck |
| GSM8K | ... | ... | ... | no bottleneck / not applicable |

If GSM8K cannot be cleanly analyzed, remove it from the abstract or qualify it.

---

## 4.10 Statistical reporting needs improvement

The paper reports some means and standard deviations, but statistical reporting is uneven.

### Issues

1. Some headline numbers are single-seed.
2. Some tables report standard deviation, others do not.
3. Some comparisons involve many seeds and tasks, but no significance tests are shown.
4. The per-count table has small sample sizes, e.g. 57–78 examples per count.
5. The logit-lens rank improvement “55,980 to 1” is dramatic, but the paper should report distributions, not only medians.
6. The equivalence test should specify the equivalence margin.
7. The cosine comparison should compare against the theoretical high-dimensional null.

### Recommendation

For all headline claims, report:

- number of seeds,
- number of examples,
- mean,
- standard deviation or bootstrap confidence interval,
- statistical test where appropriate,
- whether differences are significant.

For cosine alignment, report:

- observed mean cosine,
- random-direction baseline,
- theoretical expected cosine for random vectors in that dimension,
- confidence intervals,
- equivalence margin.

For logit ranks, report:

- median,
- interquartile range,
- fraction of examples with rank 1,
- fraction in top 10,
- fraction in top 100.

---

# 5. Concerns About Specific Claims

## 5.1 “Linear probes recover the correct count with near-perfect accuracy”

This is mostly supported by the tables, but the paper should clarify:

- whether probes are trained and evaluated on disjoint prompts,
- whether entity types are held out,
- whether templates are held out,
- whether probe hyperparameters are selected on validation data,
- why layer 0 already has high \(R^2\),
- whether probe accuracy is high because the task is synthetic.

Also, \(R^2\) is not the most intuitive metric for a discrete count. The paper should also report exact count accuracy and mean absolute error.

## 5.2 “The internal directions that encode counts are nearly orthogonal to digit rows”

The cosine evidence is suggestive, but the claim should be strengthened by analyzing digit-row differences and causal logit effects. The paper should also state whether rows were normalized before computing cosine.

## 5.3 “The model stores the count in a form that the digit logits do not naturally read out”

This is plausible, but the paper should show the distribution of digit logits for correct counts. For example:

- logit of correct digit,
- logit gap between correct digit and top token,
- rank of correct digit,
- probability mass assigned to digits.

This would make the claim more concrete.

## 5.4 “Updating only the digit rows fixes constrained decoding”

Supported for some protocols, but the 60.7% versus 93.8% discrepancy needs resolution. The paper should also clarify whether the repair is trained on the same prompts used for testing. If held-out prompts are used, the split should be described precisely.

## 5.5 “The same repair does not fix autoregressive generation”

This is the most suspicious claim because of the 60.3% full-vocabulary next-token result. The paper must explain why generation accuracy is 0.0%. If the issue is final-integer scoring, the claim should be revised.

## 5.6 “LoRA Q/V corrects upstream routing”

This is plausible but not fully proven. The paper should provide more direct evidence, such as:

- attention-pattern changes,
- ablation of specific heads,
- causal mediation analysis,
- comparison with LoRA on other modules,
- post-LoRA logit-lens across layers,
- analysis of whether the count direction itself changes.

The current evidence — increased logit-lens accuracy and reduced vocabulary rank — is consistent with the claim but not definitive.

## 5.7 “The bottleneck generalizes across character counting, addition, and list length”

Partially supported. However:

- addition baseline is already high,
- character counting may depend on tokenization,
- list length may be solvable by reading the last enumerated number,
- the paper should report per-task seed variance.

The generalization claim should be limited to “low-vocabulary aggregation tasks.”

## 5.8 “The bottleneck is absent from broader multi-step reasoning benchmarks”

The MMLU evidence is helpful, but GSM8K is not sufficiently described. The paper should either add GSM8K details or soften the claim.

## 5.9 “Scale strengthens, not refutes, the readout-bottleneck thesis”

The 14B result is interesting, but the paper should include a full table for all scales and models. Currently, the evidence for Pythia and Mistral is sparse in the main text.

---

# 6. Missing Methodological Details

The manuscript should add the following details, ideally in the appendix.

## 6.1 Benchmark generation

- Full prompt templates.
- Entity vocabulary.
- Distractor sentence templates.
- How counts, distractors, lengths, and spacings are sampled.
- How multi-digit prompts are generated.
- Train/validation/test split procedure.
- Held-out entity types and templates.
- Number of examples for each task.

## 6.2 Probe details

- Probe input: which token positions, which layers.
- Definition of entity-mean position.
- Ridge regularization strength.
- How layers were selected.
- Whether probes were trained per task or jointly.
- Cross-validation procedure.
- Whether probes were trained on ground-truth counts or model outputs.
- Probe accuracy on held-out entity types.

## 6.3 Cosine and geometry

- Whether LM-head rows were normalized.
- Which digit tokens were included: `0`–`9` or `1`–`9`.
- How the count direction was extracted.
- How random directions were sampled.
- Equivalence-test margin.
- Whether cosine was computed per layer or averaged.

## 6.4 Logit lens

- Number of prompts.
- Positions analyzed.
- Whether RMSNorm was applied exactly as in the model.
- How vocabulary rank was computed.
- Whether digit tokens were restricted or full vocabulary was used.

## 6.5 DPS

- Exact soft DPS formula.
- Exact hard DPS formula.
- When the intervention is applied: one step or every step.
- Which layer is used.
- How the probe prediction is obtained during generation.
- Why soft DPS succeeds in one protocol but fails in another.

## 6.6 9-row repair

- Training data size.
- Optimizer.
- Learning rate.
- Number of steps.
- Regularization.
- Whether only rows `1`–`9` were updated.
- Whether digit row norms were adjusted.
- Whether the repair was trained with digit-restricted loss or full-vocabulary loss.
- How held-out evaluation was performed.

## 6.7 LoRA Q/V

- Target layers.
- Target modules.
- Rank and alpha.
- Dropout.
- Learning rate.
- Batch size.
- Number of steps.
- Training tasks.
- Whether LoRA was trained on multi-task data.
- Whether evaluation tasks were held out.
- Post-LoRA performance on MMLU/GSM8K/DROP.
- Whether the base model was frozen.

## 6.8 Generation

- Maximum new tokens.
- Stopping criteria.
- EOS tokens.
- Whether newline or punctuation was used as a stop string.
- Regex for integer extraction.
- Whether first or final integer was scored.
- Whether chat templates were used.
- Whether generation was greedy or sampled.

---

# 7. Suggestions for Strengthening the Paper

Below are prioritized recommendations.

## High priority

1. **Unify the evaluation protocol.**  
   Present one primary table with all key methods under one protocol.

2. **Fix the generation-scoring ambiguity.**  
   Report first-token, first-integer, final-integer, exact-match, and format-failure metrics.

3. **Clarify the 9-row repair discrepancy.**  
   Explain why the same intervention gives 60.7%, 93.8%, and 99.9% under different protocols.

4. **Add missing baselines.**  
   Include CoT, digit-logit bias, constrained decoding, and random LoRA controls.

5. **Provide full reproducibility details.**  
   Release code, data, prompts, hyperparameters, and evaluation scripts.

6. **Temper causal language.**  
   Replace “the model knows” with “a probe can decode” unless supported by causal evidence.

7. **Strengthen the geometric analysis.**  
   Analyze digit-row differences, count subspaces, and causal logit effects.

8. **Evaluate LoRA side effects.**  
   Report post-LoRA MMLU, GSM8K, and DROP performance.

## Medium priority

1. Add a cross-model summary table with probe \(R^2\), cosine, repair accuracy, and LoRA accuracy.
2. Include Pythia and Mistral results more prominently.
3. Show confusion matrices for counts.
4. Show logit-gap distributions.
5. Show examples of generation outputs.
6. Explain layer-0 probe accuracy.
7. Discuss tokenization of digits and multi-digit numbers.
8. Move protocol explanations earlier and simplify them.

## Low priority

1. Improve table formatting using `threeparttable`.
2. Remove unused packages.
3. Fix the style-file mismatch.
4. Add model citations.
5. Ensure all figure files and bibliography entries are available.

---

# 8. LaTeX and Manuscript Preparation Issues

## 8.1 Style file mismatch

The comment says:

```latex
% NeurIPS 2026 style --- submission mode (anonymized)
```

but the paper loads:

```latex
\usepackage{iclr2027_conference}
```

This is inconsistent. If the paper is intended for NeurIPS, use the NeurIPS style file. If it is intended for ICLR, remove the NeurIPS comment. A style mismatch can lead to desk rejection if formatting requirements are not met.

## 8.2 Author block formatting

The author block is:

```latex
\author{Anonymous authors\
Paper under double-blind review}
```

This may not compile as intended. If a line break is desired, use:

```latex
\author{Anonymous authors\\
Paper under double-blind review}
```

or simply:

```latex
\author{Anonymous authors}
```

depending on venue requirements.

## 8.3 Missing bibliography file

The paper uses:

```latex
\bibliography{references}
```

but the `references.bib` file is not provided. The manuscript cannot be compiled as-is. The authors should ensure that all citation keys resolve.

Citation keys used include:

- `razeghi2022impact`
- `stolfo2023mechanistic`
- `alain2016understanding`
- `hewitt2019designing`
- `nostalgebraist2020logitlens`
- `belrose2023eliciting`
- `park2023linear`
- `geva2021transformer`
- `turner2023activation`
- `zou2023representation`
- `meng2022locating`
- `hendrycks2021measuring`
- `cobbe2021training`
- `dua2019drop`
- `elhage2022superposition`

All of these should be verified.

## 8.4 Missing figure files

The paper references:

```latex
pipeline.pdf
fig3_probe_r2_gap.pdf
logit_lens_depth.pdf
```

These are not provided. The authors should ensure that all figures are included and that fonts are embedded.

## 8.5 Unused or unnecessary packages

The paper loads:

```latex
\usepackage{nicefrac}
\usepackage{subcaption}
```

but neither appears to be used in the provided text. Removing unused packages is not required but improves cleanliness.

## 8.6 Table formatting

Some tables place notes after the tabular environment using manual spacing:

```latex
\vspace{3pt}
\par\scriptsize
```

This can be fragile. Consider using `threeparttable` for table notes.

## 8.7 Table 2: best layer inconsistency

Table 2 lists layers 0, 12, 24, and 35, then says:

```latex
\textbf{Best (layer 3)}
```

But layer 3 is not shown in the table. Either include layer 3 or explain why the best layer is not listed.

## 8.8 Use of `R^2` for count prediction

For discrete counts, exact accuracy, MAE, and confusion matrices are often more interpretable than \(R^2\). The paper should report both.

## 8.9 Model citations

The paper uses Qwen3, Mistral, and Pythia but does not appear to cite the model releases. These citations should be added.

## 8.10 AI use statement

The AI use statement is present, which is good. The authors should ensure it satisfies the target venue’s exact policy.

## 8.11 Appendix placement

The appendix appears after the bibliography. Some venues allow this; others prefer the supplementary material in a separate file. The authors should check the venue requirements.

---

# 9. Specific Questions for the Authors

1. What is the primary baseline accuracy for Qwen3-8B entity counting under the unified digit-restricted next-token protocol? Is it 10.3%, 11.3%, 13.7%, or 38.6/38.8%? Please explain the differences.

2. Why does the 9-row repair achieve 60.3% full-vocabulary next-token accuracy but 0.0% greedy generation accuracy? What are the generated outputs?

3. How exactly is “final integer” extracted during generation? What happens if the model outputs the correct digit first but then adds text containing another number?

4. What is the definition of the “entity-mean position” used for probing?

5. Why is layer-0 probe \(R^2\) so high? What information is available at layer 0?

6. Were probe hyperparameters selected on a validation set? Was the test set fully held out?

7. Were entity types and templates held out? If so, what is the performance on held-out entity types versus seen ones?

8. Were LM-head rows normalized before computing cosine similarity?

9. Did you analyze alignment with digit-row differences rather than individual digit rows?

10. What happens when the count probe direction is added to or subtracted from hidden states? Do digit logits change as predicted?

11. What are the exact training details for the 9-row repair and LoRA Q/V?

12. Was LoRA Q/V trained on entity counting only, or on all four tasks? What are the per-task generation results?

13. Does LoRA Q/V degrade performance on MMLU, GSM8K, or DROP after intervention?

14. How does LoRA Q/V compare with chain-of-thought prompting under the same final-integer scorer?

15. How does LoRA Q/V compare with simple digit-logit bias or constrained decoding?

16. What is the GSM8K negative-control result in detail?

17. Why does Pythia-410M show limited repair transfer despite the orthogonality signature?

18. What is the behavior of the repaired model on multi-digit answers, especially tokenization of `0`?

19. What is the exact formula for soft DPS and hard DPS?

20. Why does soft DPS achieve 96.3% in the single-seed protocol but only 13.2% in the mode-matched protocol? What makes it so brittle?

---

# 10. Suggested Revised Abstract Framing

The current abstract is too strong in several places. A more defensible version might be:

> Large language models often fail at simple counting tasks even when the items to be counted are explicitly present in the prompt. We investigate whether this failure arises because models do not represent counts internally, or because they cannot convert those representations into the correct output tokens. Across several decoder-only transformer families, we find that linear probes can recover counts from hidden states with high accuracy, while the corresponding count-related directions are poorly aligned with the unembedding rows for digit tokens. Targeted repair of digit rows improves constrained next-token digit prediction, but does not by itself fix unconstrained generation. A LoRA intervention on attention Q/V weights improves autoregressive generation accuracy and increases the rank of correct digit tokens. These results suggest that counting failures in low-vocabulary aggregation tasks can be partly explained by a readout bottleneck between internal representations and output-token generation.

This version avoids “the model knows” and “geometrically misaligned” as absolute claims unless supported by the strengthened analysis.

---

# 11. Minor Comments

- The phrase “true greedy autoregressive generation” is slightly odd. “Unconstrained greedy autoregressive generation” is clearer.
- The term “probe-round” is not standard. Define it explicitly when first used.
- The phrase “hard DPS” and “soft DPS” should be defined in the main text before use.
- The paper should state whether digit tokens are single tokens in each tokenizer.
- The vocabulary size appears to be around 152K for Qwen. State this explicitly when discussing rank 55,980.
- The phrase “random baseline \(0.57\times\)” for 14B is confusing. Clarify whether the count cosine is 0.57 times the random baseline.
- The paper should avoid saying “the bottleneck is absent” for GSM8K unless the analysis is fully specified.
- The Discussion claims that the 9-row repair “surpasses LoRA.” This is only true under certain constrained protocols. Be explicit.
- The phrase “the model stores the count” should be used cautiously.
- Some tables would benefit from confidence intervals.
- The manuscript should include a notation table.

---

# 12. Recommendation

## Recommendation: **Borderline Reject / Major Revision**

The paper has a strong central idea and an interesting combination of probing, geometric analysis, and intervention. The claim that counting failures may arise partly from an output-readout bottleneck is potentially valuable for mechanistic interpretability and reliable LLM deployment.

However, the current manuscript has too many issues for acceptance:

- inconsistent evaluation protocols,
- unclear generation scoring,
- overclaimed causal language,
- insufficient baselines,
- missing reproducibility details,
- incomplete cross-model evidence,
- and a potentially problematic discrepancy between full-vocabulary next-token accuracy and generation accuracy.

If the authors can unify the evaluation, clarify the generation metrics, add proper baselines, and strengthen the geometric and causal analysis, the paper could become a solid contribution.

---

# 13. Suggested Scores

These scores reflect the current manuscript.

| Criterion | Score | Justification |
|---|---:|---|
| Soundness | **2/4** | Interesting interventions, but protocol inconsistencies, unclear generation scoring, and overclaimed probe interpretations weaken the evidence. |
| Presentation | **2/4** | The writing is generally clear, but the number of protocols and inconsistent results makes the paper hard to follow. |
| Contribution | **3/4** | The representation-versus-readout framing and targeted interventions are novel and useful. |
| Significance | **3/4** | The topic is important, but the current evidence is mostly limited to synthetic low-vocabulary tasks. |
| Overall | **4/10** | Borderline reject / major revision. The core idea is promising, but substantial revisions are needed. |
| Confidence | **3/5** | Familiar with mechanistic interpretability, probing, logit lens, and LLM evaluation, but did not run the code or verify all empirical claims. |

---

# 14. Final Comments

The paper is pursuing a genuinely interesting question. The best version of this work would be a careful mechanistic study showing that certain counting failures are not due to missing internal information but to a mismatch between internal representation and output readout. That would be a useful contribution to the interpretability and reliability literature.

To get there, the authors should:

1. simplify the evaluation story,
2. make the generation metrics transparent,
3. avoid overclaiming from probes,
4. strengthen the geometry with subspace and causal analyses,
5. add strong baselines,
6. release full code and data.

With those changes, the paper could become a meaningful contribution.