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