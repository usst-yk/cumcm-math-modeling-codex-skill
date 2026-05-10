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

Use this skill as a CUMCM workflow inside Codex, not as a Web/backend system.
Default to exact task coverage, staged workflow, three-route comparison,
baseline reasoning, reproducible solving, validation, traceable results,
paper-ready figures, and Chinese modeling-paper prose.

Answer in Chinese by default. The primary audience is beginners: use natural
language, hide script commands and file internals unless asked, and run useful
scripts/templates in the background.

## Core Behavior

- Correctness before speed: parse questions, constraints, units, outputs,
  attachments, and scoring clues first.
- Full route design defaults to three routes: baseline, primary route, fallback.
  For urgent or single-question work, keep the same logic but stay concise.
- For major results, use `references/correctness-ladder.md`.
- Do not write final numbers without a saved, traceable source.
- Prefer transparent rigor over fashionable methods.

## Stage Workflow

For full problems, follow this role pipeline. Read `references/agent-workflow.md`
and `references/stage-gates.md` before stage changes.

| Stage | Read | Output |
| --- | --- | --- |
| 0 Problem Parser / 题面解析 | `agents/problem_parser.md` | problem parse |
| 1 Coordinator / 任务拆解 | `agents/coordinator.md` | task plan |
| 2 Data Auditor / 附件审计 | `references/data-audit.md` | data inventory |
| 3 Modeler / 建模路线 | `agents/modeler.md` | Qx model card |
| 4 Solver / 代码求解 | `agents/coder.md` | scripts, tables, figures, registry rows |
| 5 Validator / 验证分析 | `references/validation.md` | validation report |
| 6 Writer / 论文写作 | `agents/writer.md` | Qx paper section |
| 7 Reviewer / 终审 | `agents/reviewer.md` | final findings and blockers |

Process each subquestion as: model card -> code -> tables/figures -> registry ->
validation -> paper section. Do not draft the final abstract before solved
sections have registered results.

## Task Routing

Read `references/task-routing.md` for the complete table.

- Full problem: `references/workflow.md`, `references/problem-routing.md`.
- New project: run `scripts/init_cumcm_project.py` in the background.
- Problem parsing: read `references/problem-parsing.md`, then use
  `scripts/problem_parser.py`.
- Decomposition: parse first with `scripts/problem_parser.py`, then use
  `scripts/build_task_plan.py`.
- Single subquestion/paper: `references/task-modes.md` and
  `references/problem-routing.md`.
- Data files: run `scripts/data_profile.py`, then read `references/data-audit.md`.
- Outputs to paper: read files first, then use `references/code-to-paper.md` and
  `references/result-tracking.md`.
- Paper writing: `references/paper-writing.md`, `references/scoring-checklist.md`.
- Roadmap/flowchart: `references/technical-roadmap.md`; prefer editable
  Mermaid, Graphviz, or SVG.
- Final audit or judge review: read `references/final-review.md` and
  `references/final-checklist.md`, then lead with severity-ordered findings.

## Artifact Rules

- Inspect all sheets in every Excel workbook. State why any table is excluded.
- If sheets share a structure, concatenate them with a source-sheet column.
- Use stable lowercase names: `fig_q1_topic.png`, `tab_q1_topic.csv`.
- Paper numbers, captions, abstract, conclusion, and recommendations must trace
  to `results/result_registry.csv`.
- Default substantial papers to TeX and compile PDF when available.

## Final Handoff

Before final handoff, run `references/scoring-checklist.md`. If any item is 0,
mark the answer incomplete and list the blocker. For projects with artifacts,
use `scripts/validate_results.py`.

## Hard Never Rules

- Never invent attachment fields, data values, references, rankings, distances,
  capacities, coordinates, optimal values, or error metrics.
- Never report optimality without solver status and feasibility checks.
- Never claim "模型精度较高" without an error metric or comparison baseline.
- Never write sensitivity analysis without actual perturbation or a reproducible
  perturbation plan.
- Never cite figures/tables that were not generated or provided.
- Never leave "待补充" placeholders in final deliverables unless asked for a draft.
- Never push unrelated dirty files when syncing the skill to GitHub.

## Distribution

When changing this skill, follow `references/maintenance.md`.
