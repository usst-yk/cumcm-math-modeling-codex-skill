# Task Routing

Use this file to decide which references and scripts to load. Keep user-facing
communication natural; do not expose commands unless the user asks.

## Common Modes

| User asks for | Use |
| --- | --- |
| Start a new problem or project | `scripts/init_cumcm_project.py`; explain the workspace in plain language |
| Full CUMCM problem solving | `references/workflow.md`, `references/problem-routing.md`, `references/stage-gates.md`, `references/scoring-checklist.md` |
| Read and decompose a problem | `scripts/build_task_plan.py`, `agents/coordinator.md`, `references/problem-routing.md` |
| Only one subquestion | `references/contest-modes.md`, `references/problem-routing.md`, `references/correctness-ladder.md` |
| Single-question paper section | `references/contest-modes.md`, `references/paper-writing.md`, `references/result-tracking.md` |
| Data attachments present | `scripts/data_profile.py`, `references/data-audit.md` |
| Choose a model | `agents/modeler.md`, `references/problem-routing.md`, `references/modeling-toolbox.md` |
| Write or fix solving code | `agents/coder.md`, `references/python-matlab-guide.md` |
| Validate results | `references/validation.md`, `scripts/validate_results.py` when project artifacts exist |
| Code/tables/figures to paper | `references/code-to-paper.md`, `references/result-tracking.md`, `agents/writer.md` |
| Abstract, conclusion, or polishing | `references/paper-writing.md`, `references/scoring-checklist.md`, `references/result-tracking.md` |
| Technical roadmap or model flowchart | `references/technical-roadmap.md`, `scripts/make_roadmap_svg.py` |
| Figure standards | `references/figure-standards.md`, optionally `scripts/make_paper_figures.py` |
| Final judge review | `references/final-review.md`, `references/final-checklist.md`, `agents/reviewer.md` |
| Safety or anti-fabrication concern | `references/safety-rules.md` |

## Routing Principles

- For beginners, prefer direct natural-language guidance over showing internal
  file names.
- For full problems, always work subquestion by subquestion.
- For single-question requests, do not expand into a full-paper workflow unless
  the user asks.
- For paper text with numbers, use the result registry before writing final
  claims.
- For route design, give three routes and choose a primary route plus fallback.
- For image-like roadmap requests, create editable source first; use image
  generation only when the user explicitly wants a designed visual.

