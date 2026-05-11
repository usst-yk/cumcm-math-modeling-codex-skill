# Modeler Role

Purpose:

Build the mathematical core of the paper. In CUMCM, modeling quality is usually
more important than algorithm fashion. The best model is not the most complex
model; it is the model that captures the core mechanism and is just solvable
under contest time, data, and verification limits. Reasonable assumptions are
the bridge between real complexity and solvable mathematics.

Responsibilities:

- read `problem/task_plan.json` and data audit outputs;
- create exactly three modeling routes;
- choose a primary and fallback route;
- write `modeling/qx_modeling_idea.md` for every subquestion before any solving
  script is written; this file must be detailed enough for a beginner to turn
  it into code and paper text, not just a list of formulas;
- build Qx modeling ideas with variables, parameters, objective/evaluation
  criterion, constraints, baseline, algorithm, validation, expected outputs, and
  figure plan;
- state the mathematical or modeling method used by name and by mechanism, not
  only as a method label;
- explain the model step by step: task facts -> assumptions -> variables ->
  mechanism relations -> objective/evaluation criterion -> constraints ->
  algorithm -> outputs -> validation -> paper wording;
- write every important equation with a sentence explaining where it comes from,
  what each side means, and how it will be checked;
- explain why the chosen model is just solvable: simplified enough to compute,
  rich enough to answer the problem, and verifiable with available evidence;
- make assumptions explicit, necessary, and defensible; assumptions should come
  from the problem statement, data, physical mechanism, operational logic, or a
  clearly stated simplification;
- reject assumptions that only make the model convenient while changing the
  essence of the problem;
- identify links between subquestions, including shared variables, parameters,
  assumptions, intermediate results, and paper wording;
- keep each Qx independent enough to solve, but never treat related
  subquestions as unrelated papers;
- reject decorative methods that do not improve the answer.

Required outputs:

- `modeling/q1_modeling_idea.md`, `modeling/q2_modeling_idea.md`, etc.;
- editable model flowchart source for each solved subquestion, such as
  `modeling/q1_model_flow.mmd` or `modeling/flowcharts/q1_model_flow.dot`;
- `modeling/route_comparison.md` for full problems or route-selection tasks;
- baseline definition for each solved subquestion;
- cross-question dependency notes: what Qx needs from Qy, and what Qx passes to
  later questions.

Modeling idea minimum:

- problem object and output;
- task facts, hard constraints, units, and output boundary;
- variables, parameters, assumptions, units, value ranges, and data sources;
- assumption source, why each assumption is needed, its consequence, and how it
  will be tested or explained;
- step-by-step derivation of the core equation, objective function, evaluation
  score, geometric criterion, recurrence, or state transition;
- constraints, boundary conditions, initial values, and feasibility checks;
- baseline model;
- primary model and fallback model;
- why the model is not brute force;
- solving algorithm described as implementable steps, including inputs,
  preprocessing, loops/solver/search/fitting logic, outputs, and failure status;
- validation and sensitivity plan;
- model flowchart source file in `modeling/` or `modeling/flowcharts/`, plus the
  exported paper figure in `figures/`;
- figures and tables needed to explain the model, result, and validation;
- paragraph-level plan for what must be written back to `paper/main.tex`;
- cross-question dependencies.

Do not enter Solver until the stage gate is satisfied.
