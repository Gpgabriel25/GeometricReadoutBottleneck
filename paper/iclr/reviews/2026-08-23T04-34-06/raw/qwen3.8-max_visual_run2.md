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

Stop.