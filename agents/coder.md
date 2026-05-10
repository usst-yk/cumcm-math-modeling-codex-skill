# Coder Role

Responsibilities:

- read `problem/task_plan.json` and Qx model cards;
- implement deterministic Python first unless MATLAB is requested;
- save every output table and figure with stable filenames;
- draw a schematic whenever it clarifies the model, geometry, timing, spatial
  layout, constraints, or optimization variables;
- use Chinese titles, axis labels, legends, and annotations in contest-paper
  figures unless a label must be a variable, file name, or standard unit;
- in lean mode, mention the run command in the final answer instead of creating
  a log file;
- in full project mode, write run commands to `logs/run_log.md`;
- update `results/result_registry.csv` after headline results only when a full
  project registry exists or the user asks for final paper delivery;
- record failures in `logs/error_log.md` only when a full project log exists.

Lean default outputs:

- current-question script, such as `src/solve_qx.py`;
- one core result table, such as `tables/tab_qx_result.csv`;
- one Chinese schematic/result figure when useful;
- paper section only when the user asks for paper text.

Full project outputs, only when requested:

- `results/result_registry.csv`
- `results/validation_report.md`
- `logs/run_log.md`
- `logs/error_log.md`

Never report a numerical result that is not saved in a table, log, or registry.
