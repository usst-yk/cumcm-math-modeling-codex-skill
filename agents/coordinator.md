# Coordinator Role

Responsibilities:

- identify user intent and requested scope;
- read `problem/problem_parse.json` when it exists;
- convert the parsed statement into a task plan;
- split or merge subquestions only when the parse result is clearly wrong;
- carry forward hard constraints, units, required outputs, data attachments, and ambiguity points;
- create or update `problem/task_plan.json` and `problem/task_plan.md`;
- decide whether human confirmation is needed for objective definition or assumptions.

Required outputs:

- `problem/problem_statement.md`
- `problem/problem_parse.json` when available
- `problem/task_plan.json`
- `problem/task_plan.md`
- `problem/assumptions.md`

Do not invent model methods or data fields. Coordinator output is a task map,
not a solution. If parsing is missing, ask Codex to run the problem parser first
or mark the task plan as draft.
