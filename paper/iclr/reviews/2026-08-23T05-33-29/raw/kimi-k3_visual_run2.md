# Paper Visual Audit

## Scope
- Pages reviewed: 1–13
- Total pages: 13

## Summary
The paper uses the correct ICLR 2027 review template (line numbers, "Under review" header, anonymous author block). Main text runs pages 1–9 with the AI Use Statement on p. 9 and references starting immediately after — within the 9-page main-text limit. No anonymity leaks (the "nostalgebraist" reference is a legitimate citation, not an author leak). Tables are clean and consistently formatted (booktabs style, readable fonts, proper footnotes). The main visual weaknesses are in the figures: Figure 1 uses ASCII-style math inside diagram boxes, Figure 2 has nearly indistinguishable overlapping curves and non-typeset math in labels/legend, and Figure 3's panels are small with tiny axis labels and legends that will be hard to read in print. Page 13 is mostly blank (acceptable appendix tail). Overall a solid submission needing figure polish.

## Findings

- **Severity**: medium
- **Page**: 2
- **Element**: figure (Figure 1)
- **What is wrong**: Diagram boxes contain raw ASCII math: "R^2 → 1.0", "|cos| <= 0.032". The rest of the paper typesets these properly ($R^2$, $|\cos|$), so the figure looks inconsistent and unpolished. Mixed fonts (sans-serif box labels vs. serif body) is acceptable, but the pseudo-code math is not.
- **Why it matters**: Figure 1 is the paper's summary graphic, referenced from p. 1; reviewers will look at it early. ASCII math signals haste and clashes with the otherwise clean typesetting.
- **Minimal fix**: Regenerate the diagram with LaTeX-rendered labels (e.g., TikZ, or matplotlib with mathtext/LaTeX): "$R^2 \to 1.0$", "$|\cos| \le 0.032$", `\texttt{lm\_head}` for the head name.

- **Severity**: medium
- **Page**: 5
- **Element**: figure (Figure 2)
- **What is wrong**: (a) Axis label "Probe R^2 / Accuracy" and legend entries "Probe R^2 (all)", "Probe R^2 (easy)" use raw "R^2" instead of typeset $R^2$. (b) The "all" (blue) and "easy" (purple) curves sit nearly on top of each other at ≈1.0 and are visually indistinguishable across most of the plot — despite Table 2 showing the easy stratum markedly lower (e.g., 0.664 at layer 0), which the figure does not visually convey.
- **Why it matters**: This is the paper's central "gap" figure; the overlapping curves erase one of the two data series, and the ASCII labels repeat the Figure 1 inconsistency.
- **Minimal fix**: Use mathtext/LaTeX for labels; separate the two series visually (distinct line styles/markers, or plot the easy curve with its own emphasis); double-check that the plotted "easy" curve matches Table 2's values.

- **Severity**: medium
- **Page**: 5
- **Element**: figure (Figure 3)
- **What is wrong**: Both panels are small; axis labels ("Logit-Lens Accuracy", "Mean P(correct number)"), tick labels, and the legends are at the edge of readability, and panel (b)'s log-scale exponents ($10^{-1}$–$10^{-7}$) are very small. Legend text ("Entity-mean position", "Last-token position", "Probe R² (~0.99)") is tiny.
- **Why it matters**: Figure 3 carries the logit-lens evidence for the core claim; reviewers reading a printed or 100%-zoom PDF may not be able to read the axes.
- **Minimal fix**: Increase panel size (e.g., span the full text width with taller subplots) and raise all font sizes to roughly match the body text (~8–9pt minimum at final size).

- **Severity**: low
- **Page**: 4
- **Element**: table (Table 2)
- **What is wrong**: The "Best (layer 3)" row introduces a layer (3) absent from the listed rows (0, 12, 24, 35), which reads as visually abrupt without an in-table note that intermediate layers were swept.
- **Why it matters**: Minor; a reader may momentarily think a row is missing.
- **Minimal fix**: Add a table footnote: "Layer 3 selected over a full sweep; subset of layers shown."

- **Severity**: low
- **Page**: 13
- **Element**: layout
- **What is wrong**: Page 13 contains only the short §A.13 paragraph followed by ~75% whitespace.
- **Why it matters**: Cosmetic only; common at the end of an appendix.
- **Minimal fix**: Optional — pull up or consolidate appendix subsections, or leave as is.

- **Severity**: low
- **Page**: 5
- **Element**: caption (Figure 2)
- **What is wrong**: The caption justifies the 38.6% value by reference to "Table 3", but Table 3 is the logit-lens peak table — the 38.6%/38.8% baseline figures live in §4's prose and Table 1's neighborhood. The cross-reference reads as pointing at the wrong table.
- **Why it matters**: Reviewers cross-checking numbers may be confused about where 38.6% comes from.
- **Minimal fix**: Verify and correct the cross-reference in the caption.

## Format Compliance (ICLR 2027)
- Anonymity: ✔ anonymous block, no author names, no non-anonymous links detected.
- Page limit: ✔ main text (incl. AI Use Statement) ends on p. 9; references begin p. 9 — within the 9-page limit.
- AI Use Statement: ✔ present (p. 9), unnumbered section.
- Template: ✔ ICLR review style with line numbers. **No desk-reject risks identified.**

## High-Value Missing Visuals

- **Page or section**: §5 (Subspace geometry, p. 5)
- **Proposed visual**: A heatmap of $|\cos|$ between per-layer count-probe directions and the 9 digit-row directions of `lm_head` (layers × digits), with the random-direction baseline marked.
- **Why it improves the paper**: The paper's headline quantitative claim — orthogonality ($|\cos| \le 0.032$ across layers, probe types, and model families) — is currently delivered only in prose and scalar summaries.
- **Evidence it would clarify or support**: The reported mean $|\cos| = 0.016$, per-layer max 0.032, CI [0.015, 0.016], and the 0.013 random baseline; a heatmap would show the uniformity of the effect at a glance rather than requiring readers to trust aggregated statistics.

- **Page or section**: §A.7, Table 8 (p. 12)
- **Proposed visual**: A line plot of probe-round vs. 9-row repair accuracy as a function of count value (1–9).
- **Why it improves the paper**: The count-magnitude dependence of the repair ceiling is a key limitation result (100% → 30.6% swing), but the trend is buried in a 9-row table in the appendix.
- **Evidence it would clarify or support**: Table 8's monotone degradation of 9-row repair accuracy for counts ≥ 4, which motivates the "logit-gap ceiling model" and the vocabulary-competition explanation in §6.

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1-3 visual fixes** before the next reviewer round:
  1. Replace ASCII math ("R^2", "|cos| <=", "~") with proper typeset math in Figures 1 and 2 (and check all figure text).
  2. Enlarge Figure 3 panels and increase all axis/legend font sizes to near body-text size.
  3. Fix Figure 2's overlapping "all"/"easy" curves (distinct styles; verify values match Table 2) and correct the Figure 2 caption's Table 3 cross-reference.