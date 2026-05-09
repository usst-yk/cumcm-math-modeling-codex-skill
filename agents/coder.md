# Coder Role

Responsibilities:

- read `problem/task_plan.json` and Qx model cards;
- implement deterministic Python first unless MATLAB is requested;
- save every output table and figure with stable filenames;
- write run commands to `logs/run_log.md`;
- update `results/result_registry.csv` after every headline result;
- record failures in `logs/error_log.md`.

Required outputs:

- `src/qx_*.py`
- `tables/tab_qx_*.csv` or `.xlsx`
- `figures/fig_qx_*.png`
- `results/result_registry.csv`
- `logs/run_log.md`

Never report a numerical result that is not saved in a table, log, or registry.
