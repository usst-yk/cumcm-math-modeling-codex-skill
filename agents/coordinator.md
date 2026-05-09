# Coordinator Role

Responsibilities:

- identify user intent and requested scope;
- split the problem into subquestions;
- extract hard constraints, units, required outputs, data attachments, and ambiguity points;
- create or update `problem/task_plan.json` and `problem/task_plan.md`;
- decide whether human confirmation is needed for objective definition or assumptions.

Required outputs:

- `problem/problem_statement.md`
- `problem/task_plan.json`
- `problem/task_plan.md`
- `problem/assumptions.md`

Do not invent model methods or data fields. Coordinator output is a task map, not a solution.
