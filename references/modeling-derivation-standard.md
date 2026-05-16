# Modeling Derivation Standard

Use this before writing or revising any `modeling/qx_modeling_idea.md`.
The goal is not only to choose a method, but to make the mathematical model
readable enough that a beginner can reproduce the reasoning, code, and paper
paragraphs.

## Required Section

Every solved subquestion's modeling idea file must contain a section named
`逐步建模推导`, `逐步建模过程`, or an equivalent explicit heading. A model file
that only lists variables, assumptions, and final formulas is incomplete.

## Derivation Chain

Write the derivation as a chain of small transformations:

1. **Time/object/output**: what is being modeled, what time range or sample
   range matters, and what final quantity must be computed.
2. **Problem wording to variables**: convert each important phrase in the
   problem statement into variables, parameters, initial values, bounds, units,
   or data columns.
   Before moving on, read `references/critical-constraint-audit.md` and make a
   small table of consequence-bearing phrases: if a phrase could change the
   numerical answer or conclusion, it must become a variable, constraint,
   scenario, validation item, or explicit blocker.
3. **Mechanism or logic**: state the physical, geometric, statistical,
   operational, or evaluation mechanism that connects variables.
4. **Assumptions with purpose**: for each assumption, say what missing detail it
   resolves, why it is reasonable, and what limitation it creates.
5. **Mathematical depth choice**: decide whether the mechanism calls for a
   deeper mathematical model such as ODE/PDE, stochastic process, network flow,
   dynamic programming, robust optimization, optimal control, or causal
   inference. If yes, state whether it is the main model, correction model, or
   validation model. If no, state why a simpler model is sufficient.
6. **Equation construction**: derive each equation or criterion from the
   mechanism. Explain what the left side means, what the right side means, and
   why the equality/inequality is the right one.
7. **Constraints and boundaries**: list domain limits, time windows, capacity
   limits, feasibility requirements, initial/final conditions, and invalid
   cases.
8. **From local condition to global answer**: explain how pointwise,
   single-sample, single-path, or single-period conditions are aggregated into
   the final objective, duration, score, ranking, forecast, or strategy.
9. **Algorithm from equations**: translate formulas into implementable steps:
   inputs, preprocessing, loops/search/solver/fitting, stopping or boundary
   rules, outputs, and failure status.
10. **Detailed code modeling process**: write how the implementation embodies
   the model, not just what script to run. Use beginner-readable granularity:
   map data files and columns to code variables; state units, sorting, grouping,
   indexing, matrix/vector dimensions, and missing-value handling; translate
   formulas/criteria to functions or calculation steps; translate constraints
   to filters or checks; explain every loop/search/solver/fitting input and
   output; record boundary and failure handling; connect intermediate values to
   saved diagnostics; and map final outputs to `tables/`, `figures/`,
   `results/`, and `paper/main.tex`.
11. **Validation hooks**: state which intermediate values, baselines, edge
   cases, sensitivity checks, or conservation/feasibility checks will verify
   the model.
12. **Paper wording plan**: note which derivation paragraphs, formulas, tables,
    and figures must be written back to `paper/main.tex`.

## Task-Type Prompts

- **Geometry/physics**: explain coordinate system, object representation,
  motion law, distance/intersection/contact condition, boundary event, and
  time/space aggregation. If drag, diffusion, flow, or field evolution matters,
  consider ODE/PDE, finite-difference/finite-volume discretization, and
  conservation or limiting-case checks.
- **Optimization**: explain decision variables, objective source, every
  constraint source, baseline, solver status, and feasibility checks. For
  supply-chain, routing, or resource-allocation tasks, consider network flow,
  stochastic/robust optimization, dynamic programming, queueing, or inventory
  control before using a generic heuristic.
- **Prediction**: explain target variable, temporal split, features, baseline,
  loss metric, validation window, and error interpretation.
- **Causal/statistical intervention**: explain treatment, outcome, confounders,
  causal graph or identification strategy, model equation, and robustness tests.
- **Evaluation/ranking**: explain indicator meaning, direction, normalization,
  weight source, score aggregation, and ranking stability.
- **Simulation**: explain state variables, transition rule, parameters,
  stochastic seeds or deterministic update, repeated runs, and sensitivity.

## Minimum Self-Check

Before solving or writing the paper, ask:

- Could a beginner identify where each equation came from?
- Did every symbol in a formula appear earlier with units or meaning?
- Did the text explain why this model fits the problem better than the baseline?
- Did the text check whether a deeper mathematical model is useful, and avoid
  both under-modeling and decorative over-modeling?
- Are assumptions doing necessary work rather than hiding the conclusion?
- Is the algorithm a direct implementation of the derived equations?
- Does `modeling/qx_modeling_idea.md` explain the code modeling process in
  enough detail that the implementation can be checked without reading every
  line of `src/`?
- Could a beginner reproduce the solve from the modeling file without guessing
  hidden cleaning, sorting, loop, solver, or output steps?
- Are there validation hooks for the main mechanism and the headline result?

If any answer is no, deepen `modeling/qx_modeling_idea.md` before coding or
paper writing.
