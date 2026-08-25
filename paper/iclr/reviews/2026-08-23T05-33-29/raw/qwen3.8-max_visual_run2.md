# Paper Visual Audit

## Scope
- Pages reviewed: 1–13
- Total pages: 13

## Summary
Overall the paper renders cleanly: tables are well-formed, math glyphs are intact, anonymity is preserved, the AI-use statement is present, and main text ends on page 9 before references (format-compliant). The weak points are the figures: Figure 1 is a draft-quality schematic with ASCII math and a large dead gap before its caption; Figure 3's axis/legend typography is far below readable size; Figure 2's legend sits inside the shaded region. The final appendix page is mostly empty. No desk-reject triggers observed.

## Findings

- **Severity**: high
- **Page**: 5
- **Element**: figure (Figure 3)
- **What is wrong**: Subfigure titles, axis labels ("Logit-Lens Accuracy", "Mean P(correct number)", "Layer"), tick labels, and both legends render at an extremely small size (well below caption size, likely <6 pt). The legend entries in panel (a) are cramped and barely legible even on screen.
- **Why it matters**: Figure 3 carries the mechanistic core of the paper (probe R² vs. logit-lens accuracy, per-layer P(correct)); reviewers reading a printed or zoomed-out PDF cannot verify axis scales or legend identities, undermining the key evidence.
- **Minimal fix**: Regenerate at readable font sizes (≥8 pt for ticks/labels, ≥9 pt legends), e.g., stack the two panels vertically at full text width, or move legends outside the axes; enlarge panel titles "(a)/(b)".

- **Severity**: medium
- **Page**: 2
- **Element**: figure (Figure 1)
- **What is wrong**: The schematic uses ASCII/monospace math inside boxes ("R^2 ~ 1.0", "|cos| <= 0.032") instead of typeset math (R²≈1.0, |cos|≤0.032), mixes a bold sans-serif "Interventions" header with the body style, and uses thin gray connector lines that are hard to follow. The diagram looks like a draft relative to ICLR production quality.
- **Why it matters**: This is the paper's overview diagram; crude typography and weak visual hierarchy reduce first-impression clarity and venue fit.
- **Minimal fix**: Redraw with proper math typesetting in node labels, consistent font family/sizes, darker arrow strokes with arrowheads labeled (e.g., "bypasses"), and aligned box widths.

- **Severity**: medium
- **Page**: 2
- **Element**: layout / caption (Figure 1)
- **What is wrong**: Roughly six blank line-numbers (069–074) separate the figure graphic from its caption, creating a conspicuous empty band mid-page and making the caption appear detached from the graphic.
- **Why it matters**: The gap wastes vertical space on a text-heavy page and visually disconnects caption from figure, hurting comprehension flow.
- **Minimal fix**: Reduce the figure float's reserved height (or set the caption immediately below the graphic) so the caption abuts the diagram; reclaim the space for the Motivation text.

- **Severity**: low
- **Page**: 5
- **Element**: figure (Figure 2)
- **What is wrong**: The legend box is placed inside the axes over the shaded "gap" region, and the y-axis lower bound (0.3) leaves dead space below the 0.388 dashed baseline; the legend partially competes with the shaded fill it is meant to explain.
- **Why it matters**: Minor occlusion and clutter in an otherwise clear plot; the shaded region's meaning ("the gap") is easier to read when unobstructed.
- **Minimal fix**: Move the legend outside the plot (e.g., below the x-axis label) or to the empty upper-right margin; consider y-limits 0.3–1.05 with the legend in a figure-level strip.

- **Severity**: low
- **Page**: 13
- **Element**: layout
- **What is wrong**: After Appendix A.13 ends (~line 658), the remaining ~40 numbered lines of the page are empty.
- **Why it matters**: A half-empty final page is harmless scientifically but looks unpolished and wastes space that could absorb overflow from earlier dense pages.
- **Minimal fix**: Let appendix floats (e.g., Table 8) reflow downward, or add a short supplementary paragraph/figure to fill the page.

## High-Value Missing Visuals

- **Page or section**: Page 5, "Subspace geometry" paragraph (Section 5)
- **Proposed visual**: A compact per-layer plot of |cos| between the count-probe direction and the nearest digit-row direction of `lm_head`, with bootstrap CI bands, shown for all three model families (Qwen3-8B, Mistral-7B, Pythia-410M), plus a random-direction baseline band.
- **Why it improves the paper**: The orthogonality claim (|cos| ≤ 0.032, "indistinguishable from random") is currently text-only with CIs; a small plot would let readers see layer-wise stability and cross-family replication at a glance, mirroring the style of Figure 2.
- **Evidence it would clarify or support**: Directly visualizes the headline statistic (|cos| ≤ 0.032 vs. 0.577×-sharpened random baseline at 14B) and the claim that misalignment is a stable property across families and layers.

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1-3 visual fixes** before the next reviewer round:
  1. Re-typeset Figure 3 at readable font sizes (largest impact; currently near-unreadable axes/legends).
  2. Upgrade Figure 1 to publication quality (typeset math, consistent typography, clearer arrows) and close the dead gap between the graphic and its caption on page 2.
  3. Clean up Figure 2 legend placement; optionally fill the half-empty page 13.

Stop.