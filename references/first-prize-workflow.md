# First-Prize Workflow

Use this reference for every CUMCM task by default. The skill treats
first-prize-oriented practice as the normal contest standard, not as an
optional mode. This workflow raises the paper ceiling during modeling, not only
at the final review.

## Official Benchmark Requirement

For every CUMCM run, compare the task with official CUMCM signals before
finalizing routes:

- Contest problem reviews:
  `https://dxs.moe.gov.cn/zx/hd/sxjm/sxjmstjp/`
- Paper showcase and modeling channel:
  `https://dxs.moe.gov.cn/zx/hd/sxjm/`
- Local fallback: `references/official-benchmark.md`

If network or official pages are unavailable, record the blocker in
`results/validation_report.md` and continue with the local fallback rules. Do
not silently skip benchmark comparison when claiming completeness,
first-prize readiness, or award readiness.

## Benchmark Matching

Match by task mechanism before method name:

1. Identify the closest task type: engineering simulation, optimization,
   prediction, evaluation, scheduling, classification, clustering, spatial,
   causal, or hybrid.
2. Extract only the evaluation intent from official sources: expected mechanism,
   common mistakes, validation style, figure density, and paper risks.
3. Write the comparison into `modeling/qx_modeling_idea.md` or
   `modeling/route_comparison.md`:
   - reference source;
   - similar task type;
   - what the current solution should learn;
   - what must not be copied or overclaimed.

## Per-Question First-Prize Contribution

Every solved subquestion must state its first-prize contribution:

- **Mechanism contribution**: what problem mechanism the model captures beyond
  a method name.
- **Validation contribution**: which baseline, feasibility, error, sensitivity,
  stability, boundary, or benchmark check makes the result credible.
- **Figure contribution**: which model, result, and validation figures make the
  conclusion judge-readable.
- **Paper narrative contribution**: how the subquestion supports the whole
  paper, later questions, abstract, and conclusion.

If a subquestion has no visible first-prize contribution, mark it as a blocker
or limitation instead of calling it award-ready.

## Route Upgrade Rule

The three-route comparison must be award-oriented:

| Route | First-prize requirement |
| --- | --- |
| Baseline | Simple, explainable, and usable for sanity check or improvement comparison. |
| Primary | Mechanism-based, solvable, validated, and easy to explain in `paper/main.tex`. |
| Fallback | Deliverable under contest time if data, solver, or assumptions fail. |

The selected route should maximize correctness, validation strength, and paper
clarity under time limits. Do not select a route only because it sounds advanced.

## Critical Gate

Do not call a solution first-prize-level unless all four critical items pass:

- core mechanism;
- validation;
- traceability;
- paper readiness.

If any critical item is missing, record a P1-style blocker and give the
specific rework action. A high total score cannot compensate for a missing
critical item.

## Paper Competitiveness Rules

- The paper must explain the model as a coherent story from task facts to
  variables, equations, algorithm, results, validation, and conclusion.
- Abstract numbers must match saved tables, figures, code outputs, and
  `results/validation_report.md`.
- Figures must support conclusions, not decorate the paper.
- Do not use advanced mathematics as ornament. Every advanced model must have
  identifiable parameters, equations, solution steps, and validation.
- Do not hide weak validation behind strong wording. If evidence is incomplete,
  write the limitation and the next rework action.
