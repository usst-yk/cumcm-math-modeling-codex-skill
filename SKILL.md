---
name: cumcm-math-modeling
description: |
  CUMCM/数学建模竞赛 workflow for problem decomposition, data audit,
  route comparison, reproducible solving, validation, figures, and paper writing.
  Use for 全国大学生数学建模竞赛, CUMCM, 建模论文, 赛题分析, 技术路线图,
  模型流程图, 灵敏度分析, 摘要, 一等奖标准, or contest-style modeling reports.
---

# CUMCM Math Modeling

Use this skill as a CUMCM modeling workflow inside Codex, not as a Web/backend
multi-agent system. Default to a rigorous contest deliverable: exact task
coverage, staged role workflow, three-route comparison, baseline reasoning,
reproducible solving, validation, traceable results, paper-ready figures, and
Chinese modeling-paper prose.

Answer in Chinese by default. The primary audience is beginners: use natural
language, hide script commands and file internals unless asked, and run useful
scripts/templates in the background.

## Core Behavior

- Correctness before speed: parse subquestions, constraints, units, outputs,
  attachments, and scoring clues before solving.
- Full solutions need exactly three candidate routes: baseline/analytical,
  primary contest route, and robustness/fallback route.
- Use the correctness ladder for major results: baseline -> main model ->
  cross-check -> stress test. See `references/correctness-ladder.md`.
- Keep results traceable. Do not write final numbers without data, code output,
  equations, problem values, or explicit assumptions.
- Prefer transparent rigor over decorative complexity. Do not use fashionable
  methods only because they look like modeling.

## Stage Workflow

For full-problem work, follow the staged role pipeline. Read
`references/agent-workflow.md` and `references/stage-gates.md` before crossing
stages.

| Stage | Read | Main output |
| --- | --- | --- |
| 0 Coordinator / 题意拆解 | `agents/coordinator.md` | task plan |
| 1 Data Auditor / 附件审计 | `references/data-audit.md` | data inventory |
| 2 Modeler / 建模路线 | `agents/modeler.md` | Qx model card |
| 3 Solver / 代码求解 | `agents/coder.md` | scripts, tables, figures, registry rows |
| 4 Validator / 验证分析 | `references/validation.md` | validation report |
| 5 Writer / 论文写作 | `agents/writer.md` | Qx paper section |
| 6 Reviewer / 终审 | `agents/reviewer.md` | final findings and blockers |

For full problems, process each subquestion as a loop: model card -> code ->
tables/figures -> result registry -> validation -> paper section. Do not draft
the final abstract before solved Q sections have registered results.

## Task Routing

Read `references/task-routing.md` for the complete routing table. Minimum rules:

- Full problem: `references/workflow.md`, `references/problem-routing.md`,
  `references/scoring-checklist.md`.
- New project or workspace setup: run `scripts/init_cumcm_project.py` in the
  background and explain the created workspace simply.
- Decomposition: use `scripts/build_task_plan.py`, then refine from the problem.
- Single subquestion or single-question paper: `references/contest-modes.md`
  and `references/problem-routing.md`.
- Data files: run `scripts/data_profile.py`, then read `references/data-audit.md`.
- Outputs to paper: read files first, then use `references/code-to-paper.md`
  and `references/result-tracking.md`.
- Paper writing: `references/paper-writing.md` and
  `references/scoring-checklist.md`.
- Roadmap/flowchart: `references/technical-roadmap.md`; prefer editable
  Mermaid, Graphviz, or SVG before image-only output.
- Final audit or judge review: read `references/final-review.md` and
  `references/final-checklist.md`, then lead with severity-ordered findings.

## Artifact Rules

- Inspect all sheets in every Excel workbook; never silently use only the first
  sheet. State why any sheet/table is excluded.
- If sheets share a structure, concatenate them with a source-sheet column.
- Use stable lowercase names such as `fig_q1_topic.png`,
  `tab_q1_topic.csv`, and `tab_q1_topic.xlsx`.
- Any numerical conclusion in paper text, captions, abstract, conclusion, or
  recommendations must appear in `results/result_registry.csv`.
- Default substantial papers to TeX and compile PDF when a local TeX engine is
  available.

## Final Handoff

Before final handoff, run `references/scoring-checklist.md`. If any item is 0,
mark the answer incomplete and list the blocker. For project folders with paper,
registry, figures, tables, or logs, use `scripts/validate_results.py`.

## Hard Never Rules

- Never invent attachment fields, data values, references, rankings, distances,
  capacities, coordinates, optimal values, or error metrics.
- Never report optimality without solver status and feasibility checks.
- Never claim "模型精度较高" without an error metric or comparison baseline.
- Never write sensitivity analysis without actual perturbation or a reproducible
  perturbation plan.
- Never cite figures/tables that were not generated or provided.
- Never leave "待补充" placeholders in final deliverables unless the user asked
  for a draft.
- Never push unrelated dirty files when syncing the skill to GitHub.

## Distribution

When this skill is changed, verify changed files, commit only relevant skill
files, and push to `main`. See `references/maintenance.md`.
