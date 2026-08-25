## ⚠ DESK-REJECT RISK

- **Anonymity**: No obvious anonymity violations in the provided manuscript. Authors are anonymous and no code/repository links are visible.
- **Page limit**: Cannot verify from the provided LaTeX source whether the main text is within the ICLR 2027 limit of 9 pages before references/appendices.
- **AI use statement**: Present.
- **Style files**: The source loads `iclr2027_conference`, but a comment says “NeurIPS 2026 style.” I cannot verify from the excerpt whether the official ICLR 2027 style files are used. This should be checked to avoid a technical desk reject.

---

# 1) Core Thesis & Significance

The paper argues that transformers fail at simple counting not because they lack an internal representation of the count, but because the count representation is geometrically misaligned with the output-head rows corresponding to digit tokens. The authors support this with linear probes showing near-perfect count decodability, cosine measurements showing near-zero alignment between count directions and digit rows, logit-lens analyses showing poor vocabulary ranking of the correct digit, and interventions: a minimal 9-row output-head repair that fixes constrained next-token prediction, and a LoRA Q/V intervention that improves unconstrained autoregressive generation.

The problem is practically relevant: counting failures in LLMs are well known, embarrassing, and mechanistically interesting because the needed information is explicitly present in the prompt. The novelty is mostly integration-level rather than a brand-new primitive: the paper combines probing, logit lens, geometric alignment analysis, and targeted weight edits to localize a behavioral failure to a readout bottleneck. A reviewer can summarize the contribution unambiguously: “the model knows the count but cannot read it out through digit tokens because the relevant internal direction is misaligned with the lm_head digit rows.”

---

# 2) Technical Soundness

The paper’s central logic is attractive and falsifiable: if the count is represented but not readable, then probes should decode it, alignment with digit rows should be near zero, and targeted repair should improve readout. Much of the evidence is consistent with this story.

However, there are several nontrivial soundness concerns.

## Strengths

- The paper distinguishes representation from readout, which is the right conceptual framing.
- It uses multiple probe types and reports random-direction baselines and equivalence testing.
- The intervention ladder is sensible: probe-round, DPS, digit-row repair, LoRA Q/V.
- Controls such as shuffled rows, random-position rows, and random directions are useful.
- The logit-lens rank reduction from 55,980 to 1 under LoRA Q/V is a strong mechanistic signal.

## Significant concerns

### (b) Probe direction may not equal the model’s generative readout direction

A linear probe weight vector is a discriminative classifier/regressor direction, not necessarily the direction used by the model’s own computation. The paper tests several probe families, which helps, but the core geometric claim still relies heavily on the assumption that the probe direction approximates the internal count feature that the output head should read.

In high-dimensional spaces, small cosine values are expected for many directions. The random-direction baseline partly addresses this, but the inference would be stronger with a more explicit subspace analysis: for example, measuring whether the count-relevant subspace intersects the span of digit rows, whether canonical correlation between count subspace and digit-row subspace is low, or whether rotating the count direction into the digit-row subspace causally changes logits.

### (b) Position mismatch between probing and generation

The paper frequently probes at an “entity-mean” position, while generation reads from the last token / answer position. This is a critical distinction. If the count is decodable only from an artificial pooled position or from a position that is not directly consumed by the output head during autoregressive generation, then the claim “the model knows the count” is weaker than it appears. The model may have partial count information distributed across positions but fail to route it to the actual output position.

The logit-lens comparison between entity-mean and last-token positions is useful, but the paper should more directly establish that the count is linearly decodable from the exact hidden state used for next-token prediction. Without that, the boundary between “readout bottleneck” and “routing/position bottleneck” is blurry.

### (b) The 9-row repair may learn a new mapping rather than repair an existing one

Fine-tuning nine digit rows improves constrained digit prediction. This is strong evidence that the output head can be adapted to extract the answer, but it does not by itself prove that the original failure was solely due to geometric misalignment with a pre-existing count direction. The repaired rows may learn to exploit other features of the hidden state, including format, position, or task-specific regularities.

The shuffled-row and random-position controls help, but a stronger demonstration would show that the repaired rows align with the probe-identified count direction, or that an analytic rotation/projection of the count direction into the digit-row subspace produces a comparable improvement without gradient-based fine-tuning.

### (b) LoRA Q/V mechanism is plausible but not fully isolated

The LoRA Q/V intervention is the most deployable result, but its mechanistic interpretation needs tighter controls. The paper claims it corrects upstream routing rather than changing the count representation itself. The evidence — unchanged early-layer probe direction, increased final-layer logit-lens accuracy, rank reduction — is suggestive, but not fully conclusive.

Missing details include:

- Which layers receive LoRA adapters?
- What training data are used?
- Are train and test prompts strictly separated?
- Is LoRA trained on entity counting only or on the full multi-task mixture?
- What are the learning rate, batch size, optimization schedule, and stopping criteria?
- Are there control LoRAs trained on unrelated tasks or random label signals?
- Is the locus ablation statistically compared across Q/K/V/O/MLP variants?

Without these details, a skeptical reviewer may interpret LoRA Q/V as a task-specific fine-tune that improves formatting and digit emission, rather than a precise correction of a geometric bottleneck.

### (c) Task definition ambiguity

The entity-counting example says: “There are 2 apples near the pond.” If numerals appear in the prompt, the counting task needs to be defined very carefully. Is the model counting entity mentions, summing explicit numerals, or counting sentences containing the entity? If surface numerals are present, probes could exploit unintended cues. The paper says counts are varied independently of distractors and passage length, but the example creates ambiguity.

## Typical limitations

- Synthetic benchmark dominance.
- Limited scale range for strong intervention claims.
- Pythia-410M repair is weak, so the repair claim is less universal than the abstract suggests.
- The tasks are narrow: low-vocabulary aggregation rather than general reasoning.

## Fatal flaws

I do not identify a fatal flaw. The central claims are not obviously invalid, but they are somewhat stronger than the current evidence base.

---

# 3) Empirical Rigor

The empirical effort is substantial. The paper includes unified evaluations, multiple seeds, multiple tasks, multiple models, logit-lens analyses, ablations, and negative controls. This is much more than a typical “model fails at X” paper.

## Strengths

- The unified evaluation table is useful and necessary given the many protocol variants.
- Reporting digit-restricted next-token, full-vocabulary next-token, and greedy generation is appropriate.
- The parameter-count comparison between 9-row repair and LoRA Q/V is informative.
- The inclusion of probe-round and DPS as diagnostic upper bounds is helpful.
- The cross-task extension to character counting, addition, list length, majority vote, and max extraction is interesting.
- The negative-control motivation for MMLU/GSM8K is sensible: the bottleneck should apply mainly to low-vocabulary aggregation tasks.

## Weaknesses and gaps

### Protocol complexity creates confusion

The paper reports multiple accuracy values for the same intervention under different protocols: e.g., 9-row repair at 60.7%, 93.8%, and 99.9% depending on protocol. The authors explain this, but the proliferation of protocols makes the narrative fragile. A reader must carefully track whether a number is single-seed, multi-seed, stratified, unified, constrained, full-vocabulary, instruct-mode, or generation-mode. This increases the risk of perceived cherry-picking, even if none is intended.

A cleaner presentation would designate one primary protocol per claim and move all other variants to the appendix.

### Missing strong behavioral baselines

For counting tasks, chain-of-thought prompting is an obvious baseline. The paper discusses CoT qualitatively, but the main tables do not include a mode-matched CoT baseline. Given the title’s “How to Fix It,” readers will want to know how LoRA Q/V compares with simple prompting strategies under identical scoring.

Other useful baselines:

- Few-shot prompting.
- Constrained decoding without weight edits.
- Digit-bias addition or logit masking.
- Row-norm rescaling combined with 9-row repair.
- Full fine-tuning on the same counting data, if computationally feasible.

### Probe-round is not a general upper bound

The paper sometimes treats probe-round as an upper bound for output-side interventions. This is too strong. Probe-round upper-bounds a particular linear-probe-based logit injection strategy from a chosen position and direction. Nonlinear decoders, multi-position decoders, or interventions that alter attention/routing could exceed it. The claim should be softened.

### Negative controls are not fully convincing

The MMLU and GSM8K negative-control argument is plausible, but the evidence shown is thin. The paper reports MMLU degradation after output-row adaptation and cosine differences, but a rigorous negative control should show the same full pipeline: probe accuracy, alignment, logit lens, and intervention effect on a matched benchmark. GSM8K is mentioned but not presented with the same granularity as the counting tasks.

### Entity-counting repair gap is only partially explained

The 9-row repair reaches only 60.7% on entity counting under the unified protocol, while probe-round is 98.7%. The paper attributes this to norm competition and hidden-state diversity, but the explanation remains somewhat post hoc. A direct experiment combining row repair with norm adjustment, bias adjustment, or targeted routing would strengthen the claim.

### Reproducibility details are insufficient in the main text

The manuscript provides many numbers but not enough procedural detail for reproduction in the main text. Important missing details include dataset generation rules, exact prompt templates, probe regularization, train/test split handling, LoRA configuration, optimization hyperparameters, and scoring rules for generation failures. The appendix mentions protocols, but the main text should contain enough information for a reader to reconstruct the primary experiments without excessive inference.

## Overclaiming check

Several claims should be moderated:

- “Probe-round upper-bounds what any output-side intervention can reach” is too broad.
- “The model knows the count” is plausible but depends on the probe position and probe class.
- “How to Fix It” in the title overstates the generality of the fix, especially since the 9-row repair fails in unconstrained generation and the LoRA fix is task-specific.
- “Absent from broader multi-step reasoning benchmarks” needs more direct evidence for GSM8K and other reasoning suites.
- “Scale strengthens, not refutes” the thesis is based on limited scale points and should be framed as suggestive.

These are not fatal, but they matter because the paper’s rhetorical framing is stronger than some of its evidence.

---

# 4) Competitive Realism Check

Compared to typical accepted ICLR papers, this manuscript is above average in experimental ambition. It is not merely observational; it attempts causal localization and intervention. The combination of probing, logit lens, minimal output-head repair, and LoRA-based routing correction is likely to interest the interpretability and LLM reliability communities.

The weaknesses are serious but not unusually so for ICLR. Many accepted interpretability papers rely on probes whose causal status is imperfect, and many accepted intervention papers have task-specific scope. The key question is whether the reviewers view the evidence as sufficient to support the central mechanistic claim.

I believe at least two reasonable reviewers could score this at or above 5, especially if the rebuttal clarifies the generation-position issue and provides tighter LoRA controls. However, a skeptical reviewer could also argue that the paper overinterprets probe geometry and presents too many protocol variants. Therefore, the paper is plausible as a poster but not obviously a strong accept in its current form.

---

# 5) Weakest Link Analysis

The single issue most likely to flip accept/reject is this:

**It is not yet sufficiently established that the probed count representation is the same representation that the model must read out at the actual autoregressive generation position.**

The paper shows strong probe decodability, but much of the evidence appears tied to an “entity-mean” position. The output head during generation reads the final hidden state. If the count is only cleanly decodable from a pooled or non-generative position, the story shifts from “output head is misaligned” to “the model fails to aggregate/route count information to the output position.” LoRA Q/V partially addresses this, but the mechanism needs clearer localization.

This issue is:

- **Addressable in revision**, by adding generation-position probe analyses and tighter controls for the LoRA intervention.
- Not obviously fundamental.
- Likely to change the paper’s rhetorical framing even if the main empirical results remain.

If the authors can show that the final-token hidden state contains the count with high probe accuracy, and that LoRA Q/V specifically improves the transfer of that representation into digit-token logits, the central claim becomes much more convincing.

---

# 6) Convergence Test

**If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?**

Not safely. I would place it around the borderline zone, perhaps slightly below a stable 50% threshold, because the mechanistic claim is strong but the generation-position and LoRA-mechanism evidence is not yet airtight.

**Minimal change that would push it over the threshold:**

Add one consolidated “generative-position mechanism” table showing, for the primary tasks and models:

1. Probe \(R^2\) or classification accuracy from the exact last-token/answer-position hidden state used for next-token prediction.
2. Cosine/subspace alignment between that last-token count representation and digit rows.
3. Logit-lens rank/probability of the correct digit at generation time, before and after LoRA Q/V.
4. LoRA Q/V controls: locus ablation results, random/init controls, train/test separation, and generation accuracy on held-out natural-language templates.
5. A mode-matched CoT or constrained-decoding baseline.

This would directly connect the internal representation to the actual output pathway and reduce the risk that the paper’s central diagnosis is an artifact of probing from a non-generative position.

---

# 7) Structural Sharpness & Scope Control

The paper has one dominant contribution: the geometric readout bottleneck hypothesis for counting and related low-vocabulary aggregation tasks.

## Content that strengthens the core argument

- Unified evaluation table.
- Probe \(R^2\) versus next-token accuracy gap.
- Logit-lens accuracy and vocabulary-rank analysis.
- 9-row repair with shuffled/random controls.
- LoRA Q/V generation improvement.
- The rank reduction from 55,980 to 1.

## Neutral content

- General discussion of superposition.
- Qualitative comparison with CoT.
- Broader implications section, unless supported by more task families.

## Content that introduces new attack surface

- Majority vote, max extraction, multi-digit counting, DROP, MMLU, GSM8K, and instruct-mode results are interesting but broaden the scope substantially. Some of these are only partially supported and may invite objections about generality.
- The Pythia-410M result weakens the universality of the repair claim.
- The many protocol variants create unnecessary complexity.

## Recommended scope reduction

The paper would be stronger if the main text focused tightly on:

1. Entity counting as the primary task.
2. Character counting, addition, and list length as secondary low-vocabulary aggregation tasks.
3. Qwen3-8B and Mistral-7B as primary intervention models, with Qwen3-14B as scale evidence.
4. One primary evaluation protocol per claim.

Extensions such as majority vote, max extraction, multi-digit counts, DROP, and MMLU/GSM8K negative controls could be moved to the appendix and labeled exploratory or diagnostic. The title should also be softened unless the fix is shown to be robust in unconstrained generation across tasks and models. For example, “A Geometric Readout Bottleneck in Transformer Counting” would be more precise than “How to Fix It.”

---

# 8) ICLR Formal Scores

### Soundness: 3

The technical approach is reasonable and supported by multiple interventions, but the causal interpretation depends on probe geometry and generation-position assumptions that are not yet fully validated.

### Presentation: 3

The paper is generally clear and well-motivated, but the many protocols, overlapping tables, and missing reproduction details make it harder to evaluate. The authors’ effort to explain differing numbers is appreciated but also signals that the presentation could be simplified.

### Contribution: 3

The contribution is a useful mechanistic diagnosis plus targeted interventions. It is not a completely new methodology, but the integration of probing, geometric analysis, and repair is valuable and likely to be cited.

### Significance: 3

The finding is interesting and potentially influential for interpretability and LLM reliability, but its scope is currently limited to narrow low-vocabulary aggregation tasks. The significance would increase substantially if the bottleneck were demonstrated on more naturalistic tasks or connected to a broader class of “known but not expressible” failures.

### Overall: 5

This is a solid but borderline ICLR paper. It has enough evidence and novelty to be acceptable as a poster, but the central mechanistic claim needs tighter generation-position evidence and cleaner protocol presentation to become a clear accept.

### Confidence: 3

I am fairly confident in this assessment based on the provided manuscript, but some details would require verification in the full appendix, figures, code, and exact dataset generation pipeline.

---

# 9) Final Recommendation

**ICLR: Borderline Accept (5)**

The paper presents an interesting and empirically substantial account of counting failures as a geometric readout bottleneck. The combination of probing, logit-lens analysis, minimal output-head repair, and LoRA-based routing correction is compelling and likely relevant to the ICLR community. However, the current version leaves important questions about whether the probed representation is actually available at the autoregressive generation position, how specifically LoRA Q/V changes routing, and how the results compare with strong prompting baselines. With targeted additional evidence and more restrained framing, the paper would be a credible ICLR poster.