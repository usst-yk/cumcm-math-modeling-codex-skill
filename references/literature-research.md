# Literature Research

Use literature research only when it improves modeling choices, assumptions,
metrics, or citations. In contest time, the goal is useful evidence, not a
long survey.

## When To Research

Research before modeling if the problem involves:

- domain standards, policy rules, engineering constants, medical or safety
  thresholds, logistics rules, or public benchmarks;
- unfamiliar mechanism where assumptions would otherwise be guesswork;
- methods that need a real citation or accepted evaluation metric;
- background numbers that may appear in the introduction, assumptions, or
  validation baseline.

Skip or keep minimal when the problem statement and attached data are enough to
define all variables, constraints, and metrics.

## Source Priority

Prefer:

1. official standards, government or organizer documents, data dictionaries;
2. textbooks, solver/package documentation, classic method references;
3. recent peer-reviewed papers or reputable technical reports;
4. official websites of relevant institutions.

Avoid unsourced blogs, copied paper fragments, unverifiable lecture slides, and
AI-generated citations.

## Extraction Template

For each useful source, record:

- `source`: title, author/organization, year/date, URL/DOI;
- `fact`: the exact background fact or method detail needed;
- `use`: variable, parameter, constraint, metric, assumption, baseline, or
  citation;
- `confidence`: high, medium, low;
- `limits`: scope mismatch, outdated date, missing unit, or not directly
  applicable.

## Output Rules

- Keep notes short enough that Modeler can use them directly.
- Cite only sources actually used in the paper or model explanation.
- Mark unverifiable items as `待真实文献补充` instead of polishing them.
- Do not convert literature facts into problem data unless the problem allows
  external parameters and the paper states the assumption clearly.
