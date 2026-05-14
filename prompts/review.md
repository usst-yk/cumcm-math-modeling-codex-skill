# Review Prompt Expansions

Use this file for judge-style review, award-readiness checks, final submission
checks, and emergency rescue mode.

## Completed Prompt: Review, Award Readiness, Or Final Check

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

## Review Severity

- P1: missing answer, unsupported key number, impossible constraint, broken code,
  missing `paper/main.tex`, major contradiction, or no validation for a core
  conclusion.
- P2: weak derivation, vague variables, missing baseline, figure/table mismatch,
  poor result explanation, or abstract/body inconsistency.
- P3: wording, formatting, naming, minor figure style, or optional appendix
  improvement.

## Completed Prompt: Emergency Mode

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

Emergency mode may compress scope, but it must not fabricate confidence. A
submittable imperfect paper is better than a confident paper with unsupported
numbers or contradicted results.
