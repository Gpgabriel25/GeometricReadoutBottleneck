# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: ✅ Pass. No author-identifying information, no non-anonymous repo links, no acknowledgments, no self-revealing phrasing found.
- **Style files**: ✅ Pass. `iclr2027_conference` package is used. (Note: a stray source comment reads "NeurIPS 2026 style" — harmless, but sloppy; the compiled style is correct.)
- **Required AI use statement**: ✅ Present.
- **Page limit**: ⚠️ **Cannot verify from source.** The main text is dense (8 sections, 7 main-text tables, 4 figures); it plausibly sits at or near the 9-page limit. Authors should verify.

No desk-reject risk items beyond the unverifiable page count.

---

## 1) Core Thesis & Significance

The paper asks whether LLM counting failures arise from missing internal representations or from a failure to read those representations out into digit tokens. Across Pythia-410M, Mistral-7B, Qwen3-8B/14B, it argues the latter: linear probes decode counts at R² > 0.99 from directions statistically indistinguishable from orthogonal to `lm_head` digit rows (|cos| ≤ 0.032 vs. random baseline 0.013); a 9-row (36,864-param) repair of the output head fixes digit-restricted decoding but not generation (0.0%); LoRA Q/V rank-16 restores true greedy generation (83.1% ± 7.2%), with logit-lens rank of the correct digit dropping from 55,980 to 1.

The problem is real and widely recognized (counting is a notorious LLM failure mode), and the contribution is cleanly summarizable — one of the paper's strengths. Novelty is component-level rather than conceptual: "models know more than they say" is well-trodden (logit lens, tuned lens, probing literature); the new elements are (i) the specific probe-direction-vs-unembedding-row geometry with proper baselines, and (ii) causal localization via minimal row repair with necessity/sufficiency controls. This is a legitimate, well-executed increment for the mech-interp community.

## 2) Technical Soundness

No fatal flaws. Three significant concerns and several typical limitations:

**(b) Significant concern 1 — Probe validity at the "entity-mean" position.** The headline "the model knows the count" evidence rests on probes at the "entity-mean position," which is **never precisely defined in the main text**. Critically, Table 2 reports R² = 0.977 at **layer 0** — i.e., the count is nearly linearly decodable from raw embeddings before any transformer computation. This strongly suggests a positional/statistical leak: if hidden states are averaged over entity-mention positions, the count *is* the number of averaged positions, and averaging C positional embeddings leaks set-size (variance shrinkage) regardless of any model computation. The factorial design randomizes distractors, length, and spacing *categories* independent of count, but it cannot remove the trivial "number of mention positions" signal available at an aggregated position. Table 7 conspicuously leaves the last-token probe R² as "---". The core conclusion is rescued by the answer-position evidence (9-row repair trains a linear map from *final* hidden states and generalizes held-out; logit-lens at last-token reaches 41.6% > chance), but the paper's central premise as *presented* is partially confounded. Required fix: report last-token/answer-position probe R² in the main text and add a position-statistics control (e.g., count-matched position shuffles).

**(b) Significant concern 2 — Protocol-dependent magnitude of the flagship diagnostic.** The 9-row repair on entity counting is reported as 60.7% ± 3.1 (unified, Table 3), 93.8% (cross-model panel, Table 5), 97.5% (train), and 99.9% (instruct mode). The unified-vs-panel gap of 33 points is attributed to "seed, template, and mode differences," yet between-seed SD is only ±3.1 and baselines are nearly identical across the two protocols (13.7% vs. 11.3%) — so the stated explanation is incomplete; the real driver appears to be bare-prompt vs. diverse-template test difficulty (as the DPS appendix admits for the 96.3% → 13.2% flip). The problem is decision-relevant: **the cross-model generalization claims (Mistral 92.0%, 14B 90.3%) rest on the easier protocol**, while the honest headline number is 60.7%. The qualitative orderings (repair helps constrained decoding; fails generation; LoRA fixes generation) are robust across all protocols, so the thesis survives — but effect sizes are unstable, and the instruct-mode 99.9% (39 pp above unified) is never reconciled.

**(b) Significant concern 3 — The "deployable fix" is unevaluated for collateral damage.** LoRA Q/V is fine-tuned on counting data and pitched as deployable, but there is **no measurement of general-capability regression** (MMLU/GSM8K after the intervention). MMLU/GSM8K appear only as pre-intervention negative controls. One table would settle this.

**(c) Typical limitations**: (i) DPS and probe-round are near-circular diagnostics — hard DPS (add +100 to the probe-predicted digit) trivially restates probe accuracy; the authors mostly label these honestly as oracle/verification tools, but the abstract's framing ("two interventions") slightly inflates them. (ii) The gradient-dynamics explanation for orthogonality is speculative but is at least partially tested (3.2× vs. 1.1× alignment movement under counting vs. arithmetic fine-tuning). (iii) Greedy-only decoding; small N (200–900 prompts). (iv) A numerical wobble: at 14B, |cos| = 0.011 is claimed as "0.57× random baseline," but E[|cos|] for random directions in d = 5120 is ≈ 0.011, so this is ≈ 1.0×, not 0.57× — please clarify the baseline definition. Similarly, the count-probe |cos| appears as 0.016 (mean), 0.032 (per-layer max), and 0.035 (positive-control section) without reconciliation.

**Credit where due**: the controls are well above the mech-interp norm — shuffled-label probes, random-direction baselines, permutation tests, TOST equivalence, a positive control (expressed-feature direction at |cos| = 0.115, 3.3× the count probe), shuffled-row and random-position necessity/sufficiency controls, a locus ablation, and negative controls on MMLU/GSM8K. The parameter accounting is internally consistent everywhere I checked (36,864 = 9×4096; 7.67M LoRA matches GQA dims; 83.1 ± 7.2 recomputes exactly from the five per-seed values; stratified table averages to the unified mean). This level of care merits recognition.

## 3) Empirical Rigor

**Strengths**: multi-model (3 families + 14B), seven task variants, three evaluation modes, seeds with SDs reported, necessity/sufficiency controls, negative controls demonstrating scope (|cos| = 0.31–0.48 on MMLU vs. ≤ 0.032 for counting — the effect is specific, not a generic artifact). The two-phase encoding/projection story is supported by the logit-lens depth profile.

**Gaps**:
- *Task heterogeneity undermines the "generalizes" framing*: the addition baseline is already 93.3% (digit-restricted) — a 6.7 pp gap to probe-round is not a "bottleneck" in any meaningful sense. The strong failure is entity counting (13.7%); the other tasks show partial or weak effects. The abstract's "60.7–100.0% across four tasks" conceals this.
- *No CoT numbers in the main text*. For a paper whose title promises a fix and whose discussion mechanistically explains CoT, the actual CoT comparison is deferred to the supplement with no number given. The mechanistic explanation of CoT ("each reasoning step re-encodes the count...") is asserted, not tested — the authors admit this ("open question"), which is honest, but then the claim "to explain why CoT helps" should be softened.
- *Overclaiming check*: the title's "How to Fix It" oversells — the fix is task-specific fine-tuning (7.67M params, 200 steps on synthetic counting data) with a mechanistic account of why it works; that is valuable, but it is not a general remedy for counting. The motivation's "best models achieve ≤24%" is unsubstantiated (no frontier models tested, no citation). "Showing that the information is present" (abstract) should be "consistent with the information being present" given the aggregation confound above. Otherwise, claims are unusually carefully scoped (the limitations section is exemplary).

## 4) Competitive Realism Check

Against accepted ICLR mech-interp papers: the control density exceeds the median, the causal interventions go beyond correlational probing, and the central finding is qualitative and robust across protocols. The protocol bookkeeping burden is worse than average, and the unaddressed layer-0 probe anomaly is a genuine hole an expert reviewer will find — but the answer-position intervention evidence substantially mitigates it. I would expect at least two reasonable reviewers to score this ≥ 5. It is within acceptance variance for a poster, not comfortably above it.

## 5) Weakest Link Analysis

**Weakest link**: the combination of the entity-mean probe confound (Significant Concern 1) with the unstable flagship magnitude (Concern 2) — a skeptical reviewer can argue the paper's *premise* evidence (probes) is artifact-vulnerable and its *effect size* is protocol-dependent, leaving only "fine-tuning on the task improves the task, with a mechanistic story." This is **addressable in revision** (answer-position probe R² + position-leak control; unified protocol for the cross-model panel), not fundamental, and the convergent intervention evidence makes it unlikely to fully overturn the thesis.

## 6) Convergence Test

- **If unchanged, ≥50% acceptance chance?** Marginal — I estimate roughly 50%. The convergent causal evidence and honest scoping give it a real shot; the probe confound and protocol instability give a capable reviewer grounds to push to 4.
- **Minimal change to clear the threshold**: (i) report last-token/answer-position probe R² in the main text plus a position-statistics control addressing the layer-0 anomaly; (ii) re-run the cross-model repair table (Table 5) under the unified protocol, or provide a difficulty decomposition that actually explains 60.7 vs. 93.8; (iii) one table of MMLU/GSM8K before/after LoRA Q/V; (iv) define "entity-mean position" precisely. All are small experiments, not new research directions.

## 7) Structural Sharpness & Scope Control

The paper is well centered on one dominant contribution — the geometric readout bottleneck — and the three-claim structure in the introduction is effective. Classification of content:
- **(a) Strengthens**: logit-lens two-phase analysis; necessity/sufficiency controls; negative controls on MMLU/GSM8K; LoRA mechanism measurements (rank 55,980 → 1; probe direction invariant at layer 2).
- **(b) Neutral**: majority vote, max extraction, multi-digit extension, format robustness — supportive but compressible.
- **(c) New attack surface**: the instruct-mode and natural-language extensions (with the unreconciled 99.9% figure) and the single-seed DPS appendix (96.3% vs. 13.2% flip) invite protocol confusion and skepticism. **Recommendation**: consolidate on the unified protocol as the single canonical presentation, move all protocol variants to the appendix, and cut or compress the majority-vote/max-extraction results to one table. A paper that needs a "How to read the numbers" paragraph and a protocol-map appendix is telling you its experimental bookkeeping has outgrown its main text.

## 8) ICLR Formal Scores

- **Soundness: 3**. The causal localization logic is sound and unusually well-controlled, but the central probe evidence is measured at an undefined, shortcut-vulnerable aggregated position (layer-0 R² = 0.977 is a red flag), the answer-position probe R² is missing from the main text, and flagship magnitudes swing 60.7–99.9% across tables.
- **Presentation: 3**. Clearly written with honest scoping and reproducible parameter-level detail, but the protocol proliferation forces constant cross-referencing, and a load-bearing experimental detail (probe position) is undefined.
- **Contribution: 3**. A crisp new geometric characterization (probe-direction vs. unembedding-row orthogonality with proper baselines) plus an elegant minimal causal probe (9-row repair); incremental over the established "models know more than they say" literature.
- **Significance: 3**. Counting failures are a flagship LLM embarrassment and the mech-interp community will cite the geometric diagnosis and the rank-55,980→1 result; impact is contained by the narrow task class (low-vocabulary aggregation) and the fact that the practical fix is task-specific fine-tuning.
- **Overall: 5**. A solid, well-controlled mechanistic study that meets the ICLR poster bar: convergent causal evidence for a memorable thesis, held back from clear-accept by a probe-validity gap in the premise evidence, protocol-dependent effect sizes, and a missing collateral-damage evaluation for the proposed fix.
- **Confidence: 4**. I verified internal numerical consistency in detail and reasoned through the high-dimensional geometry; supplement and figures were not available, so some appendix-dependent claims could not be checked.

## 9) Final Recommendation

**Borderline Accept (5).** This is a carefully executed mech-interp study with a falsifiable thesis, genuine causal interventions, and control rigor well above the venue median for this genre — the kind of paper that lands as a poster. It does not clear the clear-accept bar because the "the model knows the count" premise is currently supported at a probe position vulnerable to a positional-statistics artifact (layer-0 R² = 0.977 demands an explanation), and the flagship diagnostic's effect size is protocol-dependent (60.7% vs. 93.8% vs. 99.9%) in ways the paper documents but does not resolve. The four minimal additions in Section 6 would make this a comfortable accept; none requires new ideas, only discipline in measurement and reporting.