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