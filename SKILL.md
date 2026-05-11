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
Paper quality has priority over speed for final deliverables: do not shorten
the modeling discussion, assumptions, equations, validation, or abstract merely
to finish faster.

Answer in Chinese by default. The primary audience is beginners: use natural
language, hide script commands and file internals unless asked, and run useful
scripts in the background. Do not expose or create templates unless needed.

Default to paper-first outputs: every useful analysis, modeling, solving,
validation, figure, and result must ultimately update `paper/main.tex`.
Read `references/output-policy.md` before creating project files or templates.
You may avoid empty templates and unnecessary logs, but never omit the TeX
paper entry. Read
`references/figure-plan.md` before solving or writing code for any subquestion.

## Core Behavior

- Correctness before speed: parse questions, constraints, units, outputs,
  attachments, and scoring clues first.
- Paper quality before speed: a slow but complete TeX paper is better than a
  quick thin report.
- Full route design defaults to three routes: baseline, primary route, fallback.
  For urgent or single-question work, keep the same modeling logic and reduce
  only unnecessary project files; do not shorten problem analysis, route
  comparison, modeling, solving, validation, or paper writing.
- Before writing a full paper, follow the staged usage logic in
  `examples/README.md`: parse -> compare routes -> deepen the model through
  multiple rounds -> solve -> validate -> write body -> write abstract last.
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
| 3 Modeler / 建模思路 | `agents/modeler.md` | `modeling/qx_modeling_idea.md` |
| 4 Solver / 代码求解 | `agents/coder.md` | scripts, tables, figures, registry rows |
| 5 Validator / 验证分析 | `references/validation.md` | validation report |
| 6 Writer / 论文写作 | `agents/writer.md` | update `paper/main.tex` |
| 7 Paper Assembler / 论文总装 | `agents/paper_assembler.md` | complete single-file paper |
| 8 Abstract Writer / 摘要写作 | `agents/abstract_writer.md` | final abstract |
| 9 Reviewer / 终审 | `agents/reviewer.md` | final findings and blockers |

Process each subquestion as: initial modeling idea -> code -> tables/figures ->
reverse-check code against the idea -> final modeling idea -> registry ->
validation -> update the relevant part of `paper/main.tex`. Write the final
abstract only after solved subquestions have registered or otherwise traceable
results.
When the user asks to analyze, model, solve, validate, review, or write any
part of a CUMCM problem, update `paper/main.tex`. Do not interpret "solve Qx",
"求解第 x 问", or "完成第 x 问" as "only produce code/tables". All paper text,
including single-question work and intermediate draft sections, must be written
to `paper/main.tex`. Do not create or deliver `paper/sections/*.tex`; a paper
that depends on separate Qx files is incomplete for this skill.

## Task Routing

Read `references/task-routing.md` for the complete table.

- Full problem: `references/workflow.md`, `references/problem-routing.md`.
- CUMCM A problem: read `references/cumcm-a-problem-patterns.md` before route
  comparison.
- High-level route review: use `references/official-benchmark.md` and
  `references/first-prize-rubric.md` as judge-style benchmark references.
- Model selection: use `references/method-cards.json` for compact method checks,
  then `references/method-library.md` only when details are needed.
- New project: run `scripts/init_cumcm_project.py` in the background.
- Output scope: `references/output-policy.md`; do not create full templates
  unless the user asks for a complete project/workspace.
- Problem parsing: read `references/problem-parsing.md`, then use
  `scripts/problem_parser.py`.
- Decomposition: parse first with `scripts/problem_parser.py`, then use
  `scripts/build_task_plan.py`.
- Single subquestion/paper: `references/task-modes.md` and
  `references/problem-routing.md`.
- Data files: run `scripts/data_profile.py`, then read `references/data-audit.md`.
- Figure planning: read `references/figure-plan.md`; default to model schematic
  plus result figure for each solved subquestion.
- Outputs to paper: read files first, then use `references/code-to-paper.md` and
  `references/result-tracking.md`.
- Paper writing: `references/paper-writing.md`, `references/paper-assembly.md`,
  `references/paper-quality-standard.md`, `references/scoring-checklist.md`.
- Benchmark rebuild or real-case redo: read `references/benchmark-rebuild.md`;
  delete generated outputs first, then re-parse, re-plan, re-audit, re-solve,
  re-write TeX, and validate.
- Full paper assembly: `agents/paper_assembler.md`,
  `references/paper-assembly.md`, `references/paper-quality-standard.md`, and
  `templates/paper_main.tex`.
- Final abstract: `agents/abstract_writer.md`, `references/paper-writing.md`,
  `references/result-tracking.md`, `references/scoring-checklist.md`.
- Roadmap/flowchart: `references/technical-roadmap.md`; prefer editable
  Mermaid, Graphviz, or SVG.
- Final audit or judge review: read `references/final-review.md` and
  `references/final-checklist.md`; for first-prize-level claims also read
  `references/first-prize-rubric.md`, then lead with severity-ordered findings.

## Artifact Rules

- Inspect all sheets in every Excel workbook. State why any table is excluded.
- If sheets share a structure, concatenate them with a source-sheet column.
- Use stable lowercase names: `fig_q1_topic.png`, `tab_q1_topic.csv`.
- Create only supporting files needed for the current task, but always create
  or update `paper/main.tex`. For a single subquestion, do not create full
  project templates, empty paper fragments, schema files, or logs unless the
  user explicitly asks for a complete project.
- For every solved subquestion, write the modeling idea before solving:
  `modeling/qx_modeling_idea.md`. It must include the question role,
  assumptions, variables, core equations or decision criterion, constraints,
  baseline, primary route, fallback route, solving plan, validation plan, and
  figure plan. Solver code must follow this file, not invent a different model.
- After solving, compare the actual code path, equations, constraints, solver
  status, generated tables, and figures against `modeling/qx_modeling_idea.md`.
  If they differ, write the difference and update the file to a final modeling
  idea before paper writing. Do not let `paper/main.tex` describe a model that
  is different from the executed code.
- For every solved subquestion, create a figure plan and normally generate at
  least two Chinese figures: one model/problem schematic and one result figure.
  Add validation/sensitivity/feasibility figures for optimization, prediction,
  ranking, scheduling, simulation, or any result that needs checking.
- Skip schematic figures only when a compact table is clearly better, and state
  the reason.
- Contest-paper figures default to Chinese titles, axis labels, legends,
  annotations, and captions. Keep English only for variable names, file names,
  units, or unavoidable technical tokens.
- Key numbers must trace to saved result tables, code output, problem facts, or
  `results/result_registry.csv`. Any number written in the abstract,
  conclusion, figure/table caption, or final recommendation must be registered
  in `results/result_registry.csv`.
- All papers, benchmark papers, solved reports, and intermediate paper drafts
  must use TeX (`paper/main.tex`) and compile PDF when available. Markdown may
  be used only for scratch notes, section planning, or README-style explanation,
  never as the contest-paper artifact.
- Never split a paper deliverable into `paper/sections/*.tex`. Even when the
  user asks for only one subquestion, write a self-contained `paper/main.tex`
  with the necessary problem analysis, assumptions, model, solution,
  validation, and conclusion for that subquestion.
- Final papers must be written as complete mathematical modeling papers: explain
  why the model is reasonable, how assumptions make the problem just solvable,
  how variables/equations/constraints are built, why the algorithm is chosen,
  what each result means, how code verification changed or confirmed the
  original modeling idea, and how later questions inherit earlier work.

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
- Never treat time pressure or single-question scope as a reason to reduce
  modeling depth, validation, figure coverage, or paper depth.
- Never leave "待补充" placeholders in final deliverables unless asked for a draft.
- Never push unrelated dirty files when syncing the skill to GitHub.

## Distribution

When changing this skill, follow `references/maintenance.md`.
