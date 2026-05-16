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
deliverable for solved or paper-facing work. Planning-only work should still
produce artifacts that can later be written into `paper/main.tex`, but it does
not have to edit the paper immediately.

## Always Read First

- Short beginner request intent map: `prompts/intent-map.md`
- Core rules: `references/core-rules.md`

## Workflow

For full problems, follow the staged workflow in `references/workflow.md` and
the gate checks in `references/stage-gates.md`.

For each solved subquestion:

1. Parse the task and data dependencies.
2. Write `modeling/qx_modeling_idea.md` using
   `references/modeling-derivation-standard.md`; it must include a
   beginner-readable derivation from problem wording to variables, mechanisms,
   equations/criteria, constraints, code modeling process, algorithm,
   validation, and paper wording.
3. Solve with code when needed.
4. Produce tables, GPT-image model flowchart, result figures, and validation.
5. Reverse-check code against the modeling idea.
6. Record headline value sources in saved tables, figures, and validation notes.
7. Update `paper/main.tex`.

## Task Routing

Read only the relevant file(s):

- Short or vague beginner request: `prompts/intent-map.md`, then route by the
  expanded intent below. Use `prompts/auto-complete.md` only as the compatibility
  navigation entry if needed
- Solve one subquestion or full problem: `prompts/solve.md`
- Candidate models, direct derivation, deeper model, or model optimization:
  `prompts/modeling.md`
- Abstract, paper writing, figure/table discipline, or code-to-paper writing:
  `prompts/writing.md`
- Baseline, validation, sensitivity, or reliability checks:
  `prompts/validation.md`
- Judge-style review, award readiness, or emergency mode: `prompts/review.md`
- Full problem: `references/workflow.md`, `references/problem-routing.md`
- Single subquestion: `references/task-modes.md`, `references/problem-routing.md`
- Before writing any `modeling/qx_modeling_idea.md`:
  `references/modeling-derivation-standard.md`
- Data audit: `references/data-audit.md`, then use `scripts/data_profile.py`
- Problem parsing: `references/problem-parsing.md`, then use `scripts/problem_parser.py`
- Task decomposition: use `scripts/build_task_plan.py`
- Before finalizing any model route or paper-facing claim:
  `references/critical-constraint-audit.md`
- Model selection: `references/method-cards.json`, then `references/method-library.md` if needed
- Mathematical depth: `references/advanced-math-modeling.md` when the problem has
  physical mechanisms, networks, uncertainty, causal questions, PDE/ODE dynamics,
  stochastic processes, or when the user asks for stronger mathematical modeling
- First-prize gate, rubric, and benchmark: `references/first-prize-workflow.md`,
  `references/first-prize-rubric.md`, `references/official-benchmark.md`
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

- Create or update `paper/main.tex` for solved subquestions, full-problem
  solving, paper writing/revision, code/result-to-paper work, and any validation
  or review fix that changes paper-facing claims.
- Planning-only tasks such as problem parsing, route comparison, candidate model
  brainstorming, or pre-solve derivation may stop at `problem/`, `modeling/`,
  or `results/`, but must state what would later enter the paper.
- Never split the contest-paper deliverable into `paper/sections/*.tex`.
- Standard output folders are `problem/`, `data/`, `modeling/`, `src/`,
  `tables/`, `figures/`, `results/`, and `paper/`.
- Use `data/`, not `date/`, for raw, cleaned, and processed data.
- Flowcharts and technical roadmaps are GPT-image paper figures.
- Paper figures default to the bundled Chinese font assets under `assets/fonts/`.
- Do not write final numbers without a saved, traceable source.
- Final paper-facing numeric display must use at most two decimal places in
  `paper/main.tex`, final tables embedded in the paper, and output figures
  intended for the paper. Intermediate result files, source tables, logs, and
  validation records may keep higher precision for traceability, but the final
  prose, captions, tables, and visible figure labels must not show more than two
  decimal places.
- Do not let `modeling/qx_modeling_idea.md` collapse into a formula list; every
  solved question needs a section such as “逐步建模推导” explaining how the
  model is built from the problem facts, in prose a beginner can follow.
- Do not let code exist only in `src/`. Every solved question needs a detailed
  “代码建模流程” section in `modeling/qx_modeling_idea.md` that maps data,
  variables, formulas, constraints, loops/solvers, intermediate checks, outputs,
  and figures to the actual implementation.
- Do not stop at generic contest methods when a mechanism-based mathematical
  model is justified. For physics, supply-chain, PDE/ODE, stochastic, network,
  control, or causal tasks, consider whether a deeper mathematical model can be
  used as the main model, correction model, or validation model.
- Do not force advanced mathematics for decoration. Every advanced model must
  have variables, assumptions, equations, parameter sources, numerical solution
  steps, and validation or boundary checks that can be written into the paper.
- Do not report optimality without solver status and feasibility checks.
- Do not claim high accuracy without metrics or a baseline.
- Do not leave placeholders in final deliverables unless the user asked for a draft.
- Treat terse requests such as “帮我求解第一问”, “做 Q1”, “帮我写论文”, and
  “检查一下” as complete intent shortcuts using `prompts/intent-map.md`.
  Do not ask the user to write long prompts and do not lower quality because
  the prompt is short.
- Every CUMCM run defaults to first-prize-oriented standards: perform official
  benchmark comparison and critical gate checks for core mechanism, validation,
  traceability, and paper readiness. Do not call the work complete,
  first-prize-level, or award-ready if any critical gate is missing.
