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