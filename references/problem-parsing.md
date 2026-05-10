# Problem Parsing

Use this reference before modeling any CUMCM problem statement. Parsing is a
separate stage from modeling: it extracts task facts, required outputs, risks,
and attachment dependencies without choosing methods.

## Required Parse Items

For the full problem and for each subquestion, identify:

- subquestion split: `Q1`, `Q2`, `Q3`, etc.;
- input data: attachment files, sheets, tables, fields, and provided constants;
- required outputs: forecast values, rankings, decisions, policies, diagrams,
  tables, proofs, or written explanations requested by the problem;
- decision object: what is predicted, optimized, evaluated, classified,
  scheduled, allocated, simulated, or explained;
- constraints: hard limits, feasibility conditions, comparison conditions,
  coverage requirements, and prohibitions;
- units and time range: units such as 元、件、吨、公里、小时、天、年, and ranges such
  as 2024-2030、连续 7 天、每小时、每个站点;
- attachment dependencies: which attachment or sheet each subquestion likely
  needs, and whether the dependency is explicit or inferred;
- implicit scoring points: baseline comparison, feasibility check, sensitivity,
  robustness, route comparison, reproducible code, and paper-readable figures;
- risk words: words that change interpretation or scoring.

## Risk Words

Treat these as high-priority parsing signals:

`全部`, `所有`, `每个`, `分别`, `连续`, `至少`, `不超过`, `不低于`, `最大`,
`最小`, `最优`, `预测`, `评价`, `排序`, `分类`, `调度`, `分配`, `规划`,
`约束`, `附件`, `表`, `给出`, `比较`, `检验`, `分析`, `灵敏度`.

When a risk word appears, record the sentence or phrase in the corresponding
subquestion. Do not silently smooth it into a generic task.

## Parser Outputs

`scripts/problem_parser.py` writes:

- `problem_parse.json`: machine-readable parse result;
- `problem_parse.md`: human-readable summary.

Expected top-level fields:

- `contest`
- `problem_id`
- `question_count`
- `attachments`
- `units`
- `time_ranges`
- `risk_words`
- `subquestions`
- `warnings`

Each subquestion should include:

- `id`
- `title`
- `text`
- `task_type`
- `input_data`
- `required_output`
- `decision_object`
- `constraints`
- `units`
- `time_ranges`
- `attachments`
- `implicit_scoring_points`
- `risk_words`
- `warnings`

## Handoff

After parsing, `scripts/build_task_plan.py` should prefer `problem_parse.json`
over direct regex counting. If parse fields are sparse, keep the task plan in
draft status and surface warnings instead of guessing.

