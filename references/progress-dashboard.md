# Progress Dashboard

Use this reference only for reading old benchmark notes. New projects should
record progress and gate failures in `results/validation_report.md`, not in a
separate dashboard.

## Principle

Do not create `logs/` or root-level `progress.html`.

## Event Log

If a local progress record is unavoidable for a legacy benchmark, keep it under
`results/`:

```bash
python scripts/update_progress.py --log results/progress.jsonl --html results/progress.html --stage modeling --status working --worker codex --message "Q1 model card drafted"
python scripts/update_progress.py --stage validation --status revise --event-type supervisor_gate --owner solver --blocker "result registry missing headline value" --retry-reason "rerun Q2 sensitivity table" --evidence "results/validation_audit.md"
python scripts/update_progress.py --stage review --status done --score "16/20" --rubric-status "no zero item; validation=2; traceability=2" --open
```

Appending an event renders `results/progress.html` by default. Use `--no-render` only
for batch imports. The HTML page includes a 5-second refresh tag, so an already
opened dashboard will update after each event.

Recommended fields:

- `stage`: parser, coordinator, background, data, modeling, solving,
  validation, writing, abstract, review, handoff.
- `status`: todo, working, done, revise, blocked, skipped.
- `question`: q1, q2, q3, or all.
- `worker`: human or agent name.
- `agent_role`: parser, coordinator, supervisor, modeler, solver, validator,
  writer, referee, packager, or other role.
- `event_type`: agent_start, gate_start, supervisor_gate, rework_done,
  recheck, artifact_generation, compile_done, package_done, etc.
- `owner`: role responsible for the next action after a revise/block event.
- `next_action`: concrete handoff instruction.
- `message`: short reason or result.
- `files`: comma-separated paths created or updated.
- `current_stage`: explicit dashboard stage when it differs from `stage`.
- `generated_files`: comma-separated files produced by the current event.
- `blocker` / `retry_reason`: visible reason for blocked, revise, or retry states.
- `score` / `rubric_status`: first-prize score gate or rubric review summary.
- `evidence`: comma-separated audit reports, registry rows, result tables, or
  figure files used to judge the event.

Old JSONL rows that only contain `stage`, `status`, `worker`, `message`, and
`files` remain valid. New fields are optional and are only displayed when set.

## Static HTML

Render the dashboard with:

```bash
python scripts/update_progress.py --log results/progress.jsonl --html results/progress.html --render
python scripts/update_progress.py --log results/progress.jsonl --html results/progress.html --render --open
```

Do not use `--watch` for ordinary modeling work.

Supervisor gate example:

```bash
python scripts/update_progress.py --stage validation --status revise \
  --event-type supervisor_gate --gate-id G5-validation --decision revise \
  --owner solver --issue "missing sensitivity figure" \
  --expected-fix "generate fig_q2_sensitivity.png and register it" \
  --target-rubric-item validation --evidence-needed "figure, registry row, validation audit"

python scripts/update_progress.py --stage validation --status done \
  --event-type recheck --gate-id G5-validation --decision pass \
  --owner supervisor --evidence "figures/fig_q2_sensitivity.png,results/validation_audit.md"
```

Only the `pass` recheck closes a failed gate.

The dashboard should show:

- overall stage completion;
- per-question status;
- latest events and blocker messages;
- generated files with local relative links;
- result registry status when available;
- supervisor revise/block decisions when available.

## Status Source Priority

When sources disagree, trust in this order:

1. explicit `blocked` or `revise` notes in `results/validation_report.md`;
2. verified/blocked status in `results/result_registry.csv`;
3. `problem/task_plan.json` status fields;
4. existence of files in `figures/`, `tables/`, and `paper/main.tex`;
5. informal notes.

Do not let the dashboard become the fact source. Paper numbers still come from
code output, tables, figures, problem facts, or `results/result_registry.csv`.
