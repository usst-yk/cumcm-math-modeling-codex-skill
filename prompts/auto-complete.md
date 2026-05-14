# Prompt Auto-Completion Rules

Use this file when the user's request is short, vague, or beginner-style.
Do not ask the user to restate a long prompt. Silently expand the request into
the complete workflow needed for a contest-paper deliverable.

## General Rule

Treat short requests as shorthand, not as permission to skip work.

- “求解” means: analyze, model, solve, validate, generate needed artifacts, and
  update `paper/main.tex`.
- “写论文” means: trace results first, then write deep prose into
  `paper/main.tex`.
- “检查” means: review task coverage, modeling depth, traceability,
  validation, figures/tables, and paper readiness.
- “只做第 x 问” limits the scope to that subquestion, but does not reduce
  modeling depth, validation, code traceability, figures, or paper writing.
- Do not print the expanded prompt unless the user explicitly asks to see it.

## Intent Expansion Map

| User says | Interpret as | Read next |
| --- | --- | --- |
| 帮我求解第一问 / 做 Q1 / 完成第 1 问 | Full single-question delivery for that subquestion | `references/task-modes.md`, `references/problem-routing.md` |
| 帮我做这题 / 求解整题 / 完成这道题 | Full-problem workflow | `references/workflow.md`, `references/stage-gates.md` |
| 帮我分析题目 / 怎么建模 / 给路线 | Problem parsing, data audit, and route comparison only | `references/problem-parsing.md`, `references/problem-routing.md` |
| 根据代码写论文 / 根据结果写论文 | Code-to-paper traceability and paper writing | `references/code-to-paper.md`, `references/paper-writing.md` |
| 帮我检查 / 审稿 / 看看哪里有问题 | Judge-style final review | `references/final-review.md`, `references/final-checklist.md` |
| 补图 / 画流程图 / 做技术路线图 | Figure and roadmap planning/generation | `references/figure-plan.md`, `references/technical-roadmap.md` |
| 快交了 / 时间不够 / 先救急 | Last-hours compression check | `references/task-modes.md` |

## Completed Prompt For “帮我求解第 x 问”

When the user asks to solve one subquestion, internally expand to:

1. Confirm the exact subquestion number and inspect only the required problem
   statement, attachments, existing data, code, tables, figures, and paper.
2. Parse what this subquestion asks, what data it depends on, what it must
   output, and which constraints, units, and hidden scoring points matter.
3. Create or update `modeling/qx_modeling_idea.md` before solving. It must
   include:
   - problem role and connection to other questions;
   - assumptions, variables, parameters, units, constraints, and boundaries;
   - baseline route, primary route, and fallback route;
   - beginner-readable derivation from problem wording to equations/criteria;
   - detailed code modeling process: data cleaning, sorting, grouping, unit
     conversion, variable mapping, loops/solver inputs and outputs, intermediate
     checks, failure handling, saved tables, saved figures, and paper outputs;
   - validation, sensitivity, or boundary-case plan;
   - figure plan and paper-writing plan.
4. Solve with reproducible code when calculation is needed. Save outputs under
   `src/`, `tables/`, `figures/`, and `results/`.
5. Reverse-check the executed code against the modeling idea. If the code
   differs from the initial idea, update the final modeling idea before writing
   the paper.
6. Write or update `results/validation_report.md` with headline number sources,
   validation evidence, solver status or feasibility checks, and limitations.
7. Write the current subquestion into `paper/main.tex` with deep prose:
   problem role, variables, assumptions, derivation, algorithm, result
   interpretation, validation, limitation, and handoff.
8. Run available checks before reporting completion.

## Completed Prompt For “帮我做这题”

When the user asks to solve the whole problem, internally expand to:

1. Parse the full problem and all attachments.
2. Audit data files, sheets, fields, units, missing values, duplicates, time
   ranges, and exclusions.
3. Build `problem/task_plan.json` and a route comparison.
4. For each subquestion, follow the single-question completed prompt.
5. Assemble `paper/main.tex` as one coherent paper, not a pile of fragments.
6. Write the abstract last from saved results and validation notes.
7. Run full validation checks before handoff.

## Completed Prompt For “帮我写论文”

When the user asks for paper writing, internally expand to:

1. Read existing code, result tables, figures, validation notes, and modeling
   idea files first.
2. Refuse to invent missing numbers. Mark blockers when a conclusion has no
   traceable source.
3. Write `paper/main.tex` with enough prose depth: mechanism, variables,
   equations, algorithm, result meaning, validation, and limitations.
4. Keep figures and tables limited to evidence. Do not let visuals replace
   explanation.
5. Check that abstract, body, captions, tables, figures, and validation notes
   agree.

## Completed Prompt For “帮我检查”

When the user asks for review, internally expand to:

1. Check task coverage and whether every requested output has a direct answer.
2. Check data audit, units, assumptions, model derivation, code traceability,
   saved tables, saved figures, and validation.
3. Check `paper/main.tex` for depth, consistency, figure/table balance,
   limitations, and source-backed numbers.
4. Lead with blocker findings and do not call the work complete if any P1 issue
   remains.

