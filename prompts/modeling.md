# Modeling Prompt Expansions

Use this file for model selection, direct derivation, deeper mathematical
modeling, and model improvement.

## Completed Prompt: Candidate Models

Trigger examples:

- 还有哪些模型可以考虑
- 这个问题用什么模型
- 能不能换个模型
- 给我几个建模路线

Internally expand to:

1. Classify the problem type: prediction, optimization, evaluation, simulation,
   scheduling, geometry/physics, network, causal/statistical, clustering, or
   hybrid.
2. Propose exactly three practical routes unless the user asks for broader
   brainstorming:
   - baseline route: simple, explainable, and useful for sanity checking;
   - primary route: mechanism-based, solvable, validated, and paper-friendly;
   - fallback route: deliverable if data, solver, time, or assumptions fail.
3. For each route, state:
   - what mechanism it captures;
   - variables and outputs;
   - required data;
   - likely equations, objective, constraints, or criterion;
   - implementation difficulty;
   - validation method;
   - paper value;
   - risks and failure signs.
4. Recommend one route and explain why it is better for contest scoring, not
   only why it sounds advanced.
5. Save route comparison to `modeling/route_comparison.md` for full problems or
   the relevant `modeling/qx_modeling_idea.md` for one subquestion.

Do not only list method names such as TOPSIS, ARIMA, neural network, or genetic
algorithm. Tie each candidate to the problem mechanism.

## Completed Prompt: Direct Derivation

Trigger examples:

- 可以直接推导吗
- 直接推一下公式
- 这个公式怎么来的
- 从题意一步步推导
- 别直接写代码，先推模型

Internally expand to:

1. Start from the exact problem wording. Identify objects, time, space, inputs,
   outputs, constraints, units, and missing information.
2. Convert wording into variables, parameters, sets, indices, states, decision
   variables, or observed quantities.
3. State assumptions only when they solve a real missing-information problem.
   For each assumption, explain purpose, reasonableness, and limitation.
4. Build the mechanism:
   - geometry/physics: coordinate system, motion law, distance/contact/coverage
     condition, boundary event;
   - optimization: decision variables, objective source, constraint source,
     feasible set;
   - prediction: target, features, time split, loss/error metric;
   - evaluation: indicator direction, normalization, weights, score function;
   - simulation: state, transition rule, parameters, stopping condition.
5. Derive equations step by step. For each equation, explain the left side, the
   right side, unit consistency, and why equality/inequality is appropriate.
6. Explain how local conditions become final answers: sum, maximum, integral,
   ranking, forecast, schedule, route, or policy.
7. Translate the derivation into algorithm steps, code modeling process, and
   validation hooks.
8. Save or update `modeling/qx_modeling_idea.md`, then write the paper-facing
   derivation into `paper/main.tex` if this is a solved question.

Direct derivation still needs validation. Do not present a clean derivation as
credible without a baseline, boundary case, feasibility check, error metric, or
sensitivity check.

## Completed Prompt: Deeper Mathematical Model

Trigger examples:

- 建立更深的模型
- 这个模型太浅
- 数学性不够
- 想冲奖，模型要更高级
- 能不能用更强的数学模型

Internally expand to:

1. Read the current modeling idea, code, results, validation, and paper if they
   exist.
2. Identify what the current model misses:
   - mechanism missing;
   - important constraint missing;
   - uncertainty ignored;
   - time/space dynamics simplified too much;
   - only empirical fitting without explanation;
   - only heuristic optimization without feasibility or baseline.
3. Consider deeper models only when justified:
   - ODE/PDE or finite-difference model for dynamics, diffusion, flow, motion;
   - network flow, shortest path, min-cost flow, VRP, scheduling, or CP-SAT for
     routing/resource allocation;
   - MILP, nonlinear programming, robust/stochastic optimization for decisions
     under constraints or uncertainty;
   - dynamic programming or optimal control for sequential decisions;
   - queueing/inventory models for waiting, service, stock, or supply chain;
   - Bayesian, stochastic process, Markov chain, or Monte Carlo model for
     uncertainty;
   - causal graph, DID, IV, matching, or panel model for intervention questions;
   - clustering plus differentiated modeling when heterogeneous groups matter.
4. For each deeper candidate, decide whether it is:
   - main model;
   - correction model;
   - validation model;
   - upper/lower bound;
   - explanatory model only.
5. Reject decorative complexity. Every deeper model must include variables,
   assumptions, equations, parameter sources, numerical solution steps, and
   validation or boundary checks.
6. Update `modeling/qx_modeling_idea.md` and `paper/main.tex` with the improved
   mechanism and explain what changed from the simpler model.

If the deeper model cannot be identified, estimated, solved, or validated within
contest constraints, state that clearly and use it as limitation or validation,
not as the main answer.

## Completed Prompt: Improve Or Optimize Existing Model

Trigger examples:

- 优化模型
- 改进一下模型
- 现在模型太简单
- 这个模型不够好
- 帮我提高获奖可能性

Internally expand to:

1. Read current `modeling/qx_modeling_idea.md`, code, result tables, figures,
   validation notes, and `paper/main.tex`.
2. Separate model improvement from implementation improvement:
   - model improvement changes assumptions, variables, objective, constraints,
     mechanism, validation, or paper explanation;
   - implementation improvement changes code speed, stability, solver settings,
     or plotting without changing the claimed model.
3. Audit current weaknesses:
   - unclear problem-to-variable translation;
   - missing baseline;
   - weak objective or indicator;
   - constraints not tied to problem wording;
   - no feasibility or solver status;
   - no sensitivity or boundary check;
   - black-box method with no mechanism;
   - result table not explained in paper.
4. Propose focused improvements:
   - add baseline or simplified analytical model;
   - add missing constraints or boundary conditions;
   - replace generic scoring with mechanism-based equation;
   - add robust/stochastic/sensitivity layer;
   - improve solver formulation and feasibility checks;
   - add small exact case or hand-checkable comparison;
   - rewrite paper derivation and result interpretation.
5. Implement only improvements that can be traced, solved, and validated.
6. Update modeling idea, code if needed, validation report, figures/tables if
   needed, and `paper/main.tex`.

Do not silently change conclusions. If an improved model changes headline
numbers, update all tables, figures, validation notes, abstract, and conclusion.
