# Progress Dashboard

Use this reference for full-project, supervised, or long-running CUMCM work
when the user needs to see status without reading logs.

## Principle

The dashboard is a static local handoff, not a Web platform. Keep lean mode
clean: do not create `logs/progress.jsonl` or `progress.html` unless the user
asks for a complete project, supervised workflow, dashboard, or long-running
status tracking.

## Event Log

Use `scripts/update_progress.py` to append JSONL events:

```bash
python scripts/update_progress.py --stage modeling --status working --worker codex --message "Q1 model card drafted"
```

Recommended fields:

- `stage`: parser, coordinator, background, data, modeling, solving,
  validation, writing, abstract, review, handoff.
- `status`: todo, working, done, revise, blocked, skipped.
- `question`: q1, q2, q3, or all.
- `worker`: human or agent name.
- `message`: short reason or result.
- `files`: comma-separated paths created or updated.

## Static HTML

Render the dashboard with:

```bash
python scripts/update_progress.py --render
```

The dashboard should show:

- overall stage completion;
- per-question status;
- latest events and blocker messages;
- generated files with local relative links;
- result registry status when available;
- supervisor revise/block decisions when available.

## Status Source Priority

When sources disagree, trust in this order:

1. explicit `blocked` or `revise` events in `logs/progress.jsonl`;
2. verified/blocked status in `results/result_registry.csv`;
3. `problem/task_plan.json` status fields;
4. existence of files in `figures/`, `tables/`, `paper/sections/`;
5. informal notes.

Do not let the dashboard become the fact source. Paper numbers still come from
code output, tables, figures, problem facts, or `results/result_registry.csv`.
