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
python scripts/update_progress.py --stage validation --status revise --event-type supervisor_gate --owner solver --blocker "result registry missing headline value" --retry-reason "rerun Q2 sensitivity table" --evidence "results/validation_audit.md"
python scripts/update_progress.py --stage review --status done --score "16/20" --rubric-status "no zero item; validation=2; traceability=2" --open
```

Appending an event renders `progress.html` by default. Use `--no-render` only
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

Full project initialization creates `logs/progress.jsonl` and `progress.html`
at startup:

```bash
python scripts/init_cumcm_project.py cumcm_2026_A --full
python scripts/init_cumcm_project.py cumcm_2026_A --full --open
```

## Static HTML

Render the dashboard with:

```bash
python scripts/update_progress.py --render
python scripts/update_progress.py --render --open
python scripts/update_progress.py --watch --open
```

Use `--watch --open` during supervised multi-agent work when several agents may
append or regenerate logs. The watcher re-renders the dashboard whenever the log
changes; the browser refresh then makes the new step visible.

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

1. explicit `blocked` or `revise` events in `logs/progress.jsonl`;
2. verified/blocked status in `results/result_registry.csv`;
3. `problem/task_plan.json` status fields;
4. existence of files in `figures/`, `tables/`, and `paper/main.tex`;
5. informal notes.

Do not let the dashboard become the fact source. Paper numbers still come from
code output, tables, figures, problem facts, or `results/result_registry.csv`.
