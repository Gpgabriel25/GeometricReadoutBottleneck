# Paper Visual Audit

## Scope
- Pages reviewed: 1–12
- Total pages: 12

## Summary
The paper uses the correct ICLR 2027 template (line numbers, "Under review" header, anonymous author block) and is largely clean: tables are well-formed, captions are informative, and the main text ends on page 9 with the AI Use Statement present before the references — no desk-reject risks found. The visual weaknesses are concentrated in the figures: Figure 1 uses raw ASCII math notation ("R^2", "|cos| <= 0.032") inside diagram boxes, Figure 2's legend box occludes the key dashed reference line, and Figure 3's subplots have fonts and legends that are noticeably smaller than body text and crowd the plotted curves. Tables 1–8 are all readable, uncropped, and correctly broken across pages. No anonymity leaks, acknowledgments, or non-anonymous links are visible.

## Findings

- **Severity**: medium
- **Page**: 5
- **Element**: figure
- **What is wrong**: In Figure 2, the legend box ("Probe R^2 (all) / Probe R^2 (easy) / Next-token digit accuracy (38.8%)") is placed inside the axes at the lower-left and sits directly on top of the red dashed accuracy reference line at y ≈ 0.388, which disappears behind the legend for roughly the left third of the plot.
- **Why it matters**: The dashed line is the "what the model says" anchor of the paper's central gap visualization; partially hiding it undermines the figure's single most important comparison.
- **Minimal fix**: Move the legend outside the axes (e.g., below the plot) or to the upper-left/right corner where the dashed line does not pass, or draw the dashed line on top of the legend.

- **Severity**: medium
- **Page**: 5
- **Element**: figure
- **What is wrong**: Figure 3's two subplots are rendered small: tick labels, axis labels ("Mean P(correct number)"), and the 4-entry legends are roughly half the body-text size, and in panel (a) the legend crowds the upper-left curves.
- **Why it matters**: This is the core mechanistic evidence (logit-lens accuracy by layer); reviewers should not have to zoom to read it. The legend/curve overlap also risks obscuring early-layer behavior.
- **Minimal fix**: Increase the figure to full column width (or a single \linewidth two-panel), raise all font sizes to ~8–9pt equivalent, and place legends outside the plotting area or in clearly empty regions.

- **Severity**: medium
- **Page**: 2
- **Element**: figure
- **What is wrong**: Figure 1's diagram boxes contain raw ASCII math: "R^2 ~ 1.0", "|cos| <= 0.032", while the caption and body text use typeset math ($R^2{\approx}1.0$, $|\cos|{\leq}0.032$). "lm_head" also appears in plain proportional font inside a box.
- **Why it matters**: The mismatch reads as unpolished in the paper's flagship summary figure and is inconsistent with the typography everywhere else.
- **Minimal fix**: Render the box labels with proper math typesetting (e.g., TikZ nodes with $R^2 \approx 1.0$, $|\cos| \le 0.032$, \texttt{lm\_head}).

- **Severity**: low
- **Page**: 5
- **Element**: figure
- **What is wrong**: In Figure 2 the "Probe R² (all)" and "Probe R² (easy)" curves are nearly perfectly overlapping (~0.99 everywhere), so the purple series is visually indistinguishable from the blue one; the y-axis is also truncated at 0.3.
- **Why it matters**: One of the two legend entries is effectively invisible data; the truncated axis is acceptable here but worth a reader cue.
- **Minimal fix**: Either drop the redundant series from the plot (keep it in Table 2), or offset/dash one line; note the truncated axis in the caption.

- **Severity**: low
- **Page**: 5
- **Element**: figure / text consistency
- **What is wrong**: Figure 2's x-axis is "Layer Depth (%)" (0–100) while Figure 3 and Table 2 use absolute layer indices (0–35); Figure 2's caption also cites "Table 3" for unified-evaluation sampling, but the unified evaluation is Table 1.
- **Why it matters**: Readers must mentally convert between % depth and layer index across adjacent figures; the cross-reference appears misdirected.
- **Minimal fix**: Harmonize both figures on absolute layer index (or add a secondary axis), and verify the caption's table reference.

- **Severity**: low
- **Page**: 4
- **Element**: table
- **What is wrong**: Table 1's footnote block is set in very small type spanning the full text width, noticeably below the caption font size used elsewhere.
- **Why it matters**: The footnote carries important protocol details (parameter counts, per-seed values); tiny type discourages reading it.
- **Minimal fix**: Set footnotes at \footnotesize matching the caption, or promote per-seed numbers into a compact appendix table.

## High-Value Missing Visuals

- **Page or section**: §5 (Logit-Lens Analysis), near Figure 3 / Table 3
- **Proposed visual**: A small heatmap or 2D scatter showing cosine similarity between each layer's count-probe direction and the nine `lm_head` digit rows (layers × digit rows), optionally with a random-direction baseline row.
- **Why it improves the paper**: The paper's central quantitative claim — |cos| ≤ 0.032, "indistinguishable from random" — is currently conveyed only as scalar statistics in text. A per-layer, per-digit map would make the *uniformity* of the orthogonality (no single digit row or layer rescues readout) directly visible, which the scalar means cannot show.
- **Evidence it would clarify or support**: The claim in §5 that "per-layer means ≤ 0.032" and the random-baseline equivalence (p = 0.79); it would also directly visualize the "projection attempt" phase (layers 20–35) where alignment partially rises.

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1-3 visual fixes** before the next reviewer round:
  1. Figure 2: relocate the legend so it no longer covers the dashed 38.8% reference line.
  2. Figure 3: enlarge both panels and increase font/legend sizes to match body text; move legends off the curves.
  3. Figure 1: replace ASCII math in diagram boxes with typeset math ($R^2$, $|\cos| \le 0.032$) for consistency with the rest of the paper.

Stop.