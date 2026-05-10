# Benchmark Rebuild Workflow

Use this when the user asks to redo a benchmark, rebuild a real case, or test
the skill from scratch.

## Scope

Rebuild means do not polish old results. Preserve only:

- official problem statement and extracted text in `problem/`;
- raw attachments or reconstructed benchmark data in `data/raw/`;
- solver scripts that are part of the benchmark method, unless the task asks to
  rewrite code too.

Delete generated outputs before rerunning:

- `figures/`;
- `tables/`;
- `results/`;
- `paper/`.

Then recreate only the files needed by the rebuild.

## Required Order

1. Re-parse the problem statement with `scripts/problem_parser.py`.
2. Rebuild or manually confirm `problem/task_plan.json`.
3. Re-run data audit with `scripts/data_profile.py`.
4. Write or update route comparison and modeling rounds. Follow
   `examples/README.md`: route choice, four rounds of modeling, then solve.
5. Re-run deterministic solving scripts.
6. Rebuild `results/result_registry.csv`, `results/validation_report.md`, and
   any benchmark findings.
7. Write TeX paper body from results, not from the old paper.
8. Write the abstract last from registry and validated body.
9. Compile `paper/main.tex`.
10. Run `scripts/validate_results.py --mode full` and `scripts/run_skill_evals.py`.

## Hard Rules

- Do not use a previous paper as the base when the user asks to redo from
  scratch.
- Do not let solver scripts regenerate Markdown paper artifacts.
- If the parser produces sparse or wrong task plans, fix the parser when the
  error is general; otherwise record an explicit manual-confirmation step.
- If the rebuilt paper is thinner than the previous paper, mark the rebuild
  incomplete.
