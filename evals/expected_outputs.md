# Expected Skill Behavior

Use these expectations for manual checks after skill updates.

## Quality Rubric

- Use `evals/modeling_quality_rubric.json` for 0-2 scoring.
- Use `references/first-prize-rubric.md` when the user asks whether a route or
  paper is close to first-prize level.
- Use `references/official-benchmark.md` and `evals/official_cases/` as
  official-source anchors, not as copied answer content.
- A usable answer should pass problem coverage, route comparison, baseline,
  data/units, model formulation, validation, figures, traceability, and
  paper-readiness.
- If any criterion is 0, the answer is incomplete even when all files exist.

## Full Problem

- Starts with problem decomposition, not model names.
- Inspects all data files/sheets before numeric claims.
- Gives exactly three routes and chooses primary/fallback routes.
- Builds a baseline before or beside the main model.
- Produces validation and sensitivity checks matched to task type.
- Keeps result numbers traceable through saved tables, figures, code outputs, or validation notes.
- For each subquestion, records baseline, primary, fallback route, and minimum
  validation requirements.

## Single Question

- Solves only the requested subquestion.
- Still includes scoring points, hidden constraints, three routes, baseline, model, validation, figures, and paper text.
- Keeps the file set focused: code, result tables, Chinese figures,
  and requested paper text. This must not shorten analysis, modeling, solving,
  validation, or requested paper sections.
- Notes dependencies on later questions without expanding them.

## Code To Paper

- Reads actual outputs first.
- Flags mismatches instead of silently rewriting numbers.
- Maps every headline value to a table, log, figure, equation, or explicit assumption.

## Roadmap

- Produces a GPT-image technical roadmap or model flowchart.
- Uses short labels and avoids invented methods.
- Includes caption and paper explanation.

## Final Review

- Leads with severity-ordered findings.
- Scores the first-prize gate 0-2.
- Marks incomplete if any item scores 0.
