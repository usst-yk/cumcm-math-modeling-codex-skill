# CUMCM Figure Standards

Use this as the default figure standard for mathematical modeling contest papers. The goal is not journal-style decoration; the goal is that judges can quickly see what each figure proves.

For SCI/Nature/PRL-style publication graphics, read `references/figure-standards-journal.md` only when the user explicitly asks for journal-grade figures.

## Core Rules

- Every figure must support one subquestion conclusion.
- Result, validation, and sensitivity figures must be reproducible from code or
  a saved source table. GPT-image flowcharts and technical roadmaps must keep
  their prompt/spec and pass visual text/order checks.
- Figure numbers, captions, and filenames must match the paper text.
- Use the bundled Chinese font by default: `assets/fonts/NotoSansCJKsc-Regular.otf`
  for normal Chinese text and `assets/fonts/NotoSansCJKsc-Bold.otf` for titles.
  Do not rely on macOS/Windows platform Chinese fonts as the primary choice.
- English letters, numbers, and math labels should prefer Times New Roman style;
  if Times New Roman is unavailable, fall back to Times, Nimbus Roman,
  Liberation Serif, or DejaVu Serif.
- For each solved subquestion, make a figure plan before coding or writing.
- Default to at least two figures for most solved subquestions: a final model
  flowchart and a result figure. Add validation/sensitivity figures when the
  result needs checking.
- The GPT-image prompt/spec belongs in `modeling/` or `modeling/flowcharts/`;
  the generated paper figure belongs in `figures/`.
- Additional schematic figures are expected when geometry, trajectories, timing,
  optimization variables, evaluation indicators, spatial layouts, or constraint
  relationships cannot be explained clearly by the model flowchart alone.
- For Chinese contest papers, figure titles, axis labels, legends, annotations,
  and captions should be in Chinese by default. Use English only for variables,
  file names, algorithm names, or standard units.
- Axis labels must include units when variables have units.
- The figure must be readable at normal paper size.
- Source-figure font sizes should usually be larger than body text because
  figures are scaled down in the paper. After insertion, axis labels and legends
  should be close to body-text size, tick labels should remain clearly readable,
  and the figure title may be slightly larger than body text.
- Do not use a figure only when a compact table answers the question more
  clearly; record that reason.

## Recommended Figure Types

| Purpose | Recommended figure |
| --- | --- |
| Trend or forecast | line chart with baseline or prediction interval |
| Ranking or comparison | sorted horizontal bar chart |
| Optimization result | objective breakdown, plan table, route/dispatch chart, feasibility table |
| Prediction error | actual-vs-predicted plot, residual plot, error metric table |
| Evaluation/ranking | score table, weight bar chart, ranking stability chart |
| Sensitivity analysis | parameter-result line chart, heatmap, tornado chart |
| Spatial analysis | map/scatter/grid with coordinate or distance explanation |
| Clustering/classification | cluster scatter, confusion matrix, representative samples |
| Mechanism or geometry | problem background schematic, coordinate diagram, trajectory diagram |
| Timing or staged process | timeline, Gantt-style stage chart, event sequence diagram |
| Technical route | GPT-image technical roadmap |

## Avoid

- 3D pie charts, decorative shadows, heavy gradients, and crowded color palettes.
- Figures that show process but do not support a result.
- English-only plot labels in a Chinese modeling paper when Chinese labels are
  possible.
- Platform-dependent Chinese fonts as the only font setting.
- Tiny labels inserted into a paper page.
- Unchecked AI-generated flowchart text.
- Manual image edits that change values without updating source data.

## File Naming

Use stable lowercase names:

- `fig_q1_demand_trend.png`
- `fig_q2_route_plan.png`
- `fig_q3_ranking_stability.png`
- `tab_q1_metrics.csv`
- `tab_q2_feasibility.xlsx`

## Caption Pattern

Each caption should state:

1. what the figure shows;
2. which subquestion it supports;
3. the key trend/result;
4. the source table/script for result figures, or the prompt/spec file for
   GPT-image flowcharts;
5. validation meaning when the figure is a check.

Example:

`图 3 展示问题二不同容量约束下的总成本变化。结果表明，当容量提高到 260 件后，目标函数下降幅度明显变小，说明当前方案对小幅容量扰动较稳定。`

## Readability Check

Before final handoff:

- Chinese text uses the bundled Noto Sans CJK SC font or an explicitly recorded
  fallback;
- labels are not clipped;
- legend does not cover data;
- long category names are horizontal or wrapped;
- units and sample ranges are visible;
- figure text is close to body-text size after insertion, not visibly smaller
  than the surrounding paragraph;
- paper statements do not overclaim beyond what the figure shows.
