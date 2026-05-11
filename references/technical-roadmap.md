# Technical Roadmap And Model Flowcharts

Use this reference for 技术路线图, 技术路线, 流程图, 流程框图, or 模型流程图.

## Priority

Use GPT-image by default for contest-final and paper-final technical roadmaps
and model flowcharts.

Save:

- `modeling/qx_model_flow_prompt.md` or
  `modeling/flowcharts/qx_model_flow_prompt.md`: the Chinese diagram brief,
  node list, arrow logic, caption, and paper explanation.
- `figures/fig_qx_model_flow.png`: the final model flowchart used in the paper.
- `figures/fig_route_overview.png`: the technical roadmap for the full paper or
  multi-question route.

Do not use diagram generation as a shortcut around modeling. The prompt must be
derived from the final modeling idea, code behavior, result tables, and
validation plan.

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

## Paper Integration

For every accepted roadmap or flowchart:

- save the final image under `figures/`;
- save the prompt, node list, arrow logic, and caption under `modeling/`;
- reference the figure from `paper/main.tex`;
- explain what modeling decision, data path, or validation logic the figure
  supports.
