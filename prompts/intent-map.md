# Prompt Intent Map

Use this file whenever the user's request is short, vague, beginner-style, or
missing contest-paper details. Silently expand the request into the complete
CUMCM workflow needed for the intended stage.

## Core Principle

Short prompt means shorthand, not low standard.

- Do not ask the user to write a long prompt.
- Do not lower modeling depth because the prompt is short.
- Do not skip traceability, validation, or paper writing.
- Ask a question only when the problem statement, target subquestion, or
  required data is genuinely missing and cannot be inferred from local files.

## Intent Detection

Classify the user request along four axes:

1. **Scope**: full problem, one subquestion, existing code/result, existing
   paper, or planning only.
2. **Stage**: parse, route, derive, deepen model, solve, validate, write,
   revise, review, or emergency.
3. **Artifact target**: `modeling/`, `src/`, `tables/`, `figures/`, `results/`,
   `paper/main.tex`, or all of them.
4. **Quality target**: ordinary completion, first-prize-oriented completion,
   stronger math, deeper prose, fewer figures, or final submission check.

Verb priority:

- “求解/完成/做” -> solve workflow.
- “推导/公式怎么来/能不能直接推” -> derivation workflow.
- “模型更深/高级一点/数学性不够” -> model-deepening workflow.
- “优化模型/改进模型/模型太简单” -> model-improvement workflow.
- “有哪些模型/用什么模型/模型选择” -> candidate-model workflow.
- “摘要/改摘要/重写摘要” -> abstract workflow.
- “论文/正文/写作/润色/图表太多” -> paper-writing workflow.
- “验证/敏感性/误差/基线” -> validation workflow.
- “图/流程图/路线图” -> figure workflow.
- “检查/审稿/冲奖/国一” -> review and award-readiness workflow.
- “快交了/时间不够/先救急” -> emergency workflow.

## Intent Expansion Map

| User says | Expand to | Read next |
| --- | --- | --- |
| 帮我求解第一问 / 做 Q1 / 完成第 1 问 | Full single-question delivery | `prompts/solve.md`; `references/task-modes.md`, `references/problem-routing.md` |
| 帮我做这题 / 求解整题 / 完成这道题 | Full-problem workflow | `prompts/solve.md`; `references/workflow.md`, `references/stage-gates.md` |
| 帮我分析题目 / 题目怎么做 / 给路线 | Parse, audit, and route comparison | `references/problem-parsing.md`, `references/problem-routing.md` |
| 还有哪些模型可以考虑 / 用什么模型好 | Candidate model comparison | `prompts/modeling.md`; `references/method-cards.json`, `references/method-library.md` |
| 能不能直接推导 / 直接推公式 / 公式怎么来的 | Beginner-readable derivation | `prompts/modeling.md`; `references/modeling-derivation-standard.md` |
| 建立更深的模型 / 数学性不够 / 高级一点 | Mechanism and advanced-model deepening | `prompts/modeling.md`; `references/advanced-math-modeling.md` |
| 优化模型 / 改进模型 / 现在模型太简单 | Model improvement with baseline and validation | `prompts/modeling.md`; `references/correctness-ladder.md` |
| 优化代码 / 跑得太慢 / 求解器不好 | Implementation improvement without silent claim changes | `agents/coder.md`, `references/code-to-paper.md` |
| 修改摘要 / 重写摘要 / 摘要太差 | Final abstract rewrite from traceable results | `prompts/writing.md`; `agents/abstract_writer.md` |
| 修改论文 / 论文太浅 / 正文太少 | Deep paper rewriting | `prompts/writing.md`; `references/paper-writing.md` |
| 图表太多 / 表太多 / 图片堆砌 | Figure/table discipline and prose expansion | `prompts/writing.md`; `references/figure-plan.md` |
| 补验证 / 做敏感性 / 加误差分析 | Task-matched validation | `prompts/validation.md`; `references/validation.md` |
| 根据代码写论文 / 根据结果写论文 | Code-to-paper traceability | `prompts/writing.md`; `references/code-to-paper.md` |
| 补图 / 画流程图 / 技术路线图 | Figure and roadmap planning | `prompts/writing.md`; `references/figure-plan.md` |
| 帮我检查 / 审稿 / 看哪里有问题 | Judge-style final review | `prompts/review.md`; `references/final-review.md` |
| 看看能不能国一 / 冲奖 / 一等奖标准 | Award-readiness review | `prompts/review.md`; `references/first-prize-workflow.md` |
| 快交了 / 时间不够 / 先救急 | Last-hours compression check | `prompts/review.md`; `references/task-modes.md` |

## Default Expansion Rules

- If the user mentions a subquestion, stay scoped to that subquestion unless
  shared variables or previous results must be checked.
- If the user says only “帮我求解第一问”, still deliver modeling, code,
  validation, figures/tables, result traceability, and `paper/main.tex`.
- If the user says only “修改摘要”, first check body results and validation; do
  not write unsupported abstract numbers.
- If the user says only “优化模型”, identify the weakness before changing the
  method; do not replace a working model with decorative complexity.
- If the user says only “论文太差”, deepen prose and reduce figure/table
  dominance instead of adding more charts.
- If multiple intents appear, choose the one closest to the user's main verb
  and preserve downstream artifacts that must stay consistent.

## When To Ask The User

Ask only when one of these is missing and cannot be inferred:

- the problem statement or target file;
- which subquestion is requested;
- required data attachments;
- whether to modify an existing paper or start a new one;
- whether a destructive rebuild is allowed.

Do not ask the user to choose among routine implementation details. Choose the
most reproducible, contest-appropriate route and continue.
