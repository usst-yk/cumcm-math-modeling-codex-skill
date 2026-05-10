# Final Checklist

Use this reference before final handoff or when the user asks for 审稿, 查错, 评委视角, or 最终交付检查.

When project artifacts exist, run `scripts/validate_results.py` from the project root or pass `--project <project-dir>` before final handoff. Treat P1 findings as blockers unless the user explicitly accepts the limitation.

## Severity-Ordered Review

Lead with findings ordered by severity:

- P0: answer is wrong, unsupported, violates a hard constraint, or uses uninspected required data.
- P1: major validation, traceability, or reproducibility gap that could cost awards.
- P2: unclear exposition, weak figure/table support, formatting, or completeness issue.

## First-Prize Score Gate

Score each item 0-2:

| Item | 0 | 1 | 2 |
| --- | --- | --- | --- |
| 题意覆盖 | Missing requested output | Covers output but misses constraints | Covers all subquestions, constraints, units |
| 数据审计 | Files/sheets unchecked | Basic columns checked | Full inventory, sheets, missingness, units, exclusions |
| 基线模型 | None | Descriptive only | Analytical/simplified/hand-checkable baseline |
| 主模型 | Vague method names | Partial variables/objective | Complete variables, objective/criterion, constraints |
| 求解可靠性 | No reproducible path | Code exists but diagnostics weak | Reproducible code, seed/status/feasibility checks |
| 验证 | None | One weak check | Task-appropriate error/feasibility/sensitivity/robustness |
| 图表 | Decorative or missing | Shows result but weak caption | Supports conclusion, named, readable, reproducible |
| 论文一致性 | Numbers conflict | Mostly consistent | Abstract, body, tables, figures, appendix agree |

If any item is 0, mark the deliverable incomplete and list the blocker.

## Artifact Checklist

For lean single-question work, only check files that were actually needed for
that question. Do not require empty templates, logs, or appendices.

For full projects, check:

- TeX or requested paper format exists.
- PDF compiled or compile error reported.
- Main code path and run command exist.
- Input data notes or data inventory exist.
- Generated tables and figures use stable names.
- Figure captions explain what conclusion each figure supports.
- Appendix code lists main script, inputs, outputs, dependencies, seed, and command.
- Result registry agrees with abstract, conclusion, tables, figures, and captions.
