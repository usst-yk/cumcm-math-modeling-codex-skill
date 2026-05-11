---
name: cumcm-math-modeling
description: |
  CUMCM/数学建模竞赛 workflow for problem decomposition, data audit,
  route comparison, reproducible solving, validation, figures, and paper writing.
  Use for 全国大学生数学建模竞赛, CUMCM, 建模论文, 赛题分析, 技术路线图,
  模型流程图, 灵敏度分析, 摘要, 一等奖/省奖导向审稿, or contest-style
  modeling reports. Do not use for ordinary homework, non-contest paper
  polishing, image-only editing, or pure coding fixes unless contest modeling is
  requested.
---

# CUMCM Math Modeling

Answer in Chinese by default. Treat the final contest paper as the main
deliverable: every useful analysis, model, result, validation, table, and figure
must ultimately update `paper/main.tex`.

## Always Read First

- Core rules: `references/core-rules.md`
- Output policy and folder layout: `references/output-policy.md`
- Figure, flowchart, and technical-roadmap policy: `references/figure-plan.md`
- Prompt routing for stepwise examples: `references/prompt-router.md`

## Workflow

For full problems, follow the staged workflow in `references/workflow.md` and
the gate checks in `references/stage-gates.md`.

- Correctness before speed: parse questions, constraints, units, outputs,
  attachments, and scoring clues first.
- Before writing a full paper, follow the staged usage logic in
  `examples/README.md`: parse -> compare routes -> deepen the model through
  multiple rounds -> solve -> validate -> write body -> write abstract last.
- When a user gives a broad prompt, first map it to one step in
  `examples/README.md` through `references/prompt-router.md`; do not skip
  straight to a thin complete paper unless the user explicitly asks for a quick
  draft.
- Paper quality before speed: for final papers, a slow but complete TeX paper
  is better than a quick thin report.
- Full route design defaults to three routes: baseline, primary route, fallback.
  For urgent or single-question work, keep the same modeling logic and reduce
  only unnecessary project files; do not shorten problem analysis, route
  comparison, modeling, solving, validation, or paper writing.
- For complete problems, prize-oriented work, or rework loops, use one
  independent subagent/reviewer per subquestion when available. The main agent
  coordinates symbols, data, code, figures, paper assembly, and final audit;
  subagents identify topic coverage gaps, formula/variable issues, validation
  holes, and paper weaknesses.
- Rework loop gate: when the user asks to continue, redo, optimize, prepare a
  PR, or update a case, first check `git status`. Pull/merge only when the user
  asks or has not forbidden it; if the user says "不急着 pull", organize local
  work first.
- Progress gate: if the user asks to see progress, open or regenerate the local
  progress page/dashboard before editing, then record subagent reviews,
  blockers, validations, and final outcomes when progress tooling exists.
- For 2025 CUMCM B-type optical-thickness problems, do not stop at a
  single-beam dominant-frequency baseline. Read the B-problem references and
  build the evidence chain: raw spectrum audit -> Snell/Fresnel/Cauchy model
  route -> sliding FFT/band selection -> single-angle and joint fitting ->
  residual diagnostics -> Airy multi-beam decision -> uncertainty.
- For 2025 CUMCM C-type NIPT timing and abnormality problems, do not stop at a
  thin regression/classification draft. Read the C-problem pipeline and build
  the evidence chain: official question parse -> fetal-fraction literature
  gate -> baseline concentration model -> fixed BMI timing -> iterative BMI
  boundary/timing optimization -> female-fetus screening classifier -> ROC,
  sensitivity, threshold perturbation, and screening-not-diagnosis boundary.
- For major results, use `references/correctness-ladder.md`.
- Do not write final numbers without a saved, traceable source.
- Prefer transparent rigor over fashionable methods.

For each solved subquestion:

1. Parse the task, data dependencies, and expected output.
2. Write `modeling/qx_modeling_idea.md` with detailed step-by-step modeling:
   variables, parameters, assumptions, formulas, objective/evaluation,
   constraints/criterion, algorithm, validation plan, figure/table plan, and
   paper-writing plan.
3. Solve with code when needed, and record solver/search status or feasibility
   status for optimization problems.
4. Produce result tables, a Chinese model flowchart, result figures, and
   validation/sensitivity figures.
5. Reverse-check code, tables, figures, and paper claims against the modeling
   idea; if they differ, update the final modeling idea before writing prose.
6. Register headline values, source files, validation notes, and limitations in
   `results/result_registry.csv`.
7. Write a complete Chinese paper paragraph for the subquestion in
   `paper/main.tex`.
8. Check that the abstract, body, captions, tables, and result registry agree.

## Task Routing

Read only the relevant file(s):

- Full problem: `references/workflow.md`, `references/problem-routing.md`
- Prompt/example routing: `references/prompt-router.md`
- CUMCM 2025 B / thin-film optical thickness: read
  `references/award-paper-learning.md`, `references/reference_miner.md`,
  `references/B_problem_data_pipeline.md`, `references/B_problem_model_referee.md`,
  `references/B_problem_validation.md`,
  `references/B_problem_figure_referee.md`, and
  `references/storyline_planner.md` before finalizing the route or paper.
- CUMCM 2025 C / NIPT timing and fetal abnormality: read
  `references/literature-research.md`, `references/reference_miner.md`,
  `references/award-paper-learning.md`, `references/C_problem_nipt_pipeline.md`,
  `references/first-prize-rubric.md`, and `references/storyline_planner.md`
  before finalizing the route or paper.
- Prize-oriented or reference-based paper work: inspect local excellent-paper
  packs first. If no local reference matches the problem, topic, or method
  family, autonomously search trustworthy web sources and record them. Learn
  only structure, route progression, validation habits, figure roles, and prose
  standards.
- When using award papers or public paper packs, extract only structure,
  model progression, validation logic, figure function, and style rules. Never
  copy prose, figures, final numbers, data, or unlicensed code into the skill
  or current paper.
- CUMCM A problem: read `references/cumcm-a-problem-patterns.md` before route
  comparison.
- High-level route review: use `references/official-benchmark.md` and
  `references/first-prize-rubric.md` as judge-style benchmark references.
- Model selection: use `references/method-cards.json` for compact method checks,
  then `references/method-library.md` only when details are needed.
- New project: run `scripts/init_cumcm_project.py` in the background.
- Output scope: `references/output-policy.md`; use only the standard output
  folders for both single-question and full-problem work.
- Problem parsing: read `references/problem-parsing.md`, then use
  `scripts/problem_parser.py`.
- Decomposition: parse first with `scripts/problem_parser.py`, then use
  `scripts/build_task_plan.py`.
- Single subquestion/paper: `references/task-modes.md` and
  `references/problem-routing.md`.
- Data files: run `scripts/data_profile.py`, then read `references/data-audit.md`.
- Figure planning: read `references/figure-plan.md`; default to a GPT-image
  final model flowchart plus a result figure for each solved subquestion. Save
  the Chinese flowchart prompt/spec in `modeling/qx_model_flow_prompt.md` or an
  equivalent modeling note.
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
- Roadmap/flowchart: `references/technical-roadmap.md`; use GPT-image by
  default and record the Chinese prompt/spec in `modeling/`.
- Final audit or judge review: read `references/final-review.md` and
  `references/final-checklist.md`; for first-prize-level claims also read
  `references/first-prize-rubric.md`, then lead with severity-ordered findings.
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
- Do not add case-local `logs/`, `build/`, `appendix/`, `presentation/`,
  `notebooks/`, or extra `references/` folders; formal appendices belong in
  `paper/main.tex`.
- Flowcharts and technical roadmaps default to GPT-image.
- Paper figures default to the bundled Chinese font assets under `assets/fonts/`.
- Do not write final numbers without a saved, traceable source.
- Do not report optimality without solver status and feasibility checks. For
  heuristic, grid, coordinate, genetic, simulated annealing, or other non-exact
  optimization, write "best-found/current candidate-set feasible solution" and
  keep an iteration trace, feasibility check, baseline comparison, and limitation.
- Do not claim high accuracy without metrics or a baseline. Screening/classifier
  tasks need ROC-AUC, threshold rule, sensitivity, specificity, confusion matrix,
  and, when possible, cross-validation and calibration/Brier evidence.
- Do not leave placeholders in final deliverables unless the user asked for a draft.
- Formal contest-paper prose must not expose project workflow, Codex/agent
  process, scripts, paths, dashboards, tests, registries, "run passed",
  "closed loop", "benchmark", progress-review language, or other meta writing
  in the abstract, body, captions, or conclusion. Rewrite internal workflow as
  paper-facing statements about variables, assumptions, objectives, algorithms,
  results, validation, and limitations.
