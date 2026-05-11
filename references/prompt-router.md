# Prompt Router From `examples/README.md`

Use this file when the user gives a broad request. Classify the request into one
prompt family from `examples/README.md`, then execute that workflow. Do not ask
the user to copy the prompt again unless the task is genuinely ambiguous.

## Route Table

| User state | Execute as if user chose |
| --- | --- |
| New problem, attachments, "先看看题" | Step 1: problem parse and attachment audit |
| Wants routes, "怎么建模", "思路" | Step 2/3: route comparison with baseline, primary, fallback |
| Team division or per-question work | Step 2/5: assign subquestions and synchronization points |
| "做第 x 问" | Step 5: single subquestion, complete paper-ready section |
| "模型不够细" | Step 4: four-round modeling deepening before code |
| "写代码/求解/跑结果" | Step 6: solve from `modeling/qx_modeling_idea.md` |
| "图太少/路线图" | Step 7: GPT-image flowchart plus result and validation figures |
| "根据结果写论文" | Step 8: paper body from code, tables, figures, and registry |
| "统一口径/摘要不一致" | Step 9: symbols, assumptions, numbers, figures, conclusions |
| "验证/敏感性" | Step 10: baseline, feasibility, sensitivity, residual/error checks |
| "写摘要" | Step 11: write abstract last after body and figures are stable |
| "终审/补救/上海市获奖" | Step 12: judge review, severity-ordered fixes |
| "直接完成整题" | Step 13 only as emergency; still run the per-question contract |

## Automatic Full-Problem Expansion

For a full problem, never treat Step 13 as permission to be shallow. Expand it
internally into:

1. parse statement and attachments;
2. compare three routes;
3. for each subquestion, write modeling idea before code;
4. solve and generate tables/Chinese figures;
5. reverse-check code against the modeling idea;
6. write the subquestion section into `paper/main.tex`;
7. after all subquestions, unify symbols and write abstract last.

## Per-Question Agent Pattern

When subagents are available and the user asks for depth, prize level, or
multi-round rework:

- Spawn one reviewer per active subquestion after the first draft artifacts
  exist.
- Give each reviewer one question and read-only scope.
- Ask for missing variables, assumptions, formulas, result tables, figures,
  validation, and paper paragraphs.
- Main agent integrates all findings and keeps `paper/main.tex` coherent.

## Output Contract

Every solved subquestion must leave:

- `modeling/qx_modeling_idea.md`
- at least one result table under `tables/`
- at least one model-flow figure and one result/validation figure under
  `figures/`
- traceable values in `results/result_registry.csv`
- a paper-ready section in `paper/main.tex`

If time or data is insufficient, mark the limitation explicitly in the paper and
final response; do not pretend the model is optimal or fully validated.
