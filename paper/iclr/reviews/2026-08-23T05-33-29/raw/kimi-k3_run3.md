# Review: "Why Transformers Fail at Counting and How to Fix It"

## Desk-Reject Compliance Check

- **Anonymity**: ✓ Anonymized author block; no identifying links or acknowledgments detected. No violations found in the provided source.
- **Style files**: ✓ Uses `iclr2027_conference`. Minor: the preamble comment says "NeurIPS 2026 style," which is a stale copy-paste artifact — cosmetic only, but worth cleaning since it sits directly above the style import.
- **AI use statement**: ✓ Present ("AI Use Statement").
- **Page limit**: ⚠ Cannot verify exactly from LaTeX source. The main text contains 7 sections, 3 figures, and 3 main tables; it plausibly lands near the 9-page limit. Authors should verify compiled length. Core evidence (Tables 1–2, logit-lens results) does live in the main text, which is good.

No desk-reject risk items identified.

---

## 1) Core Thesis & Significance

**Thesis**: LLMs fail at counting not because they lack internal count representations (linear probes achieve R² > 0.99) but because the count-encoding direction is nearly orthogonal to the digit rows of the unembedding matrix (|cos| ≤ 0.032, statistically indistinguishable from random). This is demonstrated via probing, logit-lens, and three interventions (9-row lm_head repair, Diagnostic Probe Steering, LoRA Q/V), with the clean dissociation that output-row repair fixes constrained decoding but not generation, while upstream LoRA fixes generation.

**Relevance**: Counting failure is a well-documented, practically relevant puzzle; a mechanistic explanation with causal localization is valuable to the interpretability community.

**Novelty**: Component-level novelty is modest (probes, logit lens, LoRA are all standard tools), but the *integration* is genuinely novel: the geometric readout-bottleneck framing, the orthogonality measurement with equivalence testing, and the constrained-vs-generation dissociation as a causal localizer form a coherent, falsifiable story that goes beyond prior documentation of counting failures.

**Summarizability**: Yes — "the model knows the count but the output head can't read it" is unambiguous and memorable. This is a real strength.

## 2) Technical Soundness

- The probing methodology is careful: factorial prompt design decoupling count from length/distractors/spacing, shuffled-label controls (R² = −0.042), four probe types, permutation tests, and TOST equivalence testing for the orthogonality claim. This is better than typical probe-based papers.
- The gradient-based explanation for *why* orthogonality arises (E[h | y=digit] dominated by non-counting contexts) is plausible but hand-wavy; the supporting empirical test is weak: counting fine-tuning raises |cos| from 0.0074 to 0.0280 — a 3.2× relative increase that is *still essentially orthogonal*. This actually undercuts the "training realigns" implication and only weakly supports the "stable fixed point" claim. **(c) Typical limitation**, since the core orthogonality finding does not depend on this explanation.
- **Internal inconsistency (significant concern, (b))**: The introduction states probe-round "upper-bounds what any output-side intervention can reach," yet in Table 2, 9-row repair on character counting (98.0%) *exceeds* probe-round (96.8%). Either probe-round is not an upper bound, or the numbers come from non-comparable protocols. This needs reconciliation — it is exactly the kind of detail that erodes reviewer trust in a numbers-dense paper.
- **Baseline instability (significant concern, (b))**: Baseline entity-counting accuracy appears as 13.7%, 17.0%, 10.3%, 38.8%, 38.6%, and "≤24%" in different places. The "How to read the numbers" paragraph explains these as protocol differences (sampling, seeds, templates, modes), and the protocol map is a genuinely good-faith effort. But a 13.7% vs 38.8% swing on the *same model and task* from sampling choices means the benchmark is highly sensitive to prompt distribution, which weakens the precision of every gap measurement built on it.
- **Addition as a "bottleneck task" (significant concern, (b))**: Addition's digit-restricted baseline is already 93.3%, with probe-round at 100%. A ~7pp gap is not evidence of the dramatic representation–output gap that defines the paper's thesis. Including addition under the claim "the bottleneck generalizes across character counting, addition, and list length" is an overreach on the evidence shown.
- Hard DPS adds +100 to the probe-predicted digit's logit — this is oracle injection, and its 98.7% "matching probe-round" is nearly tautological. The paper mostly frames it as a diagnostic, which is acceptable, but its inclusion in headline tables alongside real interventions invites misreading. **(c)** given the labeling, though I would move it out of Table 1's main comparison.

No fatal flaws. The core causal claim (9-row repair suffices for constrained decoding; shuffled-row and random-position controls fail) is well-supported by necessity/sufficiency controls.

## 3) Empirical Rigor

**Strengths**:
- Three model families + 14B scaling check, where the misalignment *sharpens* (|cos| = 0.011) yet repair still works — this is a nice falsifiable-prediction test that survived.
- Negative controls (MMLU: no orthogonality, repair degrades performance; GSM8K) support specificity of the phenomenon.
- Generation-mode analysis is unusually honest: the 9-row repair scoring 0.0% in unconstrained generation is reported prominently, diagnosed via logit-masked generation (59.2% ≈ constrained accuracy), and used to motivate the LoRA intervention. This constrained/generation dissociation is arguably the paper's best scientific contribution.
- Multi-seed reporting for headline claims; per-seed breakdowns given for LoRA.
- Pythia-410M transfer failure (31.4%) is reported and used to scope claims rather than buried.

**Weaknesses**:
- LoRA Q/V is trained on the task distribution, so "LoRA fixes counting" is partially unsurprising — fine-tuning on counting fixes counting. The contribution is the *locus specificity* (Q/V ablation, logit-lens rank 55,980→1 measurement), which is genuinely informative, but the deployability framing ("a deployable LoRA intervention") overstates a task-specific fine-tune evaluated on held-out prompts from the same synthetic distribution. No truly OOD generalization test for LoRA (e.g., new templates, new entities at generation time) is reported.
- Multi-task LoRA generation variance is high (71.5–89.0% per seed, ±7.2%). The paper attributes this to task-mix artifacts using entity-only runs (94.5–97.0%), which is reasonable but means the headline 83.1% is the *weak* configuration.
- Entity-counting 9-row repair ceiling (60.7% vs 98.7% probe-round) is honestly reported with a capacity ablation ruling out regularization and row count — good — but the remaining 31pp gap is only hypothesized (norm competition vs intra-class variance), not resolved.

**Overclaiming check**: The title's "How to Fix It" overstates: the fixes are (a) oracle injection, (b) a constrained-decoding-only repair, or (c) task-specific fine-tuning at 83% on synthetic tasks. "How to Diagnose and Partially Repair It" would be accurate. This is assertive framing rather than factual misrepresentation, so I weight it lightly, but the abstract's "improves upstream routing and achieves 83.1%" similarly elides the fine-tuning requirement.

## 4) Competitive Realism Check (Calibrated)

Relative to accepted ICLR interpretability papers: the mechanism is clearer than average, the controls (shuffled labels, TOST, permutation, necessity/sufficiency, format robustness, negative-control benchmarks) are more thorough than typical, and the generation-vs-constrained dissociation is a genuinely useful finding that others will cite. The weaknesses (number proliferation, the UB inconsistency, addition overreach, LoRA-is-just-fine-tuning concern) are within acceptance variance — they are the kind of issues that show up in rebuttals and get partially resolved.

Would two reasonable reviewers score ≥5? Yes, I believe so. The central result is crisp enough that even a reviewer annoyed by the presentation would likely land at 5. A sympathetic reviewer could go to 7. A hostile reviewer focused on "LoRA fine-tuning is not a fix" and the baseline instability could argue 4. This is a solidly-above-bar poster with some decision variance.

## 5) Weakest Link Analysis

**Single most decision-relevant issue**: the proliferation of non-comparable numbers across protocols, culminating in the probe-round "upper bound" being exceeded by the 9-row repair on character counting (98.0% vs 96.8%). In a paper whose entire contribution is quantitative gap measurements, an apparent internal contradiction in the central table invites the inference that protocols were chosen post hoc. I do not believe this is cherry-picking — the paper's protocol map suggests the opposite intent — but the character-counting inversion is currently unexplained.

**Classification**: Addressable in revision (reconcile or retract the upper-bound framing, consolidate to one primary protocol in the main text). Not fundamental. If unresolved, it could flip a borderline reviewer to reject; if resolved, the paper is decision-stable at accept.

## 6) Convergence Test (Minimal-Change Threshold)

- **As-is, ≥50% acceptance chance?** Yes, marginally — I estimate ~55–65%. The core finding is strong enough to survive the presentation issues, but the variance is real.
- **Minimal changes to push clearly over the threshold** (evidence-based, not editorial):
  1. Reconcile the probe-round upper-bound inconsistency on character counting (either re-run under a shared protocol or remove the UB claim).
  2. Pick *one* protocol for all main-text claims and move alternatives to the appendix; state the single baseline number once.
  3. Add one OOD generation evaluation for LoRA Q/V (held-out templates/entities) to support the "deployable" claim, or downgrade that claim.
  4. Drop or re-scope addition from the "bottleneck generalizes" claim given its 93.3% baseline.

## 7) Structural Sharpness & Scope Control

The paper is centered on one dominant contribution (the geometric readout bottleneck) — good. However, execution is bloated and defensive:

- **Strengthens core argument**: the 9-row constrained/generation dissociation; the 14B sharpening result; MMLU/GSM8K negative controls; necessity/sufficiency controls; the capacity ablation.
- **Neutral**: DPS (mostly an oracle diagnostic that duplicates probe-round's information); majority-vote and max-extraction extensions (fine as appendix scope-boundary evidence).
- **Introduces attack surface**: (1) The repeated "what makes this a *bottleneck*" justifications appear at least three times in near-identical form — this reads as rebuttal-driven defensiveness and pads the paper. (2) Addition as a core task. (3) The gradient fixed-point story with its weak 0.0074→0.0280 evidence. (4) The "Fullvocab repair" column, which adds a fourth number per cell to an already crowded table.

**Recommended scope reductions**: consolidate the three bottleneck-justification passages into one; move DPS to an appendix diagnostic section; demote addition to "weaker instance" status. Each of these removes a place a reviewer can poke without touching the core argument.

## 8) ICLR Formal Scores

- **Soundness: 3/4** — Core causal claims are well-supported with strong controls, but the probe-round upper-bound contradiction, baseline instability across samplings, and the weak fixed-point evidence prevent a 4.
- **Presentation: 3/4** — The writing is clear sentence-by-sentence and the protocol-map effort is commendable, but the paper requires a "how to read the numbers" paragraph to navigate its own results, and the tripled bottleneck justifications signal poor organization. Sufficient detail for reproduction appears present.
- **Contribution: 3/4** — Novel framing and causal localization of a known failure; the constrained/generation dissociation is a real conceptual contribution. Tools are standard; the value is in the synthesis.
- **Significance: 3/4** — A memorable, citable finding ("models know the count but can't say it") with a reusable diagnostic recipe (probe → alignment → targeted repair) that plausibly transfers to other competence-without-performance failures. Impact limited by synthetic-task scope and the fix being task-specific fine-tuning.
- **Overall: 6/10** — Clear accept. Above the poster mean (5.35): crisp mechanism, thorough controls, honest negative results (generation 0.0%, Pythia transfer failure) that strengthen rather than sink the paper. Held back from 7 by the internal inconsistency in the headline table, benchmark sensitivity, and the gap between "fix" rhetoric and what the interventions actually deliver.
- **Confidence: 3/5** — Fairly confident. I could not verify experimental execution, figure contents, or appendix completeness, and my assessment of protocol comparability relies on the paper's own reporting.

## 9) Final Recommendation

**ICLR: Accept (6).** This is a well-executed mechanistic interpretability study with a clean, falsifiable thesis that survives multiple genuine stress tests (14B scaling, negative controls, necessity/sufficiency ablations) — a profile comfortably above the typical accepted poster. The constrained-decoding vs. generation dissociation is a finding others will build on. The acceptance risk comes from self-inflicted wounds: an unreconciled contradiction in the central table, five different baseline numbers for the same task, and "fix" framing that outruns interventions that are either oracle-based or task-specific fine-tunes. All are addressable in revision, and none undermines the core scientific claim.

**Questions for the authors**:
1. Why does 9-row repair exceed the probe-round "upper bound" on character counting (98.0% vs 96.8%)? Same protocol?
2. For LoRA Q/V: what is generation accuracy on held-out *templates and entities*, not just held-out prompts?
3. Can you report a single canonical baseline/headline protocol and commit to it for all main-text claims?