# CUMCM Figure Standards

Use this as the default figure standard for mathematical modeling contest papers. The goal is not journal-style decoration; the goal is that judges can quickly see what each figure proves.

For SCI/Nature/PRL-style publication graphics, read `references/figure-standards-journal.md` only when the user explicitly asks for journal-grade figures.

## Core Rules

- Every figure must support one subquestion conclusion.
- Every figure must be reproducible from code or a saved source table.
- Figure numbers, captions, and filenames must match the paper text.
- Axis labels must include units when variables have units.
- The figure must be readable at normal paper size.
- Do not use a figure when a compact table answers the question more clearly.

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
| Technical route | editable Mermaid/Graphviz/SVG flowchart |

## Avoid

- 3D pie charts, decorative shadows, heavy gradients, and crowded color palettes.
- Figures that show process but do not support a result.
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
4. the source table or script when useful;
5. validation meaning when the figure is a check.

Example:

`图 3 展示问题二不同容量约束下的总成本变化。结果表明，当容量提高到 260 件后，目标函数下降幅度明显变小，说明当前方案对小幅容量扰动较稳定。`

## Readability Check

Before final handoff:

- labels are not clipped;
- legend does not cover data;
- long category names are horizontal or wrapped;
- units and sample ranges are visible;
- figure text is close to body-text size after insertion;
- paper statements do not overclaim beyond what the figure shows.
