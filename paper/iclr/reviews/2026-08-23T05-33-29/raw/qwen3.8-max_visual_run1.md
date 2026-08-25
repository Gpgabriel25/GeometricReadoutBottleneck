# Paper Visual Audit

## Scope
- Pages reviewed: 1–13
- Total pages: 13

## Summary
Typesetting is largely clean and template-compliant: anonymity header intact, AI Use Statement present (p. 9), main text ends within page 9 before references, and Tables 1–8 render with consistent rules and readable footnotes. Visual weakness is concentrated in the figures: Figure 1 is a draft-quality flowchart (ASCII math, "Im head" label) separated from its caption by a large blank band; Figures 2–3 use caret notation ("R^2") in titles/axis labels, and Figure 3's legend/tick text is at the edge of legibility. Page 13 ends with a mostly blank page still carrying line numbers 659–701. No desk-reject risks detected.

## Findings

- **Severity**: medium
- **Page**: 2
- **Element**: figure
- **What is wrong**: In the Figure 1 float, the diagram ends high on the page and the caption begins near line 075, leaving a blank band roughly a third of the float's height between graphic and caption.
- **Why it matters**: The reader must bridge a large empty region to connect the caption to the diagram; the page reads as unfinished.
- **Minimal fix**: Crop the figure's bounding box (or reduce the float height) so the caption sits directly beneath the diagram.

- **Severity**: medium
- **Page**: 2
- **Element**: figure
- **What is wrong**: Figure 1 uses raw ASCII math and ad-hoc labels: "(R^2 ~ 1.0)", "(|cos| <= 0.032)", and "Im head misaligned" (reads as "I'm head"; the body consistently uses `lm_head`).
- **Why it matters**: This schematic is the paper's only visual summary of the mechanism, but it looks like a draft and its notation is inconsistent with the properly typeset math in the body.
- **Minimal fix**: Redraw with typeset math (R²≈1.0, |cos|≤0.032) and relabel the red box "`lm_head` misaligned" in monospace to match the text.

- **Severity**: medium
- **Page**: 5
- **Element**: figure
- **What is wrong**: Figures 2–3 use caret notation in titles/axis labels ("Probe R^2 / Accuracy", "Probe R^2 (all/easy)"), and Figure 3's legend entries, tick labels, and axis labels render extremely small with thin line weights.
- **Why it matters**: At normal PDF zoom, Figure 3's legends and ticks are barely legible, and ASCII carets clash with the typeset R² used in the captions and body.
- **Minimal fix**: Regenerate plots with true superscripts (R²), ≥8 pt axis/legend fonts, and heavier line weights; relocate or shrink Figure 3(a)'s legend so it never crowds the curves.

- **Severity**: low
- **Page**: 5
- **Element**: caption
- **What is wrong**: Figure 2's caption attributes the 38.6% unified-evaluation figure to "Table 3", but Table 3 is the logit-lens peak table; the unified evaluation is Table 1.
- **Why it matters**: A reader cross-checking the number lands in an unrelated table, undermining confidence in the caption's protocol description.
- **Minimal fix**: Verify and correct the table pointer (likely Table 1, or state the protocol explicitly without a table reference).

- **Severity**: low
- **Page**: 13
- **Element**: layout
- **What is wrong**: After the appendix ends (line 658), the remainder of the page is blank yet the line-number gutter continues to 701, producing a page of orphaned numbers next to empty space.
- **Why it matters**: Sloppy final-page artifact that cheapens an otherwise tidy submission.
- **Minimal fix**: Suppress line numbering for trailing empty lines / end the document after line 658.

## High-Value Missing Visuals

- **Page or section**: §5, "Subspace geometry" paragraph (lines 265–269), adjacent to Figures 2–3.
- **Proposed visual**: A small per-layer line plot of |cos| between the count-probe direction and the `lm_head` digit rows, with bootstrap CI band and a random-direction baseline curve.
- **Why it improves the paper**: The orthogonality claim is the paper's core evidence but currently exists only as scalar summaries in prose; a per-layer curve would show the misalignment is stable across depth and would visually parallel the probe/logit-lens curves in Figures 2–3.
- **Evidence it would clarify or support**: mean |cos| = 0.016 (CI [0.015, 0.016]) vs. random 0.013 ± 0.011, per-layer means ≤ 0.032, and the sharpening to 0.011 at 14B scale.

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1-3 visual fixes** before the next reviewer round:
  1. Rebuild Figure 1: typeset math (R², |cos| ≤), correct `lm_head` label, and remove the blank band so the caption abuts the diagram.
  2. Upgrade Figures 2–3 typography: real superscripts, larger legend/tick fonts, heavier lines.
  3. Correct the Figure 2 caption's table cross-reference and eliminate the page-13 line-number artifact.

Stop.