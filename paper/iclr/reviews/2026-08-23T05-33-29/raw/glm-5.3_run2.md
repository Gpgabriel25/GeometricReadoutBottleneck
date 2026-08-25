⚠ **DESK-REJECT RISK CHECK (ICLR 2027)**

- **Anonymity**: Compliant. Authors anonymized; no repo links, acknowledgments, or self-identifying phrasing detected. (A stray LaTeX backslash in `\author{Anonymous authors\ ...}` is a typo, not a violation.)
- **Style files**: `iclr2027_conference` is loaded correctly with `article` class. A stale comment ("% NeurIPS 2026 style") contradicts the actual style used — cosmetic, should be removed, but not a violation.
- **AI use statement**: Present and compliant.
- **Page limit**: **Cannot verify from source.** The main text carries 3 figures, 5 tables, and seven dense sections; it plausibly presses against the 9-page limit. Flagging as unverifiable — authors should confirm. Note that the CoT comparison's quantitative results are deferred to the supplement ("available in the supplement"), which is acceptable only if the main-text claims do not depend on them (see §3).

---

## 1) Core Thesis & Significance

**Thesis.** The paper argues that transformer counting failures are a *geometric readout bottleneck*: counts are linearly encoded in the residual stream (probe R² > 0.99), but the encoding direction is statistically indistinguishable from orthogonal to the `lm_head` digit rows (|cos| ≈ random), so the model cannot emit what it knows. Two causal interventions localize the failure: a 9-row output-head repair (36,864 params) fixes constrained digit decoding but not generation; LoRA on attention Q/V (7.67M params) fixes upstream routing and achieves 83.1% in true autoregressive generation.

**Assessment.** The problem is real and widely recognized (the "count the r's in strawberry" folklore), and the diagnosis-versus-repair framing is crisp and falsifiable. Novelty is primarily **integration-level**: probes, logit lens, unembedding fine-tuning, and LoRA are all standard tools; the new content is the quantified orthogonality signature, the dual-locus intervention logic (output head vs. upstream routing), and the negative controls on MMLU/GSM8K showing the misalignment is task-specific. The contribution is unambiguously summarizable, which is a strength. Significance for the mech-interp community is solid — "the model knows the count but the output pathway is misaligned" is a memorable, quotable finding — though practical impact is tempered by the fact that CoT already fixes counting at inference time (see §3, §4).

## 2) Technical Soundness

The causal logic is better than average for this genre: shuffled-label probes, random-direction controls with permutation tests and TOST equivalence, shuffled-row and random-position necessity/sufficiency controls, locus ablations across Q/K/V/O/MLP, and a norm-rescaling experiment decomposing direction vs. magnitude competition. The training-dynamics account (digit rows pulled toward non-counting contexts; orthogonality as a stable fixed point) is supported by a clean fine-tuning contrast (counting FT moves |cos| 3.2×; arithmetic FT doesn't).

Issues, classified:

**(a) Fatal flaws:** None identified.

**(b) Significant concerns (decision-relevant but fixable):**

1. **Space ambiguity in the geometric claim.** The residual stream passes through the final RMSNorm (a learned diagonal rescaling) before `lm_head`. The paper reports cosines between probe directions and digit rows without stating unambiguously whether both are expressed in the *same* (pre- or post-norm) coordinates. A diagonal scaling can materially rotate directions, so the headline |cos| ≤ 0.032 number needs this specification. The causal interventions rescue the operational conclusion, but the geometric measurement — the paper's contribution (1) — should be airtight.
2. **Missing last-token probe R².** Table 4 reports last-token probe R² as "---", yet the "knows but can't say" claim is strongest if the count is decodable *at the position the output head actually reads*. If last-token R² is also >0.99, say so; if it is lower, part of the story is information not being moved to the output position, which is a different (and partly upstream) failure than pure readout misalignment. The text's mention of "partial transfer" in layers 20–35 hints the latter.
3. **Numeric consistency at 14B.** "At 14B the misalignment sharpens (|cos| = 0.011, 0.57× random baseline)": for hidden dim 5120, the expected |cos| for random directions is ≈ 0.011, which would make 0.011 ≈ 1.0× random, not 0.57×. Either the random baseline is computed differently at 14B (needs specification) or this claim is internally inconsistent with the 8B baseline (0.013 at d=4096).
4. **Unresolved 37-pp entity-counting gap.** Probe-round reaches 98.7% but 9-row repair only 60.7%, with strong count-magnitude dependence (30.6% at count 7; Table 8). Both decoders are linear, so "readout misalignment is the bottleneck" does not by itself predict this gap. The capacity ablation (Adam fitting: 67.5%; 59 rows: no gain) rules out two explanations but the paper concedes the remaining hypotheses are undiscriminated. Not fatal — the paper scopes this honestly — but it limits how cleanly claim (1) explains the full behavioral failure.

**(c) Typical limitations (common in accepted work):** single-seed protocol origins for some appendix results; Pythia-410M repair failure (scoped honestly); intervention suite concentrated on Qwen3-8B with Mistral receiving one held-out number; the |cos| "stable fixed point" argument is qualitative.

## 3) Empirical Rigor

**Strengths.** The unified evaluation table (Table 1) anchoring all methods under shared prompts/seeds/scoring is exactly the right practice, as is the protocol map (Table 6) and the refreshingly explicit "How to read the numbers" paragraph. Multi-seed reporting with per-seed values, bootstrap CIs, and negative controls (MMLU: |cos| = 0.31–0.48, adaptation *degrades* accuracy — a genuinely informative specificity control) exceed the norm for mech-interp submissions.

**Concerns.**

1. **Protocol sprawl creates apparent instability that reviewers will probe.** The same 9-row repair yields 60.7% (unified), 93.8% (cross-model panel), 97.5% (train), 99.9% (instruct). The paper explains these, and the abstract uses the conservative unified number — good — but the 60.7 vs 93.8 gap (33 pp) is attributed only to "single-seed train/held-out split," which does not obviously explain a gap of that size given the unified protocol's stratified breakdown averages ≈ 61%. The most plausible driver is count-distribution differences across test sets; this should be stated precisely.
2. **Soft DPS's collapse (96.3% single-seed → 13.2% multi-seed, an 83-pp swing)** is explained post hoc (non-digit tokens win full-vocab argmax under diverse templates) but reads as a result that was fragile to evaluation design. The narrative survives via hard DPS, yet a skeptical reader will ask how many other reported numbers are template-sensitive in ways not yet measured.
3. **CoT comparison lacks main-text numbers.** The discussion devotes a paragraph to CoT, states it "substantially improves" counting, and then defers all quantitative results to the supplement. Since CoT is the obvious practical alternative to LoRA Q/V, this comparison is core evidence for the significance of the proposed fix and belongs in the main text.
4. **DROP is the honest but damaging control.** On the one natural-distribution benchmark (single-digit DROP subset), probe-round moves accuracy only 20.0% → 30.0%. The synthetic-task effects (96–100%) thus do not transfer strongly to natural counting data. The paper flags this as "partial structure," which is candid, but it caps the real-world significance of both the diagnosis and the repair.
5. Baselines are appropriate (probe-round as oracle upper bound; full lm_head; shuffled/random controls; locus ablation standing in for generic fine-tuning baselines). Trade-offs (params vs. accuracy vs. inference overhead) are quantified. Overclaiming is well-controlled: the title is broader than the evidence, but the body scopes claims carefully ("low-vocabulary aggregation," "mid-size and larger models").

## 4) Competitive Realism Check

Against the ICLR accepted population: this paper has above-average experimental hygiene for its subfield (controlled factorial data generation, equivalence testing, necessity/sufficiency controls, negative-control benchmarks, multi-seed reporting) and a clean, falsifiable central claim whose predictions are confirmed in the predicted order (constrained vs. generation modes). Its weaknesses — protocol multiplicity, single-family intervention depth, modest real-data transfer (DROP), unresolved diagnostic gaps — are the kind present in many accepted mech-interp papers, though the protocol sprawl is worse than typical. I would expect at least two reasonable reviewers to score this ≥5. It is not Oral-tier: the intervention suite leans on one model family, and several load-bearing numbers require a decoder ring to compare.

## 5) Weakest Link Analysis

**Weakest link: protocol-induced number instability.** A reviewer who reads 60.7% / 93.8% / 97.5% / 99.9% for the same intervention, plus an 83-pp soft-DPS swing across protocols, may conclude the results are fragile to evaluation choices and discount the headline claims accordingly. This is **addressable in revision** (report the unified protocol everywhere as primary; state exactly why the cross-model panel's test distribution yields 93.8%; move CoT numbers into the main text) and is **not fundamental** — the unified table, the causal interventions, and the geometric controls are mutually consistent. Barring that reading, the paper is close to **decision-stable**.

## 6) Convergence Test

- **As-is, ≥50% acceptance chance?** Yes, modestly — the profile (clear thesis, causal localization, strong controls, honest limitations) matches accepted ICLR mech-interp posters.
- **Minimal change to push comfortably over:** (i) consolidate all headline numbers to the unified multi-seed protocol with protocol-difference explanations that are *quantitative* (e.g., count-stratified test distributions), not qualitative; (ii) report last-token probe R² and specify the norm-space of all cosine measurements; (iii) put the CoT comparison numbers in the main text; (iv) resolve or explicitly caveat the 14B "0.57× random baseline" arithmetic.

## 7) Structural Sharpness & Scope Control

The paper is well-centered on one dominant contribution (the geometric readout bottleneck) and — unusually — most optional content *strengthens* the core: negative controls (MMLU/GSM8K), majority vote, max extraction, and multi-digit extension all test scope boundaries of the same mechanism (a). Neutral content: the training-dynamics fixed-point argument (b). Content introducing attack surface: the accumulation of protocols and the appendix's single-seed DPS archaeology — presenting the soft-DPS history invites the fragility critique without adding evidentiary weight; it could be compressed to a two-sentence footnote (c). No scope reduction beyond that is needed; the task suite is broad but each task earns its place.

## 8) ICLR Formal Scores

- **Soundness: 3** — Causal interventions and controls are strong; docked for the norm-space ambiguity in the central geometric measurement, the missing last-token probe R², and the unresolved 37-pp repair gap.
- **Presentation: 2** — Clear narrative arc and good tables, but protocol multiplicity burdens every quantitative claim, key comparisons (CoT) are pushed out of the main text, and at least one number (14B, 0.57× random) appears internally inconsistent.
- **Contribution: 3** — Integration-level novelty executed well; the orthogonality signature plus dual-locus repair logic is a genuinely new characterization of a well-known failure.
- **Significance: 3** — Memorable diagnosis that the interp community will cite and reuse as a template (probe → align → repair); practical impact limited by task-specific fine-tuning and weak DROP transfer.
- **Overall: 6** — Clear accept. Comfortably above the poster mean on evidence quality and controls; held below 7 by protocol instability, single-family intervention depth, and the modest real-data effect.
- **Confidence: 4** — I am confident in the assessment of the causal logic and controls; I could not verify page count or reproduce numbers, and the norm-space question leaves some residual uncertainty about the exact magnitude of the geometric claim.

## 9) Final Recommendation

**ICLR: Accept (6).** This is a solid, well-controlled mechanistic study with a quotable central finding and unusually honest scoping; its flaws (protocol sprawl, one unresolved diagnostic gap, thin real-data transfer) are the addressable kind, not the disqualifying kind. In a ~27% acceptance pool this paper reads as a reliable poster acceptance, with an outside chance at a higher tier if the rebuttal cleanly consolidates the protocol story and supplies the missing last-token probe R² and CoT numbers.