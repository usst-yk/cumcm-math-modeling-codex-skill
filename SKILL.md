---
name: cumcm-math-modeling
description: |
  Chinese CUMCM mathematical modeling workflow for contest problem decomposition,
  route comparison, data audit, reproducible Python/MATLAB solving, validation,
  technical roadmap diagrams, and paper writing.
  Use when the user mentions 全国大学生数学建模竞赛, CUMCM, 数学建模, 建模论文,
  赛题分析, 模型建立, 模型求解, 技术路线图, 模型流程图, 灵敏度分析,
  摘要, 一等奖标准, or asks to turn a contest problem/data into a rigorous
  modeling solution and report.
  Do not use for ordinary homework, pure theory derivations, general scientific
  figure polishing, physics/DFT manuscript writing, image editing, translation,
  ordinary document polishing, or pure coding bug fixes unless the user
  explicitly wants a mathematical-modeling contest workflow.
---

# CUMCM Math Modeling

Use this skill as a CUMCM modeling workflow inside Codex, not as a Web/backend multi-agent system. Default to a rigorous contest deliverable: exact task coverage, staged role workflow, three-route comparison, analytical or baseline reasoning before computation, reproducible code, validation, traceable results, paper-ready figures, and Chinese modeling-paper prose.

Answer in Chinese by default unless the user asks otherwise.

## Core Rules

1. Correctness comes before speed.
   - Parse every subquestion before modeling.
   - Extract hard constraints, required outputs, units, time/spatial scales, data attachments, and implicit scoring points.
   - If data, equations, code outputs, figures, and paper text disagree, stop and resolve the contradiction before writing final conclusions.

2. Every full solution needs exactly three candidate routes.
   - Route A: interpretable baseline, simplified analytical model, or hand-checkable heuristic.
   - Route B: primary contest route with stronger optimization, prediction, evaluation, simulation, network, or mechanism structure.
   - Route C: robustness route, fallback route, or justified extension.
   - Compare fit, assumptions, data demand, interpretability, implementation risk, validation path, and paper expressiveness before selecting a primary route and fallback.

3. Use a correctness ladder for major results.
   - Baseline: analytical expression, simplified case, bound, naive predictor, greedy rule, or manual sample check.
   - Main model: explicit variables, parameters, objective/evaluation criterion, constraints, and reproducible algorithm.
   - Cross-check: feasibility, dimension/unit check, alternative formulation, small-case brute force, residual/error metric, or independent recomputation.
   - Stress test: perturb conclusion-driving inputs or parameters and report stability.

4. Keep results traceable.
   - Do not invent data columns, distances, coordinates, capacities, sample sizes, rankings, error metrics, optimal values, or references.
   - Do not report optimality without solver status and feasibility checks.
   - Do not claim "模型精度较高" without an error metric or comparison baseline.
   - Do not cite figures/tables that were not generated or provided.
   - Maintain a result registry for important numbers when writing a paper.

5. Use transparent rigor over decorative complexity.
   - Do not use TOPSIS/AHP/entropy weighting, neural networks, metaheuristics, grey models, or simulation layers only because they look like modeling methods.
   - Prefer exact, convex, dynamic programming, network flow, or mixed-integer formulations when the problem size allows.
   - Use neural networks only when sample size and validation design justify them.
   - For stochastic methods, fix seeds, repeat runs, and report variation.

## Stage Workflow

For full-problem work, execute the role pipeline in order and read the matching role card when the stage starts:

| Stage | Role card | Required artifact |
| --- | --- | --- |
| 0 Coordinator / 题意拆解 | `agents/coordinator.md` | `problem/task_plan.json` and `problem/task_plan.md` |
| 1 Data Auditor / 附件审计 | `references/data-audit.md` | data inventory tables |
| 2 Modeler / 建模路线 | `agents/modeler.md` | `problem/model_card_qx.md` |
| 3 Solver / 代码求解 | `agents/coder.md` | Qx scripts, tables, figures, registry rows |
| 4 Validator / 验证分析 | `references/validation.md` | `results/validation_report.md` |
| 5 Writer / 论文写作 | `agents/writer.md` | Qx paper section |
| 6 Reviewer / 终审 | `agents/reviewer.md` | final checklist and blockers |

Read `references/agent-workflow.md` and `references/stage-gates.md` before crossing stages. Do not enter Solver until task mapping, data inventory, and at least one baseline route exist. Do not enter Writer until headline numbers are registered. Do not draft the final abstract before all solved Q sections have registered results.

For full-problem solving, process each subquestion as an independent loop:
1. build Qx model card;
2. implement Qx code;
3. save Qx tables and figures;
4. register Qx headline numbers;
5. run Qx validation;
6. write Qx paper section;
7. move to Qx+1 only after unresolved blockers are recorded.

## Task Routing

- Full CUMCM problem solving: read `references/workflow.md`, `references/problem-routing.md`, `references/scoring-checklist.md`, and the relevant modeling reference. Initialize a project with `scripts/init_cumcm_project.py` when no project structure exists.
- New project / start new problem / initialize workspace: run `scripts/init_cumcm_project.py` with the requested project name, then explain briefly that it created a standard workspace for problem files, data, code, results, figures, tables, paper, and logs. Do not ask the user to run the script manually unless they explicitly want manual commands.
- Problem decomposition: use `scripts/build_task_plan.py` to create a reusable task-plan template, then refine it from the problem statement.
- Single subquestion: read `references/contest-modes.md` and `references/problem-routing.md`; solve only the requested subquestion while noting dependencies on later questions.
- Route design only: read `references/problem-routing.md` and `references/workflow.md`; deliver task decomposition, scoring surface, three overall routes, and a 72-hour order.
- Data files present: run `scripts/data_profile.py` with `--input <data-or-dir> --output <tables-dir>` before modeling; read `references/data-audit.md`.
- Code/logs/tables/figures to paper: read actual outputs first, then use `references/code-to-paper.md`, `references/result-tracking.md`, and `scripts/result_registry.py`.
- Paper writing, abstract, conclusion, or final polishing: read `references/paper-writing.md`, `references/scoring-checklist.md`, and use the result registry if numbers appear.
- Technical roadmap or model flowchart: read `references/technical-roadmap.md`; default to `scripts/make_roadmap_svg.py`, Mermaid, Graphviz, or SVG source first, and use GPT Image only when the user explicitly wants a designed image.
- Figures: read `references/figure-standards.md`; for common matplotlib styling, reuse `scripts/make_paper_figures.py`.
- Final audit or judge review: read `references/final-review.md` and `references/final-checklist.md`, then lead with severity-ordered findings.
- Result validation: use `scripts/validate_results.py` when a project contains paper, result registry, figures, tables, or logs.
- Python/MATLAB implementation details: read `references/python-matlab-guide.md`.
- Safety and anti-fabrication questions: read `references/safety-rules.md`.

## Required Blocks By Mode

Full problem:
- Problem decomposition by subquestion.
- Data inventory and attachment coverage audit when data exist.
- Three-route comparison and selected primary/fallback route.
- Per-question input -> decision/model object -> output -> validation mapping.
- Baseline, main model, validation, sensitivity/robustness, figures/tables, and paper structure.

Single question:
- Scoring points and implicit constraints.
- Three routes for that question.
- Variables, parameters, objective/evaluation function, constraints, derivation or baseline, algorithm, validation, visualization plan, and TeX-ready Chinese paper text.

Data-to-code-to-paper:
- Data profile outputs, deterministic code path, generated tables/figures, result registry, TeX paper draft, and reproduction command.

Code-to-paper:
- Read output files before writing; synchronize all text numbers with saved outputs; flag inconsistencies instead of guessing.

Roadmap/flowchart:
- Editable source file first (`.mmd`, `.dot`, or `.svg`), exported figure second, caption and paper explanation third.
- Keep labels short, high-level, and paper-readable. Do not add methods not present in the paper or selected route.

## Data And Artifact Rules

- Inspect all sheets in every Excel workbook. Never silently use only the first sheet.
- If sheets share a structure, concatenate them with a source-sheet column.
- If a sheet/table is excluded, state why.
- Compare covered row counts, reconstructed task counts, and time ranges with wording such as "全部", "一周", "全年", "所有样本".
- Generate stable lowercase names: `fig_q1_topic.png`, `tab_q1_topic.csv`, `tab_q1_topic.xlsx`.
- Default substantial papers to TeX; compile PDF when a local TeX engine is available.
- Appendix code should name the main script, inputs, outputs, dependencies, seed, and run command.

## First-Prize Score Gate

Before final handoff, score each item 0-2. If any item is 0, mark the answer incomplete and list the blocker.

| Item | Check |
| --- | --- |
| 题意覆盖 | Every requested subquestion, constraint, unit, and output form is covered. |
| 数据审计 | All files/sheets, fields, units, missingness, time ranges, and exclusions are checked. |
| 基线模型 | At least one analytical, simplified, or hand-checkable baseline exists. |
| 主模型 | Variables, parameters, objective/evaluation criterion, and constraints are complete. |
| 求解可靠性 | Code is reproducible, seeds fixed when needed, and solver/status diagnostics reported. |
| 验证 | Error, feasibility, sensitivity, robustness, or boundary checks match the task type. |
| 图表 | Each figure/table supports a concrete conclusion and has a paper-ready caption. |
| 论文一致性 | Abstract, body, tables, figures, appendix, and result registry agree. |

## Hard Never Rules

- Never invent attachment fields or use data not present unless clearly labeled as an assumption or example.
- Never write sensitivity analysis without actually perturbing parameters or giving a reproducible perturbation plan.
- Never write "得到", "计算得到", or final numeric claims without data, code output, equations, problem-statement values, or explicit assumptions.
- Never leave "待补充" placeholders in final deliverables unless the user asked for a draft.
- Never push unrelated dirty files when syncing the skill to GitHub.

## Distribution

When this skill is changed and a GitHub remote is configured, verify the changed files, commit only the relevant skill files, and push to `main`. Keep distribution on the live main branch; do not create GitHub Releases or GitHub Packages for this skill.
