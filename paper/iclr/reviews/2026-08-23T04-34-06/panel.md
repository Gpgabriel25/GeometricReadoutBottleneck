# Paper Review Panel — {timestamp}

## Score Summary

| Critic | Runs | Scores | Median | Sub-Scores (Sound/Pres/Cont/Sig) | Recommendation |
|--------|------|--------|--------|----------------------------------|----------------|
| DeepSeek v4 pro | 3 | 7, 7, 7 | 7 | 4/4/4/3 | Accept (2), Strong Accept (1) |
| MiMo v2.5 pro | 3 | 6, 6, 6 | 6 | 3/3/3/3 | Accept (3) |
| GLM 5.3 | 3 | 6, 6, 6 | 6 | 3/2/3/3 | Accept (3) |
| Kimi k3 | 3 | 6, 5, 4 | 5 | 3/3/3/3 | Accept (1), Borderline Accept (1), Borderline Reject (1) |
| MiniMax m3 | 3 | 6, 6, 5 | 6 | 3/3/3/3 | Accept (2), Borderline Accept (1) |
| Qwen 3.8 max | 3 | 5, 4, 5 | 5 | 3/2/3/3 | Borderline Accept (2), Borderline Reject (1) |

## Visual Critics

| Critic | Runs | Verdicts |
|--------|------|----------|
| Kimi k3 | 2 | Needs polish / Needs polish |
| Qwen 3.8 max | 2 | Needs polish / Needs polish |

## Panel Aggregate

- **Median score**: 6.0
- **Mean score**: 5.72
- **IQR**: 5–6
- **Score range**: 4–7
- **Median sub-scores**: Soundness 3, Presentation 3, Contribution 3, Significance 3

## Recommendation Breakdown

| Recommendation | Count (of 18 text critics) |
|----------------|---------------------------|
| Strong Accept (8-9) | 1 |
| Accept (6-7) | 11 |
| Borderline Accept (5) | 4 |
| Borderline Reject (4) | 2 |
| Reject (2-3) | 0 |

## Consensus Strengths

Mentioned by ≥3 critics. Group by theme, attribute to specific critics.

### Theme 1: Rigorous experimental methodology and controls
- DeepSeek v4 pro (run 1, 2, 3): "The probe analysis...ridge regression with factorial-controlled benchmark...permutation and TOST...causal interventions..."
- MiMo v2.5 pro (run 1, 2, 3): "Factorial prompt design...negative controls...converging evidence streams..."
- GLM 5.3 (run 1, 2, 3): "Unusually well-controlled...shuffled-label probes, random-direction baselines, permutation tests, TOST, necessity/sufficiency controls, negative controls..."
- Kimi k3 (run 1, 2, 3): "Orthogonality claim handled with unusual statistical care...random-direction baselines, permutation tests, TOST, four probe types, three model families, shuffled-label probes, positive control...necessity/sufficiency controls..."
- MiniMax m3 (run 1, 2, 3): "Multi-model, multi-scale, multi-probe design...held-out evaluation...multi-seed reporting...factorial prompt design...negative controls...shuffled-label, random-direction, TOST, positive-control probes..."
- Qwen 3.8 max (run 1, 2, 3): "Multiple model families, multiple scales, multiple tasks, multiple evaluation modes, controls...intervention component is main empirical strength."

### Theme 2: Clear geometric diagnosis and causal interventions
- DeepSeek v4 pro (run 1): "The combination of probe R², cosine alignment, logit-lens, and three interventions provides converging evidence..."
- MiMo v2.5 pro (run 2): "Clean falsifiable predictions...converging interventions..."
- GLM 5.3 (run 1): "The falsifiable-prediction structure (row-repair fixes constrained but not generation; LoRA fixes both) is a strength."
- Kimi k3 (run 1): "The causal logic — constrained decoding should be fixed by output-row repair, generation should not, and upstream (Q/V) repair should fix both — is a genuinely falsifiable structure."
- MiniMax m3 (run 1): "A clearly formulated dichotomy (representation vs. readout)...falsifiable predictions exactly observed."
- Qwen 3.8 max (run 1): "The diagnostic logic is attractive: probe, measure alignment, intervene, check constrained vs generation."

### Theme 3: Multi-model, multi-task, multi-scale validation
- DeepSeek v4 pro (run 2): "Evaluations on Pythia-410M, Mistral-7B, Qwen3-8B, and Qwen3-14B...multiple tasks..."
- MiMo v2.5 pro (run 3): "Multiple seeds, multiple tasks, multiple models, multiple scales, negative controls."
- GLM 5.3 (run 1): "Multi-model (4 models, 3 families, 0.4B–14B), multi-task (4 primary + 3 extension tasks), multi-seed."
- Kimi k3 (run 2): "Three model families and an additional 14B checkpoint are examined."
- MiniMax m3 (run 2): "Geometric claim well-supported across 3 model families and 4 probe types."
- Qwen 3.8 max (run 3): "Multiple model families, multiple tasks, multiple protocols, multiple intervention levels...above median for interpretability papers."

### Theme 4: Negative controls (MMLU, GSM8K) effectively bound scope
- DeepSeek v4 pro (run 1): "Negative controls on MMLU and GSM8K convincingly show that the effect is task-specific."
- MiMo v2.5 pro (run 2): "MMLU/GSM8K negative controls are important and well-chosen."
- GLM 5.3 (run 1): "Negative controls on standard benchmarks are rare; necessity/sufficiency controls are rare."
- Kimi k3 (run 1): "Negative controls (MMLU/GSM8K: |cos| = 0.31–0.48, no bottleneck) correctly bound the claim's scope."
- MiniMax m3 (run 1): "Negative controls (MMLU, GSM8K) at appropriate strength."
- Qwen 3.8 max (run 3): "Explicit negative controls...well-chosen."

## Consensus Weaknesses

Mentioned by ≥3 critics. Group by theme, include severity classification from the critics.

### Theme 1: Inconsistent numerical reporting across tables
- **Severity**: Significant concern (flagged by 11 critics from 4 model families)
- DeepSeek v4 pro (run 3): "The explanation for the entity‑counting repair ceiling (≈60% constrained decoding) is only partially unpacked."
- GLM 5.3 (run 1): "Cross-table protocol inconsistency for the same intervention. The 9-row repair appears as 60.7% ± 3.1% (unified table), 93.8% held-out (Table 5), and 99.9% (instruct mode) — with no in-text reconciliation."
- GLM 5.3 (run 2): "Cross-table irreconcilability. The same method carries materially different numbers across tables..."
- GLM 5.3 (run 3): "Cross-protocol numerical inconsistency. The same intervention appears as 60.7% and 93.8%."
- Kimi k3 (run 1): "The unreconciled cross-table number discrepancies for the same model/task (60.7% vs. 93.8% vs. 56.7% for 9-row repair; 96.3% vs. 13.2% for soft DPS)."
- Kimi k3 (run 2): "Number sprawl and unreconciled protocols. Entity counting baseline appears as 10.3%, 11.3%, 13.7%, 14.2%, 17.0%, and 38.8% across the paper."
- Kimi k3 (run 3): "The protocol and numerical provenance of the headline results are not auditable as presented."
- MiniMax m3 (run 1): "Internal numerical inconsistency in the headline 9-row repair result. Table 1 reports 60.7% ± 3.1%, while Table 4 reports 93.8% held-out."
- MiniMax m3 (run 2): "Numerical inconsistency between tables. Table 1 and Table 2 report 9-row repair at 60.7%, but Table 3 reports 93.8%."
- Qwen 3.8 max (run 1): "Quantitative inconsistencies across tables and claims. Several numbers do not line up cleanly."
- Qwen 3.8 max (run 2): "Inconsistent numerical reporting. Examples: abstract/main table 60.7%, later table 93.8%, Discussion 93–99%."
- Qwen 3.8 max (run 3): "Inconsistent or ambiguous intervention results. The manuscript contains apparent inconsistencies in the reported effectiveness of the 9-row repair."

### Theme 2: Entity counting repair ceiling not fully explained
- **Severity**: Significant concern (flagged by 12 critics from all 6 model families)
- DeepSeek v4 pro (run 1): "The entity‑counting repair ceiling (60.7% vs. 98.7% probe‑round) is a substantial gap that is partially attributed to vocabulary competition and hidden‑state variance... The underlying cause is not fully disentangled."
- DeepSeek v4 pro (run 2): "The ‘digit‑row repair’ degrades sharply for larger counts (Table 8, entity counting), and the explanation (intra‑class variance) is plausible but not experimentally teased apart."
- DeepSeek v4 pro (run 3): "The residual error in the entity‑counting repair... the paper attributes this to digit‑row norm competition and hidden‑state diversity, but these factors are not disentangled experimentally."
- MiMo v2.5 pro (run 2): "The 37pp gap between probe-round (98.7%) and 9-row repair (60.7%) is partially but not fully explained."
- GLM 5.3 (run 1): "The flagship-task repair ceiling (60.7%) is labeled, not explained. ‘Task-level ceiling’ is a restatement."
- GLM 5.3 (run 2): "The 60.7% entity counting ceiling for the 9-row repair... The authors offer two explanations but do not disentangle them."
- GLM 5.3 (run 3): "The 38 pp gap on entity counting (probe-round 98.7% vs. 9-row repair 60.7%) is partially unexplained."
- Kimi k3 (run 1): "The entity counting 9-row repair gap (60.7% vs. probe-round 98.7%) is partially explained but not fully resolved."
- Kimi k3 (run 2): "The 38 pp gap on entity counting (probe-round 98.7% vs. 9-row repair 60.7%) is not fully explained."
- MiniMax m3 (run 1): "Entity-counting 9-row repair ceiling (60.7%) is only partially explained. The 37 pp gap is attributed to two confounded hypotheses."
- MiniMax m3 (run 3): "The 37 pp entity-counting gap is partially unexplained. The paper offers post-hoc explanations but does not decisively discriminate them."
- Qwen 3.8 max (run 3): "The 38 pp gap on entity counting (probe-round 98.7% vs. 9-row repair 60.7%) is partially unexplained."

### Theme 3: Missing chain-of-thought baseline in main text
- **Severity**: Noted by 10 critics from 4 model families
- GLM 5.3 (run 1): "CoT accuracy is never reported in the main text under the paper's own corrected final-integer scorer."
- GLM 5.3 (run 2): "No quantitative CoT comparison in the main text. Since ‘How to Fix It’ is in the title, a main-text table row for CoT is needed."
- GLM 5.3 (run 3): "The CoT comparison — central to the practical ‘How to Fix It’ claim — is discussed in the main text with no numbers."
- Kimi k3 (run 1): "No reported CoT baseline number. The Discussion claims CoT ‘places alongside LoRA Q/V’ but presents no CoT accuracy under the paper's own final-integer scorer."
- Kimi k3 (run 2): "Missing CoT baseline. The Discussion devotes a paragraph to CoT but gives no number."
- Kimi k3 (run 3): "No CoT comparison in main text. The paper should report CoT under the same final-answer scorer."
- MiniMax m3 (run 2): "CoT comparison acknowledged but not head-to-head under matched compute."
- MiniMax m3 (run 3): "Practical significance of LoRA Q/V vs. CoT is not decisively demonstrated."
- Qwen 3.8 max (run 1): "Chain-of-thought prompting is discussed but not given a rigorous table in the main text."
- Qwen 3.8 max (run 2): "No clear comparison to chain-of-thought prompting with a defined scoring protocol."

### Theme 4: Soft DPS fragility and protocol sensitivity
- **Severity**: Significant concern (flagged by 7 critics from 3 model families)
- GLM 5.3 (run 3): "Soft DPS fragility. Soft DPS goes from 96.3% (single-seed) to 13.2% (multi-seed), attributed to protocol differences but the explanation does not mechanistically account for the gap."
- Kimi k3 (run 1): "Soft DPS fragility. 96.3% vs. 13.2% across protocols, explanation not fully satisfying."
- Kimi k3 (run 2): "Soft DPS fragility. 96.3% (single-seed) vs. 13.2% (multi-seed) is explained as non-digit tokens winning, but that means the original result was a prompt-format artifact."
- Kimi k3 (run 3): "Soft DPS is listed at 13.2% under digit-restricted argmax, yet the appendix explains failure by full-vocabulary argmax — inconsistent."
- MiniMax m3 (run 1): "Soft vs. Hard DPS discrepancy is hand-waved. The explanation is plausible but should be quantified."
- MiniMax m3 (run 2): "Soft DPS vs. Hard DPS inconsistency. Soft DPS fails (13.2%) while Hard DPS achieves 98.7%. The explanation reveals the bottleneck is not purely geometric."
- Qwen 3.8 max (run 1): "Soft DPS failure (13.2% in multi-seed vs. 96.3% single-seed) highlights protocol sensitivity."

### Theme 5: Overclaiming relative to scope (title, “How to Fix It”, “model knows the count”)
- **Severity**: Noted by 8 critics from 5 model families
- DeepSeek v4 pro (run 2): "The title ‘Why Transformers Fail at Counting’ is slightly broad given the synthetic focus, but the paper body is well-scoped."
- GLM 5.3 (run 1): "The title ‘Why Transformers Fail at Counting’ is broader than the demonstrated effect."
- GLM 5.3 (run 3): "The title's ‘How to Fix It’ oversells a fix demonstrated on synthetic tasks with an 83.1% ceiling."
- Kimi k3 (run 1): "Title promises a ‘fix’ that the paper itself shows fails in deployment mode (0.0% generation for minimal repair)."
- Kimi k3 (run 2): "Title oversells a fine-tuning intervention."
- Kimi k3 (run 3): "The broad ‘how to fix it’ framing and ‘deployable’ LoRA claim are overextended."
- MiniMax m3 (run 1): "The title’s ‘How to Fix It’ leans on the weaker half of the contribution."
- Qwen 3.8 max (run 2): "Overclaiming: ‘How to Fix It’ is too strong; ‘the model knows the count’ is too strong without causal proof at output positions."

## Unique Findings

Observations noted by only 1 critic that deserve attention.

- **GLM 5.3 (run 2)**: "Layer-0 probe R² = 0.977 is unexplained and potentially undermining. If ‘layer 0’ denotes the embedding output, near-perfect count decoding before any attention aggregation implies the probe reads a surface artifact rather than an internally computed aggregate."
- **GLM 5.3 (run 1)**: "A numeric inconsistency at 14B: |cos| = 0.011 claimed as '0.57× random baseline' implies a baseline of ~0.019, but the expected E[|cos|] for random directions at d=5120 is ≈ 0.011, so the ‘scale sharpens the bottleneck’ claim needs arithmetic checked."
- **Kimi k3 (run 3)**: "Qwen3-14B is said to show that ‘targeted repair’ recovers 90.3%, but the table evaluates nine-row repair plus DPS, not the nine-row repair alone."
- **MiMo v2.5 pro (run 1)**: "The soft DPS failure in the multi-seed protocol (13.2% vs. 96.3% in single-seed) is attributed to protocol differences, but the paper could be more explicit about what changed and why the soft boost magnitude (α=5.0) was insufficient."
- **Qwen 3.8 max (run 2)**: "Probe evidence may not establish that the model ‘knows’ the count due to entity-mean construction leaking count information. The probe may be exploiting the fact that the input was constructed from a variable number of entity positions."
- **MiniMax m3 (run 1)**: "The Discussion's ‘surpassing LoRA (84%, 4M params)’ claim matches no number in the paper (LoRA is 7.67M params, 83.1%/91.7%/96.0%) and appears to compare across protocols where the unified evaluation shows the opposite ordering."
- **DeepSeek v4 pro (run 3)**: "The paper claims that orthogonality is a stable fixed point of training dynamics, but the empirical support — one pair of fine-tuning runs starting from slightly different checkpoints (0.0074 vs. 0.0087) — is fragile."
- **GLM 5.3 (run 3)**: "The 0.0% generation result for the 9-row repair is unexplained and internally contradictory as written. Table 1 reports 60.3% full-vocabulary next-token accuracy, yet greedy generation is exactly 0.0%. A plausible confound never addressed is digit tokenization variants (bare digit ‘3’ vs. space-prefixed ‘ 3’)."

## Visual Issues (from visual critics)

Merged from 4 visual reviews, deduplicated, sorted by severity.

### Critical
None identified.

### High
None identified.

### Medium
- **Figure 1 (page 2)**: ASCII math notation ("R^2", "|cos| <= 0.032") in diagram boxes instead of typeset math; large blank space between diagram and caption; thin faint arrows difficult to trace. — flagged by all 4 visual critics.
- **Figure 3 (page 5)**: Subplots too small, legend and tick fonts near illegible; the green dotted "Probe R² (~0.99)" reference line described in caption is not clearly visible in panel (a) — appears clipped or missing. — flagged by all 4 visual critics.
- **Figure 2 (page 5)**: Legend box obscures the dashed 38.8% reference line; two probe R² curves (all/easy) are visually indistinguishable; axis label uses "R^2" instead of proper R². — flagged by Kimi k3 (run 1, run 2) and Qwen 3.8 max (run 1, run 2).

### Low
- **Table 1 footnote (page 4)**: Set in very small font, noticeably below caption font size — flagged by Kimi k3 (run 1, run 2).
- **Figure 2 layout**: Legend box overlaps shaded gap region; line-number gutter starts at "000" — flagged by Qwen 3.8 max (run 1, run 2).
- **Figure stacking (page 5)**: Figures 2 and 3 stacked on same page, compressing Figure 3 — flagged by Kimi k3 (run 1, run 2).

## Score Distribution

```
Score 1: ▏
Score 2: ▏
Score 3: ▏
Score 4: ▏█ (2 reviews)
Score 5: ▏███ (4 reviews)
Score 6: ▏█████████ (9 reviews)
Score 7: ▏███ (3 reviews)
Score 8: ▏
Score 9: ▏
```

## Full Reviews

[Complete markdown text of each individual review, grouped by model family, labeled with run number. Preserve ALL detail — do not summarize, truncate, or paraphrase. Each review is a verbatim copy of the critic's output.]

### DeepSeek v4 pro

#### Run 1
```
# ICLR 2027 Review

## ⚠ DESK-REJECT RISK: None Detected
- **Anonymity**: No author-identifying information found. All citations are properly anonymized and in third person. No non-anonymous code/repo links.
- **Page limit**: Main text is within 9 pages (standard ICLR limit). The appendix is unlimited and not required for core claims.
- **AI use statement**: Present and appropriately placed.
- **Style files**: Official ICLR 2027 LaTeX style appears to be used.
- **Verdict**: No desk-reject violation is apparent from the provided material.

---

## 1) Core Thesis & Significance
The paper posits that transformer failures in simple counting tasks stem from a *geometric readout bottleneck*: the model internally encodes counts with near-perfect accuracy (linear probes achieve $R^2>0.99$), but the count-encoding directions are nearly orthogonal to the output head’s digit-token rows ($|\cos| \leq 0.032$). The model *knows* the count but cannot *output* it because the readout pathway is misaligned. The authors provide causal evidence via two targeted interventions: (1) a diagnostic 9‑row repair of the digit rows in the output head, which recovers high accuracy under constrained decoding but not during generation, and (2) a LoRA Q/V intervention that corrects upstream attention routing and achieves 83.1% greedy generation accuracy. The problem is practically relevant to any setting where a language model must emit a precise aggregate from a small vocabulary, and the finding is of broad interest to mechanistic interpretability. The novelty is integration‑level: combining linear probes, logit‑lens, and tiny parameter‑space interventions to localize and fix a well‑known behavioral failure, yielding a crisp, testable geometric explanation.

## 2) Technical Soundness
The technical claims are well‑supported and methodologically sound.

- **Probe analysis**: The use of ridge regression with a factorial‑controlled benchmark (breaking correlations between count, distractors, length, spacing) is a strong defense against spurious shortcut learning. The high $R^2$ ($>0.99$) is robust across layers and models.
- **Orthogonality claim**: The cosine alignment of count‑probe directions with `lm_head` digit rows is carefully compared to a random‑direction baseline and tested via permutation and TOST equivalence. The result holds across probe types and model families.
- **Causal interventions**: The 9‑row repair is a minimal, interpretable manipulation that cleanly separates the readout bottleneck from other stages. The sharp contrast between constrained (60.7–100%) and generation (0%) performance for the same repair is a powerful localization. The LoRA Q/V results are backed by logit‑lens (rank‑drop from 55k to 1) and locus ablation, providing mechanistic confirmation.
- **Contribution‑type alignment**: The paper is primarily a *Concepts & Feasibility* study with negative‑result elements (the orthogonality as a surprising, stable property). The evidence thoroughly supports the feasibility of the proposed diagnosis.

**Genuine methodological gaps (classified):**
- **(c) Typical limitation**: The synthetic benchmark is highly controlled, which is a strength for internal validity but limits ecological generalization. The natural‑language and instruct‑mode results partially address this, but real‑world counting tasks (e.g., in a QA context) are not explored.
- **(c) Typical limitation**: The 9‑row repair is trained on the same distribution of counting prompts, so it is not a zero‑shot intervention. This is acceptable for a diagnostic tool, but the paper’s title (“How to Fix It”) might imply a more general remedy. The authors carefully qualify this in the text.
- **(b) Significant concern (fixable)**: The entity‑counting repair ceiling (60.7% vs. 98.7% probe‑round) is a substantial gap that is partially attributed to vocabulary competition and hidden‑state variance. The capacity ablation rules out simple capacity limits, but the underlying cause is not fully disentangled. The paper would benefit from a more explicit model of this ceiling, perhaps by manipulating prompt diversity or digit‑row norms. This does not invalidate the bottleneck diagnosis, but it weakens the claim that the 9‑row repair is a complete readout fix.

No fatal flaws were identified.

## 3) Empirical Rigor
The empirical evaluation is extensive and well‑controlled.

- **Sufficiency for core claims**: The combination of probe $R^2$, cosine alignment, logit‑lens, and three interventions (probe‑round, 9‑row repair, LoRA Q/V) provides converging evidence that the bottleneck is real and causally responsible. The negative controls on MMLU and GSM8K convincingly show that the effect is task‑specific.
- **Baselines and comparisons**: The random‑direction probes, shuffled‑label tests, and TOST equivalence are appropriate for the orthogonality claim. The comparison of 9‑row repair to full `lm_head` repair (94.2% vs. 93.8%) nicely demonstrates that only the digit rows matter. The comparison with chain‑of‑thought is fair and clarifies the distinct mechanistic contribution.
- **Trade‑offs**: The paper quantifies the generation gap (0.000 for LoRA Q/V) and the cost of interventions (36k vs. 7.7M parameters). The multi‑task vs. entity‑only generation accuracies ($83.1\% \pm 7.2\%$ vs. $97.0\%$) are reported transparently.
- **Overclaiming check**: The paper does not overclaim. The distinction between diagnostic (9‑row) and deployable (LoRA Q/V) interventions is clear. The authors acknowledge that the repair is not a universal fix and that the 9‑row generation failure is a routing issue. The scope is explicitly limited to low‑vocabulary aggregation tasks. I see no inflated claims.

**Minor issues**:
- The addition baseline is already high (93.3%), so the intervention’s impact there is less dramatic. The paper acknowledges this.
- The LoRA Q/V multi‑task variance ($71.5$–$89.0\%$) is attributed to task‑mix artifacts; this is plausible but not fully explained. A breakdown by task for LoRA Q/V would strengthen the analysis.

## 4) Competitive Realism Check (Calibrated)
Relative to typical ICLR accepted papers, this work is **strongly above average**. The paper provides a clear, falsifiable mechanistic explanation for a well‑documented phenomenon, backed by multiple converging lines of evidence and causal interventions. The experimental design is thorough, the writing is crisp, and the contribution is both novel and practically insightful. The weaknesses (synthetic domain, repair ceiling, limited scale) are well within the acceptance variance for top‑tier ML venues. I would expect at least two reasonable reviewers to score this ≥5 (Accept/Poster), and many would likely argue for a 6 or 7.

## 5) Weakest Link Analysis
The single issue most likely to flip accept/reject is the **substantial gap between the probe‑round ceiling and the 9‑row repair accuracy on entity counting (60.7% vs. 98.7%)**. This gap is not fully explained, and it weakens the claim that the readout bottleneck is the *only* cause of the failure — there may be additional routing or representational shortcomings that the 9‑row repair does not fix. The paper addresses this partially (vocabulary competition, norm rescaling) but does not fully close the loop. If a reviewer were to fixate on this, they might argue that the diagnosis is incomplete.

- **Addressable in revision**: The authors could design targeted experiments to tease apart the remaining gap (e.g., normalize digit‑row norms and re‑test, or train a separate probe on held‑out entity subsets to see if the residual stream’s encoding degrades with count). This would strengthen the diagnostic claim without requiring a new intervention.

The issue is **unlikely to change the outcome** because the core bottleneck (orthogonal encoding, recovery via DPS and LoRA Q/V) is already convincingly demonstrated. The 60.7% repair is still a 4.4× improvement over baseline and is sufficient to substantiate the geometric hypothesis.

## 6) Convergence Test (Minimal‑Change Threshold)
- **If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?** Yes. The paper is already well above the ICLR poster mean in terms of contribution, soundness, and significance. The evidence is robust, and the narrative is compelling.
- **Minimal change to push over the threshold**: The paper is already a clear accept. The only improvement that would materially increase its score would be a deeper analysis of the entity‑counting repair ceiling, but that is not required for acceptance.

## 7) Structural Sharpness & Scope Control
The paper is centered on a single dominant contribution: the geometric readout bottleneck. The narrative flows cleanly from probe evidence to causal intervention to mechanistic explanation.

- **Content that strengthens the core argument**: The orthogonal alignment analysis, the 9‑row repair, the logit‑lens, the LoRA Q/V locus ablation, and the negative controls are all directly supportive.
- **Neutral content**: The multi‑digit and majority‑vote extensions are interesting but not essential; they broaden the scope without diluting the core message. The training‑dynamics hypothesis for orthogonality is speculative but adds mechanistic depth.
- **Content that introduces new attack surface**: The claim that orthogonality is a stable fixed point of training dynamics is speculative and could be challenged, but it is presented as a plausible explanation, not a proven fact. The paper would be slightly stronger if this were demoted to a discussion point (as it already is) without over‑emphasis.

**Recommendation**: No scope reductions are needed. The paper is well‑scoped and self‑aware.

## 8) ICLR Formal Scores

- **Soundness (1–4)**: **4** — The claims are exceptionally well‑supported by theory, probes, and causal interventions. The experimental protocols are rigorous, with careful controls for confounding factors.
- **Presentation (1–4)**: **4** — The paper is clearly written, well‑structured, and the figures effectively communicate the core findings. The pipeline diagram (Fig. 1) is especially helpful.
- **Contribution (1–4)**: **4** — The discovery of a geometric readout bottleneck as the root cause of counting failures, combined with targeted causal repairs, is a novel and valuable contribution to mechanistic interpretability. The paper provides a new diagnostic lens for competence‑without‑performance failures.
- **Significance (1–4)**: **4** — The finding is likely to influence interpretability research and could inspire similar diagnoses for other failures. The idea that a model “knows” something but cannot output it due to geometric misalignment is a memorable and broadly applicable insight. The community will notice and cite this work.
- **Overall (1–10)**: **7 (Strong Accept)** — Well above the ICLR poster mean. The work is thorough, novel, and provides a crisp mechanistic explanation with strong causal evidence. It is not a landmark (8+) because it is still a focused study on a specific task family, but within its scope it is outstanding.
- **Confidence (1–5)**: **4** — I am confident in the evaluation, but the entity‑counting repair ceiling and the limited scale (up to 14B) leave some open questions that I cannot fully adjudicate.

## 9) Final Recommendation (Venue‑Calibrated)
**ICLR: Strong Accept (7)**. The paper delivers a compelling, well‑executed mechanistic investigation of a well‑known behavioral failure. The geometric diagnosis is novel, the causal interventions are clean and minimally invasive, and the evidence is robust across multiple models and tasks. The manuscript is clearly written and appropriately scoped. While the entity‑counting repair ceiling and the synthetic‑domain focus are minor limitations, they do not detract from the core contribution. This work is a strong candidate for an oral presentation and will be a valuable addition to the interpretability literature.
```

#### Run 2
```
# Review

## 1) Core Thesis & Significance

The paper argues that transformer failures at simple counting tasks stem not from an inability to internally encode the count, but from a geometric misalignment between the count‑encoding directions in the residual stream and the rows of the output embedding (`lm_head`) that correspond to digit tokens. The central claim is that by rewriting as few as the nine digit rows of the output head, or by applying a low‑rank (LoRA) correction to attention Q/V weights, one can almost fully restore counting performance in constrained and autoregressive settings, respectively.

The problem is practically relevant because counting errors are pervasive even in capable LLMs, and understanding why this happens has broad implications for large model reliability. The novelty lies in the precise geometric diagnosis and the targeted, minimal interventions that demonstrate causality. A reviewer can unambiguously summarize the contribution as: “Transformers possess an accurate internal count representation that is nearly orthogonal to the output head; repairing this misalignment via a handful of parameter updates recovers counting ability.”

## 2) Technical Soundness

The methodology is carefully constructed. Linear probes, logit‑lens measurements, and cosine‑similarity analyses are used to demonstrate that counts are linearly decodable but that the decoding direction is orthogonal to the digit rows. The DPS (Diagnostic Probe Steering) and minimal 9‑row fine‑tuning experiments provide causal evidence that the bottleneck is located exactly at the readout stage.

- **Theoretical framing**: The claim of orthogonality is supported by multiple probe types (ridge, LDA, mean‑difference, PCA) and across three model families. The explanation of why orthogonality arises (dominating non‑counting contexts for digit tokens) is plausible and supported by empirical fine‑tuning dynamics.
- **Methodological gaps**:  
  - The paper only tests decoder‑only transformers up to 14B parameters; the claim that “scale strengthens the bottleneck” is plausible but not confirmed beyond that scale.  
  - The generation‑mode repair via LoRA Q/V requires fine‑tuning; the paper does not explore few‑shot or in‑context variants of the repair, which would increase practical impact.  
  - The “digit‑row repair” degrades sharply for larger counts (Table 8, entity counting), and the explanation (intra‑class variance) is plausible but not experimentally teased apart from norm competition.

These are (b) significant but fixable concerns; none are fatal.

## 3) Empirical Rigor

The experiments are extensive and well‑controlled:

- **Baselines and controls**: The paper includes shuffled‑probe, random‑direction, random‑position and shuffled‑row baselines. The negative controls on MMLU and GSM8K (where no misalignment is present) effectively demonstrate that the bottleneck is not a universal feature of the model.
- **Multiple models and tasks**: Evaluations on Pythia‑410M, Mistral‑7B, Qwen3‑8B, and Qwen3‑14B, and on entity counting, character counting, addition, list length, majority vote, and max extraction convincingly show that the phenomenon generalises across architectures and low‑vocabulary aggregation tasks.
- **Overclaiming check**: The paper is careful about scope, e.g., explicitly stating that 9‑row repair does not fix autoregressive generation and that the LoRA Q/V intervention is the deployable fix. The discussion of chain‑of‑thought is fair and highlights complementarity without inflating claims.
- **Trade‑offs**: Parameter efficiency (36K–7.7M parameters) vs. generation accuracy is clearly reported.

The empirical support for the core claim is strong.

## 4) Competitive Realism Check (Calibrated)

Compared to typical ICLR accepted papers (poster‑tier, average score ~5.35), this paper:

- Presents a crisp, well‑motivated hypothesis with a clear mechanistic story.
- Provides a rich set of controlled experiments that go beyond surface‑level probing.
- Offers a minimal causal intervention that pinpoints the bottleneck.
- The weaknesses (scale limits, lack of few‑shot repair, incomplete explanation of the entity‑counting ceiling) are within the range seen in accepted work.

It is very likely that at least two reasonable reviewers would score this ≥5, and many would place it in the 6–7 range. The paper is comfortably above the acceptance bar.

## 5) Weakest Link Analysis

The single issue most likely to flip accept/reject is: **the limited scope of the generation‑mode repair and the absence of a more straightforward, non‑fine‑tuned corrective strategy (e.g., logit‑based steering without weight modification) for full autoregressive decoding.** The LoRA Q/V approach works but requires per‑task fine‑tuning; if the bottleneck cannot be alleviated without weight updates, the practical impact is reduced.

This is addressable in revision, e.g., by exploring activation‑steering methods that achieve comparable generation accuracy without training, or by showing that a single LoRA Q/V module generalises across many related aggregation tasks. It is unlikely to fundamentally change the outcome because the diagnostic contribution is already solid.

## 6) Convergence Test (Minimal‑Change Threshold)

If the authors made no further changes, the paper already has a strong acceptance chance at ICLR (>50%). The diagnostic evidence, multiple models, and controlled interventions provide a self‑contained story.

A minimal change that would further strengthen it: add an experiment showing that a simple, inference‑only intervention (e.g., steering the residual stream toward the probe direction before the output head) can improve autoregressive generation accuracy to a nontrivial level, thus demonstrating that the bottleneck can be partially addressed without fine‑tuning. This would widen the appeal and demonstrate generality.

## 7) Structural Sharpness & Scope Control

The paper is well‑focussed on one dominant contribution: localising and fixing a geometric readout bottleneck in counting. The narrative flows cleanly from diagnosis (probes, logit‑lens) to causal verification (9‑row repair, DPS, LoRA Q/V).  

- Content that strengthens the core argument: the detailed subspace geometry, the norm‑rescaling experiment, the LoRA Q/V mechanism analysis (logit‑lens improvement, rank drop).
- Neutral content: the discussion of chain‑of‑thought, while fair, is tangential and could be slightly shortened.
- Content that introduces new attack surface: the multi‑digit extension (counts 10–20) is suggestive but not central; it opens questions about token‑level vs. number‑level alignment, but the paper handles it cautiously.

No major scope over‑extension; the paper would benefit from a very minor trim of the CoT discussion, but the current version is acceptable.

## 8) ICLR Formal Scores

- **Soundness (4)**: The technical claims are rigorously tested with multiple complementary methods and controls. No obvious flaws in the reasoning or experimental design.
- **Presentation (4)**: The paper is exceptionally clear, well‑organised, and uses figures and tables effectively. The method and results are easy to follow, and the appendices provide exhaustive detail.
- **Contribution (3)**: The geometric diagnosis and targeted minimal repair are novel and provide a mechanistic explanation for a well‑known failure mode. The contribution is significant but not paradigm‑shifting.
- **Significance (3)**: The finding is likely to influence future work on interpretability and model editing; the diagnostic pipeline (probe → alignment check → targeted repair) could generalise. It meets the bar for oral/poster recognition.
- **Overall (7)**: The paper presents a compelling, well‑executed investigation with impressive causal evidence. It clearly stands above the poster mean (5.35) and is strong enough for a top‑tier accept. It is not a landmark (9), but it is a very good ICLR paper.
- **Confidence (5)**: I am absolutely certain about the evaluation; the evidence is direct and the analysis is thorough.

## 9) Final Recommendation (Venue‑Calibrated)

**ICLR Accept (7)**. The paper delivers a crisp, well‑diagnosed geometric explanation of transformer counting failures and backs it with minimal, causally probed interventions. The experimental breadth (multiple models, tasks, negative controls) and the clean narrative put it solidly above the ICLR poster threshold. While the generation‑mode repair still requires fine‑tuning, this does not diminish the diagnostic contribution, and the paper explicitly scopes the limitation. This is exactly the kind of high‑quality, insight‑driven work that deserves acceptance.
```

#### Run 3
```
# ICLR 2027 Review

**Reviewer #XXXX**

---

### ⚠ Desk-Reject Risk Check
From the provided manuscript, I can verify that:
- Anonymity appears maintained (authors listed as “Anonymous authors”; no acknowledgments or non-anonymous code links visible).
- The main text length is ≤9 pages (excluding references and appendix).
- The AI Use Statement is present and does not count toward page limit.
- The paper uses the official `iclr2027_conference` style file.

I see no grounds for a desk reject. If additional supplementary material exists that violates anonymity, I cannot assess it, but the plain text suggests compliance.

---

## 1. Core Thesis & Significance
The paper diagnoses a well-known failure mode: transformer language models consistently fail at simple counting tasks. The central contribution is a geometric explanation: the model’s residual stream encodes counts with near-perfect linear separability, but the count-encoding direction is orthogonal to the digit‑token rows of the output head (`lm_head`). The failure is therefore a readout bottleneck, not a lack of internal representation. The authors support this with (a) linear probes achieving $R^2>0.99$, (b) cosine alignment near chance level, (c) a minimal 9‑row output‑head repair that recovers constrained decoding, and (d) a LoRA‑based intervention on attention Q/V weights that achieves strong (83 %) autoregressive generation accuracy. The insight generalizes across architectures, scales, and low‑vocabulary aggregation tasks (character counting, addition, list length) while being absent from multi‑step reasoning benchmarks (MMLU, GSM8K).

The problem is practically relevant given widespread LLM usage, and the mechanistic framing (probing → alignment → targeted repair) is a crisp, falsifiable diagnostic pipeline. Novelty is mainly integrative but high: the specific geometric bottleneck, its causal dissection, and the template for diagnosing similar “competence without performance” failures are novel. A reviewer would unambiguously summarize the contribution as “counting failure is a geometric misalignment between count representations and digit‑token output rows, fixable with modest targeted interventions.”

## 2. Technical Soundness
The claims are well‑supported methodologically.

- **Probing:** Linear probes are trained on a held‑out split of the factorial design, and controls (shuffled labels, random directions, TOST equivalence) are thorough. The near‑perfect $R^2$ across layers is robust.
- **Orthogonality measurement:** Cosine similarity is compared to a random‑direction baseline with permutation tests, confirming alignment is no better than chance. Additional probe types (LDA, mean difference, PCA) reinforce the result. The gradient‑stability argument for why orthogonality appears is plausible and supported by targeted fine‑tuning experiments (counting fine‑tuning moves alignment, while arithmetic fine‑tuning does not).
- **Causal interventions:** The 9‑row repair is a minimal causal probe: only 36k parameters, evaluated strictly on held‑out test prompts. Its near‑100 % success in constrained decoding and complete failure in generation cleanly isolate the readout bottleneck from upstream routing failures. The LoRA Q/V intervention, DPS, and logit‑lens measurements form a convergent set of evidence.
- **Potential concerns:**  
  - (b) *Significant concern but fixable:* The explanation for the entity‑counting repair ceiling (≈60 % constrained decoding) is only partially unpacked. Norm competition and intra‑class hidden‑state diversity are mentioned; a more granular decomposition (e.g., regressing residual error on count magnitude, distractors, or passage length) would strengthen the mechanistic story. However, the ceiling does not undermine the core bottleneck claim—it merely limits the efficacy of a 9‑row repair in one task.
  - (c) *Typical limitation:* The theoretical justification of orthogonality as a stable fixed point is heuristic (gradient conditioning argument), not a formal proof. This is acceptable for an empirical mechanistic paper.
  
No fatal flaws were detected. The diagnostic chain is logically tight.

## 3. Empirical Rigor
The experimental design is notably thorough:

- **Controlled, independent factors:** The factorial setup ($C, D, L$, spacing) prevents distributional shortcuts and ensures probes learn genuine count features.
- **Multi‑model, multi‑scale validation:** Pythia‑410M, Mistral‑7B, Qwen3‑8B, Qwen3‑14B. The bottleneck signature appears across all, and repair efficacy scales appropriately with model size.
- **Multi‑task extension:** Character counting, addition, list length, max extraction, and majority vote all exhibit the same bottleneck, strengthening the claim that this is a general low‑vocabulary aggregation phenomenon.
- **Intervention toolkit:** DPS (hard and soft), 9‑row repair, full‑head repair, LoRA Q/V, and logit‑masked generation provide a comprehensive causal map. The distinction between next‑token and autoregressive generation is handled carefully, with explicit protocol maps.
- **Negative controls:** MMLU and GSM8K show higher alignment (cos 0.3–0.48) and no benefit from output‑row adaptation, confirming specificity. DROP shows a modest gain, hinting at partial structure.
- **Logit‑lens depth analysis:** Mapped across layers for entity‑mean and last‑token positions, clarifying the partial projection attempt in upper layers.
- **Overclaiming check:** The paper’s language is precise; it claims a bottleneck, not a panacea. The 83 % generation accuracy for LoRA Q/V is modest but functionally significant, and the authors note that CoT offers a complementary approach. All claims match the presented evidence.

The experiments substantially support the core thesis, and the ablation and control suite would satisfy ICLR reviewing standards.

## 4. Competitive Realism Check
Comparing this to typical accepted ICLR papers in the interpretability and mechanistic understanding space, the submission is clearly above the poster mean. It offers a crisp, falsifiable hypothesis, exhaustive probing, and multiple targeted interventions that converge on a single mechanistic story. The flaw being investigated (counting failure) is both tangible and widely recognized, making the findings immediately shareable. The weaknesses—limited scope to low‑vocabulary aggregation, not completely closing the entity‑counting gap—are within acceptance variance for a strong interpretability paper. I can easily imagine at least two reasonable reviewers assigning a score ≥5 (Accept/Poster). The evidence quality and novelty justify acceptance, and the paper would likely spark follow‑up work.

## 5. Weakest Link Analysis
The single issue most likely to flip an accept/reject decision is the **residual error in the entity‑counting repair**. The 9‑row repair achieves only 60.7 % on entity counting despite a near‑perfect probe ceiling. The paper attributes this to digit‑row norm competition and hidden‑state diversity, but these factors are not disentangled experimentally (e.g., a direct measurement of the linear separability of count‑value classes under the mild ridge regression used for the repair, or a controlled ablation of the norm scaling). A skeptical reviewer could interpret this as evidence that the bottleneck is not fully localized to the 9 rows, or that the probe direction is not perfectly aligned with the count feature. However, the rest of the evidence—DPS, LoRA Q/V, and logit‑lens—strongly points to a routing/alignment issue, so this is addressable with a few additional analyses. It is unlikely to change the outcome if the authors add the suggested decompositions, but in its current state it is a noticeable loose end.

This is a (b) significant concern but not fundamental; it is **addressable in revision**.

## 6. Convergence Test
**Yes**, the paper in its current form has a ≥50 % acceptance chance at ICLR. The core insight is novel, the experiments are convincing, and the story is memorable.

If I were to suggest a minimal change to raise confidence further, it would be to **add a decomposition of the entity‑counting repair gap** into (1) the fraction explained by suboptimal probing (e.g., comparing ridge‑probe accuracy with a nearest‑centroid oracle), and (2) the fraction explained by digit‑row norm disadvantage, via a simple rescaling step. Even a preliminary analysis would tighten the bottleneck claim. That said, the paper is already decision‑stable.

## 7. Structural Sharpness & Scope Control
The paper is well‑centered on one dominant contribution. The pipeline (probe → alignment → interventions) is presented cleanly, and the narrative flows logically.

- Material that strengthens the core argument: factorial design, cosine alignment, 9‑row repair, LoRA Q/V, logit‑lens, generation‑mode breakdowns.
- Neutral extensions: the majority‑vote and max‑extraction tasks. They reinforce the “low‑vocabulary aggregation” generalization but do not add fundamentally new mechanistic insight. They could be moved to a brief remark.
- Content that introduces potential attack surface: the discussion of CoT and the philosophical “superposition” speculation. Both are well‑hedged and do not weaken the empirical footing, but they are not essential.

A targeted scope reduction (e.g., trimming the majority‑vote/max‑extraction details from the main text to a terse paragraph) would tighten the presentation slightly, but the current structure is already acceptable.

## 8. ICLR Formal Scores

- **Soundness (3/4):** Solid experimental methodology with comprehensive controls. The theoretical gradient‑fixed point argument is plausible but not rigorously proven; a minor gap.  
- **Presentation (4/4):** Exceptionally clear, well‑organized, with informative figures and tables. The protocol mapping and stratification of evaluation modes are excellent for reproducibility.  
- **Contribution (4/4):** A novel, falsifiable geometric diagnosis of a well‑known behavioral failure, backed by a rich interventional toolkit. The diagnostic strategy (probe → alignment → repair) is a significant conceptual contribution.  
- **Significance (3/4):** Likely to influence interpretability research on output‑side bottlenecks. The scope is currently limited to low‑vocabulary aggregation, but the framing (“competence without performance” via readout misalignment) is broadly applicable and will attract attention.  
- **Overall (7/10):** Maps to a strong accept. The paper meets the 7 anchor: clear contribution, thorough evaluation, a memorable finding. It comfortably exceeds the ICLR poster mean and would be a welcome addition to the program. I do not see a path to 8 (exceptional, oral‑tier) because the domain is somewhat narrow, but it is a very strong poster.  
- **Confidence (4/5):** I am confident in the assessment. I have expertise in mechanistic interpretability and have carefully checked the experimental logic.

## 9. Final Recommendation

**Recommendation: ICLR Accept (Poster, Score 7)**

This paper provides a crisp, rigorous, and compelling mechanistic explanation for why transformers fail at counting. The diagnostic pipeline—linear probing, alignment analysis, minimal output‑head repair, and LoRA‑based routing correction—is thorough and yields a clear geometric story. The finding that count representations are almost perfectly encoded but orthogonal to the digit‑token output directions is both falsifiable and practically relevant. The evaluation is unusually careful, with attention to protocol matching, multi‑scale validation, and negative controls. The main weakness, the entity‑counting repair ceiling, is partially explained and does not undermine the bottleneck diagnosis. Given the high novelty, strong evidence, and potential to inspire follow‑up work on readout bottlenecks, the paper clearly meets ICLR’s acceptance bar. It will be a useful and well‑cited contribution to the interpretability community.
```

### MiMo v2.5 pro

#### Run 1
```
# Review: "Why Transformers Fail at Counting and How to Fix It"

---

## 1) Core Thesis & Significance

The paper argues that transformer counting failures are not due to absent internal representations (linear probes achieve R²>0.99 at every layer) but rather a **geometric readout bottleneck**: the subspace encoding counts is nearly orthogonal to the lm_head digit rows (|cos| ≤ 0.032, indistinguishable from random). The authors validate this diagnosis through a well-structured causal pipeline—probe → cosine alignment → logit lens → targeted intervention—across three model families (Pythia-410M, Mistral-7B, Qwen3-8B/14B) and four low-vocabulary aggregation tasks.

The problem is practically relevant: counting is a basic capability where LLMs fail despite the information being explicitly present. The novelty is integration-level rather than component-level—probes, logit lens, and LoRA are all known tools, but the specific geometric characterization (orthogonality to digit rows as a stable fixed point of training dynamics) and the causal localization via 9-row repair constitute a novel and well-supported contribution. A reviewer can summarize this unambiguously: "The model knows the count but the output pathway is geometrically misaligned with the tokens needed to express it."

---

## 2) Technical Soundness

**Overall: Well-supported with minor gaps.**

The core claims are well-evidenced:
- **Claim 1 (orthogonality):** Supported by four probe types, permutation tests (p=0.79), TOST equivalence testing, and bootstrap CIs. The random-direction baseline (0.013±0.011) matching the observed alignment (≤0.032) is convincing. **(b)**
- **Claim 2 (9-row repair fixes constrained decoding, not generation):** Cleanly demonstrated—the 0.0% generation accuracy vs. 60.7–100.0% constrained accuracy is a sharp diagnostic. The logit-masked generation experiment (59.2%, matching constrained next-token) elegantly confirms the repair encodes the correct answer. **(c)**
- **Claim 3 (LoRA Q/V restores generation):** 83.1%±7.2% across 5 seeds with generation gap of 0.000. The locus ablation (Q/V vs. K/O/MLP) and the logit-lens rank drop (55,980→1) provide mechanistic specificity. **(c)**

**Genuine methodological gaps:**
- The "orthogonality as stable fixed point" argument (§5, gradient analysis) is intuitive but not formally proven. The empirical fine-tuning evidence (counting fine-tuning raises |cos| 3.2× while arithmetic does not) is suggestive but the two runs start from different checkpoints (0.0074 vs. 0.0087), making the comparison slightly confounded. The paper acknowledges this ("the informative contrast is the relative change within each run") but a controlled experiment from the same checkpoint would strengthen the claim. **(c)** — typical limitation.
- The 37pp gap on entity counting (probe-round 98.7% vs. 9-row repair 60.7%) is partially but not fully explained. The capacity ablation rules out fitting method and row count, and norm competition is documented, but the intra-class hidden-state diversity explanation is asserted rather than quantitatively decomposed. **(c)** — typical limitation.

No fatal flaws identified.

---

## 3) Empirical Rigor

**Experiments are thorough and well-designed.**

**Strengths:**
- The factorial prompt design (varying C, D, L, spacing independently) prevents distributional shortcuts—a genuine methodological contribution that strengthens all downstream claims.
- Three evaluation modes (next-token, generation, instruct) with explicit protocol mapping (Table A1) prevent mode-matching errors.
- Negative controls on MMLU (|cos|=0.31–0.48, no bottleneck) and GSM8K demonstrate task specificity.
- Cross-model validation across three families with consistent geometric signatures.
- Necessity/sufficiency controls: shuffled-digit rows (14.0% < baseline 17.0%) and random-position rows (matches baseline exactly).
- Per-count stratified analysis (Table A4) reveals the repair ceiling is count-magnitude-dependent, adding nuance.

**Minor concerns:**
- The soft DPS failure (13.2% in multi-seed protocol vs. 96.3% in single-seed) is attributed to protocol differences (diverse templates). The paper explains this clearly but it highlights sensitivity to evaluation protocol—a reader might worry about brittleness.
- The multi-task LoRA Q/V variance (71.5–89.0% across seeds) is attributed to task-mix artifacts. The entity-only per-task results (94.5–97.0%) are reassuring, but the variance explanation would benefit from a seed-level breakdown showing which tasks vary most.
- The natural-language counting extension (8 categories × 8 templates) is a good step but still controlled; 5 entity types seen during training, 3 held out—probe-round 96.3% on held-out entities is encouraging but the template diversity is limited.

**Overclaiming check:** The title "Why Transformers Fail at Counting" is slightly broad given the synthetic focus, but the paper body is well-scoped with explicit limitations. Claims are calibrated to evidence. No clear overclaiming detected.

---

## 4) Competitive Realism Check (Calibrated)

**Compared to typical ICLR poster accepts:**
- The experimental rigor (converging evidence streams, proper controls, cross-model validation) is **above average** for ICLR. Many accepted mechanistic interpretability papers present a single model, single task, and fewer controls.
- The causal localization story (9-row repair → LoRA Q/V → DPS) is unusually clean and well-structured.
- The negative controls on MMLU/GSM8K are a level of rigor that many accepted papers lack.

**Compared to strong ICLR accepts:**
- The task scope is narrower than ideal—primarily synthetic counting with extensions to related aggregation tasks. Strong accepts often demonstrate insights on more diverse, naturalistic benchmarks.
- The core insight (models encode information they can't express) builds on well-established ideas in mechanistic interpretability. The novel contribution is the specific geometric characterization and causal validation, which is meaningful but not a conceptual breakthrough.

**Would at least two reasonable reviewers score this ≥5?** Yes. The experimental quality, clear narrative, and honest scoping make this a solid submission. The synthetic task focus might cause one reviewer to score it 4, but the converging evidence and cross-model validation should push most reviewers to 5–6.

---

## 5) Weakest Link Analysis

**The single issue most likely to flip accept/reject: task scope and ecological validity.**

The core experiments are on synthetic counting prompts. While the paper extends to character counting, addition, list length, majority vote, max extraction, and natural-language counting, all are controlled aggregation tasks where the answer is a single token from a small set. The MMLU/GSM8K negative controls show the effect is *specific* to such tasks—which is scientifically clean but also scopes the contribution narrowly.

A skeptical reviewer might ask: "If this bottleneck only manifests on low-vocabulary aggregation tasks, how important is the finding?" The paper's defense—that the diagnostic pipeline generalizes to any task with a similar geometric structure—is reasonable but predictive rather than demonstrated.

**Classification:** Addressable in revision (additional task families, more naturalistic settings). **Unlikely to change the outcome** given the paper's honest scoping and the strength of evidence within the demonstrated scope.

---

## 6) Convergence Test (Minimal-Change Threshold)

**If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?**

**Yes, marginally.** The paper is well-executed, clearly written, and makes a genuine contribution. The experimental rigor exceeds the median ICLR submission. However, the synthetic task focus and the somewhat narrow scope place it in the borderline accept zone where reviewer variance is high.

**Minimal change to push over threshold:** Add one experiment demonstrating the bottleneck (or its absence) on a more naturalistic task where the answer is not a single digit—for example, extractive QA or structured prediction where the output is a short span. This would test whether the "low-vocabulary aggregation" scope boundary is sharp or gradual, significantly strengthening the paper's significance argument.

---

## 7) Structural Sharpness & Scope Control

**The paper is well-centered on one dominant contribution:** the geometric readout bottleneck diagnosis and its causal validation.

**(a) Strengthens core argument:**
- The factorial prompt design (prevents shortcuts)
- The three-intervention pipeline (9-row → LoRA Q/V → DPS)
- Negative controls on MMLU/GSM8K
- Cross-model validation
- Logit-lens mechanistic analysis
- The gradient dynamics explanation for why orthogonality arises

**(b) Neutral:**
- The instruct-mode and natural-language extensions (good to have but don't change the core story)
- The multi-digit extension (10–20 counts)

**(c) Potential attack surface:**
- The CoT comparison paragraph in the Discussion is somewhat discursive—it raises questions (does CoT improve alignment?) without answering them. This is minor but could invite reviewer criticism.
- The majority vote and max extraction results in the appendix, while supportive, dilute the narrative slightly. They would be stronger as a brief main-text mention rather than appendix-only.

**Scope is well-controlled.** The paper does not overextend—it explicitly scopes to low-vocabulary aggregation and acknowledges limitations. The main text is focused; the appendix provides depth without cluttering the narrative.

---

## 8) ICLR Formal Scores

**Soundness (3/4):** Claims are well-supported by converging evidence (probes, cosine alignment, logit lens, interventions, controls). The gradient dynamics argument for why orthogonality arises is suggestive but not formally proven. Minor gaps in explaining the entity-counting repair ceiling. No fatal methodological issues.

**Presentation (4/4):** Exceptionally well-written. The narrative arc (diagnosis → verification → intervention → scope) is clear and compelling. Figures and tables are informative and well-designed. Protocol mapping table (Appendix Table A1) is a thoughtful inclusion. The paper is a model of clear scientific writing for mechanistic interpretability.

**Contribution (3/4):** Novel geometric characterization of a well-known failure mode, with clean causal validation. The specific finding that count-encoding directions are orthogonal to digit rows—and that this is a stable fixed point of training dynamics—is new and well-supported. The diagnostic pipeline (probe → alignment → intervention) is reusable. Builds on established tools rather than introducing fundamentally new methods.

**Significance (3/4):** The finding has clear implications for understanding LLM failures and for practical intervention (LoRA Q/V). The diagnostic strategy generalizes conceptually. However, the demonstrated scope is limited to low-vocabulary aggregation tasks, and the practical impact of the LoRA intervention (83.1% on counting) is modest in the broader LLM landscape. The insight that "models know more than they can say" is important but not entirely new.

**Overall (6/10):** Clear accept. Comfortably above the poster mean (5.35). The experimental rigor, converging evidence, and clean causal story place this in the top ~15–20% of submissions. The synthetic task scope and the building-on-known-foundations nature of the contribution prevent a higher score, but the execution quality is above average for accepted work.

**Confidence (4/5):** Confident. The paper is technically sound, well-presented, and the claims are well-calibrated to the evidence. I have reviewed the methodology carefully and find no major issues. Minor uncertainty about the generalizability beyond low-vocabulary aggregation tasks.

---

## 9) Final Recommendation

**Accept (6/7)**

This is a well-executed mechanistic interpretability paper that identifies a specific, causally validated geometric bottleneck behind transformer counting failures. The experimental design is above average for ICLR—converging evidence streams, proper controls, cross-model validation, and honest scoping. The presentation is excellent. The main limitation is the synthetic task focus, which scopes the contribution to low-vocabulary aggregation tasks; this is typical of accepted mechanistic studies but prevents the paper from reaching the significance level of a top-5% contribution. At least two of three reasonable reviewers would likely score this ≥5, making acceptance probable though not certain.
```

#### Run 2
```
# Review: "Why Transformers Fail at Counting and How to Fix It"

---

## 1) Core Thesis & Significance

The paper argues that transformer counting failures are not due to missing internal representations (linear probes achieve R² > 0.99) but rather a **geometric readout bottleneck**: the subspace encoding counts is nearly orthogonal to the output head's digit-token rows (|cos| ≤ 0.032, indistinguishable from random). The authors support this with three converging interventions—9-row lm_head repair (constrained decoding), LoRA Q/V (autoregressive generation), and Diagnostic Probe Steering (analytical bypass)—plus logit-lens measurements showing the correct digit's rank drops from ~56K to 1 after routing correction.

The problem is practically relevant: counting is a basic capability that frontier models fail at, and understanding *why* is important for both interpretability and capability improvement. The novelty is integration-level: combining probes, geometric analysis, logit-lens, and targeted interventions into a coherent diagnostic pipeline. A reviewer could summarize the contribution unambiguously: "Models encode counts perfectly but the output head cannot read them out due to geometric orthogonality, which can be diagnosed and partially fixed."

---

## 2) Technical Soundness

**Theoretical claims.** The orthogonality claim is well-supported with bootstrap CIs, permutation tests (p = 0.79 vs. random), and TOST equivalence testing across four probe types and three model families. The gradient-dynamics explanation for *why* orthogonality arises (digit rows are optimized for non-counting contexts, making orthogonality a stable fixed point) is plausible and partially tested via fine-tuning experiments (3.2× vs. 1.1× alignment change for counting vs. arithmetic fine-tuning).

**Methodological gaps, classified:**

- **(b) Significant concern:** The 9-row repair achieves only 60.7% on entity counting despite probe-round being 98.7%. The authors attribute the 37pp gap to norm competition and hidden-state diversity, but these two factors are not disentangled experimentally. The capacity ablation (Adam fine-tuning: 67.5%; 59-row expansion: no improvement) rules out fitting artifacts but doesn't isolate the causal contribution of each factor. This is the weakest link in the causal chain.

- **(b) Significant concern:** Pythia-410M repair reaches only 31.4%, and the authors scope the repair claim to "mid-size and larger models." This is honest but means the geometric bottleneck diagnosis is most actionable only above a certain scale threshold, which is not well-characterized.

- **(c) Typical limitation:** The gradient-dynamics explanation for orthogonality is supported by one pair of fine-tuning runs with slightly different starting checkpoints (0.0074 vs. 0.0087). The relative change is informative, but the absolute starting-point difference weakens the comparison slightly. This level of evidence is common in accepted mechanistic interpretability work.

- **(c) Typical limitation:** The soft DPS failure under the multi-seed protocol (13.2%) vs. success under single-seed (96.3%) is attributed to protocol differences (diverse templates). This is explained but suggests the intervention is sensitive to prompt distribution, which limits its utility as a diagnostic tool.

---

## 3) Empirical Rigor

**Sufficiency of experiments.** The paper presents a well-structured experimental program: probes → geometric analysis → logit-lens → causal interventions → cross-model/task validation → negative controls. Each claim has at least two independent lines of evidence.

**Baselines.** Appropriate: random-direction controls, shuffled-row controls, random-position controls, permutation tests. The MMLU/GSM8K negative controls are important and well-chosen—they show the bottleneck is specific to low-vocabulary aggregation, not a universal property.

**Trade-offs.** Well-quantified: the paper clearly distinguishes constrained next-token (diagnostic) from autoregressive generation (deployable), and reports parameter counts for each intervention (36K for 9-row, 7.67M for LoRA Q/V, 4K for DPS).

**Overclaiming.** The paper is generally careful. The claim "the model knows the count" is slightly strong—probes can decode counts, but this is a statement about linear decodability, not necessarily about the model's functional access. However, the causal interventions (DPS matching probe-round exactly) partially justify this language. The scope boundaries are explicitly stated.

**Minor concern:** The LoRA Q/V multi-task generation variance is notable (71.5%–89.0%, σ = 7.2%). The authors attribute this to task-mix artifacts and show entity-only per-seed results (97.0%, 96.5%, 94.5%), which is reassuring but the multi-task variance deserves more discussion—is the model learning task-specific routing that sometimes conflicts?

---

## 4) Competitive Realism Check

This paper is well-calibrated for ICLR. It presents a clear mechanistic finding with converging evidence, honest scoping, and practical implications. The experimental design is more thorough than many accepted interpretability papers: multiple models, multiple tasks, multiple evaluation modes, negative controls, and necessity/sufficiency checks.

Compared to typical accepted ICLR papers:
- The weaknesses (60.7% entity counting gap, Pythia limitation) are within the variance of accepted work.
- The strengths (clean causal localization, striking logit-lens rank improvement, cross-model validation) exceed the median poster.
- The paper does not claim SOTA on counting—it claims to *explain* counting failure, and it does so convincingly.

Would at least two reasonable reviewers score this ≥ 5? Yes. The paper has a clear thesis, strong evidence, and honest limitations. A reviewer focused on mechanistic interpretability would find the geometric diagnosis novel and well-supported. A reviewer focused on practical impact would find the LoRA Q/V intervention meaningful.

---

## 5) Weakest Link Analysis

The single issue most likely to flip accept/reject is the **60.7% entity counting ceiling for the 9-row repair**. This is the headline diagnostic result, and the 37pp gap from the probe-round ceiling (98.7%) is substantial. The authors offer two explanations (norm competition, hidden-state diversity) but do not disentangle them. If a reviewer interprets this gap as evidence that the bottleneck is *not* fully localized to the output head—i.e., that there is also an encoding-side problem—the core thesis weakens.

However, this is **addressable in revision**: a controlled experiment varying prompt diversity at fixed count values (as the authors suggest in their limitations) could isolate the two factors. Moreover, the LoRA Q/V result (83.1% generation) independently confirms the bottleneck is primarily in routing, not encoding. The 9-row repair is explicitly framed as a diagnostic instrument, not the deployable fix.

**Decision-stable:** The LoRA Q/V and DPS results independently support the core thesis even if the 9-row repair ceiling is imperfectly explained.

---

## 6) Convergence Test (Minimal-Change Threshold)

**If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?**

Yes. The paper has a clear thesis, strong converging evidence, good experimental design, and honest scoping. The main weakness (60.7% entity counting gap) is acknowledged and partially explained. The paper is above the poster mean in contribution quality and experimental rigor.

**What minimal change would push it over the threshold?**

The single highest-value addition would be a controlled experiment disentangling norm competition from hidden-state diversity for the entity counting gap—e.g., holding prompt diversity fixed while varying count values, or measuring intra-class variance per count value and correlating it with per-count repair accuracy (Table 13 in the appendix already provides per-count data; a regression analysis would be straightforward). This would close the one remaining gap in the causal story.

---

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant contribution: the geometric readout bottleneck diagnosis. Content is well-organized:

- **(a) Strengthens core argument:** Probe analysis, cosine alignment, logit-lens, 9-row repair, LoRA Q/V, negative controls, cross-model validation. All directly support the thesis.
- **(b) Neutral:** The majority-vote and max-extraction extensions are interesting but somewhat redundant—they confirm the same bottleneck on slightly different tasks without adding mechanistic insight.
- **(c) Introduces new attack surface:** The multi-digit extension (counts 10–20) is mentioned briefly but the 42.1% fullvocab repair result is not well-integrated into the main narrative. It raises questions about multi-token output that the paper doesn't fully address.

**Scope is well-controlled.** The authors explicitly limit claims to low-vocabulary aggregation tasks and single-token outputs. The discussion section honestly identifies open questions (frontier scale, encoder-decoder architectures, CoT mechanism). No scope reduction is needed—the paper is already focused.

---

## 8) ICLR Formal Scores

- **Soundness (4):** Excellent. Multiple converging lines of evidence, rigorous statistical testing (permutation tests, TOST equivalence, bootstrap CIs), necessity/sufficiency controls, and cross-model validation. The methodology is thorough and the claims are well-supported.

- **Presentation (3):** Good. The paper is well-organized with a clear narrative arc (diagnosis → verification → intervention → scope). The unified evaluation table (Table 1) is effective. Some figures are referenced but not included in the provided manuscript (pipeline.pdf, fig3_probe_r2_gap.pdf, logit_lens_depth.pdf), which limits full assessment. The writing is clear but occasionally dense.

- **Contribution (3):** Good. The geometric readout bottleneck is a novel and well-supported mechanistic finding. The diagnostic pipeline (probe → alignment → targeted repair) is a useful methodological contribution. The integration of multiple interpretability tools into a coherent diagnosis is valuable.

- **Significance (3):** Good. The finding has implications for understanding transformer failures beyond counting—the diagnostic framework could apply to other "competence without performance" failures. The practical LoRA Q/V intervention is meaningful. However, the scope is limited to low-vocabulary aggregation tasks, and the broader impact on model capabilities is not yet demonstrated.

- **Overall (6):** Clear accept. The paper presents a well-executed mechanistic study with a clear thesis, strong evidence, and honest scoping. It is comfortably above the poster mean (5.35) and would be a solid poster at ICLR. The contribution is not paradigm-shifting but is a meaningful advance in understanding transformer failures.

- **Confidence (4):** Confident. The experimental design is thorough and the claims are well-supported. I have reviewed the methodology carefully and find it sound. Minor uncertainty about the 60.7% entity counting gap and the Pythia limitation, but these are acknowledged by the authors.

---

## 9) Final Recommendation

**Accept (6).** This is a well-executed mechanistic interpretability paper that identifies a specific geometric mechanism for transformer counting failures. The experimental evidence is strong and converging: probes, cosine alignment, logit-lens, causal interventions, and negative controls all point to the same conclusion. The paper is honest about its limitations (60.7% entity counting gap, Pythia limitation, narrow task scope) and the core thesis is well-supported. The contribution is above the ICLR poster mean and would be a valuable addition to the mechanistic interpretability literature. The main weakness—the unexplained 37pp gap in entity counting—is acknowledged and partially addressed, and does not undermine the central claim.
```

#### Run 3
```
# Review: "Why Transformers Fail at Counting and How to Fix It"

---

## 1) Core Thesis & Significance

The paper advances a single, clearly articulated thesis: transformers fail at counting not because they lack internal count representations (linear probes achieve R² > 0.99 at every layer), but because the count-encoding subspace is geometrically orthogonal to the output head's digit-token rows (|cos| ≤ 0.032, indistinguishable from random). This "readout bottleneck" is diagnosed via probe–alignment analysis and confirmed through three causal interventions of increasing scope: a 9-row lm_head repair (constrained decoding), Diagnostic Probe Steering (oracle bypass), and LoRA Q/V fine-tuning (upstream routing correction achieving 83.1% autoregressive generation).

The problem is practically relevant — counting is a well-documented, embarrassingly simple failure mode of frontier LLMs. The novelty is at the mechanism level: the paper does not merely document the failure but provides a geometric explanation with falsifiable predictions (digit-row repair should fix constrained decoding but not generation; upstream routing correction should fix both). A reviewer can summarize the contribution unambiguously.

---

## 2) Technical Soundness

**Strengths:**
- The probe analysis is rigorous: ridge regression with R² > 0.99 across all layers, validated with shuffled-label controls (R² = −0.042), four probe types (ridge, LDA, mean-difference, PCA), and bootstrap confidence intervals.
- The cosine alignment analysis includes permutation tests (p = 0.79), TOST equivalence testing, and a positive control (probe for predicted continuation token achieves |cos| = 0.115, 3.3× higher).
- The causal interventions are well-designed: necessity/sufficiency controls (shuffled-digit rows degrade below baseline; random-position rows match baseline), capacity ablations (Adam vs. ridge, 9 vs. 59 rows), and locus ablations (Q/K/V/O/MLP separately).
- The explanation for why orthogonality arises (gradient dynamics push digit rows toward non-counting contexts, creating a stable fixed point) is supported by fine-tuning experiments showing counting data raises |cos| by 3.2× while arithmetic data does not.

**Concerns:**
- **(b) Significant concern:** The soft DPS failure in the multi-seed protocol (13.2% vs. 96.3% in single-seed) is attributed to protocol differences (diverse templates causing non-digit tokens to win full-vocabulary argmax). This is plausible but the paper could be more explicit about what changed and why the soft boost magnitude (α=5.0) was insufficient. The hard DPS (α=100 or α=20) resolves this, but the soft DPS discrepancy weakens the claim that the probe direction alone is sufficient.
- **(c) Typical limitation:** The entity counting 9-row repair gap (60.7% vs. probe-round 98.7%) is partially explained by norm competition and hidden-state diversity but not fully resolved. The paper is honest about this.
- **(c) Typical limitation:** The Pythia-410M 9-row repair (31.4%) limits the cross-model claim at small scale. The paper scopes this appropriately.

No fatal flaws identified.

---

## 3) Empirical Rigor

The experimental design is strong:
- **Multiple seeds:** 3–5 seeds per headline result, with between-seed standard deviation reported.
- **Multiple tasks:** Entity counting, character counting, addition, list length, plus extensions (majority vote, max extraction, multi-digit counts).
- **Multiple models:** Qwen3-8B, Mistral-7B, Pythia-410M, Qwen3-14B.
- **Multiple scales:** 0.4B–14B.
- **Negative controls:** MMLU (|cos| = 0.31–0.48, no bottleneck) and GSM8K (no bottleneck). DROP shows partial bottleneck (+10pp).
- **Factorial benchmark design:** Counts, distractors, passage lengths, and mention spacings varied independently to prevent distributional shortcuts.
- **Protocol transparency:** Table mapping every metric to its protocol; consistent scoring (final integer for generation).

**Concerns:**
- The paper does not compare against chain-of-thought quantitatively in a controlled experiment. The discussion section addresses CoT mechanistically, but a direct accuracy comparison under the same prompts/seeds would strengthen the practical positioning.
- The LoRA Q/V multi-task variance (71.5–89.0%) is explained as a task-mix artifact, but the entity-only per-seed numbers (97.0%, 96.5%, 94.5%) are only reported in a table footnote. This is a key result that deserves more prominence.
- The natural-language counting extension (8 entity categories × 8 templates) reports probe-round 96.3% vs. 88.7% baseline but does not report the 9-row repair or LoRA Q/V results for this setting.

These are minor gaps, not decision-relevant weaknesses.

---

## 4) Competitive Realism Check (Calibrated)

Compared to typical accepted ICLR papers:
- **Above average:** The paper has a clean research question, multiple converging lines of evidence, cross-model/cross-task validation, negative controls, and honest scope limitations. The experimental methodology is more thorough than many accepted interpretability papers.
- **At average:** The task scope is narrow (low-vocabulary aggregation). The practical impact of the interventions is limited (LoRA Q/V requires fine-tuning; 9-row repair doesn't work in generation).
- **Below average:** No frontier-scale validation (70B+). No comparison with CoT under controlled conditions.

The weaknesses are within acceptance variance for ICLR poster papers. At least two reasonable reviewers would likely score this ≥5. The paper's strength is in the mechanistic clarity and experimental rigor, not in dominant SOTA performance.

---

## 5) Weakest Link Analysis

The single issue most likely to flip accept/reject is the **narrow task scope**. The paper demonstrates the geometric readout bottleneck only for low-vocabulary aggregation tasks (counting, addition, list length). The negative controls (MMLU, GSM8K) show the effect is *absent* from broader reasoning, but they don't show the diagnostic *strategy* generalizes to other "competence without performance" failures. A reviewer could argue the contribution is a well-executed case study rather than a general finding.

However, this is **addressable in revision**: the paper already has partial evidence (majority vote, max extraction, multi-digit counts, DROP) that could be expanded. The diagnostic strategy (probe → alignment → targeted repair) is explicitly proposed as generalizable, and confirming it on 1–2 additional task families would significantly strengthen the claim.

This issue is **unlikely to change the outcome** — the paper is strong enough to accept as a focused mechanistic study.

---

## 6) Convergence Test (Minimal-Change Threshold)

**If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?**

Yes. The paper has a clear contribution, strong experimental methodology, and honest scope limitations. The weaknesses (narrow task scope, no frontier-scale validation) are typical of accepted interpretability papers.

**What minimal change would push it over the threshold?**

The paper is already above the threshold. If forced to suggest one change: add a controlled CoT comparison under the same prompts/seeds/scoring protocol. This would address the most obvious gap in the related work discussion and provide a practical benchmark for the LoRA Q/V intervention.

---

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant contribution: the geometric readout bottleneck diagnosis. Content analysis:

- **(a) Strengthens core argument:** Probe analysis, cosine alignment, 9-row repair, LoRA Q/V, logit-lens analysis, negative controls, cross-model validation, factorial benchmark design.
- **(b) Neutral:** The mechanistic explanation for why orthogonality exists (training dynamics section). Interesting but not essential to the core claim.
- **(c) Introduces new attack surface:** The soft DPS discrepancy (13.2% vs. 96.3%) and the entity counting gap (60.7% vs. 98.7%) are honestly reported but create openings for skeptical reviewers. The paper handles these well with additional experiments (hard DPS, capacity ablations).

The paper is not overextended. The scope is appropriate for the contribution.

---

## 8) ICLR Formal Scores

**Soundness (3):** Claims are well-supported by multiple lines of evidence (probes, cosine alignment, causal interventions, negative controls). The methodology is rigorous with proper controls and ablations. The soft DPS discrepancy and entity counting gap are minor blemishes, not fundamental issues.

**Presentation (3):** Well-organized with clear narrative flow. Tables and figures are informative. The paper is dense but readable. The protocol map (Table in appendix) is a good practice. Some results could be given more prominence (e.g., entity-only LoRA Q/V per-seed numbers).

**Contribution (3):** Novel geometric diagnosis of a well-known failure mode. The causal localization via 9-row repair is elegant. The mechanistic explanation (training dynamics) adds depth. The diagnostic strategy (probe → alignment → targeted repair) is potentially generalizable.

**Significance (3):** The finding that counting failure is a geometric readout bottleneck is memorable and will interest the interpretability community. The diagnostic strategy could apply to other "competence without performance" failures. However, the task scope is narrow and the practical impact of interventions is limited.

**Overall (6):** Clear accept. Comfortably above the poster mean (5.35). The paper has a clean research question, strong experimental methodology, novel mechanistic insight, and honest scope limitations. The weaknesses (narrow task scope, no frontier-scale validation) are within acceptance variance.

**Confidence (4):** Confident. I've read the paper carefully, the methodology is clear, and the results are well-presented. I may have missed some subtleties in the geometric analysis, but the core claims are well-supported.

---

## 9) Final Recommendation

**Accept (6)**

This paper provides a clean, well-executed mechanistic study of counting failures in transformers. The geometric readout bottleneck diagnosis is novel, supported by multiple converging lines of evidence, and honestly scoped. The experimental methodology is more thorough than many accepted interpretability papers, with proper controls, ablations, and cross-model validation. The weaknesses (narrow task scope, no frontier-scale validation) are typical of accepted work and do not undermine the core contribution. The paper would be a solid poster at ICLR.
```

### GLM 5.3

#### Run 1
```
# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: Compliant as far as visible. Authors are anonymized; no repo links, no acknowledgments, no self-revealing phrasing. (The LaTeX comment `% NeurIPS 2026 style` is invisible in the compiled PDF and not a violation, though it should be cleaned up.)
- **Page limit**: **Cannot verify from source.** The main-text density (8 sections, 7+ tables, 3 figures) is at real risk of exceeding 9 pages; authors should verify. Core evidence does appear to live in the main text.
- **AI use statement**: Present and appropriately scoped. ✓
- **Style files**: `iclr2027_conference` package with `article` class — the standard ICLR pattern. ✓

No desk-reject flags, subject to page-count verification.

---

## 1) Core Thesis & Significance

The paper argues that transformer counting failure is a **geometric readout bottleneck**: counts are linearly encoded in the residual stream (probe R² > 0.99) but the encoding directions are statistically indistinguishable from orthogonal to the `lm_head` digit rows (|cos| ≤ 0.032, matching a random-direction baseline). Three interventions triangulate the claim: a 9-row `lm_head` repair (36,864 params) fixes constrained decoding but not generation; probe-based steering (DPS) bypasses the head analytically; LoRA on attention Q/V (7.67M params) corrects upstream routing and reaches 83.1% ± 7.2% in true greedy generation, with logit-lens rank of the correct digit dropping from 55,980 to 1.

The problem is practically relevant (counting failures are a widely discussed LLM pathology) and the contribution is a clean, falsifiable mechanistic diagnosis with causal verification — the kind of contribution a reviewer can summarize unambiguously. Novelty is component-level (probes, logit lens, targeted fine-tuning are standard tools) but the integration — quantifying encoding-vs-readout geometry and repairing at three distinct loci — is genuinely insightful and goes beyond prior counting work (Razeghi et al., Stolfo et al.), which localized failures without identifying the geometric cause.

## 2) Technical Soundness

The core claims are unusually well-supported. The factorial prompt design independently randomizes count, distractors, length, and spacing, closing the distributional-shortcut loophole for probes. Controls are above venue standard: shuffled-label probes (R² ≈ 0), random-direction cosine baselines with permutation tests and TOST equivalence, a positive control (continuation-token probe achieves |cos| = 0.115, 3.3× the count probe), shuffled-row and random-position necessity controls, negative controls on MMLU/GSM8K, locus ablations for LoRA, and capacity ablations for the row repair.

**Issue classification:**

- **(a) Fatal flaws**: None.
- **(b) Significant concerns (decision-relevant, fixable):**
  1. **Cross-table protocol inconsistency for the same intervention.** The 9-row repair appears as 60.7% ± 3.1% (unified table, entity counting), 93.8% held-out (Table 5), and 99.9% (instruct mode) — with no in-text reconciliation. Baseline appears as 13.7%, 11.3%, and 17.0% (appendix). The paper's protocol map is commendable, but a reader cannot currently determine which number is canonical for the row repair. This invites cherry-picking suspicion the paper probably doesn't deserve (the headline claims use the *conservative* multi-seed numbers), but it must be fixed.
  2. **The flagship-task repair ceiling (60.7%) is labeled, not explained.** "Task-level ceiling" is a restatement. The stratified table (30.6% at count 7, 100% at count 2, 71.9% at count 9) shows non-monotonic, unstable decision boundaries between adjacent digits — under-analyzed.
  3. **A numeric inconsistency at 14B**: |cos| = 0.011 claimed as "0.57× random baseline" implies a baseline of ~0.019, but for 5120-dim hidden states the expected E[|cos|] for random directions is ≈ 0.011 (and the paper's own 8B measurement, 0.013 ± 0.011 in 4096 dims, matches theory). The "scale sharpens the bottleneck" claim needs this arithmetic checked.
  4. **Minor text–table mismatch**: "Probe R² exceeds 0.99 at every layer" vs. layer 0 = 0.977 in Table 2.
- **(c) Typical limitations**: probe-direction ≠ unique encoding direction (mitigated by four probe types and the causal DPS result); Pythia-410M repair transfer failure (honestly scoped); scale capped at 14B; the orthogonality-as-fixed-point argument is a verbal model with supportive but not rigorous evidence.

## 3) Empirical Rigor

Broadly sufficient and above average. Multi-model (4 models, 3 families, 0.4B–14B), multi-task (4 primary + 3 extension tasks), multi-seed with reported per-seed values, and a genuinely unified evaluation table. The logit-masked generation control (59.2%, matching constrained accuracy) is an elegant confirmation that the row repair encodes the right answer and the generation failure is routing. The LoRA mechanism analysis (probe direction unchanged at layer 2; final-layer R² 0.974 → 0.998; logit-lens 9.3% → 71.8%) directly supports the routing interpretation.

**Gaps:**

- **CoT accuracy is never reported in the main text** under the paper's own corrected final-integer scorer, despite CoT being invoked as a comparable intervention. For a paper whose deployable fix scores 83.1%, this number belongs in the main text. "Substantially improves" is not evidence.
- **Addition is weak evidence for generality**: baseline is already 93.3%, so the "bottleneck" there is worth ≤ 7 pp. Including it in the abstract's generality claim is a stretch.
- **External validity is thinner than the title suggests.** On DROP the probe-round improvement is +10 pp (20% → 30%); on natural-language counting the baseline is already 88.7%. The bottleneck is large and well-characterized on the *synthetic* distribution the authors designed, and much smaller on natural text. The title "Why Transformers Fail at Counting" is broader than the demonstrated effect; the paper's own scope statements are more honest than its title.
- Reproduction details (learning rates, batch sizes, LoRA data mixture, the 200/300 training steps) are not in the main text.

**Overclaiming check**: confined to the title/framing and the two flagged numeric statements. The body's claims are carefully scoped and mode-labeled — notably the candid admission that the 9-row repair achieves 0.0% in generation.

## 4) Competitive Realism Check

Compared to typical accepted ICLR mechanistic-interpretability papers, this one has *more* controls than most (negative controls on standard benchmarks are rare; necessity/sufficiency controls are rare; mode-matched protocol harmonization is rare). The weaknesses — synthetic-task focus, protocol sprawl, a partially unexplained flagship gap — are within acceptance variance. The "knows the count but can't say it" dissociation, quantified geometrically and verified causally at three loci, is a memorable finding that the interpretability community will cite. I would expect at least two reasonable reviewers to score ≥ 5, with clustering around 5–7.

## 5) Weakest Link Analysis

The **single most decision-relevant issue is the cross-table protocol inconsistency** (60.7% vs. 93.8% vs. 99.9% for the 9-row repair; multiple baselines). A careful reviewer reading Table 5 next to Table 1 cannot tell which measurement is authoritative, and this is exactly the pattern that triggers a downgrade from "solid" to "suspicious." It is **addressable in revision** (annotate every table row with its protocol; add one reconciliation paragraph) and **unlikely to be fundamental** — the conservative numbers already support the headline claims. Secondary: missing CoT number in the main text (addressable).

## 6) Convergence Test

- **With no further changes**: I estimate a ~50–60% acceptance chance — the empirical substance is above the poster bar, but the protocol ambiguity and missing CoT baseline give a skeptical reviewer room to push to 4–5.
- **Minimal change to clear the threshold**: (i) a protocol reconciliation pass making every accuracy number's mode/N/seeds explicit at point of use (one table or per-row annotations); (ii) the CoT baseline number under the final-integer scorer in the main text; (iii) one paragraph explaining or explicitly flagging the instruct-mode 99.9% vs. base-mode 60.7% repair discrepancy, and correcting the 14B "0.57×" arithmetic. These are evidence-presentation changes, not new experiments, and would make this a comfortable accept.

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant contribution: the geometric readout bottleneck, diagnosed and causally verified.

- **(a) Strengthens**: unified evaluation table; necessity/sufficiency controls; logit-masked generation control; LoRA mechanism measurements; MMLU/GSM8K negative controls (rare and valuable for scoping); multi-digit extension (tests the token-level claim).
- **(b) Neutral**: majority vote and max extraction (generality evidence; could be compressed to one paragraph each).
- **(c) Attack surface**: the single-seed soft-DPS pilot (96.3%) that collapses to 13.2% under the harmonized protocol. The appendix discloses this honestly, but the narrative would be tighter — and less vulnerable — if presented as "pilot experiment that motivated protocol harmonization" rather than a headline result requiring an explanatory footnote. The title is also mild attack surface relative to the DROP/NL evidence; consider scoping it ("A Geometric Readout Bottleneck in Transformer Counting").

## 8) ICLR Formal Scores

- **Soundness (3/4)**: Claims are supported by an unusually strong control suite (permutation tests, TOST, shuffled controls, negative controls, causal interventions). Held below 4 by unreconciled cross-table numbers, the unexplained 60.7% flagship ceiling, and two checkable numeric inconsistencies (14B baseline ratio; layer-0 R²).
- **Presentation (3/4)**: Dense but organized, with numbered claims, mode labels, and a protocol map. Docked for protocol sprawl that forces the reader to reconstruct which measurement supports which claim, and for the unexplained instruct/base repair discrepancy.
- **Contribution (3/4)**: A crisp, novel-in-combination diagnosis — orthogonal-to-unembedding encoding with causal repair at three loci — that advances beyond prior counting localization work. Tools are standard; the insight is not.
- **Significance (3/4)**: Addresses a widely recognized failure mode with a memorable, quotable finding and a generalizable diagnostic recipe (probe → measure alignment → targeted repair). Practical deployment impact is moderate (CoT already fixes counting at inference cost), but the mechanistic clarification of *why* CoT helps is valuable.
- **Overall (6/10)**: Clear accept. Comfortably above the poster mean (5.35) on experimental substance; not at 7 because external validity on natural text is materially weaker than the synthetic evidence and the flagship-task repair result remains partially unexplained; not at 5 because the control rigor and causal completeness exceed the typical accepted mech-interp paper.
- **Confidence (4/5)**: The analysis is self-contained and I checked internal consistency of the headline numbers (they reconcile, with the flagged exceptions); I could not inspect figures or the referenced supplement.

## 9) Final Recommendation

**Accept (6).**

This is a well-controlled mechanistic study with a clean causal story and a memorable finding; its weaknesses (protocol sprawl, synthetic-task concentration, a partially explained repair ceiling) are the kind that accepted ICLR papers routinely carry and that a rebuttal can largely neutralize. With protocol reconciliation and the CoT number in the main text, I would not be surprised to see this score 7 from other reviewers; as submitted, 6 is the defensible calibrated rating.
```

#### Run 2
```
# Review: "Why Transformers Fail at Counting and How to Fix It"

**Desk-Reject Compliance Check:**
- **Anonymity**: ✅ Anonymous authors, no self-identifying links, citations in third person. No violations found.
- **Page limit**: ⚠ Cannot verify precisely from source, but main text density (7 sections, 5 tables, 3 figures) suggests it is at or near the 9-page limit. Authors should confirm.
- **Style files**: ✅ Uses `iclr2027_conference` (the "NeurIPS 2026" comment on line 3 is stale and should be removed, but the actual package is correct).
- **AI use statement**: ✅ Present, and properly scoped.

No desk-reject risk items identified.

---

## 1) Core Thesis & Significance

The paper argues that transformer counting failures are a *geometric readout bottleneck*: counts are linearly encoded in the residual stream (probe R² > 0.99) but the encoding directions are statistically indistinguishable from random relative to the `lm_head` digit rows (|cos| ≤ 0.032). The claim is causally localized by a minimal 9-row repair of the output head (fixes constrained decoding, fails in generation), and a LoRA Q/V intervention is shown to repair upstream routing, restoring 83.1% true autoregressive generation accuracy.

The problem is practically relevant (counting failures are among the most widely recognized LLM failure modes), the framing is crisp, and the contribution is unambiguous and summarizable in one sentence: *the model knows the count but the output head can't read it out.* Novelty is component-level (probes, logit lens, targeted repair are all established tools) but the combination — orthogonal-encoding diagnosis + minimal causal repair + negative controls on non-counting benchmarks — is a genuinely new, memorable result.

## 2) Technical Soundness

The core methodology is sound and unusually well-controlled for this literature: shuffled-label probes, random-direction cosine baselines with permutation tests and TOST equivalence, shuffled-row and random-position necessity/sufficiency controls, multi-seed reporting, and a locus ablation for the LoRA intervention. The falsifiable-prediction structure (row-repair fixes constrained but not generation; LoRA fixes both) is a strength.

Issues, classified:

**(a) Fatal flaws: none.**

**(b) Significant concerns:**
1. **Layer-0 probe R² = 0.977 is unexplained and potentially undermining.** If "layer 0" denotes the embedding output, near-perfect count decoding *before any attention aggregation* implies the probe reads a surface/distributional artifact rather than an internally computed aggregate — which would complicate the "model computes the count internally" story. If layer 0 means the first block's output, this is fine, but the convention must be stated. The definition of "entity-mean position" (mean over entity-mention positions? a single position?) is also underspecified, and this matters: with RoPE-only models, a mean over k identical entity-token embeddings at layer 0 should be count-independent, making R² = 0.977 hard to explain. This needs one clarifying paragraph.
2. **Cross-table irreconcilability.** The same method carries materially different numbers across tables: 9-row repair is 60.7% (Tables 1–2, unified protocol) but 93.8% held-out (Table 3, legacy single-seed protocol); baseline is 13.7% / 11.3% / 10.3% / 17.0% in four places; soft DPS is 96.3% (Table 5) vs. 13.2% (Table 1). The protocol map and mode labels mitigate, but the Discussion's claim that the 9-row repair "surpass[es] LoRA (84%, 4M params)" matches *no* number in the paper (LoRA is 7.67M params, 83.1%/91.7%/96.0%) and appears to compare across protocols where the unified evaluation shows the opposite ordering (LoRA 96.0% vs. 9-row 60.7% next-token). This specific sentence reads as protocol cherry-picking even if unintentional.
3. **The 14B "sharpening" arithmetic.** |cos| = 0.011 is claimed to be 0.57× the random baseline (~0.019), but the expected E|cos| for random directions scales as ~√(2/πd) ≈ 0.011 at d = 5120 — *smaller* than at 4096 (0.0125, matching your 8B baseline of 0.013), not larger. Either the 14B random baseline is measured differently (needs specification) or the "0.57× random" claim is wrong. Also, being *more orthogonal than random* is a strange configuration that is asserted rhetorically ("scale strengthens the bottleneck") without mechanistic explanation.
4. **Orthogonality is the high-dimensional default.** |cos| ≈ 0.016 in 4096-dim space is what one expects between any two unrelated directions. The paper is aware of this and the positive control (predicted-continuation probe at |cos| = 0.115, 3.3× the count probe) is the right defense — but 0.115 is still small in absolute terms, and the paper would be stronger with alignment measurements for several *expressed* features to establish the reference distribution. (Minor: the positive control section cites the count probe as 0.035 vs. the headline ≤ 0.032 — reconcile.)

**(c) Typical limitations:** the orthogonality-as-fixed-point gradient argument is heuristic; the counting-fine-tune experiment starts from slightly different checkpoints (disclosed, honestly); DPS is an oracle diagnostic, appropriately framed as such.

## 3) Empirical Rigor

Strengths: factorial prompt design with independently randomized confounds (good anti-shortcut hygiene); four tasks plus majority-vote, max-extraction, and multi-digit extensions; three model families plus a 14B scale check; MMLU/GSM8K negative controls with a plausible mechanistic signature difference (|cos| = 0.31–0.48 vs. ≤ 0.032); quantified parameter/accuracy trade-offs (36.9K vs. 7.67M vs. 622M); the logit-masked generation experiment (59.2% matching constrained accuracy) is an elegant diagnosis of the 9-row generation failure.

Weaknesses:
1. **Addition is not evidence of a bottleneck.** Baseline is 93.3% — there is essentially no failure to explain. Citing it as support that "the bottleneck generalizes" (abstract, contributions) is a mild overclaim; it shows the repair doesn't hurt a solved task.
2. **No quantitative CoT comparison in the main text.** The Discussion devotes a paragraph to CoT but gives no number; the corrected-scorer CoT comparison is deferred to the supplement. Since "How to Fix It" is in the title, a main-text table row for CoT under the identical final-integer scorer is needed to contextualize the 83.1% LoRA result.
3. **GSM8K negative control is underexplained.** How is the "answer-relevant direction" probed for free-form numeric answers, and why would it not suffer the same digit-row orthogonality? One sentence in the main text carries this control; the details apparently live in an appendix I cannot fully evaluate.
4. The unified-evaluation N (200 prompts × 3 seeds) is adequate but modest for the headline entity-counting claims, particularly given the 7.2 pp LoRA seed spread.

Overclaiming check: the abstract and claims 1–3 are carefully scoped (the abstract honestly reports the 0.0% generation result for the row repair). The main overreach is the Discussion's cross-protocol "surpassing LoRA" sentence and the inclusion of addition as bottleneck evidence. Otherwise the claims track the evidence well.

## 4) Competitive Realism Check

Compared to typical accepted ICLR mechanistic-interpretability papers, this one has above-average control density (permutation tests, TOST, necessity/sufficiency controls, negative controls, locus ablation, multi-seed) and above-average breadth (4 models, 7+ tasks). The weaknesses — protocol fragmentation, one unexplained probe result, one analytic wobble at 14B — are the kind that cost fractions of a point, not acceptance. Papers with strong controlled ablations and honest scoping like this routinely land at 5–7. At least two reasonable reviewers would score this ≥ 5; I would expect the median review to be a 6 with one reviewer possibly at 4–5 if they are unpersuaded by the orthogonality interpretation (the "so what — everything is orthogonal in high-d" objection, which the positive control answers but not exhaustively).

## 5) Weakest Link Analysis

The single issue most likely to flip accept→reject: **protocol fragmentation and cross-table number irreconcilability**, exemplified by the Discussion's "surpassing LoRA (84%, 4M params)" claim that cannot be traced to any table and inverts under the unified protocol. A meticulous reviewer who tries to verify the headline claims against Table 1 will find that several of the paper's most quotable numbers (93.8%, 96.3% soft DPS, 97.5%) come from a legacy single-seed protocol, which creates an impression of favorable-number selection even though the unified numbers (60.7–100.0%, 83.1%) are themselves sufficient to support the thesis.

Status: **addressable in revision** — consolidate all headline numbers under the unified protocol, demote legacy-protocol numbers to a clearly-labeled appendix table, and delete or fix the "surpassing LoRA" sentence.

## 6) Convergence Test (Minimal-Change Threshold)

**If no further changes: does this have ≥50% acceptance chance at ICLR?** Yes. The core claims are each supported by mode-matched, multi-seed numbers in Tables 1–2, the controls are strong, and the limitations section is unusually honest. In my estimation this is a clear poster accept as-is.

**Minimal changes that would push it toward 7:** (i) one canonical results table with every method under the unified protocol, legacy numbers removed or explicitly quarantined; (ii) a one-paragraph explanation of the layer-0 probe result and the exact probing position definition; (iii) a main-text CoT row under the final-integer scorer; (iv) fix or justify the 14B random-baseline arithmetic. All are evidence/clarification changes, not new experiments.

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant contribution (the geometric readout bottleneck). Content audit:
- **(a) Strengthens:** logit-lens depth analysis; necessity/sufficiency controls; MMLU/GSM8K negative controls; logit-masked generation diagnosis; locus ablation for LoRA.
- **(b) Neutral:** majority vote, max extraction, multi-digit, DROP, instruct-mode results (generality checks; each adds protocol surface but they are scoped as extensions).
- **(c) New attack surface:** the *addition* task (baseline 93.3% — invites the "no failure to fix" objection); the single-seed legacy DPS protocol retained in the appendix (invites protocol-inconsistency objections); the 14B "sharpening" claim (invites the baseline-arithmetic objection). Recommendation: move addition to a one-line robustness note, label all legacy-protocol numbers as such in their captions, and either fix the 14B baseline computation or soften to "misalignment persists at 14B."

The Discussion–Conclusion sections are disciplined and the limitations section is a model of its kind.

## 8) ICLR Formal Scores

- **Soundness: 3/4.** Methods are sound with unusually strong controls; docked for the unexplained layer-0 probe result, the 14B baseline arithmetic, and one cross-protocol claim in the Discussion that the unified table contradicts.
- **Presentation: 2/4.** Prose is clear and the protocol map is a good idea, but the same quantities appear under 4+ different values across tables, at least one Discussion number (84%, 4M LoRA) matches nothing in the paper, and the central probing position ("entity-mean") is insufficiently defined for reproduction.
- **Contribution: 3/4.** The orthogonal-encoding/readout-misalignment diagnosis with minimal causal repair is a novel, crisply-stated contribution to mech-interp; the LoRA fix itself is standard PEFT but is elevated by the mechanistic verification (rank 55,980 → 1).
- **Significance: 3/4.** Addresses a widely-known failure mode with a memorable, quotable finding ("knows the count, can't say it"); likely to be cited by both interp and LLM-failure-analysis communities. Not field-shaping.
- **Overall: 6/10.** Clear accept. Comfortably above the poster mean: strong controlled experiments, broad validation, honest scoping. Held below 7 by protocol fragmentation that impedes verification and two analytic loose ends, all fixable.
- **Confidence: 4/5.** I am confident in the assessment of the presented evidence; I could not fully evaluate appendix/supplement-only details (CoT comparison, GSM8K control methodology) and cannot verify page count from source.

## 9) Final Recommendation

**ICLR: Accept (6).**

This is a well-executed mechanistic study that converts a meme-level LLM failure into a precise geometric diagnosis with causal localization, appropriate negative controls, and an honest account of what each intervention does and does not fix. The experimental substance is well above the acceptance bar; the score is capped by presentation debt — irreconcilable numbers across overlapping tables and two unexplained analytic details — that a careful revision would fully resolve. I expect this paper to be a solid, well-cited poster and would not be surprised to see it promoted if the protocol consolidation is done well.
```

#### Run 3
```
# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: ✅ Pass. Anonymous authors, no self-identifying links, prior work cited in third person.
- **Page limit**: ⚠️ Cannot verify from LaTeX source. Main-text content (Sections 1–7 + figures/tables) appears plausibly within 9 pages, but I cannot confirm the compiled length. Note that some load-bearing evidence (CoT comparison, DPS sensitivity analyses) is deferred to a "supplement" that is not part of the provided material.
- **AI use statement**: ✅ Present.
- **Style files**: ✅ Uses `iclr2027_conference` per the official template pattern. (A stale comment reads "NeurIPS 2026 style" — harmless leftover, but sloppy; also `\author{Anonymous authors\ ...}` contains a `\ `-space typo where a line break was likely intended.)

No desk-reject risks identified beyond the unverifiable page count.

---

## 1) Core Thesis & Significance

The paper asks whether transformer counting failures stem from missing internal representations or from an inability to read those representations out as output tokens. Using linear probes, logit-lens analysis, and three targeted interventions (9-row `lm_head` repair, LoRA on attention Q/V, and "Diagnostic Probe Steering"), the authors argue for a *geometric readout bottleneck*: counts are linearly decodable (R² > 0.99) but the count-encoding directions are nearly orthogonal to the digit rows of the output head (|cos| ≤ 0.032, statistically indistinguishable from random).

The problem is practically relevant (counting failures are well-documented and embarrassing), the contribution is cleanly summarizable, and the causal logic — constrained decoding should be fixed by output-row repair, generation should not, and upstream (Q/V) repair should fix both — is a genuinely falsifiable structure that the paper's experiments largely confirm. Novelty is integration-level (probes, logit lens, LoRA, and ROME-style row edits are all known tools) but the specific finding — that the misalignment is *causally* localized and repairable with 36,864 parameters under constrained decoding — is new and, to my knowledge, not established by prior counting work (Razeghi et al., Stolfo et al.).

## 2) Technical Soundness

**Strengths**: The causal logic is unusually well-instrumented: shuffled-label probes (R² = −0.042), random-direction controls, permutation tests, TOST equivalence testing, necessity/sufficiency controls (shuffled rows degrade below baseline), a locus ablation across Q/K/V/O/MLP, and negative controls on MMLU. Internal arithmetic checks out (9 × 4096 = 36,864; LoRA rank-16 Q/V ≈ 7.66M; 46,080 = 9 × 5120), which suggests genuine care.

**Concerns**:

**(b) Significant — the "knows vs. says" claim conflates three representational loci with very different decodability.** (i) The *entity-mean* aggregate (Table 3): R² ≈ 0.997, but this is a constructed multi-position average, and the reported layer-0 R² = 0.977 is a red flag — for RoPE models with a constant mention token, layer-0 states at mention positions are identical, so the mean cannot encode count unless the construction itself leaks it (e.g., via surface-form variation or position statistics). The factorial design randomizes distractors/length/spacing but does not remove count–position correlations in an averaged representation. (ii) *Last-token early layers*: claimed "R² ≥ 0.99 from layer 2" in one sentence, with no table or figure. (iii) *Last-token final layer* — the state the output head actually reads: its linear decodability is never directly reported, but the 9-row repair *is* a freely-trained linear readout from this state, and it plateaus at 60.7% (67.5% with Adam, no gain with 59 rows). If final-state linear decodability were ~99%, freely-trained rows should approach it; the paper's own "task-level ceiling" admission implies it is not. This means that for the flagship entity-counting task, the failure is *not* purely output-head geometry — count information at the readout position appears substantially degraded (~60–67%), which reframes the clean dichotomy "representation perfect / readout broken" into "partial aggregation loss + geometric misalignment." The dichotomy holds cleanly for character counting, addition, and list length (9-row repair 98–100%); it does not for entity counting, which is nonetheless the headline task. **Required: per-layer probe R² and linear classification accuracy at the last-token position (especially the final layer) for entity counting.**

**(b) Significant — the 0.0% generation result for the 9-row repair is unexplained and internally contradictory as written.** Table 1 reports the 9-row repair at 60.3% *full-vocabulary* next-token accuracy at the answer position, yet greedy generation is exactly 0.0%, and the appendix attributes this to "full-vocabulary argmax at each step is still misaligned" — contradicting Table 1's own 60.3%. A plausible confound the paper never addresses is digit tokenization variants: the 9 repaired rows are presumably bare digit tokens ("3"), while a base model's natural emission after a prompt or template is often " 3" (space-prefixed) — a *different* vocabulary row that was not repaired. The logit-masked control (59.2%) masks to the repaired token set and therefore cannot distinguish "upstream routing failure" from "wrong token variant wins." Since the constrained-vs-generation dissociation is nested Claim 2, the paper owes the reader error traces and an explicit treatment of digit-token variants. Note the repair also scores *below* the unmodified baseline (7.2% generation), which demands explanation.

**(b) Significant — cross-protocol numerical inconsistency.** The same intervention (9-row repair, held-out, Qwen3-8B entity counting) appears as 60.7% (Table 2, "mode-matched primary") and 93.8% (Table 4), and the Discussion summarizes "93–99% held-out accuracy," i.e., quoting the easier protocol while the primary protocol yields 60.7%. The Discussion also cites "LoRA (84%, 4M params)" — a configuration that appears in no table. Baseline entity-counting accuracy takes at least seven distinct values across the paper (7.2%, 10.3%, 11.3%, 13.7%, 14.2%, 17.0%, 38.6/38.8%). Soft DPS flips from 96.3% (Table 6) to 13.2% (Table 1) across protocols with only a partial reconciliation. The protocol-map appendix and "mode-matched" labels show commendable awareness, but the execution leaves the reader unable to reconstruct which number is canonical.

**(c) Typical limitations**: The probing-fallacy caveat (decodable ≠ used) is largely mitigated by the causal interventions, though see the locus issue above. The gradient-dynamics "why orthogonality" argument is a heuristic, not a proof — and the paper's own fine-tuning result (counting data raises |cos| by 3.2×) shows orthogonality is not a stable fixed point under the counting distribution, which is consistent with but weaker than the "stable fixed point" framing. GSM8K is claimed as a negative control in the abstract but no GSM8K numbers appear anywhere in the provided text. The intro's "best models achieve ≤24%" sits awkwardly beside the paper's own 38.8% stratified next-token figure. The 14B result (|cos| = 0.011, "0.57× random baseline") is *below* chance alignment, which would imply active avoidance rather than passive orthogonality — an interpretive distinction the paper glosses over.

## 3) Empirical Rigor

**Sufficient**: The core geometric claims are supported with statistics rare to see at this venue (bootstrap CIs, permutation tests, TOST). Multi-seed reporting (3–5 seeds) for headline numbers. The factorial prompt design is a serious attempt to kill distributional shortcuts. Mode-matched Table 1/Table 2 comparisons are exactly the right discipline. Trade-offs are quantified (parameters vs. accuracy; LoRA vs. CoT inference cost).

**Insufficient**: (1) The CoT comparison — central to the practical "How to Fix It" claim, since CoT requires no fine-tuning — is discussed in the main text with *no numbers* ("also substantially improves entity counting"). (2) GSM8K numbers absent. (3) No error analysis for the 0.0% generation result (see above). (4) The multi-digit claim "each digit position is independently misaligned" is asserted, not measured. (5) Real-benchmark transfer is weak and under-discussed relative to the title: DROP single-digit improves only 20.0% → 30.0%, which honestly tempers the claim that this bottleneck explains real counting failure, yet the abstract does not mention it. (6) Missing the single most decisive probe experiment (last-token final-layer classification accuracy; §2 above).

**Overclaiming check**: The abstract is accurate and appropriately hedged. The title's "How to Fix It" oversells a fix demonstrated on synthetic tasks with an 83.1% ceiling and marginal real-benchmark transfer; the body is more careful ("we are not claiming to beat CoT"). The Discussion's "93–99%" summary is selective relative to the primary protocol.

## 4) Competitive Realistic Check

Compared to typical accepted ICLR mechanistic-interpretability papers, this one is above average in controls (necessity/sufficiency, equivalence testing, locus ablations, negative controls) and in causal design, but below average in numerical hygiene and internal consistency. The memorable finding — correct digit rank dropping 55,980 → 1 under LoRA Q/V, and a 9-row repair causally restoring constrained decoding — is the kind of result reviewers repeat to colleagues. The weaknesses (protocol proliferation, unexplained 0.0%, locus conflation) are the kind that draw one low review but are addressable in rebuttal. At least two reasonable reviewers scoring ≥5: **yes, likely** — this is a plausible 5/6/6/4 review profile.

## 5) Weakest Link Analysis

**Weakest link**: the gap between the "the model knows the count" narrative and what is actually demonstrated *at the readout locus* for entity counting (~60–67% linear decodability implied by the repair ceiling, versus R² > 0.99 only at construction-assisted or early-layer loci), compounded by the unexplained 0.0% generation number. This is **addressable in revision**: it requires one additional probe table (last-token, per-layer, classification accuracy) and error traces for generation, plus a modest reframing ("partial aggregation degradation plus geometric misalignment" for entity counting). It is **not fundamental** — the orthogonality measurement, the DPS/oracle results, and the LoRA mechanism analysis stand independently — and the dissociation logic survives even if the 0.0% turns out to be a tokenization artifact (logit-masked 59.2% vs. LoRA 83.1% still separates output-head-only from upstream repair). Short of that clarification, I would not call this decision-stable; with it, the paper is comfortably acceptable.

## 6) Convergence Test (Minimal-Change Threshold)

As submitted: roughly a coin flip (~50%) — the controls and causal design argue for accept; the inconsistencies and the locus conflation give a skeptical reviewer enough to argue 4.

Minimal changes to clear the bar, in order of importance:
1. **Report last-token per-layer probe R² and final-layer linear classification accuracy for entity counting**, and reframe the "knows vs. says" claim accordingly.
2. **Explain the 0.0% generation result** with error traces and an explicit analysis of digit-token variants ("3" vs. " 3"); reconcile it with the 60.3% full-vocab next-token number.
3. **Harmonize the 9-row repair numbers** (60.7% vs. 93.8%) across Tables 1/2/4 and the Discussion; remove or define the dangling "LoRA (84%, 4M params)".
4. **Put CoT and GSM8K numbers in the main text.**

All four are evidence-based and feasible within a rebuttal cycle.

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant contribution with three nested, falsifiable claims — good structure.

- **(a) Strengthens the core**: mode-matched Tables 1–2, logit-lens section, locus ablation, MMLU negative control, necessity/sufficiency controls.
- **(b) Neutral**: majority vote, max extraction, multi-digit, 14B extensions (these support generality at modest cost).
- **(c) Adds attack surface**: the soft-DPS protocol saga (96.3% vs. 13.2%) is confusing and not load-bearing — demote to the appendix and keep only hard DPS in the main text. The "why orthogonality" gradient paragraph invites theory critique it cannot defend — either formalize or explicitly label it a conjecture. The Discussion's cross-protocol summary sentences ("93–99%", "LoRA 84%") should be rewritten against the primary protocol. The multi-digit "independently misaligned" sentence should be cut or supported. The task-definition example in §3 is ambiguous about whether numerals inside sentences are quantities to be summed or distractors to be ignored ("There are 2 apples…" with the answer defined as "the number of mentions"), which hampers reproduction.

## 8) ICLR Formal Scores

- **Soundness: 3/4.** The causal program (probes → geometry → interventions → controls) is sound and unusually well-instrumented, and most claims are supported. Docked for the locus conflation underlying the headline "knows" claim on entity counting, the unexplained/contradictory 0.0% generation number, and cross-table inconsistencies.
- **Presentation: 2/4.** Prose is clear and the claims-then-evidence structure is good, but the same quantity takes different values across tables and sections, key comparisons (CoT, GSM8K) are discussed without numbers, one task-defining example is ambiguous, and reproduction requires resolving protocol details the main text does not supply.
- **Contribution: 3/4.** A novel causal dissection of a well-documented failure mode: geometric misalignment of count directions with output rows, localized by a 9-row repair, with a deployable upstream fix and reusable diagnostic recipe. Individual tools are known; the finding and its causal validation are new.
- **Significance: 3/4.** The readout-bottleneck framing and the probe-then-measure-alignment-then-repair recipe are likely to be cited and applied to other competence-without-performance failures. Practical impact is limited by synthetic-task scope, an 83.1% generation ceiling, and weak DROP transfer (+10pp).
- **Overall: 6/10.** A clear accept: comfortably above the poster mean on experimental substance and causal design, held below 7 by internal-consistency problems and an over-clean "knows vs. says" narrative that the paper's own 60.7% entity-counting number complicates.
- **Confidence: 4/5.** I read the source closely and checked internal arithmetic, but figures, the supplement, and compiled output were unavailable.

## 9) Final Recommendation

**ICLR: Accept (6).**

This is a genuinely strong mechanistic study whose causal logic — constrained decoding fixed by output-row repair, generation fixed only by upstream Q/V repair, with mechanism confirmed by logit-lens rank shifts — is the kind of clean dissociation ICLR mech-interp reviewers value, and the control suite (necessity/sufficiency, equivalence testing, locus ablation, negative controls) exceeds venue norms. It is held back from a higher score by real but repairable hygiene failures: conflicting numbers for the same intervention across tables, an unexplained 0.0% generation result that contradicts the paper's own Table 1, and a headline framing ("the model knows the count") that the readout-locus evidence for entity counting only partially supports. If the rebuttal supplies the last-token probe measurements, generation error traces, and the missing CoT/GSM8K numbers, I would expect this to settle as a solid poster accept.
```

### Kimi k3

#### Run 1
```
# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: No author-identifying information visible in the provided source. ✅ (Cannot verify supplementary/repo links — none provided.)
- **Style files**: Uses `iclr2027_conference.sty` and matching bibliographystyle. ✅ (The stale comment "% NeurIPS 2026 style" in the preamble is editorially sloppy but not a violation.)
- **AI use statement**: Present. ✅
- **Page limit**: Cannot be verified from uncompiled LaTeX source. Main text (Intro through Conclusion) appears dense but plausibly within 9 pages; the volume of floated tables/figures makes this uncertain — authors should verify. Core evidence (Tables 1–4, logit-lens figure) does live in the main text. ⚠ Unverifiable.

No desk-reject risk identified from the material provided.

---

## 1) Core Thesis & Significance

**Thesis**: LLMs fail at counting not because they don't represent counts internally (linear probes recover counts at R² > 0.99), but because the count-encoding direction is geometrically misaligned with the `lm_head` digit rows (|cos| ≤ 0.032, statistically indistinguishable from random directions). The paper supports this with logit-lens analysis, a minimal 9-row output-head repair (fixes constrained decoding), and a LoRA Q/V intervention (fixes autoregressive generation, 83.1%).

**Relevance**: Practically relevant — counting/aggregation failures are well-documented and embarrassing for deployed LLMs, and a mechanistic account of *why* has been missing. The problem is real, though the "low-vocabulary aggregation" scope is narrower than the title implies.

**Novelty**: The framing is component-level novel: prior work documented failures (Razeghi et al.) and localized heads (Stolfo et al.), but the explicit *representation–readout geometric gap* — quantified via probe-vs-logit-lens divergence on the *same* hidden states, with a random-direction equivalence test — is a genuinely new and crisply stated claim. The "linearly encoded but not output-promoted" observation is a nice complement to Geva et al.'s FFN-promotion story.

**Summarizability**: A reviewer can unambiguously state the contribution: "counts are linearly decodable but orthogonal to digit unembedding rows; this is causally the bottleneck; it is repairable." That clarity is a strength.

## 2) Technical Soundness

**Well-supported claims**:
- The orthogonality claim is handled with unusual statistical care: random-direction baselines, permutation tests, TOST equivalence, four probe types, three model families, shuffled-label probes, and a positive control (predicted-token probe achieves 3.3× higher alignment). This is better than most accepted interpretability work.
- The "why is orthogonality stable" gradient fixed-point argument is assumption-light and receives direct empirical support (counting FT raises |cos| 3.2×; arithmetic FT 1.1×).
- Necessity/sufficiency controls (shuffled rows below baseline; trained rows at random positions at baseline) properly earn the causal "bottleneck" language.

**Concerns**:

- **(b) Significant concern — internally inconsistent headline numbers across tables.** The 9-row repair on Qwen3-8B entity counting is reported as 60.7% (Tables 1–2), 93.8% "held-out" (Table `intervention_comparison`), and 56.7% as the "ridge baseline in the ablation replication" (Appendix capacity ablation). Baseline digit-restricted accuracy appears as 13.7%, 11.3%, 17.0%, and 38.8% in different places. The paper gestures at protocol differences and provides a protocol map, but the largest gap (60.7 vs. 93.8, same model, same task, both "held-out") is never reconciled in text. Even if each number is individually honest, this invites the suspicion of protocol shopping and must be fixed with an explicit reconciliation.
- **(b) Significant concern — soft DPS fragility.** Soft DPS goes from 96.3% (single-seed protocol) to 13.2% ≈ baseline (multi-seed protocol), attributed to full-vocabulary argmax being dominated by non-digit tokens. But the appendix states the *single-seed* protocol also used "argmax over all tokens," so the explanation given does not actually account for the discrepancy ("single-seed vs. diverse templates" is not a mechanism). Hard DPS (+100 to a logit) is answer-forcing, not an intervention — fine as a probe-correctness check, but it should not be presented alongside repairs.
- **(c) Typical limitation — the "fixes" are task-specific fine-tuning.** Both the 9-row repair and LoRA Q/V are trained on counting data. "Fine-tuning on task X improves task X" is not surprising; the scientific value is the *localization* (9 rows suffice; Q/V locus beats alternatives), which the paper does establish via the locus ablation. But the title's "How to Fix It" leans on the weaker half of the contribution.
- **(c) Typical limitation — unexplained non-monotonic per-count pattern.** The 9-row repair collapses at counts 4–7 (30–51%) but recovers at 8–9 (49–72%). This striking pattern gets no mechanistic comment.

No fatal flaws: the core geometric claim survives all stated controls.

## 3) Empirical Rigor

**Strengths**:
- Factorial prompt design (count ⊥ distractors ⊥ length ⊥ spacing) properly defends against probe shortcuts — this is the right way to run probing studies and is frequently skipped in accepted papers.
- Three evaluation modes explicitly labeled; generation scored by final integer with an explicit warning about first-integer scoring inflation.
- Negative controls (MMLU/GSM8K: |cos| = 0.31–0.48, no bottleneck, repair *hurts*) correctly bound the claim's scope.
- Multi-seed reporting with per-seed values disclosed (LoRA: 71.5–89.0% multi-task; 94.5–97.0% entity-only).

**Gaps**:
- **No reported CoT baseline number.** The Discussion claims CoT "places alongside LoRA Q/V" but presents no CoT accuracy under the paper's own final-integer scorer (it is mentioned as "available in the supplement," not provided here). Since CoT is the zero-training-cost competitor for the deployable fix, this head-to-head belongs in the main text. This is the most conspicuous missing baseline.
- **No full fine-tuning baseline for generation.** LoRA Q/V is compared only against the paper's own interventions; full-FT generation accuracy would calibrate whether 83.1% reflects routing-specific repair or generic task learning. The locus ablation partially substitutes for this but not fully.
- High-variance headline: 83.1% ± 7.2% across 5 seeds is a wide band for the paper's flagship deployable number; the entity-only numbers (94.5–97.0%) suggest the multi-task mix drives the variance, which is fine but should temper the abstract's presentation.
- Trade-offs are quantified honestly (inference-cost vs. training-cost framing vs. CoT; parameter counts for each intervention).

**Overclaiming check**: The abstract and claims are mostly well-calibrated — the paper explicitly scopes the 9-row repair to constrained decoding and discloses its 0.0% generation result prominently. Two exceptions: (i) the title promises a "fix" that the paper itself shows fails in the deployment mode (0.0% generation for the minimal repair; the working fix is plain LoRA fine-tuning); (ii) "the bottleneck generalizes" leans on addition, where the constrained baseline is already 93.3%, leaving little bottleneck to explain.

## 4) Competitive Realism Check (Calibrated)

Against the ICLR 2026 population (poster accept mean ≈ 5.35): this paper's *diagnostic* half — clean falsifiable claim, four probe types, equivalence testing, necessity/sufficiency controls, negative controls, cross-model replication — is comfortably above the accepted-paper bar for mechanistic interpretability work. Many accepted interpretability papers rely on a single probing analysis with none of these controls.

The *intervention* half is where accepted-paper variance bites: the number inconsistencies across tables and the absent CoT number are the kind of thing that produces one frustrated 3–4 score in an otherwise positive review pool. Would at least two reasonable reviewers score ≥5? **Yes**, plausibly three — the core finding is memorable and the evidence for it is strong even if one discounts every intervention number entirely. The weaknesses are within acceptance variance, not below it.

## 5) Weakest Link Analysis

**Weakest link**: the unreconciled cross-table number discrepancies for the same model/task (60.7% vs. 93.8% vs. 56.7% for 9-row repair; 96.3% vs. 13.2% for soft DPS under two protocols whose stated difference doesn't mechanistically explain the gap).

**Classification**: *Addressable in revision* — a single reconciliation table (rows = each reported number, columns = exact protocol: split, argmax scope, template set, seed count) plus one paragraph explaining the soft-DPS discrepancy would resolve it. It is not fundamental to the geometric claim, but left unfixed it is decision-relevant because it converts the paper's laudable protocol-transparency effort into a credibility liability. This is the issue most likely to flip a borderline reviewer.

## 6) Convergence Test (Minimal-Change Threshold)

- **As-is, ≥50% acceptance chance?** Roughly at the threshold — I estimate ~45–55%, driven by review-pool variance on the number-consistency issue and title-oversell reaction. Not safely above.
- **Minimal changes to push over** (evidence-based, not editorial):
  1. A reconciliation table/appendix mapping every reported accuracy to its exact protocol, with an explicit explanation of the 60.7 vs. 93.8 gap and a mechanistic (not just "different templates") account of the soft-DPS discrepancy.
  2. Report the CoT baseline under the paper's own final-integer scorer in the main text alongside LoRA Q/V.
  3. Retitle or subtitle to scope the "fix" claim (e.g., "...: A Geometric Readout Bottleneck"), or move the deployable-fix framing behind the diagnosis framing.

Items 1–2 are small experiments/tables, not new research programs.

## 7) Structural Sharpness & Scope Control

The paper is centered on one dominant contribution (the geometric readout bottleneck) and most material serves it:

- **(a) Strengthens core**: probes + orthogonality statistics, logit-lens two-phase analysis, necessity/sufficiency controls, negative controls, gradient fixed-point explanation, scale sharpening at 14B.
- **(b) Neutral**: majority-vote and max-extraction extensions (nice but the counting story stands without them); DROP +10pp partial result.
- **(c) Introduces attack surface**: (i) the soft-DPS single-seed result (96.3%) presented at all, given its fragility — the hard-DPS/probe-round equivalence already makes the diagnostic point; (ii) the "intervention comparison" table mixing protocols in one view invites the confusion flagged in §5; (iii) the per-count stratified table exposes an unexplained non-monotonicity that reviewers will poke.

**Recommended scope reduction**: drop or fully quarantine the single-seed soft-DPS result and merge all intervention numbers into one protocol-locked table. This removes two attack surfaces at zero cost to the thesis.

## 8) ICLR Formal Scores

- **Soundness: 3/4** — The core geometric claim is supported by an unusually complete control battery; however, unexplained cross-table numeric inconsistencies and the under-explained soft-DPS protocol sensitivity prevent a 4.
- **Presentation: 3/4** — Well-organized, honest scope labeling, explicit protocol map; but the proliferation of unreconciled numbers across tables undermines the clarity the structure otherwise achieves.
- **Contribution: 3/4** — A genuinely new, crisply falsifiable mechanistic claim (encoded-but-orthogonal-to-readout) plus causal localization; the repair side is closer to informed fine-tuning than to a novel fix.
- **Significance: 3/4** — Memorable finding with a reusable diagnostic recipe (probe → align → targeted repair) applicable to other competence/performance gaps; impact bounded by the low-vocabulary-aggregation scope and sub-frontier model scales.
- **Overall: 6/10** — Clear accept: a well-controlled, memorable mechanistic diagnosis comfortably above the poster mean, held back from 7 by number-consistency issues, the absent CoT head-to-head, and an intervention story weaker than the diagnosis.
- **Confidence: 4/5** — Confident in the assessment of the probing/geometry evidence and the review dynamics; residual uncertainty on whether the cross-table discrepancies have a benign explanation the authors could trivially supply.

## 9) Final Recommendation (Venue-Calibrated)

**ICLR: Accept (6/10)**.

The paper delivers a clean, falsifiable, and well-controlled mechanistic answer to a widely observed failure — counts are linearly represented but geometrically inaccessible to the output head — with controls (equivalence testing, shuffled rows, negative benchmarks) that exceed typical accepted interpretability work. Its liabilities — unreconciled numbers across protocols, no reported CoT comparison for the generation-mode fix, and a title that oversells a fine-tuning intervention — are real but addressable and fall within the variance of accepted ICLR papers. In a typical review pool this lands as a solid poster with a plausible path to stronger scores after revision.
```

#### Run 2
```
# Blind Peer Review — ICLR 2027

## Desk-Reject Compliance Check

- **⚠ DESK-REJECT RISK (style comment, minor):** The preamble comment reads `% NeurIPS 2026 style --- submission mode (anonymized)` while the actual package loaded is `iclr2027_conference`. The style file itself appears correct; the stale comment suggests the template was repurposed and should be cleaned, but this is not a violation.
- **AI use statement:** Present ("AI Use Statement"). ✓
- **Anonymity:** Main text is anonymous; citations are third-person. The figure PDFs (`pipeline.pdf`, `fig3_probe_r2_gap.pdf`, `logit_lens_depth.pdf`) and `references.bib` are external files whose metadata I cannot inspect — authors should verify no identifying metadata is embedded.
- **Page limit:** Cannot be verified exactly from source. My estimate of main text (intro through conclusion, excluding references/appendix/AI statement) is ~8–9 pages with 3 figures and 6 tables — plausibly compliant but tight; if any figure renders taller than expected it could exceed 9 pages. Verify after compilation.

No hard desk-reject violation identified from the provided material.

---

## 1) Core Thesis & Significance

**Thesis:** LLMs fail at counting not because they lack a count representation (linear probes achieve R² > 0.99) but because the count-encoding direction is nearly orthogonal to the `lm_head` digit rows (|cos| ≤ 0.032) — a *geometric readout bottleneck*. Three interventions localize it: 9-row `lm_head` repair fixes constrained decoding (60.7–100.0%) but not generation (0.0%); LoRA Q/V fixes upstream routing and achieves 83.1% ± 7.2% greedy generation; DPS bypasses the output head entirely.

**Relevance:** Counting is a canonical, well-documented LLM failure (Razeghi et al., Stolfo et al.), and the "model knows but can't say" framing connects to the broader competence-vs-performance question in interpretability. The problem is real but narrow; the paper appropriately scopes claims to low-vocabulary aggregation tasks and uses MMLU/GSM8K as negative controls.

**Novelty:** Integration-level. Probes, logit lens, LoRA, and targeted weight editing are all standard tools; the novelty is (a) the specific orthogonality finding with careful equivalence testing, (b) the causal localization via the 9-row probe, and (c) the clean mode-specific dissociation (output-head repair fixes constrained decoding; upstream routing repair fixes generation). A reviewer can summarize the contribution unambiguously — a strength.

## 2) Technical Soundness

The core evidential chain (probe → cosine/TOST → logit lens → intervention with shuffled-row and random-direction controls) is sound and unusually well-controlled. Shuffled-label probes (R² = −0.042), permutation tests, TOST equivalence, four probe types, and three model families support the orthogonality claim. Specific issues:

- **(b) Significant concern — DPS circularity.** "Hard DPS" adds +100 to the probe-predicted digit's logit. Since the probe is trained on ground-truth counts, hard DPS *is* a probe decoder; its 98.7% matching probe-round is tautological, not a "confirmation that bypassing the output head recovers full probe accuracy." The paper mostly labels it as a bypass/diagnostic, but it occupies intervention tables alongside real methods. This is presentational overreach rather than an error.
- **(b) Significant concern — training-dynamics "why" is thin.** The claim that orthogonality is a stable fixed point of gradient dynamics is supported by two fine-tuning runs (|cos| 0.0074→0.0280 counting vs. 0.0087→0.0096 arithmetic) from *different checkpoints*, with final values hovering near the random baseline (0.013 ± 0.011). Suggestive, not established. The paper partially concedes this.
- **(b) Significant concern — missing generation-mode baselines.** The headline deployable claim rests on LoRA Q/V (83.1%). There is no full fine-tuning baseline, no LoRA-all-projections baseline with *generation* accuracy numbers, and no CoT number in any main table (relegated to "the supplement"). The locus ablation compares logit-lens alignment, but only Q/V's per-seed generation accuracy is reported. Without these, "upstream routing specifically must be fixed" is under-supported relative to "any fine-tuning on counting data helps."
- **(c) Typical limitation — probe interpretability.** Layer-0 probe R² = 0.977 invites the question of whether probes read near-lexical count cues. The factorial design (distractors, length, spacing varied independently of C) is a genuine mitigation, but the passages contain per-sentence numerals ("There are 2 apples…"), and the manuscript never explicitly states that within-sentence numerals are decorrelated from C. Worth one clarifying sentence.
- **(c) Typical limitation — addition as evidence.** Addition baseline is already 93.3%; the bottleneck barely exists behaviorally on this task, so its inclusion in "generalizes across … addition" overstates the cross-task story slightly.

No fatal flaws. The core claims that matter (orthogonality; 9-row locality under constrained decoding; LoRA Q/V generation gains over a 7.2% baseline) are adequately supported.

## 3) Empirical Rigor

**Strengths (above the ICLR poster median):** Mode-matched comparisons; a protocol map table; seeds and CIs on headline numbers (N=200 × 3–5 seeds); stratified per-count breakdown; held-out entity types/templates; format robustness; capacity ablation (Adam vs. ridge, 9 vs. 59 rows); necessity/sufficiency controls (shuffled rows below baseline, random-position rows at baseline); cross-model replication including a sharpening effect at 14B.

**Weaknesses:**

- **Number sprawl and unreconciled protocols.** "Entity counting baseline" appears as 10.3%, 11.3%, 13.7%, 14.2%, 17.0%, and 38.8% across the paper, and the 9-row held-out result appears as both **60.7%** (Table `mode_matched_extval`, harmonized protocol) and **93.8%** (Table `intervention_comparison`, unspecified earlier protocol; the ablation appendix also cites 56.7% as a ridge "baseline replication"). Most variants are individually annotated, but Table `intervention_comparison` — which contains the most flattering numbers (93.8%, 94.2%) — defers its protocol to an appendix that does not obviously reconcile it. A skeptical reviewer will wonder whether the impressive numbers come from a superseded single-template protocol.
- **Soft DPS fragility.** 96.3% (single-seed) vs. 13.2% (multi-seed) is explained in the appendix as non-digit tokens winning full-vocab argmax. The explanation is credible, but it means the original DPS result was a prompt-format artifact; the appendix treatment is honest, yet it underscores how protocol-sensitive the whole pipeline is.
- **LoRA variance.** Per-seed generation 71.5–89.0% (±7.2%) on N=200/seed is noisy; the entity-only numbers (94.5–97.0%) suggest the multi-task headline conflates task mixing with method performance. The authors say this; fine.
- **Trade-offs:** Quality-vs-cost is addressed qualitatively (CoT externalizes; LoRA has zero inference overhead) but never quantified — no tokens-per-answer or latency comparison, and no CoT accuracy under the corrected final-integer scorer in the main text.
- **Overclaiming check:** Mostly clean. Two flags: "near-perfect accuracy (R²>0.99)" conflates R² with accuracy (minor); GSM8K is invoked as a negative control but no GSM8K behavioral numbers are shown, only cosine values pooled with MMLU (minor).

## 4) Competitive Realism Check (Calibrated)

This sits comfortably within the population of accepted ICLR interpretability papers: a clean mechanistic case study with causal interventions, controls that most accepted posters omit (TOST, shuffled rows, capacity and locus ablations), multi-model replication, and honest negative results (Pythia-410M repair failure, generation-mode 0.0%). The weaknesses — moderate novelty, one niche task family, reporting inconsistency across protocols, missing FT/CoT baselines for the generation claim — are within acceptance variance; accepted posters routinely have worse. Would at least two reasonable reviewers score ≥5? Yes, very likely; plausible reviewer spread is {4, 5, 6} or {5, 5, 6}. It is not dominant SOTA anywhere and does not need to be; the mechanism + ablations carry it to the poster bar.

## 5) Weakest Link Analysis

**Single most decision-relevant issue:** the unexplained discrepancy between Table `mode_matched_extval` (9-row held-out entity counting = 60.7%) and Table `intervention_comparison` (9-row held-out = 93.8%, full-head = 94.2%), under protocols whose relationship the text never reconciles. A reviewer who catches this can plausibly flip to reject on "untrustworthy headline numbers," even though the harmonized Table 2 numbers independently support every core claim.

**Status:** Addressable in revision — unify protocols, relabel legacy results explicitly, or drop Table `intervention_comparison` entirely. Not fundamental; the harmonized protocol stands on its own.

Runner-up: absence of full-FT / LoRA-all-loci generation baselines and the corrected-scorer CoT number for the deployability claim — also addressable.

## 6) Convergence Test (Minimal-Change Threshold)

- **As-is acceptance probability:** ~50%. The science clears the poster bar, but the Table 2/3 inconsistency plus missing generation baselines give a skeptical reviewer a concrete, legitimate reject path.
- **Minimal changes to push over threshold (all evidence-based, none editorial):**
  1. Reconcile or remove Table `intervention_comparison`; state explicitly which protocol each number belongs to and why held-out 9-row repair is 60.7% in one table and 93.8% in another.
  2. Add full fine-tuning and LoRA-on-other-loci baselines with *generation* accuracy, plus the CoT final-integer number, to Table 1's columns.
  3. Show GSM8K behavioral numbers or drop it from the negative-control claim.

These are cheap experiments using infrastructure the authors clearly already have; items 1–2 would likely move this to a 6.

## 7) Structural Sharpness & Scope Control

The paper is centered on one dominant claim (geometric readout bottleneck) and the discussion stays disciplined about scope. However, the intervention zoo — probe-round, soft DPS, hard DPS, 9-row repair, fullvocab repair, norm rescaling, logit-masking, LoRA Q/V — creates attack surface:

- **(a) Strengthens core:** probes + logit lens + orthogonality statistics; 9-row repair with shuffled-row controls; LoRA Q/V with logit-lens mechanism evidence; MMLU negative control.
- **(b) Neutral:** multi-digit extension, majority vote, max extraction (fine in appendix), instruct-mode result.
- **(c) Introduces attack surface:** DPS in all forms (label-informed, protocol-fragile, tautologically matches probe-round); Table `intervention_comparison` (legacy protocol, best-looking numbers); the training-dynamics fixed-point story (two fine-tunes, near-random final alignments).

**Recommended scope reductions that raise acceptance probability:** demote DPS to a clearly-labeled decoding diagnostic (one line in main text, details in appendix); delete or fully annotate Table `intervention_comparison`; present the training-dynamics account strictly as a hypothesis. This costs nothing and removes the three easiest reject hooks.

## 8) ICLR Formal Scores

- **Soundness (1-4): 3.** Core claims are well-supported with strong controls, but DPS is label-informed, the training-dynamics "why" rests on two weak fine-tuning runs, and the generation claim lacks FT/loci baselines.
- **Presentation (1-4): 3.** Well-organized with an exemplary protocol map, but the intervention sprawl, six different "baseline" numbers, and the unreconciled 60.7% vs. 93.8% held-out results genuinely impede evaluation.
- **Contribution (1-4): 3.** Integration-level novelty: a clean, causally localized geometric diagnosis of a known failure. Tools are standard; the orthogonality finding and mode-specific dissociation are real new insights.
- **Significance (1-4): 3.** A portable diagnostic recipe (probe → align → repair) and a memorable "orthogonal readout" result that interpretability researchers will cite; impact bounded by the narrow task family and by fine-tuning being required for the fix.
- **Overall (1-10): 5.** Borderline accept: solid, honest, well-controlled poster-tier work whose reporting inconsistencies and missing baselines currently give reviewers a concrete reject path that a light revision would close.
- **Confidence (1-5): 4.** Familiar with the probing/logit-lens/model-editing literature; cannot compile the paper or inspect figures, and some protocol relationships may be clarified in the absent supplement.

## 9) Final Recommendation (Venue-Calibrated)

**ICLR: Borderline Accept (5).**

This is a rigorous, honest mechanistic case study whose central finding — counts are linearly encoded in directions statistically indistinguishable from random w.r.t. the digit unembedding — is well-supported by equivalence testing, causal row-level interventions, and multi-model replication, and it sits squarely in the accepted-poster population by experimental substance. What keeps it from a clear accept is not the science but the evidence presentation: two unreconciled headline numbers for the same repair (60.7% vs. 93.8%), a label-informed "intervention" (DPS) presented alongside real ones, and missing full-FT/CoT baselines for the deployability claim — all fixable in revision with experiments the authors can obviously run. If those are addressed, this becomes a comfortable accept.
```

#### Run 3
```
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
```

### Visual: Kimi k3

#### Run 1
```
# Paper Visual Audit

## Scope
- Pages reviewed: 1–12
- Total pages: 12

## Summary
The paper uses the correct ICLR 2027 template (line numbers, "Under review" header, anonymous author block) and is largely clean: tables are well-formed, captions are informative, and the main text ends on page 9 with the AI Use Statement present before the references — no desk-reject risks found. The visual weaknesses are concentrated in the figures: Figure 1 uses raw ASCII math notation ("R^2", "|cos| <= 0.032") inside diagram boxes, Figure 2's legend box occludes the key dashed reference line, and Figure 3's subplots have fonts and legends that are noticeably smaller than body text and crowd the plotted curves. Tables 1–8 are all readable, uncropped, and correctly broken across pages. No anonymity leaks, acknowledgments, or non-anonymous links are visible.

## Findings

- **Severity**: medium
- **Page**: 5
- **Element**: figure
- **What is wrong**: In Figure 2, the legend box ("Probe R^2 (all) / Probe R^2 (easy) / Next-token digit accuracy (38.8%)") is placed inside the axes at the lower-left and sits directly on top of the red dashed accuracy reference line at y ≈ 0.388, which disappears behind the legend for roughly the left third of the plot.
- **Why it matters**: The dashed line is the "what the model says" anchor of the paper's central gap visualization; partially hiding it undermines the figure's single most important comparison.
- **Minimal fix**: Move the legend outside the axes (e.g., below the plot) or to the upper-left/right corner where the dashed line does not pass, or draw the dashed line on top of the legend.

- **Severity**: medium
- **Page**: 5
- **Element**: figure
- **What is wrong**: Figure 3's two subplots are rendered small: tick labels, axis labels ("Mean P(correct number)"), and the 4-entry legends are roughly half the body-text size, and in panel (a) the legend crowds the upper-left curves.
- **Why it matters**: This is the core mechanistic evidence (logit-lens accuracy by layer); reviewers should not have to zoom to read it. The legend/curve overlap also risks obscuring early-layer behavior.
- **Minimal fix**: Increase the figure to full column width (or a single \linewidth two-panel), raise all font sizes to ~8–9pt equivalent, and place legends outside the plotting area or in clearly empty regions.

- **Severity**: medium
- **Page**: 2
- **Element**: figure
- **What is wrong**: Figure 1's diagram boxes contain raw ASCII math: "R^2 ~ 1.0", "|cos| <= 0.032", while the caption and body text use typeset math ($R^2{\approx}1.0$, $|\cos|{\leq}0.032$). "lm_head" also appears in plain proportional font inside a box.
- **Why it matters**: The mismatch reads as unpolished in the paper's flagship summary figure and is inconsistent with the typography everywhere else.
- **Minimal fix**: Render the box labels with proper math typesetting (e.g., TikZ nodes with $R^2 \approx 1.0$, $|\cos| \le 0.032$, \texttt{lm\_head}).

- **Severity**: low
- **Page**: 5
- **Element**: figure
- **What is wrong**: In Figure 2 the "Probe R² (all)" and "Probe R² (easy)" curves are nearly perfectly overlapping (~0.99 everywhere), so the purple series is visually indistinguishable from the blue one; the y-axis is also truncated at 0.3.
- **Why it matters**: One of the two legend entries is effectively invisible data; the truncated axis is acceptable here but worth a reader cue.
- **Minimal fix**: Either drop the redundant series from the plot (keep it in Table 2), or offset/dash one line; note the truncated axis in the caption.

- **Severity**: low
- **Page**: 5
- **Element**: figure / text consistency
- **What is wrong**: Figure 2's x-axis is "Layer Depth (%)" (0–100) while Figure 3 and Table 2 use absolute layer indices (0–35); Figure 2's caption also cites "Table 3" for unified-evaluation sampling, but the unified evaluation is Table 1.
- **Why it matters**: Readers must mentally convert between % depth and layer index across adjacent figures; the cross-reference appears misdirected.
- **Minimal fix**: Harmonize both figures on absolute layer index (or add a secondary axis), and verify the caption's table reference.

- **Severity**: low
- **Page**: 4
- **Element**: table
- **What is wrong**: Table 1's footnote block is set in very small type spanning the full text width, noticeably below the caption font size used elsewhere.
- **Why it matters**: The footnote carries important protocol details (parameter counts, per-seed values); tiny type discourages reading it.
- **Minimal fix**: Set footnotes at \footnotesize matching the caption, or promote per-seed numbers into a compact appendix table.

## High-Value Missing Visuals

- **Page or section**: §5 (Logit-Lens Analysis), near Figure 3 / Table 3
- **Proposed visual**: A small heatmap or 2D scatter showing cosine similarity between each layer's count-probe direction and the nine `lm_head` digit rows (layers × digit rows), optionally with a random-direction baseline row.
- **Why it improves the paper**: The paper's central quantitative claim — |cos| ≤ 0.032, "indistinguishable from random" — is currently conveyed only as scalar statistics in text. A per-layer, per-digit map would make the *uniformity* of the orthogonality (no single digit row or layer rescues readout) directly visible, which the scalar means cannot show.
- **Evidence it would clarify or support**: The claim in §5 that "per-layer means ≤ 0.032" and the random-baseline equivalence (p = 0.79); it would also directly visualize the "projection attempt" phase (layers 20–35) where alignment partially rises.

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1-3 visual fixes** before the next reviewer round:
  1. Figure 2: relocate the legend so it no longer covers the dashed 38.8% reference line.
  2. Figure 3: enlarge both panels and increase font/legend sizes to match body text; move legends off the curves.
  3. Figure 1: replace ASCII math in diagram boxes with typeset math ($R^2$, $|\cos| \le 0.032$) for consistency with the rest of the paper.

Stop.
```

#### Run 2
```
# Paper Visual Audit

## Scope
- Pages reviewed: 1–12
- Total pages: 12

## Summary
The paper is on the correct ICLR 2027 template (line numbers, "Under review" header, anonymous author block), main text ends on page 9 with the References beginning on the same page — within the 9-page limit — and an AI Use Statement is present on page 9. No anonymity leaks were detected (the "nostalgebraist" entry is a cited LessWrong post, not an author identity). Tables 1–8 are all well-formed: no clipping, no split cells, consistent booktabs styling. The visual weaknesses are concentrated in the three figures: Figure 1 uses ASCII math inside diagram boxes, Figure 2 has indistinguishable overlapping curves and a mixed-unit axis label, and Figure 3's panels are rendered too small, with tiny legends/tick labels and a reference line that appears missing or clipped. None of these are blocking, but they reduce polish and readability of the core evidence figures.

## Findings

- **Severity**: medium
- **Page**: 2
- **Element**: figure (Figure 1)
- **What is wrong**: In-box text uses raw ASCII notation — `(R^2 ~ 1.0)`, `(|cos| <= 0.032)` — instead of typeset math (R² ≈ 1.0, |cos| ≤ 0.032) as used in the caption and body. The elbow connector arrows from "lm_head misaligned" to the three intervention boxes look like default auto-layout output and visually collide at the source box edge.
- **Why it matters**: This is the paper's summary diagram, referenced from page 1; ASCII math in the figure clashes with the caption's typeset math and reads as a draft artifact.
- **Minimal fix**: Re-render box labels with mathtext/ LaTeX (e.g., `$R^2 \approx 1.0$`, `$|\cos| \le 0.032$`), and route the three arrows from distinct anchor points on the misalignment box.

- **Severity**: medium
- **Page**: 5
- **Element**: figure (Figure 2)
- **What is wrong**: The "Probe R^2 (all)" (blue) and "Probe R^2 (easy)" (purple) curves sit on top of each other at ≈0.99 for nearly the entire x-range and are visually indistinguishable. The y-axis label "Probe R^2 / Accuracy" mixes two quantities (R² and accuracy), and "R^2" is plain text rather than R². The in-plot title duplicates the caption.
- **Why it matters**: Reviewers cannot tell whether the two probe conditions differ; the mixed axis label invites misreading of the 38.8% dashed line as an R² value.
- **Minimal fix**: Use distinct line styles (solid vs. dashed) and/or slight vertical offsets for the two probe series; relabel the axis (e.g., "Probe $R^2$ / next-token accuracy") or use a dual annotation; drop the redundant in-plot title.

- **Severity**: medium
- **Page**: 5
- **Element**: figure (Figure 3)
- **What is wrong**: Both panels are small relative to the column width; tick labels, axis labels, and the 4-entry legend in panel (a) are at the edge of readability at print size. The legend lists a green dotted "Probe R² (~0.99)" reference line, but no green dotted line is discernible in panel (a) — it appears to be clipped at the top axis boundary or omitted. Panel (b)'s log-scale y-axis ticks (10⁻¹–10⁻⁷) are especially cramped.
- **Why it matters**: Figure 3 carries the central logit-lens evidence; a legend entry with no visible corresponding line undermines trust in the plot, and tiny text fails ICLR's readability bar.
- **Minimal fix**: Increase panel size (e.g., full-width figure) and font sizes by ~2 pt; verify the green dotted reference line renders inside the axes (adjust y-limits or clip_on=False) or remove it from the legend.

- **Severity**: low
- **Page**: 4
- **Element**: table (Table 1) / caption-note
- **What is wrong**: The note under Table 1 ("9-row repair = 36,864 params directly rewritten; LoRA Q/V = 7.67M trainable…") is set in a very small font spanning the full text width, noticeably smaller than other table notes.
- **Why it matters**: Contains per-seed numbers needed to interpret the headline result; small dense notes get skipped.
- **Minimal fix**: Match the note font size to the other table notes (cf. Table 4's note on page 6) or fold the per-seed values into a compact second row/appendix pointer.

- **Severity**: low
- **Page**: 5
- **Element**: layout
- **What is wrong**: Figures 2 and 3 are stacked on the same page with Figure 3's two-panel content compressed to fit; the result is that the paper's two key evidence figures compete for one page.
- **Why it matters**: Figure 3's small size (see above) is partly a consequence of this stacking.
- **Minimal fix**: Let Figure 3 float to its own position with more width, or move Figure 2's shaded-region version to the appendix and keep a single-panel version in text.

## High-Value Missing Visuals

- **Page or section**: §5, "Vocabulary competition" (page 6)
- **Proposed visual**: A histogram or ranked plot of `lm_head` row norms across the vocabulary with the 9 digit rows highlighted, showing they fall in the 12th–29th percentile.
- **Why it improves the paper**: The norm-competition claim currently rests on three inline numbers (percentile range, 0.0% argmax wins, 0.33% top-100); a single plot makes the digit-row disadvantage immediately visible and supports the "rescaling alone is insufficient" argument.
- **Evidence it would clarify or support**: The claim that norm rescaling (3× boost) raises fullvocab accuracy only from 0% to ≈26.5%, i.e., that directional misalignment — not just norm — causes the bottleneck.

- **Page or section**: §5, "Subspace geometry" (page 4–5)
- **Proposed visual**: Per-layer |cos| between the layer's count-probe direction and digit rows, optionally overlaid with the random-direction baseline band (0.013 ± 0.011).
- **Why it improves the paper**: The headline statistic |cos| ≤ 0.032 is currently a scalar buried in prose; a per-layer curve would show whether orthogonality is uniform across depth or concentrated in the "projection attempt" layers 20–35, directly supporting the two-phase encoding–projection story.
- **Evidence it would clarify or support**: The Encoding (layers 0–20) vs. Projection attempt (layers 20–35) mechanism described on page 6.

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1-3 visual fixes** before the next reviewer round:
  1. Enlarge Figure 3 and its fonts; restore or remove the missing green dotted "Probe R²" reference line.
  2. Replace ASCII math in Figure 1 boxes with typeset math and clean up the arrow routing.
  3. Differentiate the two overlapping probe curves in Figure 2 (line style) and fix the mixed-unit y-axis label.
```

### Visual: Qwen 3.8 max

#### Run 1
```
# Paper Visual Audit

## Scope
- Pages reviewed: 1–12
- Total pages: 12

## Summary
Overall rendering is clean: ICLR template, anonymity header, line numbers, tables, and math all render without broken glyphs or clipped equations. Tables 1–8 are well-formed and readable. The weak points are the two figure pages: Figure 1 has large dead whitespace and ASCII-style math labels ("R^2", "<=", "Im head"), and Figures 2–3 use caret notation, tiny legend/tick fonts, and reference lines that are hard to discern or inconsistent with the caption. No desk-reject risks detected: main text ends on page 9 (before references), an AI Use Statement is present, and no author identities leak.

## Findings

- **Severity**: medium
- **Page**: 2
- **Element**: figure
- **What is wrong**: Figure 1 leaves a large blank band (~6–7 line heights) between the bottom of the diagram ("Wrong digit" box) and the caption; the diagram also uses ASCII math ("R^2 ~ 1.0", "|cos| <= 0.032") and "Im head" instead of proper symbols and the paper's `lm_head` monospace convention; connector arrows from the red box to the three intervention boxes are thin, faint gray, and hard to trace.
- **Why it matters**: This is the paper's only schematic and the first thing reviewers see; the whitespace wastes a scarce main-text page and the ASCII notation looks unfinished next to properly typeset math in the caption.
- **Minimal fix**: Regenerate with a tight bounding box (crop internal margin), use real glyphs (R², |cos| ≤ 0.032, `lm_head`), and darken/thicken the three intervention arrows or label them; let the caption sit directly under the diagram.

- **Severity**: medium
- **Page**: 5
- **Element**: figure
- **What is wrong**: Figure 3 legend and tick labels are near-illegibly small at print size; the "Probe R² (>0.99)" dotted reference line described in the caption ("green dotted") is not clearly discernible in panel (a) — it appears clipped/blended at the top axis, while the visible dotted line is the 38.6% final-output line.
- **Why it matters**: The logit-lens figure is core evidence for the readout bottleneck; reviewers must squint to read it, and the promised reference line does not visually land.
- **Minimal fix**: Raise all figure fonts to ≥8 pt, move the legend outside or to an empty corner, and draw the probe-R² reference line fully inside the axes in the color stated in the caption.

- **Severity**: low
- **Page**: 5
- **Element**: figure
- **What is wrong**: Figure 2's y-axis label reads "Probe R^2 / Accuracy" with a caret instead of R²; the legend box sits on top of the shaded gap region (readable, but the red dashed line runs into the legend edge).
- **Why it matters**: Minor typography inconsistency with the rest of the paper, which uses proper math typesetting.
- **Minimal fix**: Use mathtext/Unicode R² in the axis label; nudge the legend or add a white frame so the dashed line and legend do not collide.

- **Severity**: low
- **Page**: 1
- **Element**: layout
- **What is wrong**: Line-number gutter starts at "000" rather than 001/1.
- **Why it matters**: Purely cosmetic, but slightly unpolished.
- **Minimal fix**: Start line numbering at 1 if the template option is trivially adjustable; otherwise ignore.

## High-Value Missing Visuals

- **Page or section**: Page 12 / §A.7–A.9 (and Results §6)
- **Proposed visual**: Small line/bar plot of accuracy vs. count value (1–9) for probe-round vs. 9-row repair, directly from Table 8.
- **Why it improves the paper**: The count-dependent collapse of the repair (100% at counts 1–3 down to ~30–50% at 5–9, while probe-round stays ~100%) is currently buried in an appendix table; a plot makes the "task-level ceiling" and norm-competition story instantly visible.
- **Evidence it would clarify or support**: Supports the claim that the remaining 31 pp gap is a task-level ceiling, not a fitting/capacity limitation (§A.12), and visualizes Table 8's divergence between the two curves.

- **Page or section**: Page 5 / §5 (Subspace geometry)
- **Proposed visual**: Per-layer |cos| alignment curve between the count-probe direction and `lm_head` digit rows (with the random-direction baseline band, |cos| ≈ 0.013±0.011).
- **Why it improves the paper**: Orthogonality (|cos| ≤ 0.032) is the paper's central geometric claim, but it is only shown as text and a single scalar in Figure 1; Figure 2 shows R² and accuracy, not alignment.
- **Evidence it would clarify or support**: Would directly visualize the |cos| = 0.016 mean, per-layer ≤ 0.032 values, and the TOST-equivalence/permutation baselines (lines 259–261), showing alignment stays at chance level across depth.

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1-3 visual fixes** before the next reviewer round:
  1. Re-typeset Figure 1 (crop whitespace, proper R²/≤/`lm_head` glyphs, clearer arrows).
  2. Fix Figure 3 legibility (font sizes, visible caption-consistent probe-R² reference line) and Figure 2's "R^2" axis label.
  3. Optionally add the per-count accuracy plot (Table 8 data) to make the repair ceiling visually explicit.

No  DESK-REJECT RISK items: anonymity intact, main text ≤ 9 pages before references, AI Use Statement present, template/citation style consistent with ICLR.

Stop.
```

#### Run 2
```
# Paper Visual Audit

## Scope
- Pages reviewed: 1–12
- Total pages: 12

## Summary
Overall the paper renders cleanly: tables are well-formed, text is dense but readable, and the ICLR template, anonymity, 9-page main-text limit, and AI-use statement all appear compliant. The weaknesses are concentrated in the figures: Figure 1's caption is detached from the schematic by a large blank band, and the schematic uses ASCII math ("R^2", "<=") instead of proper glyphs; Figures 2–3 reuse ASCII carets in axis/legend text; Figure 3's legend and tick fonts are near the legibility limit and its advertised probe-R² reference line is not discernible in the render. No broken glyphs, cropped equations, or malformed tables were found.

## Findings

- **Severity**: medium
- **Page**: 2
- **Element**: figure (layout)
- **What is wrong**: In Figure 1, there is a ~1-inch blank band between the bottom of the schematic ("Wrong digit" box) and the caption block; the caption appears detached from the graphic, leaving a conspicuous hole in the top half of the page.
- **Why it matters**: Readers may not associate the caption with the schematic at a glance, and the wasted vertical space pushes "Motivation" down; it reads as a broken float.
- **Minimal fix**: Remove the extra vertical space/fixed height in the figure environment so the caption sits directly beneath the schematic (standard `\floatsep`-scale spacing).

- **Severity**: medium
- **Page**: 2
- **Element**: figure (typography)
- **What is wrong**: Figure 1 boxes contain ASCII math: "(R^2 ~ 1.0)" and "(|cos| <= 0.032)" with caret, tilde, and "<=" instead of rendered symbols, inconsistent with the properly typeset caption immediately below.
- **Why it matters**: This is the first visual evidence reviewers see; raw-code-style math inside boxes looks like an unpolished draft and clashes with the venue's typesetting quality.
- **Minimal fix**: Regenerate the box labels with mathtext/Unicode (R² ≈ 1.0, |cos| ≤ 0.032) matching the caption.

- **Severity**: medium
- **Page**: 5
- **Element**: figure (Figure 3)
- **What is wrong**: Legend entries and axis tick labels in both subplots are extremely small (≈5–6 pt effective), e.g. "Final output acc. (38.6%)", "Probe R^2 (~0.99)", and the tick numbers; borderline unreadable at print resolution.
- **Why it matters**: Reviewers must compare the red/blue curves and the reference lines; illegible legends force zooming and undermine the logit-lens evidence.
- **Minimal fix**: Increase legend/tick font sizes to ≥8 pt, or move the legend of (a) outside the axes / shorten entries; consider enlarging the figure to full text width.

- **Severity**: medium
- **Page**: 5
- **Element**: figure (Figure 3a)
- **What is wrong**: The legend advertises a "Probe R^2 (~0.99)" reference line, but no line is discernible near y ≈ 1.0 in the rendered subplot; only the dotted line near 0.4 (final-output accuracy) is visible.
- **Why it matters**: The probe-R² reference is the key contrast in the caption ("Probe R² ≈ 0.99 shown for reference"); if it is clipped or drawn off-axis, the legend is misleading.
- **Minimal fix**: Verify the reference line is plotted within the axis range (y-axis already spans 0–1.0) with a visible color/linestyle; if present, thicken it or annotate it directly.

- **Severity**: low
- **Page**: 5
- **Element**: figure (Figure 2 typography)
- **What is wrong**: Axis label and legend use ASCII caret: "Probe R^2 / Accuracy", "Probe R^2 (all)", "Probe R^2 (easy)".
- **Why it matters**: Minor typographical inconsistency with the rest of the paper, which uses proper R² glyphs in captions and text.
- **Minimal fix**: Use mathtext superscripts (R²) in the ylabel and legend strings.

- **Severity**: low
- **Page**: 5
- **Element**: figure (Figure 2 legend)
- **What is wrong**: The legend box floats over the shaded gap region at mid-left; it is legible but partially covers the shaded area that is itself the message of the plot.
- **Why it matters**: Slightly obscures the "knows vs. says" gap visualization.
- **Minimal fix**: Move the legend to the empty lower-right region (below the red dashed line) or outside the axes.

## High-Value Missing Visuals

- **Page or section**: Page 5–6 (§5, "Subspace geometry" / "Why is orthogonality there?")
- **Proposed visual**: A small histogram/density plot of |cos| between the count-probe direction and lm_head digit rows across layers, overlaid with the random-direction baseline distribution.
- **Why it improves the paper**: The orthogonality claim (|cos| ≤ 0.032 ≈ random) is the paper's central geometric evidence but is currently only in prose and scalar summaries.
- **Evidence it would clarify or support**: Directly visualizes that the count direction is statistically indistinguishable from random directions relative to digit rows (bootstrap CI [0.015, 0.016] vs. random 0.013 ± 0.011), making the TOST equivalence result immediate.

- **Page or section**: Page 12 (Table 8, §A.7)
- **Proposed visual**: A count-stratified line/bar chart of accuracy vs. count value (1–9) for probe-round vs. 9-row repair.
- **Why it improves the paper**: Table 8 shows probe-round flat near 100% while repair degrades 92%→30%; a chart makes this divergence—and the "task-level ceiling" interpretation—visible at a glance and could be promoted to the main text to support the capacity-ablation discussion.
- **Evidence it would clarify or support**: The claim that the remaining 31 pp gap is a task-level ceiling, not a fitting/capacity limitation (§A.12).

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1-3 visual fixes** before the next reviewer round:
  1. Figure 1: close the figure–caption gap and replace ASCII math in box labels with properly typeset symbols.
  2. Figure 3: enlarge legend/tick fonts and ensure the probe-R² ≈ 0.99 reference line actually renders in panel (a).
  3. Figure 2: use proper R² superscripts in axis/legend text and relocate the legend off the shaded gap.
```