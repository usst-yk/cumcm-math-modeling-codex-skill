---
name: cumcm-math-modeling
description: Chinese CUMCM mathematical modeling workflow for first-prize-level problem decomposition, 3-route comparison, analytical derivation, optimization/simulation, Python/MATLAB implementation planning, validation, technical roadmap diagrams, model flowcharts, visualization, and paper writing. Use when the user mentions 全国大学生数学建模竞赛, CUMCM, 数学建模, 建模论文, 赛题分析, 模型建立, 模型求解, 技术路线图, 流程框图, 模型流程图, 灵敏度分析, 摘要, 一等奖标准, or asks to turn a contest problem/data into a deep modeling solution and report.
---

# CUMCM Math Modeling

Use this skill to behave like a CUMCM modeling coach and paper coauthor. Default to a first-prize-level deliverable: deep problem decomposition, three-route comparison, mechanism/analytical reasoning before numerical computation, reproducible algorithms, strong validation, answer-driven figures, and a paper narrative judges can follow quickly.

## First-Prize Default Standard

Unless the user explicitly asks for a quick or shallow answer, every full solution must be rebuilt to this standard:

1. Start with 3 modeling routes and compare them.
   - Route A: simple baseline or interpretable analytical route.
   - Route B: main contest route with stronger mechanism, optimization, prediction, simulation, network, or evaluation structure.
   - Route C: robustness/fallback route or a higher-complexity extension.
   - Compare by fit to each subquestion, data demand, interpretability, implementation risk, validation path, and paper expressiveness.
   - Select one primary route and one fallback; state what each route contributes and why rejected routes are insufficient.

2. For every subquestion, include all required blocks.
   - Problem restatement: input, decision/model object, output, and validation criterion.
   - Variables and parameters: decision variables, state variables, exogenous parameters, units, and notation table entries.
   - Objective function or evaluation criterion: what is optimized, fitted, predicted, classified, ranked, or explained.
   - Constraints: physical, logical, statistical, resource, boundary, data-quality, and contest-statement constraints.
   - Analytical derivation: simplified model, monotonicity, bounds, equilibrium, dimensional analysis, convexity/KKT, or limiting cases; if no derivation is feasible, explain why and give a sanity-check baseline.
   - Algorithm steps: reproducible procedure, input/output, initialization, parameter estimation, convergence or stopping rule, and complexity when relevant.
   - Validation plan: baseline comparison, residual/error/feasibility checks, sensitivity analysis, boundary cases, and robustness to missing or perturbed data.
   - Visualization design: figures/tables with filename, axes/units, supported subquestion, expected conclusion, and paper-ready caption plan.
   - Paper paragraph: concise contest-style Chinese text that can be pasted into the model establishment, solution, or result analysis section.

3. Add a depth audit before finalizing.
   - Identify which subquestions are still too descriptive, too algorithmic, or weakly validated.
   - Check whether every important conclusion is traceable to data, code output, equations, or stated assumptions.
   - Check whether the solution contains at least one interpretable baseline and one robustness/sensitivity comparison.
   - Remove decorative methods that do not improve a specific answer.

## Core Workflow

1. Identify the problem type and scoring surface.
   - Extract all tasks, deliverables, constraints, data files, and implicit evaluation criteria.
   - Rewrite each question into "input -> decision/model -> output -> validation".
   - Flag missing data, ambiguous terms, and assumptions that must be stated.
   - For detailed route selection, load `references/problem-routing.md`.

2. Build a route before equations.
   - Give exactly 3 candidate modeling routes for full solutions, then select one primary route and one fallback.
   - Include a comparison table covering fit, assumptions, data demand, interpretability, implementation risk, validation, and paper impact.
   - Prefer a route that can be implemented and validated within contest time.
   - Avoid overly decorative models that do not improve the answer to a specific subquestion.

3. Try analytical reasoning before numerical computation.
   - First seek simplified equations, closed-form relationships, monotonicity, bounds, equilibrium conditions, dimensional analysis, or convexity/KKT conditions.
   - Use the analytical result as a baseline, explanation, or sanity check even when the final model needs numerical optimization or simulation.
   - Compare analytical and numerical results: identify agreement, deviation, applicable range, and what the numerical model adds.

4. Define assumptions and notation early.
   - Keep assumptions minimal, checkable, and tied to model feasibility.
   - Define symbols in a table before using dense equations.
   - Separate data preprocessing assumptions from mechanism/model assumptions.

5. Design the model and solution method.
   - For each subquestion, specify problem restatement, variables, objective, constraints, analytical derivation, algorithm steps, validation plan, visualization design, and paper paragraph.
   - Use mature methods where possible: regression, optimization, graph/network models, time series, classification/clustering, simulation, grey prediction, TOPSIS/AHP/entropy weighting, queueing, cellular automata, or differential equations.
   - State why the chosen method fits the data scale and question form.

6. Verify with data and stress tests.
   - Include units, dimensions, residual checks, error metrics, feasibility checks, and boundary cases.
   - Do sensitivity analysis on parameters that influence conclusions, not every parameter.
   - Compare at least one baseline or alternative model when feasible.
   - Apply the minimum validation set by task type:
     - Prediction/fitting: baseline comparison, train/test or rolling validation when data permits, residual analysis, and MAE/RMSE/MAPE/R2 as appropriate.
     - Optimization/scheduling: feasibility check, constraint violation table, objective value, baseline scheme comparison, and sensitivity to key parameters.
     - Evaluation/ranking: indicator direction check, normalization check, weight perturbation, ranking stability, and at least one alternative weighting or scoring comparison when feasible.
     - Simulation/propagation: boundary cases, parameter sensitivity, repeated runs for stochastic models, and interpretation of peak/final-state behavior.
     - Classification/clustering: confusion matrix or cluster validity indicators, feature contribution or cluster interpretation, and error case analysis.
   - If a validation item cannot be performed because data are missing, state why and provide the planned validation formula or table template.

7. Write for judges.
   - Start from conclusions and evidence, not method inventory.
   - Put the strongest result in the abstract and conclusion.
   - Use compact figures/tables that answer subquestions directly.
   - Generate figures from code with stable filenames, units, readable labels, and paper-ready captions.

## Paper Delivery, Traceability, and Style

Use these rules for every modeling-paper deliverable unless the user explicitly asks for a different format or style.

1. Default paper delivery format.
   - Default to LaTeX/TeX as the primary paper handoff format.
   - For substantial paper writing, generate a `.tex` file and compile or attempt to compile a PDF when a local TeX engine is available.
   - Keep Markdown as a drafting aid only when the user asks for quick text or when TeX generation is unnecessary.
   - If the user asks for Word, PPT, or Markdown, follow that request, but keep formulas, tables, figures, and captions consistent with the TeX version when both exist.
   - TeX papers should follow this section order by default: problem restatement, assumptions and notation, data processing, model establishment, model solution, results, validation and sensitivity analysis, model evaluation, conclusion, appendix.
   - When compiling TeX, report whether PDF compilation succeeded. If compilation fails, fix the TeX when feasible; otherwise state the compile error and leave the `.tex` file usable.

2. Hard traceability rules.
   - Do not write numerical conclusions without data, code output, problem-statement conditions, or an explicitly stated assumption.
   - Do not invent distances, coordinates, prices, capacities, sample sizes, error metrics, rankings, or optimization results.
   - Do not write "得到", "计算得到", "结果为", or equivalent result language unless the result is traceable to executed code, provided data, problem-statement conditions, or a clearly labeled assumption.
   - If geographic distance is needed, do not fabricate distance without coordinates, a route table, a map/geocoding source, or an explicit approximation method.
   - Example numbers must be labeled as "示例" and must not be mixed with real computed results.
   - If a required value is missing, write the formula, input table template, and reproducible computation path instead of filling an unsupported number.
   - Maintain a result registry for important numbers: conclusion, value, unit, source file or equation, and reproduction command. Use this registry to keep abstract, body text, tables, and conclusions consistent.

3. Unit and dimension discipline.
   - Every physical quantity should carry a unit in notation tables, formulas, tables, and figure axes.
   - Before writing final results, check common conversions such as days versus hours, km versus m, tons versus kg, yuan versus ten-thousand yuan, and one-way versus round-trip distance.
   - If a model mixes normalized indicators and physical quantities, state which variables are dimensionless and which retain units.
   - If a formula changes units, explain the conversion factor or keep the computation in code with a named variable.

4. Figure and table naming convention.
   - Use stable lowercase filenames with the pattern `fig_q{subquestion}_{topic}.png` for figures and `tab_q{subquestion}_{topic}.csv` or `.xlsx` for tables.
   - Examples: `fig_q1_route.png`, `fig_q1_cost_stack.png`, `fig_q1_load_factor.png`, `tab_q1_summary.csv`, `tab_q1_sensitivity.csv`.
   - For generated paper-ready charts, save both a raster version for documents and, when practical, a vector or source version for reproducibility.
   - Keep filenames aligned with paper references so tables and figures can be regenerated and reinserted without renaming.

5. Chinese paper language constraints.
   - Avoid colloquial and AI-like phrasing such as "我们可以", "建议可以", "本 AI", "智能生成", and empty transitional sentences.
   - Avoid repeatedly using "通过上述分析可以看出"; prefer evidence-driven wording such as "结果表明", "模型表明", "敏感性分析显示", and "本文构建".
   - Each substantive paragraph should be supported by at least one of: equation, data result, code output, figure/table reference, explicit assumption, or validation statement.
   - Write in concise contest-paper style: define the model object, state the method, give the result, and explain the implication.
   - Do not overstate model capability; state uncertainty, approximation, and missing-data risk directly.

## Single-Question and Code-to-Paper Modes

Use these modes when the user narrows the scope to one subquestion, asks to write from existing code/results, asks for an abstract, or asks for a paper audit.

1. Single-question mode.
   - Trigger when the user says "只做第1问", "只写问题一", "仅分析第二问", "single question", or equivalent.
   - Only solve and write the specified subquestion. Do not develop models for other subquestions.
   - Still mention how this subquestion connects to later questions when it affects assumptions, variables, or reusable outputs.
   - Required blocks: scoring points, implicit constraints, 3 modeling routes, selected route, variables, objective/evaluation function, constraints, analytical derivation, algorithm, validation, visualization, TeX-ready paper text, and deliverable checklist.
   - If the specified subquestion requires data from another subquestion or missing external data, state the dependency and provide the reproducible input template instead of inventing values.

2. Code-to-paper mode.
   - Trigger when the user provides code, generated tables, figures, logs, notebooks, or asks "根据代码写论文", "把结果写成论文", "code to paper", or equivalent.
   - Inspect the actual code outputs before writing results. Prefer reading saved CSV/XLSX/JSON/logs over manually copying numbers from memory.
   - Write model solution, result analysis, validation, and figure/table captions using only traceable outputs.
   - Keep all numerical values in the paper synchronized with output files; if a number appears in text, it should be found in a table, figure, log, code output, or stated assumption.
   - If code and paper disagree, treat the code output as the source of truth unless the user specifies otherwise, and flag the inconsistency.

3. Abstract generation rules.
   - The abstract must be result-oriented, not background-oriented.
   - For each solved subquestion, state the model used, core result, key numerical conclusion, and validation or robustness check.
   - Do not include unsupported numbers, vague superiority claims, or method lists without results.
   - If a subquestion has no computed result yet, write the model and pending input clearly instead of fabricating a conclusion.
   - Keep the abstract concise: problem context only when needed, then model-result-validation in the order of the paper.

4. Paper review and audit mode.
   - Trigger when the user asks for "审稿", "查错", "论文审核", "评委视角", "还有什么问题", or equivalent.
   - Lead with findings ordered by severity. Focus on answer coverage, missing constraints, unsupported results, inconsistent numbers, weak validation, unclear figures, and reproducibility gaps.
   - Reference exact section names, equations, tables, figures, or file paths when available.
   - If no major issue is found, state that clearly and list remaining risks such as missing sensitivity analysis, weak external validity, or formatting checks.
   - Do not rewrite the whole paper unless requested; provide actionable fixes first.

5. Final deliverable checklist.
   - For a completed subquestion or full paper, check whether the workspace contains: `.tex`, compiled PDF when possible, source code, input data notes, generated tables, generated figures, captions, appendix code, and reproducible run commands.
   - Verify that table and figure filenames follow the naming convention, and that paper references match the saved filenames.
   - Verify that all headline conclusions are traceable to code output, data, formulas, or explicit assumptions.
   - If any item is missing, list it under "需补充" rather than implying the handoff is complete.

6. Appendix code standards.
   - The appendix should identify the main entry script, input files, output files, random seed, dependencies, and run command.
   - Code in the appendix should be sufficient for reproduction but may omit repetitive boilerplate if a full source file is provided separately.
   - Use deterministic scripts where possible; fix random seeds for stochastic algorithms.
   - Do not include private tokens, API keys, absolute personal credentials, or unrelated environment probing.
   - Appendix code comments should explain modeling steps and outputs, not narrate obvious programming operations.

## Final Quality Gates

Before treating a modeling answer, paper section, or artifact set as complete, apply these gates.

1. Scope gate.
   - The answer covers exactly the requested question range.
   - Every output requested by the prompt is present, and unrelated subquestions are not expanded.

2. Evidence gate.
   - Each headline conclusion links to a formula, table, figure, code output, input data, or explicit assumption.
   - The result registry, if created, agrees with the abstract, conclusion, tables, and figure captions.

3. Model gate.
   - Variables, parameters, objective/evaluation function, and constraints are defined before dense formulas.
   - At least one interpretable baseline or simplified analytical result is present unless the user explicitly asks for a brief answer.

4. Validation gate.
   - The minimum validation set for the problem type has been performed or explicitly marked as not possible with the reason.
   - Sensitivity analysis targets parameters that can change the conclusion, not decorative parameters.

5. Artifact gate.
   - TeX/PDF, code, tables, figures, and appendix materials use stable filenames and are internally consistent.
   - Generated figures have paper-ready captions and are readable at normal paper size.
   - If GPT Image produced a flowchart, the selected image has been checked for text accuracy and layout defects when possible.

## Technical Roadmap and Model Flowcharts

Use this mode when the user asks for 技术路线图, 技术路线, 流程图, 流程框图, 模型流程图, or asks to draw a roadmap based on an existing paper.

1. Base the diagram on the provided paper or draft.
   - Extract the actual problem sequence, core modeling ideas, adopted models, solving logic, validation methods, and final outputs from the paper.
   - Do not add methods, data, metrics, or validation steps that are not in the paper. If a key step is missing, mark it as "需补充" in the explanation, not as a finished result.
   - Keep the roadmap logic as "题目任务 -> 建模思路 -> 核心模型 -> 模型求解 -> 结果验证 -> 结论输出".
   - The roadmap should show the paper's main modeling strategy, not implementation details. Omit routine data-cleaning steps, field fixes, file paths, parameter parsing, code outputs, and other operational details unless they are central to the model.

2. Generate a paper-ready technical roadmap.
   - Use GPT Image direct generation for 技术路线图 and 模型流程框图.
   - Default to black-and-white styling: white nodes, black lines, black text, no gradients, no color blocks, no decorative icons, and no illustrative mini-pictures.
   - Use short, high-level node labels. Put detailed explanation after the chart, not inside the boxes.
   - For a single-question paper, keep the roadmap to about 8-12 nodes when possible. For multi-question papers, group by subquestion only when it improves readability.
   - Avoid dense nested subgraphs, long chains of preprocessing nodes, and step-by-step code execution nodes.
   - A good roadmap reads like the modeling idea of the paper: "问题识别 -> 指标/变量构造 -> 模型选择 -> 求解评价 -> 结论应用".
   - Avoid "AI-like" wording such as "我们可以", "建议可以", "本 AI", "智能生成", or empty transitional phrases. Use direct paper language.

3. Always include a separate model flowchart for the adopted model.
   - Default structure: 输入数据 -> 数据预处理 -> 变量构造 -> 模型假设 -> 模型方程/目标函数 -> 参数估计/算法求解 -> 结果输出 -> 验证与敏感性分析 -> 结论解释.
   - If the paper uses multiple core models, provide one compact combined flowchart or one flowchart per model, depending on clarity.
   - For optimization models, show objective, constraints, solver, feasibility check, and sensitivity analysis.
   - For prediction or fitting models, show training/estimation, error metrics, residual checks, and validation set or baseline comparison.
   - For evaluation models, show indicator construction, normalization, weighting, scoring/ranking, robustness check, and interpretation.
   - The model flowchart may include necessary technical steps, but should still emphasize modeling logic over file handling or code mechanics.

4. Image-generation default.
   - Default to GPT Image for paper-ready 技术路线图 and 模型流程框图.
   - For GPT Image prompts, keep node text short and few, require black-and-white academic style, white background, black lines, rectangular nodes, no icons, no decorative pictures, no gradients, and high legibility.
   - Warn briefly that generated image text may need manual review, especially for Chinese labels, and offer to generate several variants when final publication quality matters.
   - Before image generation, draft a short node list and keep it stable. The image prompt should include the exact title and node labels.
   - After image generation, inspect the rendered chart when possible. Check for Chinese label errors, missing nodes, wrong arrows, unreadable text, and unintended decoration.
   - If the chart has label errors or layout defects, regenerate with fewer nodes or shorter labels. Generate up to 3 variants when final publication quality matters.
   - Save selected route images with names such as `fig_q1_route.png` and model flow images with names such as `fig_q1_model_flow.png`.

5. Required output for roadmap requests.
   - "技术路线图": GPT Image-generated black-and-white flowchart.
   - "模型流程框图": GPT Image-generated black-and-white flowchart.
   - "图注": one concise Chinese caption suitable for the paper.
   - "论文说明段": one short Chinese paragraph explaining why the route supports the paper's solution.
   - For GPT Image output, output the generated image paths or rendered image previews, plus the same figure captions and paper explanation text.
   - "需补充信息": only list missing paper details that affect the chart's correctness.

## Operating Rules

- Answer in Chinese by default unless the user asks otherwise.
- When the user provides a full problem statement, first produce a task decomposition and exactly 3 modeling routes before writing code.
- When the user asks to solve only one subquestion, switch to single-question mode: solve only that subquestion, but include scoring points, implicit constraints, 3 routes, model details, validation, visualizations, and TeX-ready paper text.
- When the user says the solution is not deep enough, "按 CUMCM 一等奖标准重做", "想得不够多", or similar, rewrite the solution using the First-Prize Default Standard instead of merely adding model names.
- When the user asks for a technical roadmap or model flowchart, follow "Technical Roadmap and Model Flowcharts": base it on the paper, keep the roadmap focused on the main modeling idea rather than data-cleaning or code details, keep the content concise, default to black-and-white GPT Image-generated flowcharts, and do not use illustrative icons or decorative mini-pictures.
- When data is provided, inspect columns, missingness, units, and obvious outliers before modeling.
- When starting a new contest project, use `scripts/init_cumcm_project.py` to create `data/`, `src/`, `figures/`, `tables/`, `paper/`, and `appendix/`.
- When CSV/XLSX data is available, use `scripts/data_profile.py` before modeling to generate field summaries, missing/outlier checks, correlations, descriptive statistics, and a data preprocessing draft.
- When writing code, prefer Python unless the user asks for MATLAB; use deterministic scripts/notebooks that can regenerate tables and figures.
- When writing a paper section, default to TeX delivery for substantial outputs, and use contest style: concise, formal, equation-supported, data-supported, and linked to the specific subquestion.
- Enforce the hard traceability rules: no data-backed conclusion without data or code output, no invented geographic distance without coordinates or an explicit approximation method, no "得到" unless the result is traceable, and all example values must be labeled as examples.
- Name generated figures and tables using stable patterns such as `fig_q1_route.png`, `fig_q1_cost_stack.png`, `tab_q1_summary.csv`, and `tab_q1_sensitivity.csv`.
- Use formal Chinese paper language: prefer "本文构建", "结果表明", and "模型表明"; avoid "我们可以" and repetitive "通过上述分析可以看出".
- When the user asks to write from code/results, use code-to-paper mode: read actual output files first, synchronize numbers with generated tables and figures, and flag inconsistencies.
- When the user asks for an abstract, produce a result-oriented abstract with model, key result, numerical conclusion, and validation for each solved subquestion.
- When the user asks for review or audit, lead with severity-ordered findings and focus on answer coverage, traceability, constraints, validation, figures, and reproducibility.
- Before final handoff, run the final deliverable checklist and state missing TeX/PDF/code/table/figure/appendix/run-command items if any.
- When providing appendix code, include main script, inputs, outputs, dependencies, random seed, and run command.
- Prefer analytical modeling where feasible: derive simplified expressions, bounds, or structural conclusions before relying on numerical algorithms; then compare analytical predictions with numerical or data-driven results.
- For every major conclusion, provide either an equation-based reason, a data/code-backed result, a baseline comparison, or a stated assumption with risk.
- When creating plots, follow `references/figure-standards.md`; every figure should answer a subquestion, be generated reproducibly from code, include units, and be saved in a paper-ready format.
- Whenever generating a figure, always output a paper-ready Chinese caption/explanation paragraph that can be pasted into the modeling paper; include what the figure shows, the key trend/result, the subquestion it supports, and analytical-vs-numerical comparison when relevant.
- Follow `references/safety-rules.md`: do not fabricate data results, references, metrics, or conclusions that cannot be traced to code output, data, or stated assumptions.
- Adapt to the user's contest mode using `references/contest-modes.md`, such as route-only, problem-one writing, full paper drafting, code-to-paper writing, paper audit, or final two-hour compression.
- When uncertain, state the assumption and how it affects model risk rather than hiding uncertainty.

## Scripts and Assets

- `scripts/init_cumcm_project.py <project_dir>`: create a contest project skeleton and copy paper/appendix templates.
- `scripts/data_profile.py <csv-or-xlsx-or-data-dir> --outdir tables/data_profile`: inspect CSV/XLSX data and draft a data preprocessing section.
- `assets/paper-template.md`: Markdown paper skeleton for direct filling.
- `assets/paper-template.docx`: Word paper skeleton for handoff and formatting.
- `assets/assumptions-symbols-template.md`: assumptions and notation tables.
- `assets/appendix-code-template.md`: appendix code format template.

## Reference Files

Load only the needed reference:

- `references/workflow.md`: detailed 72-hour contest workflow, problem-type routing, and deliverable checklist.
- `references/modeling-toolbox.md`: common CUMCM model families, when to use them, validation requirements, and failure modes.
- `references/problem-routing.md`: detailed model routing for evaluation, prediction, optimization, propagation, spatial, image, and text problems.
- `references/analytical-vs-numerical.md`: analytical-first modeling workflow and how to compare analytical and numerical results.
- `references/figure-standards.md`: code-generated figure standards for CUMCM papers, including file naming, export formats, chart choices, and captions.
- `references/paper-writing.md`: Chinese modeling paper structure, abstract pattern, section templates, and final review checklist.
- `references/contest-modes.md`: operating modes for route-only analysis, single-question writing, full-paper drafting, code-to-paper writing, paper auditing, and final compression.
- `references/scoring-checklist.md`: judge-oriented checklist for abstract, question coverage, validation, figures, reproducibility, and model evaluation.
- `references/safety-rules.md`: anti-fabrication and traceability rules for data, citations, metrics, and conclusions.
- `references/python-matlab-guide.md`: Python and MATLAB implementation routes, project conventions, plotting, and reproducibility guidance.
