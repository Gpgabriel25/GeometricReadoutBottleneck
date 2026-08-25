# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: ✅ No author-identifying information found; no non-anonymous repo links; no acknowledgments.
- **Page limit**: ⚠️ **Cannot verify from source.** The main text is dense (7 tables, 3 figures, 9 sections); it plausibly approaches or exceeds 9 pages. Authors should verify; core evidence does appear to live in the main text.
- **Required AI use statement**: ✅ Present.
- **Style files**: ✅ Uses `iclr2027_conference`. The stale comment "% NeurIPS 2026 style" above it is sloppy but harmless. Minor LaTeX typo in `\author{Anonymous authors\ ...}` (single backslash line break).

No desk-reject risks identified beyond the unverifiable page count.

---

## 1) Core Thesis & Significance

The paper asks whether LLM counting failures stem from absent internal representations or from an inability to read those representations out into output tokens. Using linear probes, logit-lens, and cosine geometry, it shows that counts are linearly encoded with R² > 0.99 in Qwen3-8B/Mistral-7B/Pythia-410M/14B, but the count-encoding direction is statistically indistinguishable from random relative to `lm_head` digit rows (|cos| ≤ 0.032). Two interventions causally dissociate the stages: fine-tuning only 9 digit rows (36,864 params) fixes constrained digit decoding (60.7–100%) but not autoregressive generation (0.0%); LoRA Q/V rank-16 (7.67M params) fixes upstream routing and achieves 83.1% ± 7.2% in true greedy generation.

The problem is practically relevant (counting is a famous, widely-shared LLM failure), and the contribution is a novel *integration*: standard tools (probes, logit lens, LoRA) combined into a clean causal argument with a memorable finding ("the model knows the count but the output head can't say it"). The contribution is unambiguously summarizable. Novelty is component-level but the central finding — orthogonality of a perfectly-encoded feature to its output rows, with a 9-row repair causally confirming it — is, to my knowledge, new.

## 2) Technical Soundness

The core diagnosis is well-supported and unusually well-controlled: shuffled-label probes (R² = −0.042), random-direction cosines with permutation and TOST equivalence tests, shuffled-row and random-position repair controls, format robustness, negative controls on MMLU/GSM8K (|cos| = 0.31–0.48 vs. ≤ 0.032), and the falsifiable-prediction structure (row repair fixes constrained but not generation; upstream repair fixes both; logit-masked generation at 59.2% matches constrained 60.7%) is genuinely confirmatory. The logit-lens rank shift (55,980 → 1) after LoRA Q/V, and the dissociation between count-probe direction stability at layer 2 and final-layer alignment improvement, are strong mechanistic evidence.

Issues:

- **(b) Significant concern — no capability-retention evaluation for the deployable fix.** A 7.67M-parameter intervention on attention Q/V is claimed to be "deployable," but the paper never measures collateral damage: no post-LoRA perplexity, MMLU, or GSM8K. The MMLU numbers reported (70.2% baseline, 55.6% after output-row adaptation) are for the *negative control*, not for LoRA. For a paper whose title promises a fix, the cost of the fix is unquantified.
- **(b) Significant concern — protocol heterogeneity produces internal inconsistency.** The same 9-row repair yields 60.7% (unified multi-seed), 93.8% (single-seed cross-model panel), 97.5% (train), and 99.9% (instruct). The paper is commendably transparent ("How to read the numbers," protocol map), but a 33-pp swing between the unified and cross-model held-out numbers — both on held-out prompts — is attributed only to "seed, template, and mode differences" without a decomposition. This weakens confidence in which number represents the method.
- **(c) Typical limitation** — the gradient-dynamics explanation for orthogonality is plausible and supported by the fine-tuning contrast (3.2× vs. 1.1×), but remains a sketch rather than a derivation.
- **(c) Typical limitation** — Pythia-410M repair fails (31.4%); claim is honestly scoped to mid-size models.

No fatal flaws. The causal logic is sound and the controls exceed the venue norm.

## 3) Empirical Rigor

**Strengths:** multi-seed reporting with SDs, 500-prompt logit-lens, stratified by-count analysis (Table 8 honestly reveals the 9-row repair degrades to ~30–40% at counts 5–7 — this is the kind of unflattering detail that strengthens credibility), negative controls, capacity ablations (Adam vs. ridge; 9 vs. 59 rows), and locus ablation across Q/K/V/O/MLP.

**Gaps:**

1. **CoT baseline has no number in the main text.** For a paper titled "How to Fix It," the most obvious competing fix (prompt the model to count step-by-step) is discussed qualitatively and relegated to the supplement. The discussion is mechanistically thoughtful, but a number is needed in the main text.
2. **The locus ablation — the key evidence that Q/V specifically matters — is summarized in one sentence without a table.** This is the paper's main defense against "you just fine-tuned on counting data," and it deserves quantitative exposure.
3. **Addition as evidence of generality is weak**: baseline is already 93.3% (digit-restricted). The abstract's claim that the bottleneck "generalizes across … addition" overstates a near-ceiling case.
4. Train/test splits are within one synthetic generator; the natural-language extension (96.3% probe-round vs. 88.7% baseline) and DROP (+10 pp) partially address distributional generality, and the DROP result honestly shows only partial transfer.
5. Overclaiming check: mostly clean. The title's "Fix It" is defensible given 83.1% generation, but the fix is in-domain LoRA fine-tuning — closer to standard practice than the "geometric repair" framing suggests. The abstract accurately reports the 0.0% generation failure of the 9-row repair.

## 4) Competitive Realism Check

Compared to accepted ICLR mechanistic-interpretability papers, this one has *above-average* experimental hygiene: negative controls, equivalence testing, necessity/sufficiency controls, and mode-matched evaluation are more than I typically see. The central dissociation (output-head repair fixes constrained decoding but not generation; upstream repair fixes both) is a clean, memorable result that reviewers will appreciate. The weaknesses (no capability-retention check, protocol soup, modest 14B scale ceiling) are the kind present in many accepted papers. At least two reasonable reviewers would score this ≥5; I would expect scores in the 5–7 band with a likely poster outcome.

## 5) Weakest Link Analysis

**Weakest link: the deployable intervention (LoRA Q/V) is validated only on the target task family, with no measurement of what it breaks.** A reviewer can accept the diagnosis fully and still object that "correcting upstream routing" is indistinguishable from ordinary task fine-tuning until general-capability retention and the full locus-ablation numbers are shown.

- **Addressable in revision**: yes — a post-LoRA MMLU/GSM8K/perplexity table and a locus-ablation table are cheap experiments relative to what's already here.
- **Fundamental**: no.
- **Unlikely to change the outcome**: the diagnosis stands independently, so this caps the score rather than flipping it.

Secondary link: the 60.7%-vs-93.8% protocol inconsistency, which is addressable by a decomposition or by reporting the cross-model panel under the unified protocol.

## 6) Convergence Test

- **If unchanged, ≥50% acceptance chance at ICLR?** Yes — I estimate ~60%. The controls, causal dissociation, and honest scoping put it comfortably at poster level.
- **Minimal change to push it toward 7:** (i) a capability-retention table for LoRA Q/V (MMLU/GSM8K/perplexity before/after); (ii) the CoT accuracy number and the locus-ablation table in the main text; (iii) re-running the cross-model comparison under the unified protocol to collapse the 60.7/93.8 discrepancy.

## 7) Structural Sharpness & Scope Control

The paper is centered on one dominant contribution (the geometric readout bottleneck) and the three nested claims give it a clear spine.

- **(a) Strengthens**: negative controls (MMLU/GSM8K), stratified by-count table, generation-mode dissociation with logit-masked control, the "why orthogonality is stable" analysis.
- **(b) Neutral**: majority vote, max extraction, multi-digit extension — useful generality evidence but each adds a new protocol and thus attack surface.
- **(c) New attack surface**: the sheer count of reported protocols (single-seed DPS, unified, cross-model, instruct, stratified, generation) forces the "How to read the numbers" section into existence. I recommend consolidating to two protocols (unified constrained + generation) in the main text and moving the rest entirely to the appendix; and dropping or compressing the addition task (near-ceiling baseline) from the headline range "60.7–100.0%," which currently spans from underwhelming to perfect across tasks with very different baselines.

## 8) ICLR Formal Scores

- **Soundness: 3/4.** Claims are well-supported by controlled, multi-seed experiments with appropriate statistics; docked for the missing capability-retention evaluation of the deployable intervention and the unexplained magnitude of cross-protocol discrepancies.
- **Presentation: 3/4.** Clear prose, explicit claim structure, and an unusually honest protocol map; but the number multiplicity (four different accuracies for one intervention in the main text) taxes the reader, and figures could not be inspected from the source.
- **Contribution: 3/4.** Novel geometric diagnosis of a well-known failure with causal localization via a 9-row repair; the intervention itself is standard LoRA with a good locus analysis.
- **Significance: 3/4.** Counting is a high-visibility failure mode; the probe→align→repair diagnostic recipe and the "competence without performance" framing will be cited and reused. Not field-shaping.
- **Overall: 6/10.** Clear accept. Good work with addressable gaps — above the poster mean, not oral-tier.
- **Confidence: 4/5.** Confident in the assessment; figures and the supplement were not inspectable, and the exact page count could not be verified.

## 9) Final Recommendation

**Accept (6).** This is a well-controlled mechanistic study with a memorable central finding, honest negative controls, and a causal dissociation (constrained vs. generation repair) that few papers in this genre deliver. The main gaps — no capability-retention measurement for the LoRA fix, the CoT baseline absent from the main text, and protocol-induced number inconsistencies — are all addressable in rebuttal or revision and do not undermine the core diagnosis. I expect it to land as a solid poster at ICLR.