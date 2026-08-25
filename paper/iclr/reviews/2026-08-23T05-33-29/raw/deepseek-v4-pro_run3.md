# Peer Review: *Why Transformers Fail at Counting and How to Fix It*

**⚠ DESK-REJECT RISK CHECK**
- **Anonymity:** No identifying information detected in main text or references. Pass.
- **Page limit:** I cannot verify exact length from the provided LaTeX, but the manuscript appears concise and likely within 9 pages. Apparent adherence.
- **AI use statement:** Present and properly placed. Pass.
- **Style files:** Uses `iclr2027_conference`, seems correct. Pass.

No desk-reject issues are evident.

---

## 1) Core Thesis & Significance
The paper argues that transformer counting failures arise not from an inability to represent counts internally, but from a geometric readout bottleneck: the count-encoding directions in the residual stream are nearly orthogonal to the digit-token rows of the output embedding (`lm_head`). The claim is cleanly layered: (1) counts are linearly encoded with near-perfect fidelity (probe \(R^2>0.99\)), yet (2) those encoding directions are orthogonal to the digit rows (\(|\cos|\leq 0.032\)), and (3) this misalignment causes output failure, which can be repaired by minimal interventions (9-row output-head fine‑tuning for constrained decoding, LoRA on attention Q/V for full autoregressive generation). The task (low‑vocabulary aggregation: counting, addition, list length) is well‑motivated and practically relevant, as such failures are common even in strong LLMs. The insight is a crisp mechanistic explanation with targeted causal fixes, and the negative controls (MMLU, GSM8K) carefully bound the scope. This is a significant, self-contained contribution that is likely to be remembered and cited.

## 2) Technical Soundness
The core methodology is sound—linear probes, logit‑lens analysis, cosine alignment tests, and targeted interventions—all applied systematically. A particular strength is the triangulation: probes show information is present, logit‑lens shows it is not read out, and minimal repairs confirm the bottleneck locus. The use of shuffled‑label probes, random‑direction baselines, TOST equivalence testing, and positive controls forestalls many common confounds. The theoretical argument about why orthogonality is a stable fixed point of training dynamics (gradient decomposition) is plausible and partially backed by fine‑tuning data, though not a full theoretical proof. I classify this as a minor limitation (c) typical, not a flaw.

One concern (which I view as category b, significant but fixable) is that the generation‑mode repair via LoRA Q/V is only validated in‑task; the paper claims the repair corrects routing to the output head, but we do not see how this affects the model’s broader capabilities (e.g., language modeling perplexity on general text). A small degradation would be acceptable, but no measurement is provided. This does not undermine the core diagnosis, but it tempers claims of “deployability.” The authors acknowledge fine‑tuning is required; adding a perplexity sanity check would strengthen the realism.

## 3) Empirical Rigor
Experiments are extensive and well‑controlled. The factor‑randomized synthetic benchmark avoids distributional shortcuts, and the multi‑seed protocols with held‑out splits are appropriate. The evaluation modes (next‑token, full‑vocabulary, generation) are clearly delineated, and the paper scrupulously notes when numbers differ due to protocol changes—a rare and commendable clarity. Ablations address capacity (ridge vs. Adam, row count), necessity/sufficiency (shuffled‑row and random‑position controls), and format robustness. The LoRA Q/V routing mechanism is verified with logit‑lens rank reduction, and the per‑task breakdown (entity‑only generation reaching 94.5–97.0%) shows that the multi‑task variance is not a reliability issue. The evidence strongly supports the core claims.

A minor overclaim flag: the abstract says “the correct digit’s rank drops from 55,980 to 1” — this is for the best‑case entity‑only logit‑lens after LoRA Q/V, but the paper reports multi‑task rank drops that are still dramatic (e.g., 32,265→16). The statement is not wrong but should ideally be qualified as “best‑case” in the abstract. This does not significantly affect the score.

Overall, empirical rigor is well above the average ICLR accepted paper.

## 4) Competitive Realism Check
Compared to typical accepted ICLR papers, this submission is strong on evidence, clarity, and mechanistic contribution. The finding is not merely an incremental improvement but a novel geometric diagnosis of a well‑known behavioral failure, backed by multiple convergent interventions. Weaknesses (mainly the scope limitation to low‑vocabulary aggregation and the lack of a general‑domain perplexity check after fine‑tuning) are typical of mechanistic interpretability work and are not disqualifying. I estimate at least two reasonable reviewers would score this ≥5 (Accept/Poster), likely 6 or 7. The paper sits comfortably in the acceptance range.

## 5) Weakest Link Analysis
The weakest link is the missing evaluation of how the LoRA Q/V repair affects the model’s overall language generation quality (perplexity or downstream task performance outside counting). This is decision‑relevant because it distinguishes a targeted fix from a hack that might destroy other capabilities. It is **addressable in revision**: a simple perplexity measurement on a standard held‑out corpus (e.g., WikiText‑2) before and after LoRA Q/V would suffice. Even a small degradation would be acceptable if it remains usable. Without this, the “deployable” claim is slightly overconfident. This is the single issue most likely to flip accept/reject, but I believe it would not change the outcome if the authors can provide a reassuring result in the rebuttal.

## 6) Convergence Test
- **If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?**  
  Yes. The evidence is strong, the mechanistic story is compelling, and the presentation is clear. The paper already exceeds the ICLR acceptance bar.

- **What minimal change would push it over the threshold?**  
  Even without changes, it is already above threshold. However, adding a perplexity check after LoRA Q/V fine‑tuning (even a one‑paragraph note) would remove the only lingering concern and strengthen the claim of a deployable fix.

## 7) Structural Sharpness & Scope Control
The paper is well‑centered on a single dominant contribution: the geometric readout bottleneck. The structure—diagnosis → causal localization → repair—is logical.

- **(a) Strengthens core argument:** The probe, logit‑lens, and intervention sections form a tight causal chain. The generation‑mode analysis and DPS are essential.
- **(b) Neutral:** The brief CoT comparison is useful context but slightly tangential; it could be shortened without loss.
- **(c) Adds attack surface:** The claim that CoT and LoRA Q/V are complementary is stated but not empirically validated; a direct comparison under equal scoring would invite scrutiny. The paper wisely avoids over‑claiming here.

If I were to recommend any reduction, it would be to trim the CoT discussion to a sentence and move the detailed argument to an appendix. No major restructuring is needed.

## 8) ICLR Formal Scores
- **Soundness (4/4):** Claims are well‑supported by rigorous probing, causal interventions, and geometric measurements. Methodology is sound, with strong controls for confounds.
- **Presentation (4/4):** Exceptional clarity; the figures and tables are informative, the narrative flows logically, and the paper carefully distinguishes evaluation modes. Reproduction should be straightforward.
- **Contribution (4/4):** A genuinely new mechanistic insight—the geometric readout bottleneck—replacing a vague behavioral failure with a precise, testable causal explanation. The minimal repair strategy is elegant and generalizable.
- **Significance (4/4):** This will likely influence subsequent work on output‑head geometry and competence‑without‑performance failures. The diagnostic pipeline (probe → alignment → repair) is a model for future interpretability research.
- **Overall (7/10):** Strong accept. Well above the poster mean, with clear contribution, thorough evaluation, and a memorable finding. I would not go to 8 because the deployability claim is not yet fully de‑risked by a broader language modeling check, and the task scope is bounded to low‑vocabulary aggregation.
- **Confidence (4/5):** Confident in the main findings; the only uncertainty is the general‑language impact of the LoRA Q/V repair, which I consider minor.

## 9) Final Recommendation
**ICLR: Accept (7 — Strong Accept)**  

This paper provides a crisp, mechanistic explanation for a puzzling LLM failure through a combination of probing, geometric analysis, and targeted causal interventions. The evidence is thorough and well‑controlled, and the resulting insight is both deep and actionable. While the absence of a perplexity evaluation after fine‑tuning slightly limits the claim of a deployable fix, it does not diminish the core contribution. I expect this work to be widely shared and cited, and it deserves a strong accept.