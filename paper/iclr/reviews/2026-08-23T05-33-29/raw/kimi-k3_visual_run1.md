# Paper Visual Audit

## Scope
- Pages reviewed: 1–13
- Total pages: 13

## Summary
The submission is generally clean and recognizably ICLR-style: correct header, line numbers, anonymous author block, readable body text, and an explicit AI Use Statement before references. I do not see a desk-reject-level anonymity violation. The main visual weaknesses are concentrated in the results pages: several key figures/tables are dense, use very small legends/footnotes, or mix metrics on shared axes in ways that make the central “knows vs. says” claim harder to parse than it should be. Page 13 is mostly blank but harmless. Overall: solid draft, needs targeted polish on Figures 2–3 and Tables 1/4/5 rather than a redesign.

## Findings

- **Severity**: low  
  **Page**: 9  
  **Element**: layout / compliance  
  **What is wrong**: Main text, Conclusion, AI Use Statement, and the start of References all share page 9.  
  **Why it matters**: This is not automatically a violation, but it makes the page-limit boundary visually ambiguous: a reviewer/checker may wonder whether main text ends “within 9 pages” or references are beginning too early.  
  **Minimal fix**: If possible, force References to start at the top of page 10, or add a clear page break so the ≤9-page main-text boundary is unambiguous.

- **Severity**: medium  
  **Page**: 4  
  **Element**: table footnote / caption  
  **What is wrong**: Table 1’s footnote line under the table is very small and compressed, while the caption above is long; the fine print contains important protocol details and per-seed values.  
  **Why it matters**: The footnote disambiguates headline numbers that recur throughout the paper; if unreadable, reviewers may misread 60.7%, 83.1%, etc. as inconsistent.  
  **Minimal fix**: Move the longest protocol note into the caption or text, increase footnote font one step, and split the dense per-seed list into a separate short sentence.

- **Severity**: medium  
  **Page**: 5  
  **Element**: Figure 2 axis / legend  
  **What is wrong**: The y-axis label reads “Probe R^2 / Accuracy,” mixing two different quantities; the red dashed next-token accuracy line and probe R² curves share one axis without enough visual separation. The legend also sits inside the plotting region and competes with the curves.  
  **Why it matters**: This is the paper’s central gap figure; conflating R² and accuracy on one labeled axis can make the “representation–output gap” look like a plotting error rather than a finding.  
  **Minimal fix**: Use a clearer y label such as “Probe R² and digit accuracy,” annotate the dashed line directly at y≈0.388, move the legend outside or to a less crowded corner, and consider a light right-side annotation for “output accuracy.”

- **Severity**: medium  
  **Page**: 5  
  **Element**: Figure 3 subplots / log-scale labels  
  **What is wrong**: Figure 3(a)–(b) are small; tick labels, legends, and the log-scale exponents in panel (b) are hard to read at rendered size. The green dotted probe reference in (a) is visually faint near the top, and the sharp final-layer red excursion in (b) is visually prominent but not marked.  
  **Why it matters**: The logit-lens evidence is mechanistically important, but tiny labels reduce trust in exact values such as 0.234/0.416 and the rank/probability changes.  
  **Minimal fix**: Increase figure width/font sizes, use direct line labels instead of a boxed legend where possible, and add a small annotation for the final-layer spike/drop in panel (b) if it is meaningful.

- **Severity**: low  
  **Page**: 5  
  **Element**: float ordering / cross-reference  
  **What is wrong**: Text says “The results are striking (Figure 3, Table 3):” on page 5, but Table 3 appears at the top of page 6.  
  **Why it matters**: Minor reading friction; the reader must flip forward for the table supporting the immediately following paragraph.  
  **Minimal fix**: If layout permits, place Table 3 on the same page as the paragraph or soften the reference to “Figure 3 and Table 3” without implying same-page locality.

- **Severity**: low  
  **Page**: 6  
  **Element**: Table 3 / local density  
  **What is wrong**: Table 3 is readable but visually plain and slightly disconnected from the surrounding mechanism discussion; em-dashes for probe R² at last-token/final-output rows may be mistaken for missing values rather than “not applicable.”  
  **Why it matters**: The contrast between probe R² and peak logit-lens accuracy is a key quantitative bridge; ambiguity around dashes weakens it.  
  **Minimal fix**: Replace em-dashes with “n/a” and add a one-line note explaining why probe R² is not reported at output-read positions.

- **Severity**: medium  
  **Page**: 7  
  **Element**: Tables 4–5 density and footnotes  
  **What is wrong**: Tables 4 and 5 are information-dense with tiny dagger/star footnotes; Table 5’s multi-row Qwen3-8B block, parameter counts, training steps, and accuracy values are readable but visually crowded.  
  **Why it matters**: These are primary evidence tables; reviewers should not have to hunt for whether a number is multi-seed, held-out, full-vocab, or generation-mode.  
  **Minimal fix**: Slightly increase row height/footnote size, bold the protocol-defining column headers, and move dagger/star definitions into the caption in plain language.

- **Severity**: low  
  **Page**: 7  
  **Element**: text emphasis / numerical scanning  
  **What is wrong**: Long result paragraphs contain many inline percentages and transformations, e.g., rank drops “55,980 → 1,” “16.2% to 67.4%,” “24.7% to 98.9%,” all in prose.  
  **Why it matters**: The LoRA Q/V mechanism evidence is strong but hard to scan; important before/after pairs are buried.  
  **Minimal fix**: Convert the three LoRA Q/V before/after measurements into a compact 3-row mini-table or aligned inline list.

- **Severity**: low  
  **Page**: 10–12  
  **Element**: appendix tables / consistency  
  **What is wrong**: Appendix Tables 6–8 are clean, but Table 8’s count-stratified collapse of 9-row repair is only visible numerically; the non-monotonic drop is not visually immediate.  
  **Why it matters**: The count-magnitude dependence is a useful diagnostic and would be clearer as a small plotted curve.  
  **Minimal fix**: Keep Table 8, but add a tiny companion plot in A.7 if space allows.

- **Severity**: low  
  **Page**: 13  
  **Element**: layout / blank space  
  **What is wrong**: Page 13 contains only a short A.13 paragraph and is otherwise blank.  
  **Why it matters**: Mostly cosmetic; suggests an avoidable float/page-break artifact at the end of the appendix.  
  **Minimal fix**: Not required. If desired, pull A.13 upward or allow the appendix to end on page 12.

- **Severity**: none observed  
  **Page**: 1–13  
  **Element**: anonymity / required statement  
  **What is wrong**: No visible author names, acknowledgments, or non-anonymous repository usernames. AI Use Statement is present as an unnumbered section near the end of main text.  
  **Why it matters**: Avoids ICLR desk-reject risks.  
  **Minimal fix**: No action beyond preserving anonymity in any added links/supplement.

## High-Value Missing Visuals

- **Page or section**: Section 5, after Figure 3 / “Subspace geometry” paragraph  
  **Proposed visual**: A small 2D schematic showing the count-probe direction, the `lm_head` digit-row subspace, and the near-90° angle, with a second mini-panel showing the post-LoRA Q/V rotated/readout-aligned state.  
  **Why it improves the paper**: The paper’s core claim is geometric; a schematic would make “orthogonal but linearly present” intuitive before readers encounter tables of cosines.  
  **Evidence it would clarify or support**: Reported values `|cos| ≤ 0.032`, random baseline `0.013 ± 0.011`, and the claim that repair realigns readout rather than creating the count representation.

- **Page or section**: Appendix A.7 / Table 8  
  **Proposed visual**: A compact line plot of probe-round vs. 9-row repair accuracy across count values 1–9.  
  **Why it improves the paper**: Table 8 hides a striking pattern: 9-row repair is near-perfect for count 2 but collapses at counts 4–7. A plot would make the magnitude-dependent ceiling obvious.  
  **Evidence it would clarify or support**: Table 8 values: probe-round remains 96.8–100.0%, while 9-row repair drops to 51.3%, 39.7%, 37.0%, 30.6% for counts 4–7 before recovering at 9.

- **Page or section**: Section 6 / Mechanism of LoRA Q/V  
  **Proposed visual**: A three-point before/after bar or arrow diagram for LoRA Q/V: count-encoding layer unchanged, final-layer probe R² amplified, logit-lens accuracy/rank improved.  
  **Why it improves the paper**: The mechanism paragraph is strong but prose-heavy; a visual would make the routing-specificity claim easier to verify at a glance.  
  **Evidence it would clarify or support**: Layer-2 `|cos|` 0.0089→0.0070, final-layer ridge-probe R² 0.974→0.998, logit-lens accuracy 9.3%→71.8%, correct-digit median rank 55,980→1.

## Overall Visual Verdict
- **Status**: Needs Polish
- **Top 1–3 visual fixes** before the next reviewer round:
  1. Rework Figure 2 so probe R² and output accuracy are clearly distinguished and the dashed accuracy line is directly annotated.
  2. Enlarge Figure 3 fonts/legends and annotate the final-layer excursion in the log-scale panel.
  3. De-densify Tables 1/4/5 footnotes and make protocol labels obvious in captions so headline numbers are not misread.