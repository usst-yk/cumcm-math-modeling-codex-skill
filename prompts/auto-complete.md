# Prompt Auto-Completion Rules

Use this file whenever the user's request is short, vague, beginner-style, or
missing contest-paper details. Do not ask the user to write a long prompt.
Silently expand the request into the complete CUMCM workflow needed for the
intended stage.

## 0. Core Principle

Short prompt means shorthand, not low standard.

- Do not lower modeling depth because the prompt is short.
- Do not treat “求解” as only writing code or only reporting a number.
- Do not treat “写论文” as polishing text before checking result sources.
- Do not treat “优化模型” as cosmetic method replacement.
- Do not treat “直接推导” as permission to skip assumptions, variables,
  constraints, validation, or paper writing.
- Do not print the expanded prompt unless the user explicitly asks to see it.
- Ask a question only when the required problem statement, data, or target
  subquestion is genuinely missing and cannot be inferred from local files.

Every useful output should still support `paper/main.tex`.

## 1. Intent Detection

First classify the user request along four axes:

1. **Scope**: full problem, one subquestion, existing code/result, existing
   paper, or only planning.
2. **Stage**: parse, route, derive, deepen model, solve, validate, write,
   revise, review, or emergency.
3. **Artifact target**: `modeling/`, `src/`, `tables/`, `figures/`, `results/`,
   `paper/main.tex`, or all of them.
4. **Quality target**: ordinary completion, first-prize-oriented completion,
   stronger math, deeper prose, fewer figures, or final submission check.

If several intents appear, choose the one closest to the user's verb:

- “求解/完成/做” -> solve workflow.
- “推导/公式怎么来/能不能直接推” -> derivation workflow.
- “模型更深/高级一点/数学性不够” -> model-deepening workflow.
- “优化模型/改进模型/模型太简单” -> model-improvement workflow.
- “有哪些模型/用什么模型/模型选择” -> model-candidate workflow.
- “摘要/改摘要/重写摘要” -> abstract workflow.
- “论文/正文/写作/润色” -> paper-writing workflow.
- “验证/敏感性/误差/基线” -> validation workflow.
- “图/流程图/路线图” -> figure workflow.
- “检查/审稿/冲奖/国一” -> review and award-readiness workflow.

## 2. Intent Expansion Map

| User says | Expand to | Read next |
| --- | --- | --- |
| 帮我求解第一问 / 做 Q1 / 完成第 1 问 | Full single-question delivery | `references/task-modes.md`, `references/problem-routing.md` |
| 帮我做这题 / 求解整题 / 完成这道题 | Full-problem workflow | `references/workflow.md`, `references/stage-gates.md` |
| 帮我分析题目 / 题目怎么做 / 给路线 | Parse, audit, and route comparison | `references/problem-parsing.md`, `references/problem-routing.md` |
| 还有哪些模型可以考虑 / 用什么模型好 | Candidate model comparison | `references/problem-routing.md`, `references/method-cards.json`, `references/method-library.md` |
| 能不能直接推导 / 直接推公式 / 公式怎么来的 | Beginner-readable derivation | `references/modeling-derivation-standard.md` |
| 建立更深的模型 / 数学性不够 / 高级一点 | Mechanism and advanced-model deepening | `references/advanced-math-modeling.md`, `references/modeling-derivation-standard.md` |
| 优化模型 / 改进模型 / 现在模型太简单 | Model improvement with baseline and validation | `references/problem-routing.md`, `references/correctness-ladder.md` |
| 优化代码 / 跑得太慢 / 求解器不好 | Implementation improvement without changing claims silently | `agents/coder.md`, `references/code-to-paper.md` |
| 修改摘要 / 重写摘要 / 摘要太差 | Final abstract rewrite from traceable results | `agents/abstract_writer.md`, `references/result-tracking.md` |
| 修改论文 / 论文太浅 / 正文太少 | Deep paper rewriting | `references/paper-writing.md`, `references/paper-assembly.md` |
| 图表太多 / 表太多 / 图片堆砌 | Figure/table discipline and prose expansion | `references/paper-writing.md`, `references/figure-plan.md` |
| 补验证 / 做敏感性 / 加误差分析 | Task-matched validation | `references/validation.md`, `references/correctness-ladder.md` |
| 根据代码写论文 / 根据结果写论文 | Code-to-paper traceability | `references/code-to-paper.md`, `references/paper-writing.md` |
| 补图 / 画流程图 / 技术路线图 | Figure and roadmap planning | `references/figure-plan.md`, `references/technical-roadmap.md` |
| 帮我检查 / 审稿 / 看哪里有问题 | Judge-style final review | `references/final-review.md`, `references/final-checklist.md` |
| 看看能不能国一 / 冲奖 / 一等奖标准 | Award-readiness review | `references/first-prize-workflow.md`, `references/first-prize-rubric.md` |
| 快交了 / 时间不够 / 先救急 | Last-hours compression check | `references/task-modes.md` |

## 3. Completed Prompt: Solve One Subquestion

Trigger examples:

- 帮我求解第一问
- 只做第 2 问
- 完成 Q3
- 第四问怎么做

Internally expand to:

1. Identify the requested subquestion and inspect the problem statement,
   relevant attachments, existing `problem/`, `data/`, `modeling/`, `src/`,
   `tables/`, `figures/`, `results/`, and `paper/main.tex`.
2. Parse the subquestion: input, output, decision/model object, constraints,
   units, time/space scope, data dependencies, and hidden scoring points.
3. Create or update `modeling/qx_modeling_idea.md` before solving. It must
   include:
   - this question's role in the whole problem;
   - assumptions, variables, parameters, units, constraints, and boundaries;
   - baseline route, primary route, and fallback route;
   - beginner-readable derivation from problem wording to equations/criteria;
   - detailed code modeling process: data cleaning, sorting, grouping, unit
     conversion, variable mapping, loops/solver inputs and outputs, intermediate
     checks, failure handling, saved tables, saved figures, and paper outputs;
   - validation, sensitivity, feasibility, error, or boundary-case plan;
   - figure plan and paper-writing plan.
4. Solve with reproducible code when calculation is needed. Save code, tables,
   figures, and validation notes under the standard folders.
5. Reverse-check code against the modeling idea. If the implementation differs,
   update the final modeling idea before writing the paper.
6. Update `results/validation_report.md` with headline number sources,
   validation evidence, solver status or feasibility checks, and limitations.
7. Write the current subquestion into `paper/main.tex` with deep prose:
   problem role, variables, assumptions, derivation, algorithm, result
   interpretation, validation, limitation, and handoff.
8. Run available checks before reporting completion.

## 4. Completed Prompt: Solve Full Problem

Trigger examples:

- 帮我做这道题
- 求解整题
- 完成这道数学建模题

Internally expand to:

1. Parse the full problem and all attachments.
2. Audit data files, sheets, fields, units, missing values, duplicates, time
   ranges, and exclusions.
3. Build or update `problem/problem_parse.*`, `problem/task_plan.*`, and
   route comparison.
4. For each subquestion, follow the single-question completed prompt.
5. Connect subquestions through shared variables, assumptions, intermediate
   results, and final conclusions.
6. Assemble `paper/main.tex` as one coherent paper, not a pile of fragments.
7. Write the abstract last from saved results and validation notes.
8. Run full validation checks before handoff.

## 5. Completed Prompt: Candidate Models

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
   - likely equations/objective/criterion;
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

## 6. Completed Prompt: Direct Derivation

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
7. Translate the derivation into algorithm steps and validation hooks.
8. Save or update `modeling/qx_modeling_idea.md`, then write the paper-facing
   derivation into `paper/main.tex` if this is a solved question.

Direct derivation still needs validation. Do not present a clean derivation as
credible without a baseline, boundary case, feasibility check, error metric, or
sensitivity check.

## 7. Completed Prompt: Deeper Mathematical Model

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

## 8. Completed Prompt: Improve Or Optimize Existing Model

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

## 9. Completed Prompt: Abstract Revision

Trigger examples:

- 修改摘要
- 摘要太差
- 重写摘要
- 摘要没有深度
- 摘要要冲奖一点

Internally expand to:

1. Read `paper/main.tex`, saved result tables, figures, code outputs, and
   `results/validation_report.md`.
2. Check that every abstract number has a source. If a number is unsupported,
   do not use it.
3. For each solved subquestion, include:
   - problem object;
   - mathematical/modeling method;
   - key result;
   - validation evidence;
   - limitation or reliability boundary when important.
4. Do not write background-heavy abstract. Focus on method, result, validation,
   and contribution.
5. Keep abstract consistent with body, captions, conclusion, and saved results.
6. Write the revised abstract into `paper/main.tex`.

If body text or validation is too weak, return an abstract blocker list before
polishing.

## 10. Completed Prompt: Paper Writing Or Rewriting

Trigger examples:

- 写论文
- 修改论文
- 论文太差
- 正文太少
- 论文没有深度
- 论文图表太多

Internally expand to:

1. Read modeling ideas, code outputs, tables, figures, validation notes, and the
   current `paper/main.tex`.
2. Refuse to invent missing numbers. Mark blockers when a conclusion has no
   source.
3. Rewrite with deep prose:
   - problem role;
   - problem-to-variable translation;
   - assumptions and why they are necessary;
   - mathematical derivation;
   - algorithm and reproducibility;
   - result interpretation;
   - validation;
   - limitation;
   - handoff to next question or final conclusion.
4. Reduce figure/table dominance:
   - keep only key body visuals;
   - move process tables and repetitive plots to appendix/artifacts;
   - explain every retained visual before and after it appears.
5. Update `paper/main.tex` only. Do not split into `paper/sections/*.tex`.
6. Run available checks.

## 11. Completed Prompt: Validation, Sensitivity, And Baseline

Trigger examples:

- 补验证
- 做敏感性分析
- 加误差分析
- 没有基线
- 怎么证明结果可靠

Internally expand to:

1. Identify task type and choose matching checks:
   - prediction: baseline, train/test or rolling validation, residuals, MAE/RMSE/MAPE/R2;
   - optimization: feasibility, solver status, constraint violation, baseline
     scheme, sensitivity, small exact case when possible;
   - evaluation/ranking: indicator direction, normalization, weight perturbation,
     rank stability, alternative weighting;
   - simulation: boundary case, conservation, parameter sensitivity, repeated
     runs when stochastic;
   - geometry/physics: unit check, limiting case, threshold margin, boundary
     event check;
   - classification/clustering: confusion matrix, stability, cluster meaning,
     holdout or perturbation.
2. Save validation tables/figures under `tables/`, `figures/`, and
   `results/validation_report.md`.
3. Explain in `paper/main.tex` what the check proves and what it does not prove.
4. If validation fails, record limitation and fallback route instead of hiding
   the failure.

## 12. Completed Prompt: Figure, Flowchart, Or Roadmap

Trigger examples:

- 补图
- 画流程图
- 做技术路线图
- 图太少
- 图看不懂

Internally expand to:

1. Decide which figure is needed:
   - model flowchart;
   - technical roadmap;
   - problem structure or geometry schematic;
   - result figure;
   - validation/sensitivity/feasibility figure.
2. Before generating the image, write the prompt/spec under `modeling/` or
   `modeling/flowcharts/`.
3. Use Chinese labels, title, legend, axis/unit labels, and readable paper style.
4. Save final figures under `figures/` with stable names.
5. Write captions and paper explanation into `paper/main.tex`.
6. Do not add decorative figures. Each figure must support a conclusion.

## 13. Completed Prompt: Code Or Result To Paper

Trigger examples:

- 根据代码写论文
- 根据结果表写正文
- 代码跑完了，写进论文
- 这些图怎么写进论文

Internally expand to:

1. Read code, result tables, figures, logs, and validation notes before writing.
2. Map every headline value to source file and field.
3. Translate code logic into model establishment and solving process.
4. Record code-to-model consistency in `modeling/qx_modeling_idea.md`.
5. Write result interpretation, validation, and limitations into
   `paper/main.tex`.
6. Do not describe a model that code did not implement.

## 14. Completed Prompt: Review, Award Readiness, Or Final Check

Trigger examples:

- 帮我检查
- 审稿
- 看看能不能获奖
- 能不能国一
- 最终检查

Internally expand to:

1. Check problem coverage, data audit, assumptions, variables, derivation,
   code traceability, result sources, validation, figures/tables, and
   `paper/main.tex`.
2. Apply first-prize gates by default:
   - core mechanism;
   - validation;
   - traceability;
   - paper readiness.
3. Lead with blocker findings in severity order.
4. Do not call the work complete, award-ready, or first-prize-level if any P1
   blocker remains.
5. If the user asks to fix issues, edit the relevant artifacts and rerun checks.

## 15. Completed Prompt: Emergency Mode

Trigger examples:

- 快交了
- 只剩两个小时
- 先救急
- 先给我能交的版本

Internally expand to:

1. Preserve correctness and traceability first.
2. Identify the highest-value fixes:
   - unsupported abstract numbers;
   - missing direct answer;
   - missing validation;
   - figure/table mismatch;
   - obvious formula/variable inconsistency;
   - uncompiled or missing `paper/main.tex`.
3. Avoid large model rewrites unless current answer is unusable.
4. Produce a clear remaining-risk list.
5. Never invent results to fill gaps.

## 16. When To Ask The User

Ask only when one of these is missing and cannot be inferred:

- the problem statement or target file;
- which subquestion is requested;
- required data attachments;
- whether to modify an existing paper or start a new one;
- whether a destructive rebuild is allowed.

Do not ask the user to choose among routine implementation details. Choose the
most reproducible, contest-appropriate route and continue.

