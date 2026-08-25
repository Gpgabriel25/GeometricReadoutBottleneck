# Paper Visual Audit

## Scope
- Pages reviewed: 1–12
- Total pages: 12

## Summary
The paper is on the correct ICLR 2027 template (line numbers, "Under review" header, anonymous author block), main text ends on page 9 with the References beginning on the same page — within the 9-page limit — and an AI Use Statement is present on page 9. No anonymity leaks were detected (the "nostalgebraist" entry is a cited LessWrong post, not an author identity). Tables 1–8 are all well-formed: no clipping, no split cells, consistent booktabs styling. The visual weaknesses are concentrated in the three figures: Figure 1 uses ASCII math inside diagram boxes, Figure 2 has indistinguishable overlapping curves and a mixed-unit axis label, and Figure 3's panels are rendered too small, with tiny legends/tick labels and a reference line that appears missing or clipped. None of these are blocking, but they reduce polish and readability of the core evidence figures.

## Findings

- **Severity**: medium
- **Page**: 2
- **Element**: figure (Figure 1)
- **What is wrong**: In-box text uses raw ASCII notation — `(R^2 ~ 1.0)`, `(|cos| <= 0.032)` — instead of typeset math (R² ≈ 1.0, |cos| ≤ 0.032) as used in the caption and body. The elbow connector arrows from "lm_head misaligned" to the three intervention boxes look like default auto-layout output and visually collide at the source box edge.
- **Why it matters**: This is the paper's summary diagram, referenced from page 1; ASCII math in the figure clashes with the caption's typeset math and reads as a draft artifact.
- **Minimal fix**: Re-render box labels with mathtext/ LaTeX (e.g., `$R^2 \approx 1.0$`, `$|\cos| \le 0.032$`), and route the three arrows from distinct anchor points on the misalignment box.

- **Severity**: medium
- **Page**: 5
- **Element**: figure (Figure 2)
- **What is wrong**: The "Probe R^2 (all)" (blue) and "Probe R^2 (easy)" (purple) curves sit on top of each other at ≈0.99 for nearly the entire x-range and are visually indistinguishable. The y-axis label "Probe R^2 / Accuracy" mixes two quantities (R² and accuracy), and "R^2" is plain text rather than R². The in-plot title duplicates the caption.
- **Why it matters**: Reviewers cannot tell whether the two probe conditions differ; the mixed axis label invites misreading of the 38.8% dashed line as an R² value.
- **Minimal fix**: Use distinct line styles (solid vs. dashed) and/or slight vertical offsets for the two probe series; relabel the axis (e.g., "Probe $R^2$ / next-token accuracy") or use a dual annotation; drop the redundant in-plot title.

- **Severity**: medium
- **Page**: 5
- **Element**: figure (Figure 3)
- **What is wrong**: Both panels are small relative to the column width; tick labels, axis labels, and the 4-entry legend in panel (a) are at the edge of readability at print size. The legend lists a green dotted "Probe R² (~0.99)" reference line, but no green dotted line is discernible in panel (a) — it appears to be clipped at the top axis boundary or omitted. Panel (b)'s log-scale y-axis ticks (10⁻¹–10⁻⁷) are especially cramped.
- **Why it matters**: Figure 3 carries the central logit-lens evidence; a legend entry with no visible corresponding line undermines trust in the plot, and tiny text fails ICLR's readability bar.
- **Minimal fix**: Increase panel size (e.g., full-width figure) and font sizes by ~2 pt; verify the green dotted reference line renders inside the axes (adjust y-limits or clip_on=False) or remove it from the legend.

- **Severity**: low
- **Page**: 4
- **Element**: table (Table 1) / caption-note
- **What is wrong**: The note under Table 1 ("9-row repair = 36,864 params directly rewritten; LoRA Q/V = 7.67M trainable…") is set in a very small font spanning the full text width, noticeably smaller than other table notes.
- **Why it matters**: Contains per-seed numbers needed to interpret the headline result; small dense notes get skipped.
- **Minimal fix**: Match the note font size to the other table notes (cf. Table 4's note on page 6) or fold the per-seed values into a compact second row/appendix pointer.

- **Severity**: low
- **Page**: 5
- **Element**: layout
- **What is wrong**: Figures 2 and 3 are stacked on the same page with Figure 3's two-panel content compressed to fit; the result is that the paper's two key evidence figures compete for one page.
- **Why it matters**: Figure 3's small size (see above) is partly a consequence of this stacking.
- **Minimal fix**: Let Figure 3 float to its own position with more width, or move Figure 2's shaded-region version to the appendix and keep a single-panel version in text.

## High-Value Missing Visuals

- **Page or section**: §5, "Vocabulary competition" (page 6)
- **Proposed visual**: A histogram or ranked plot of `lm_head` row norms across the vocabulary with the 9 digit rows highlighted, showing they fall in the 12th–29th percentile.
- **Why it improves the paper**: The norm-competition claim currently rests on three inline numbers (percentile range, 0.0% argmax wins, 0.33% top-100); a single plot makes the digit-row disadvantage immediately visible and supports the "rescaling alone is insufficient" argument.
- **Evidence it would clarify or support**: The claim that norm rescaling (3× boost) raises fullvocab accuracy only from 0% to ≈26.5%, i.e., that directional misalignment — not just norm — causes the bottleneck.

- **Page or section**: §5, "Subspace geometry" (page 4–5)
- **Proposed visual**: Per-layer |cos| between the layer's count-probe direction and digit rows, optionally overlaid with the random-direction baseline band (0.013 ± 0.011).
- **Why it improves the paper**: The headline statistic |cos| ≤ 0.032 is currently a scalar buried in prose; a per-layer curve would show whether orthogonality is uniform across depth or concentrated in the "projection attempt" layers 20–35, directly supporting the two-phase encoding–projection story.
- **Evidence it would clarify or support**: The Encoding (layers 0–20) vs. Projection attempt (layers 20–35) mechanism described on page 6.

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1-3 visual fixes** before the next reviewer round:
  1. Enlarge Figure 3 and its fonts; restore or remove the missing green dotted "Probe R²" reference line.
  2. Replace ASCII math in Figure 1 boxes with typeset math and clean up the arrow routing.
  3. Differentiate the two overlapping probe curves in Figure 2 (line style) and fix the mixed-unit y-axis label.