⚠ **DESK-REJECT RISK**

- **Anonymity:** No obvious author-identifying information in the provided manuscript. The paper is anonymized appropriately.
- **Page limit:** Cannot be verified from the raw LaTeX source. The main text appears reasonably compact, but the authors should ensure that the compiled main text is ≤ 9 pages for submission, excluding references and appendices.
- **AI use statement:** Present.
- **Style files:** The manuscript uses `iclr2027_conference.sty` and `iclr2027_conference` bibliography style, which appears appropriate. I cannot verify from the provided source whether these are the official ICLR 2027 files.

---

# 1) Core Thesis & Significance

The paper investigates why transformer language models fail at simple counting tasks even when the items to be counted are present in the prompt. The central claim is that the failure is not primarily due to missing internal count representations; rather, the model encodes count information in directions that are poorly aligned with the output unembedding rows corresponding to digit tokens. The authors support this with linear probes showing high count decodability, cosine/logit-lens analyses showing weak alignment to digit rows, and interventions: a minimal 9-row `lm_head` repair that helps constrained digit prediction, a probe-based logit bypass, and a LoRA Q/V intervention that improves autoregressive generation.

The problem is practically and scientifically relevant: counting failures are well known, easy to demonstrate, and conceptually important because they expose a gap between internal competence and observable output. The novelty is mainly integrative and mechanistic: the paper combines probing, geometric alignment analysis, logit lens, targeted output-head editing, and LoRA-based routing repair to localize a specific failure mode. A reviewer should be able to summarize the contribution unambiguously: “models internally represent counts, but the output pathway is geometrically misaligned with digit tokens; fixing the output head helps constrained decoding, while fixing upstream routing helps generation.”

The contribution is not a new architecture or a new benchmark, but a diagnostic and interventional story. Its strength depends on whether the causal evidence is clean and whether the scope is not overstated.

---

# 2) Technical Soundness

The paper’s technical approach is broadly sensible. The distinction between “information is absent” and “information is present but not readable by the output head” is a good one. The use of multiple probes, logit-lens measurements, cosine alignment, and interventions is appropriate for this kind of mechanistic claim. The strongest evidence is the combination of:

1. high probe decodability,
2. low alignment between count directions and digit rows,
3. improvement from targeted output-row repair under constrained decoding,
4. improvement from upstream LoRA repair in generation,
5. logit-rank diagnostics showing that the correct digit becomes much more likely after intervention.

However, there are several decision-relevant concerns.

### Significant concern: inconsistent or ambiguous intervention results

The manuscript contains apparent inconsistencies in the reported effectiveness of the 9-row repair.

- Table 1 / unified evaluation reports the 9-row repair at **60.7%** digit-restricted next-token accuracy for entity counting.
- Table 4 also reports **60.7%** for entity counting under the mode-matched protocol.
- But Table 5 reports **9-row `lm_head` held-out accuracy of 93.8%** for Qwen3-8B, and the discussion says updating only 9 output rows yields **93–99% held-out accuracy** across Qwen3-8B and Mistral-7B.

These numbers are not obviously compatible unless they refer to different tasks, different evaluation sets, different scoring restrictions, or different training protocols. The paper does not make this sufficiently clear. This is the kind of inconsistency that can materially undermine confidence in the causal localization claim, because the 9-row repair is the paper’s primary minimal intervention.

Similarly, the discussion states that the 9-row repair “surpasses LoRA,” but the paper also shows that the 9-row repair achieves **0.0% generation accuracy**, whereas LoRA Q/V achieves **83.1% generation accuracy**. The comparison is therefore mode-dependent and needs to be stated very precisely. As written, the claim risks misleading readers.

Classification: **significant concern**, likely addressable by clarification, unified tables, and explicit protocol labels. If the discrepancy reflects genuinely different protocols, the paper must say so unambiguously. If it reflects an error, it would become more serious.

### Significant concern: orthogonality in high dimensions needs careful framing

The paper claims that count-encoding directions are “nearly orthogonal” to digit rows, with absolute cosine values around 0.01–0.03. In high-dimensional residual streams, many unrelated directions will have small cosines simply by geometry. The authors do include random-direction baselines, permutation tests, and TOST equivalence testing, which is good. But the claim would be more convincing with stronger reference distributions and subspace-level analyses, for example:

- cosine distribution between count directions and all vocabulary rows, not only digit rows;
- comparison against probe directions for other salient features known to be output-relevant;
- canonical correlation or subspace-angle analysis between the count-encoding subspace and the digit-row subspace;
- separate analysis for one-hot digit directions rather than a single scalar count regression direction;
- explicit report of last-token probe accuracy/R², since autoregressive decoding reads from the final position.

The current evidence is suggestive but not fully definitive. The claim “the model stores the count in a form that the digit logits do not naturally read out” is plausible, but the geometric argument should be framed carefully to avoid implying that small cosine values are automatically abnormal in high-dimensional spaces.

Classification: **significant concern**, but addressable with additional analysis and more cautious wording.

### Significant concern: LoRA Q/V improvement needs stronger controls

The LoRA Q/V intervention is important because it is the paper’s deployable fix for generation. The mechanism claimed is that LoRA improves upstream routing rather than changing the count representation itself. The paper supports this by showing that the probe direction at layer 2 is unchanged, final-layer probe R² increases, logit-lens accuracy increases, and the correct digit’s vocabulary rank improves.

This is encouraging, but the evidence remains partly correlational. A LoRA module trained on counting prompts could learn task-specific format shortcuts, digit-biasing behavior, or surface-pattern routing rather than genuinely aligning the internal count representation with the output pathway. Useful controls would include:

- LoRA trained with shuffled or corrupted count labels;
- LoRA applied to all attention projections or MLPs as baselines;
- evaluation on held-out templates, entity types, and natural-language variants;
- evaluation of whether LoRA degrades unrelated capabilities;
- testing whether a simple digit-logit bias or constrained decoding baseline achieves similar generation behavior.

The paper mentions a locus ablation and reports entity-only per-task accuracies, which helps, but the causal interpretation of LoRA Q/V would be stronger with more explicit negative controls.

Classification: **significant concern**, addressable in revision.

### Typical limitation: “the model knows the count” is too strong

The phrase “the model knows the count” is rhetorically effective but scientifically loose. A linear probe achieving high R² shows that some linearly accessible information exists in hidden states. It does not necessarily show that the model’s computation uses that representation, that the representation is stable across contexts, or that it corresponds to the same notion of counting used by humans. The paper partially acknowledges this by distinguishing constrained decoding and generation, but the language could be more precise.

Classification: **typical limitation**.

### Typical limitation: synthetic task dependence

The core evidence is strongest on synthetic entity-counting prompts with controlled distractors, lengths, and spacings. This is appropriate for isolating mechanisms, but the paper’s title and framing imply a broader account of counting failures. The natural-language extension, instruct-mode analysis, and DROP subset are useful, but they are not enough to establish that the same bottleneck dominates counting failures in general.

Classification: **typical limitation** for mechanistic interpretability work, but it affects the strength of the paper’s general claims.

### Fatal flaw?

I do not see a fatal flaw in the core idea. The paper does not merely observe a correlation; it performs interventions. However, the causal story is weakened by reporting inconsistencies and by the fact that the 9-row repair does not fix unconstrained generation. The paper’s final account is therefore not “the output head alone is the bottleneck,” but rather “the output head is one component of a readout/routing bottleneck.” The paper should say this more consistently.

---

# 3) Empirical Rigor

The empirical effort is substantial. The authors evaluate multiple models, multiple tasks, multiple protocols, and multiple intervention levels. The inclusion of constrained next-token, full-vocabulary next-token, and autoregressive generation is especially important, because it exposes the gap between diagnostic decoding and actual deployment.

### Strengths

- Multiple model families: Pythia, Qwen, Mistral.
- Multiple scales up to 14B.
- Multiple tasks: entity counting, character counting, addition, list length, majority vote, max extraction, multi-digit counts.
- Multiple intervention types: probe-round oracle, hard/soft DPS, 9-row repair, full-vocabulary repair, LoRA Q/V.
- Controls: shuffled labels, random directions, shuffled rows, random-position controls, capacity ablations, format robustness.
- Quantified trade-offs: parameter counts, constrained vs unconstrained decoding, probe ceiling vs actual repair.

This level of empirical thoroughness is above the median for interpretability papers and is one of the manuscript’s main assets.

### Weaknesses in empirical support

#### Missing or underreported external baselines

For a paper titled “Why Transformers Fail at Counting and How to Fix It,” the empirical comparison could include more baselines:

- chain-of-thought prompting with a clearly defined scoring protocol;
- few-shot counting prompts;
- constrained decoding with digit masking;
- simple output biasing or digit-token logit adjustment;
- full LoRA or adapter fine-tuning on the same counting data;
- existing counting benchmarks, if applicable.

The discussion mentions CoT, but the manuscript does not provide a strong quantitative CoT baseline in the main text. Since CoT is the most natural practical intervention, this omission is noticeable.

#### Side effects are not sufficiently measured

The 9-row repair modifies digit rows of the output head. This could affect any task involving numbers, dates, list formatting, arithmetic, or even general punctuation if the repaired rows interact with other tokens. The paper notes that output-row adaptation degrades MMLU in one negative-control experiment, which is important. But the manuscript does not systematically evaluate side effects for the main interventions.

For LoRA Q/V, the paper should report whether the intervention harms general language modeling, arithmetic, MMLU, GSM8K, or other capabilities. A targeted repair is much more compelling if it improves counting without materially degrading other behavior.

#### Addition and list length weaken the “failure” framing

The paper includes addition and list length as low-vocabulary aggregation tasks. However, addition already has a strong baseline of **93.3%**, and list length is **57.7%**. These are not equally strong examples of “counting failure.” Including them as evidence that the bottleneck generalizes is acceptable, but the paper should be careful not to imply that the same failure is present with equal strength on all four tasks. The strongest case is entity counting.

#### Multi-digit results are weak

The multi-digit extension shows probe-round at 93.8% but full-vocabulary repair at only 42.1%. This is honest and useful, but it limits the practical significance of the fix. Many real counting failures involve multi-digit outputs or multi-token answers. The paper scopes itself to single-token low-vocabulary aggregation, which is reasonable, but the title and abstract may give a broader impression.

#### Overclaiming check

The following claims should be softened or clarified:

- “The model knows the count” should be replaced with “a linear probe can recover the count from intermediate hidden states.”
- “How to Fix It” is too broad if the fix is task-specific, fine-tuning-based, and not effective for unconstrained generation in the 9-row case.
- “The bottleneck generalizes across character counting, addition, and list length” should be qualified, because the baseline failure strength differs across tasks.
- “The model stores the count in a form that the digit logits do not naturally read out” is plausible, but the high-dimensional geometry should be discussed with more care.

These are not necessarily fatal, but they matter because the paper’s claims are one of its main contributions.

---

# 4) Competitive Realism Check

Compared with typical ICLR-accepted interpretability or mechanistic papers, this manuscript has several favorable properties:

- a clear mechanistic hypothesis;
- direct measurements rather than only behavioral correlations;
- interventions that test the hypothesis;
- multiple models and tasks;
- explicit negative controls;
- a memorable diagnostic result: count information is decodable but poorly aligned with digit output rows.

The weaknesses are also common in this literature:

- dependence on synthetic tasks;
- difficulty proving that a probed representation is causally used;
- risk of overinterpreting geometric metrics;
- limited evaluation of side effects;
- potential protocol-dependent results.

The most unusual issue is the apparent inconsistency between different tables and claims about the 9-row repair. That is not a typical limitation; it is a presentation and reliability concern. If clarified, the paper is plausibly within acceptance variance. If left unexplained, it could become the reason for rejection.

Would at least two reasonable reviewers likely score this ≥5? Yes, probably. One reviewer may value the mechanistic diagnosis and intervention story highly. Another may worry about synthetic scope and inconsistent reporting. A third may focus on the fact that the 9-row repair fails generation. The paper is not obviously below the ICLR bar, but it is not immune to criticism either.

---

# 5) Weakest Link Analysis

The single issue most likely to flip accept/reject is:

**Ambiguity and apparent inconsistency in the intervention results, especially the 9-row repair numbers across tables and discussion.**

Specifically, the reader must reconcile:

- 9-row repair at 60.7% for entity counting under the mode-matched protocol;
- 9-row repair at 93.8% held-out in the intervention comparison table;
- discussion text saying 9-row repair yields 93–99% held-out accuracy and “surpasses LoRA”;
- generation-mode result of 0.0% for the same repair.

If these numbers correspond to different protocols, the paper must state that explicitly and preferably consolidate the headline results in one table. If they do not, the inconsistency is serious.

This weakness is **addressable in revision**. The authors can add a unified table with one protocol per column, clearly indicate task, decoding mode, argmax scope, scoring rule, and seed setup, and avoid cross-protocol comparisons in the prose.

A secondary weak link is the lack of side-effect evaluation for the interventions. This is also addressable but less likely to single-handedly flip the decision if the core mechanism is clarified.

---

# 6) Convergence Test

If the authors made no further changes, the paper is borderline. It has enough interesting evidence to be accepted by some reviewer configurations, but the reporting inconsistencies and scope overclaims give other reviewers enough reason to reject. I would not assign it a robust ≥50% acceptance probability as written.

The minimal change that would most improve the paper is not editorial but evidential/presentational:

1. **Create one consolidated headline table** for the main entity-counting results, with rows for baseline, probe-round, hard DPS, 9-row repair, and LoRA Q/V, and columns for:
   - digit-restricted next-token,
   - full-vocabulary next-token,
   - unconstrained greedy generation,
   - held-out natural-language templates,
   - side-effect proxy, e.g. MMLU or a small general benchmark.

2. **Explicitly reconcile all 9-row repair numbers.** If 60.7% and 93.8% come from different protocols, state exactly what differs: task, training set, evaluation set, scoring, digit restriction, or template distribution.

3. **Add at least one LoRA control**, preferably random-label LoRA or LoRA on another module, to strengthen the claim that Q/V LoRA is correcting routing rather than learning a generic digit bias.

If only one change is possible, it should be the unified, unambiguous intervention table. That would remove the largest attack surface.

---

# 7) Structural Sharpness & Scope Control

The paper has one dominant contribution: the geometric readout-bottleneck diagnosis for counting. The best parts of the paper are those directly supporting that contribution:

- probe decodability;
- cosine alignment with digit rows;
- logit-lens gap;
- 9-row constrained repair;
- LoRA Q/V generation repair;
- rank-drop diagnostic.

Some content is neutral but potentially distracting:

- majority vote and max extraction are interesting extensions, but they broaden the paper’s scope and invite questions about whether the same mechanism applies to non-count aggregation.
- multi-digit results are honest but weak, and they may reduce the perceived strength of the fix.
- the addition task has a strong baseline and does not fit the “failure” narrative well.
- the MMLU/GSM8K negative-control idea is good, but the evidence is underdeveloped in the main text.

Some content introduces new attack surface:

- broad claims about “fixing” counting;
- claims that the bottleneck generalizes across all four low-vocabulary tasks;
- the phrase “model knows the count”;
- the comparison to CoT without a strong quantitative main-text baseline;
- the 14B result, which is interesting but not enough to establish scaling behavior.

I would recommend scope reduction:

- make entity counting the primary task;
- present one secondary task, perhaps character counting or list length, as a generalization test;
- move majority vote, max extraction, multi-digit, and DROP analyses to the appendix or shorten them substantially;
- frame the 9-row repair as a constrained diagnostic intervention, not a deployable fix;
- frame LoRA Q/V as a targeted fine-tuning intervention for low-vocabulary aggregation, not a general solution to counting.

This would make the paper sharper and reduce the number of claims that need to be defended.

---

# 8) ICLR Formal Scores

**Soundness: 3**  
The core methodology is reasonable and the intervention logic is compelling, but the apparent inconsistencies in the 9-row repair results, the high-dimensional interpretation of cosine alignment, and the limited controls for LoRA Q/V prevent a higher score.

**Presentation: 3**  
The paper is clearly motivated and generally well organized, but the protocol complexity and inconsistent intervention numbers make it harder to trust the headline claims. A unified table and more precise mode-specific language would substantially improve the manuscript.

**Contribution: 3**  
The paper provides a useful mechanistic framing and a set of targeted interventions. The contribution is more integrative and diagnostic than fundamentally new, but it is still meaningful for interpretability and model editing.

**Significance: 3**  
The finding is likely to be interesting to interpretability researchers and may inform targeted fine-tuning or steering methods. However, the practical impact is limited by synthetic task dependence, weak multi-digit repair, and lack of side-effect analysis.

**Overall: 5**  
This is a borderline accept. The central idea is interesting, the empirical effort is substantial, and the intervention story is stronger than a purely correlational probing paper. However, the manuscript as presented has important clarity and scope issues. If the authors reconcile the intervention results, reduce overclaiming, and add a few controls, the paper could become a clear accept.

**Confidence: 3**  
I am fairly confident in the assessment of the mechanistic claims and experimental design, but some details depend on protocol distinctions that are not fully clear from the manuscript.

---

# 9) Final Recommendation

**ICLR recommendation: Borderline Accept (5).**

The paper presents a compelling mechanistic hypothesis: counting failures can arise from a readout/routing bottleneck rather than from absent internal count representations. The combination of probing, logit-lens analysis, output-row repair, and LoRA Q/V intervention is stronger than typical correlation-only interpretability work. However, the manuscript currently overextends its scope and contains ambiguous or inconsistent intervention results, especially around the 9-row repair. With clearer protocol reporting, a unified results table, stronger controls for the LoRA intervention, and more careful language about “knowing” and “fixing” counts, the paper would be substantially more convincing.