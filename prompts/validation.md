# Validation Prompt Expansions

Use this file when the user asks for validation, sensitivity analysis, error
analysis, baselines, reliability checks, or proof that results are credible.

## Completed Prompt: Validation, Sensitivity, And Baseline

Trigger examples:

- 补验证
- 做敏感性分析
- 加误差分析
- 没有基线
- 怎么证明结果可靠
- 结果可靠吗

Internally expand to:

1. Identify task type and choose matching checks:
   - prediction: naive baseline, train/test or rolling validation, residuals,
     MAE/RMSE/MAPE/R2, and error explanation;
   - optimization: feasibility, solver status, constraint violation, baseline
     scheme, sensitivity, and small exact case when possible;
   - evaluation/ranking: indicator direction, normalization, weight
     perturbation, rank stability, and alternative weighting;
   - simulation: boundary case, conservation, parameter sensitivity, repeated
     runs when stochastic, and step-size or convergence check;
   - geometry/physics: unit check, limiting case, threshold margin, boundary
     event check, and parameter scale check;
   - classification/clustering: confusion matrix, stability, cluster meaning,
     holdout or perturbation.
2. Define what each check proves and what it cannot prove.
3. Save validation tables/figures under `tables/`, `figures/`, and
   `results/validation_report.md`.
4. Link every validation conclusion to a source table, figure, metric, solver
   log, or code output.
5. Explain in `paper/main.tex` what the check proves and what it does not prove.
6. If validation fails, record limitation and fallback route instead of hiding
   the failure.

## Sensitivity Design

Choose only meaningful perturbations:

- parameters estimated from data;
- thresholds or weights set by assumptions;
- resource limits, capacities, costs, speeds, or time windows;
- initial conditions or boundary values;
- stochastic seeds or scenario probabilities.

For each perturbation, state:

- baseline value and source;
- perturbation range and reason;
- affected result;
- stability conclusion;
- whether the paper claim must be weakened.

## Baseline Design

Every baseline must be simple enough to explain and close enough to the task to
be fair.

- Prediction: last value, moving average, seasonal naive, or simple regression.
- Optimization: current scheme, greedy scheme, nearest-neighbor route, equal
  allocation, or relaxed bound.
- Evaluation: equal weights, entropy weights, expert weights, or single-index
  ranking.
- Simulation/physics: limiting case, analytical special case, or simplified
  numerical model.

Do not use a weak straw baseline only to make the main model look good.
