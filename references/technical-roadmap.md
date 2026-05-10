# Technical Roadmap And Model Flowcharts

Use this reference for 技术路线图, 技术路线, 流程图, 流程框图, or 模型流程图.

## Priority

For contest-final or paper-final diagrams, use GPT-image by default when a
polished bitmap figure is needed. When the diagram must be edited repeatedly,
create an editable Mermaid (`.mmd`), Graphviz DOT (`.dot`), or SVG source first,
then export it to SVG/PDF/PNG.

Save:

- `modeling/qx_model_flow_prompt.md` or `modeling/flowcharts/qx_model_flow_prompt.md`:
  the Chinese diagram brief, node list, arrow logic, caption, and paper
  explanation.
- editable `.mmd`, `.dot`, or `.svg` source beside the exported image when an
  editable workflow is used.
- `figures/fig_qx_model_flow.png`: the final model flowchart used in the paper.
- `figures/fig_route_overview.png`: the technical roadmap for the full paper or
  multi-question route.

## Technical Roadmap Structure

Default logic:

`题目任务 -> 数据与指标 -> 建模思路 -> 核心模型 -> 模型求解 -> 验证分析 -> 结论输出`

Rules:

- Base the diagram on the provided problem, paper, or selected route.
- Do not add methods, data, metrics, or validation steps that are not in the solution.
- Keep labels short and high-level; put details in the caption or paper paragraph.
- Prefer 8-12 nodes for one subquestion and grouped lanes for multi-question papers.
- Avoid code-level steps unless they are central to the modeling logic.
- Every solved subquestion should normally have a final model flowchart. If a
  pure symbolic derivation or compact table is clearer than a flowchart, record
  that reason in `modeling/qx_modeling_idea.md` and `paper/main.tex`.

## Model Flowchart Structure

Default logic:

`输入数据 -> 数据预处理 -> 变量构造 -> 模型假设 -> 模型方程/目标函数 -> 参数估计/算法求解 -> 结果输出 -> 验证与敏感性分析 -> 结论解释`

Task-specific additions:

- Optimization: objective, constraints, solver, feasibility check, baseline comparison, sensitivity.
- Prediction: train/validation split or rolling validation, baseline, error metrics, residual check.
- Evaluation: indicator direction, normalization, weighting, score/ranking, ranking stability.
- Simulation: state variables, transition rules, parameter estimation, repeated runs, boundary cases.

## Style

- Use a light background, high-contrast text, restrained colors, rectangular nodes, clear arrows, and no decorative icons.
- Size node text for the final paper canvas; labels should remain near body-text size after insertion.
- If labels overlap, remove nodes or shorten labels before shrinking text.
- Output a Chinese caption and one paper explanation paragraph with every diagram.

## GPT-Image Brief Requirements

Write the prompt before generating the image. Include:

- paper context and subquestion id;
- diagram title in Chinese;
- exact node labels;
- arrow order and any grouped lanes;
- required visual style: clean white background, rectangular nodes, high-contrast
  Chinese text, no decorative icons, no extra methods;
- caption and the one paragraph that will be written into `paper/main.tex`.

After generation, inspect the image. If labels, arrows, or node order are wrong,
regenerate rather than silently using the flawed image.

## Mermaid Starter

```mermaid
flowchart LR
  A["题目任务"] --> B["数据与指标"]
  B --> C["建模思路"]
  C --> D["核心模型"]
  D --> E["模型求解"]
  E --> F["验证分析"]
  F --> G["结论输出"]
```
