# Expected Skill Behavior

Use these expectations for manual checks after skill updates.

## Full Problem

- Starts with problem decomposition, not model names.
- Inspects all data files/sheets before numeric claims.
- Gives exactly three routes and chooses primary/fallback routes.
- Builds a baseline before or beside the main model.
- Produces validation and sensitivity checks matched to task type.
- Keeps result numbers traceable through a registry or source references.

## Single Question

- Solves only the requested subquestion.
- Still includes scoring points, hidden constraints, three routes, baseline, model, validation, figures, and paper text.
- Notes dependencies on later questions without expanding them.

## Code To Paper

- Reads actual outputs first.
- Flags mismatches instead of silently rewriting numbers.
- Maps every headline value to a table, log, figure, equation, or explicit assumption.

## Roadmap

- Produces editable Mermaid/DOT/SVG source before bitmap output.
- Uses short labels and avoids invented methods.
- Includes caption and paper explanation.

## Final Review

- Leads with severity-ordered findings.
- Scores the first-prize gate 0-2.
- Marks incomplete if any item scores 0.
