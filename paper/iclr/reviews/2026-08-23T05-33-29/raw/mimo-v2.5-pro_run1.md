# Review: "Why Transformers Fail at Counting and How to Fix It"

---

## ⚠ Desk-Review Compliance

- **Anonymity**: Clean. No identifiable information detected in main text or supplementary material. Author line reads "Anonymous authors."
- **Page limit**: Main text body fits within 9 pages (references and appendices excluded). Compliant.
- **AI use statement**: Present at end of main text. Compliant.
- **Style files**: Uses `iclr2027_conference` style. Compliant.

No desk-reject risk items.

---

## 1) Core Thesis & Significance

**Central contribution.** The paper diagnoses LLM counting failures as a *geometric readout bottleneck*: linear probes recover counts at R²>0.99 from intermediate layers, yet the probe-identified directions are nearly orthogonal (|cos| ≤ 0.032) to the output-head digit rows — statistically indistinguishable from random. A minimal 9-row lm_head repair localizes the bottleneck causally to the output stage (constrained decoding up to 100%), while a LoRA Q/V intervention corrects upstream routing and achieves 83.1% in autoregressive generation.

**Problem relevance.** Counting failures in LLMs are well-documented, practically annoying, and surprisingly persistent. Prior work documented the phenomenon without a principled mechanistic explanation. The problem is relevant — and importantly, the paper scopes itself explicitly to low-vocabulary aggregation rather than claiming broad applicability.

**Novelty.** This is both component-level (the geometric orthogonality finding is new) and integration-level (the pipeline from probes → logit-lens → cosine alignment → causal interventions is a coherent diagnostic framework). The "probe-round" construction and the contrast between constrained decoding and generation as diagnostic tools are clever experimental designs.

**Unambiguous summarizability.** Yes. A reviewer can condense the contribution to: "Transformers encode counts internally but can't read them out because the encoding subspace is orthogonal to digit output weights; selective repair proves it."

---

## 2) Technical Soundness

**Theoretical claims.** The paper's core claim — that orthogonality is a structural, stable property of the trained model — is supported by multiple converging lines of evidence:
- Four probe types (ridge, LDA, mean-difference, PCA) all recover the same geometry.
- Permutation tests (p=0.79) and TOST equivalence testing confirm the alignment is no better than random.
- Necessity/sufficiency controls (shuffled-digit rows degrade below baseline; random-position rows match baseline) confirm the specific row-token mapping matters.
- The training dynamics explanation (digit rows conditioned on non-counting contexts producing E[h|y=digit] orthogonal to counts) is tested via A/B fine-tuning (3.2× vs. 1.1× alignment change).

**Identified issues:**

(a) **No fatal flaws.** The causal chain — encode → misalign → misroute — is each supported by direct evidence with appropriate controls.

(b) **Significant concern — entity-counting gap.** The 37 pp gap between probe-round (98.7%) and 9-row repair (60.7%) on entity counting is the weakest point. The paper offers two partial explanations (digit-row norm competition accounting for fullvocab 0%→26.5%, hidden-state diversity 1.5× higher for entity vs. list-length) but does not disentangle them. The capacity ablation (Adam fine-tuning 67.5%, expanded-row 67.5%) rules out fitting/regularization as explanations, which is useful. However, the 60.7% ceiling on the primary task remains somewhat unsatisfying and needs further decomposition. This is fixable but relevant to the "how to fix" framing of the title.

(c) **Typical limitation — Pythia-410M.** The 9-row repair achieves only 31.4% on Pythia, limiting cross-model claims at small scale. The authors honestly acknowledge this and appropriately scope the repair claim to mid-size+ models. This is within normal acceptance variance.

(d) **Typical limitation — explanation of orthogonality origin.** The training-dynamics argument is plausible and tested indirectly, but not proven from scratch. This is the standard limitation of post-hoc interpretability work and not penalized.

---

## 3) Empirical Rigor

**Strengths (extensive):**
- Three model families (Pythia, Mistral, Qwen3) spanning 0.4B–14B.
- Four tasks sharing the same evaluation protocol (entity counting, character counting, addition, list length) plus extensions to majority vote, max extraction, and multi-digit counts.
- Negative controls on MMLU and GSM8K confirming the bottleneck is specific (|cos| = 0.31–0.48 vs. ≤0.032).
- Multi-seed evaluation (3 seeds × 200 prompts, or 5 seeds for generation) with standard deviations reported.
- Shuffled-label controls, random-direction baselines, permutation tests, TOST equivalence testing — this is above-average statistical rigor for an ICLR interpretability paper.
- Format robustness (4 formats), instruct-mode persistence, natural-language generalization (8 entity types, 3 held out).
- Per-count stratified breakdown (Table in Appendix) revealing magnitude-dependent accuracy patterns.
- Locus ablation (Q/K/V/O/MLP + combinations) confirming Q/V as the optimal intervention site.
- Logit-lens rank diagnostics (55,980→1) providing concrete mechanism illustration.

**Weaknesses:**
- Per-task generation accuracy breakdowns for LoRA Q/V are only given for entity counting (97.0%, 96.5%, 94.5%). Multi-task generation (71.5%–89.0%) across seeds hides per-task variation. Adding per-task generation numbers would strengthen the "how to fix it" claim.
- CoT is discussed as a comparison point but no quantitative CoT numbers are provided under their corrected scoring protocol. A quantitative comparison table would be informative.
- The natural-language counting extension (probe-round 96.3% vs. 88.7% baseline) is mentioned in passing but deserves more detail — this is important for the generalization claim.

**Overclaiming check.** The title "Why Transformers Fail at Counting and How to Fix It" is aggressive but defensible: the "why" is substantially argued (geometric misalignment), and the "fix" is partially achieved (83.1% in generation). The paper appropriately scopes all major claims to low-vocabulary aggregation and does not claim broad reasoning improvements beyond that scope. No factual overclaims detected.

---

## 4) Competitive Realism Check (Calibrated)

**Compared to typical ICLR accepted papers:**
- The experimental design is *more* thorough than average: multiple negative controls, causal localization with minimal interventions, TOST testing, cross-model validation.
- The mechanical interpretability contribution (geometric readout bottleneck as a general diagnostic concept) aligns well with a growing ICLR sub-area.
- The paper is well-centered on one dominant claim with multiple supporting evidence streams.

**Weaknesses vs. acceptance variance:**
- The 60.7% entity-counting ceiling is notable but within variance — accepted interpretability papers frequently have partial mechanistic explanations.
- The Qwen3-family dominance (Mistral and Pythia get less coverage) is typical of multi-model studies.
- The protocol-switching between tables (noted but requiring careful reading) is a presentation issue, not a soundness issue.

**Would two reasonable reviewers score this ≥5?** Yes. The core finding is clean, the experiments are unusually thorough for this type of work, and the scoping is honest. This clears the poster bar comfortably.

---

## 5) Weakest Link Analysis

The single issue most likely to flip accept/reject is the **uneven repair ceiling across tasks**: 60.7% on entity counting (the primary task) vs. ~100% on character counting, addition, and list-length. Reviewers skeptical of the "how to fix" framing may demand a fuller explanation of why entity counting is harder to repair, given that the same geometric signature (|cos| ≤ 0.032) appears across all tasks.

**Classification:** Addressable in revision. The existing partial explanations (norm competition, hidden-state diversity, count-magnitude dependence shown in the stratified table) could be combined into a more quantitative decomposition. Even without revision, the honest acknowledgment and partial evidence likely keep this in the "typical limitation" zone rather than "fatal flaw."

**Decision-stability assessment:** This issue is unlikely to flip the decision. The causal localization story (9-row repair works on 3/4 tasks, LoRA Q/V fixes the remaining gap) is strong enough that the entity-counting ceiling reads as an open question, not a refutation.

---

## 6) Convergence Test (Minimal-Change Threshold)

**If the authors made no further changes, does this have ≥50% acceptance chance at ICLR?**

**Yes, ~65–70%.** The paper is above the poster mean in contribution significance, experimental rigor, and novelty. The core narrative is clean, falsifiable, and well-supported. The weaknesses (entity-counting gap, limited Pythia results, CoT comparison slowness) are within typical ICLR acceptance variance for interpretability papers.

**Minimal change to push it over the threshold:** Add a quantitative comparison table with Chain-of-Thought under the same scoring protocol. CoT is the natural baseline intervention that practitioners currently use; showing that LoRA Q/V matches CoT accuracy at zero inference-time cost (vs. CoT's token multiplication) would make the practical contribution concrete and address the "so what?" question for practitioners. This is a single addition, not a restructuring.

---

## 7) Structural Sharpness & Scope Control

**Centered contribution?** Yes. The entire paper is organized around one dominant claim (geometric readout bottleneck) with three interventions serving as converging evidence. Every section advances the core narrative.

- **(a) Strengthens core argument:** Probe R² analysis (§4), logit-lens (§5), 9-row repair necessity/sufficiency controls (§6), LoRA Q/V locus ablation, negative controls on MMLU/GSM8K, cross-model validation, format robustness, generation-mode mismatch diagnosis. All of this is load-bearing.
- **(b) Neutral:** Some of the appendix material (format robustness, capacity ablation) adds depth without weakening the argument. The Multi-Digit Extension in the appendix is useful but could be condensed to increase the impact-to-length ratio.
- **(c) Introduces new attack surface:** None detected. The paper is disciplined in scope.

**Scope reductions that increase acceptance probability:** None needed. The paper is already well-scoped. If anything, the presentation could be tightened by moving the "How to Read the Numbers" paragraph and protocol disclaimers to the appendix — the multiple-protocol reporting is honest but creates cognitive load for reviewers.

---

## 8) ICLR Formal Scores

**Soundness (4/4):** Exceptionally rigorous. Multiple probe types, permutation tests, TOST equivalence, necessity/sufficiency controls, cross-model validation, and honest reporting of variance and limitations. No identified flaws in the experimental methodology.

**Presentation (3/4):** Clear overall with a well-structured narrative. The "how to read the numbers" paragraph is necessary but reveals that the multi-protocol reporting introduces some cognitive overhead. Key tables (Tables 1, 2, 3) are well-designed and informative. The pipeline figure in Figure 1 effectively communicates the diagnosis. Minor deduction for the density of protocol details requiring careful cross-referencing.

**Contribution (4/4):** Novel geometric diagnosis with a clean causal story. The observation that linearly decodable features can be output-inaccessible is a meaningful addition to the mechanistic interpretability toolkit, especially the demonstration that this is a stable fixed point of training dynamics. The multi-level intervention design (output-head repair + upstream routing correction) is elegant.

**Significance (3/4):** The finding enriches our understanding of a commonly observed LLM failure mode and offers a reusable diagnostic strategy (probe → alignment → targeted repair). The negative controls on MMLU/GSM8K appropriately bound the finding's scope to low-vocabulary aggregation. Bump to 4 would require demonstration that this diagnostic framework resolves other "competence without performance" failures beyond counting. As is, the community impact is meaningful for the interpretability subcommunity and counting/arithmetic researchers.

**Overall (6/10):** Clear accept. The paper provides a clean, falsifiable mechanistic explanation for a well-documented LLM failure mode, validated across three model families with unusually thorough experimental controls. It meets the ICLR poster bar comfortably and is above the poster mean — a solid contribution with a memorable core finding (knows but can't say) that will be easily cited and built upon.

**Confidence (4/5):** Confident. The experimental methodology is transparent and reproducible, and the claims are appropriately scoped. Slight uncertainty on whether the entity-counting ceiling might concern other reviewers enough to push toward reject, but I consider this unlikely given the multiple converging evidence streams.

---

## 9) Final Recommendation

**Accept (6/10) — Clear Poster Accept**

This paper presents a well-executed mechanistic study that cleanly isolates a geometric readout bottleneck as the cause of transformer counting failures. The experimental design is unusually thorough for this class of work: multiple model families, four validation tasks, negative controls on MMLU/GSM8K, necessity/sufficiency controls, TOST equivalence testing, and multi-level causal interventions. The core finding — that count-encoding directions are orthogonal to digit output-row weights, and that this orthogonality is a stable property of training dynamics — is novel, falsifiable, and memorable. The remaining gap on entity-counting repair (60.7%) and the limited Pythia results are typical limitations, not fatal flaws. The paper is above the ICLR poster mean in contribution significance and experimental rigor, and the "knows but can't say" framing will resonate with the interpretability community.