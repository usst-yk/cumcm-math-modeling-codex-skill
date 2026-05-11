---
name: cumcm-math-modeling
description: |
  CUMCM/数学建模竞赛 workflow for problem decomposition, data audit,
  route comparison, reproducible solving, validation, figures, and paper writing.
  Use for 全国大学生数学建模竞赛, CUMCM, 建模论文, 赛题分析, 技术路线图,
  模型流程图, 灵敏度分析, 摘要, 一等奖标准, or contest-style modeling reports.
  Do not use for ordinary homework, non-contest paper polishing, image-only
  editing, or pure coding fixes unless contest modeling is requested.
---

# CUMCM Math Modeling

Answer in Chinese by default. Treat the final contest paper as the main
deliverable: every useful analysis, model, result, validation, table, and figure
must ultimately update `paper/main.tex`.

## Always Read First

- Core rules: `references/core-rules.md`
- Output policy and folder layout: `references/output-policy.md`
- Figure, flowchart, and technical-roadmap policy: `references/figure-plan.md`

## Workflow

For full problems, follow the staged workflow in `references/workflow.md` and
the gate checks in `references/stage-gates.md`.

For each solved subquestion:

1. Parse the task and data dependencies.
2. Write `modeling/qx_modeling_idea.md` with detailed step-by-step modeling.
3. Solve with code when needed.
4. Produce tables, GPT-image model flowchart, result figures, and validation.
5. Reverse-check code against the modeling idea.
6. Register headline values in `results/result_registry.csv`.
7. Update `paper/main.tex`.

## Task Routing

Read only the relevant file(s):

- Full problem: `references/workflow.md`, `references/problem-routing.md`
- Single subquestion: `references/task-modes.md`, `references/problem-routing.md`
- Data audit: `references/data-audit.md`, then use `scripts/data_profile.py`
- Problem parsing: `references/problem-parsing.md`, then use `scripts/problem_parser.py`
- Task decomposition: use `scripts/build_task_plan.py`
- Model selection: `references/method-cards.json`, then `references/method-library.md` if needed
- CUMCM A problem: `references/cumcm-a-problem-patterns.md`
- Code to paper: `references/code-to-paper.md`, `references/result-tracking.md`
- Paper writing: `references/paper-writing.md`, `references/paper-assembly.md`
- Abstract: `agents/abstract_writer.md`
- Review: `references/final-review.md`, `references/final-checklist.md`
- Maintenance: `references/maintenance.md`

Role cards live in `agents/`. Use them when entering that stage:
problem parser, coordinator, modeler, coder, writer, assembler, abstract writer,
and reviewer.

## Non-Negotiables

- Always create or update `paper/main.tex`.
- Never split the contest-paper deliverable into `paper/sections/*.tex`.
- Standard output folders are `problem/`, `data/`, `modeling/`, `src/`,
  `tables/`, `figures/`, `results/`, and `paper/`.
- Use `data/`, not `date/`, for raw, cleaned, and processed data.
- Flowcharts and technical roadmaps default to GPT-image.
- Do not write final numbers without a saved, traceable source.
- Do not report optimality without solver status and feasibility checks.
- Do not claim high accuracy without metrics or a baseline.
- Do not leave placeholders in final deliverables unless the user asked for a draft.
