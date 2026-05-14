# Prompt Auto-Completion Rules

This is the compatibility entry for short beginner prompts. Do not load every
prompt rule by default. For terse requests, read `prompts/intent-map.md` first,
then load only the matching task file.

## Core Principle

Short prompt means shorthand, not low standard.

- Do not ask the user to rewrite a long prompt.
- Do not lower modeling depth because the prompt is short.
- Do not treat “求解” as only writing code or only reporting a number.
- Do not treat “写论文” as polishing text before checking result sources.
- Do not treat “优化模型” as cosmetic method replacement.
- Do not treat “直接推导” as permission to skip assumptions, variables,
  constraints, validation, or paper writing.
- Do not print the expanded prompt unless the user explicitly asks to see it.

Every useful output should still support `paper/main.tex`.

## Read Next

| Short request type | Load |
| --- | --- |
| Intent detection and routing | `prompts/intent-map.md` |
| 求解第一问 / 做整题 / 完成 Qx | `prompts/solve.md` |
| 还有哪些模型 / 直接推导 / 模型更深 / 优化模型 | `prompts/modeling.md` |
| 修改摘要 / 写论文 / 图表太多 / 根据代码写正文 | `prompts/writing.md` |
| 补验证 / 做敏感性 / 没有基线 / 结果可靠吗 | `prompts/validation.md` |
| 帮我检查 / 能不能国一 / 快交了 | `prompts/review.md` |

## Covered Completed Prompts

The detailed rules now live in smaller files:

- `prompts/solve.md`: Solve One Subquestion, Solve Full Problem.
- `prompts/modeling.md`: Candidate Models, Direct Derivation, Deeper
  Mathematical Model, Improve Or Optimize Existing Model.
- `prompts/writing.md`: Abstract Revision, Paper Writing Or Rewriting, Figure,
  Flowchart, Or Roadmap, Code Or Result To Paper.
- `prompts/validation.md`: Validation, Sensitivity, And Baseline.
- `prompts/review.md`: Review, Award Readiness, Or Final Check, Emergency Mode.

## Default Expansion

When the user gives a short request, silently expand it into:

1. inspect the local problem, data, modeling, code, results, figures, and
   `paper/main.tex`;
2. identify the target subquestion or stage;
3. create or update the relevant `modeling/qx_modeling_idea.md`;
4. solve, validate, write, or review according to the matching prompt file;
5. keep numbers traceable through saved tables, figures, validation notes, and
   code outputs;
6. update `paper/main.tex` whenever the work produces paper-facing content;
7. run available checks before reporting completion.
