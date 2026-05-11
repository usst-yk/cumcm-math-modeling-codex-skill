# Validation

Use this reference after code has generated outputs and before writing final paper conclusions.

## Minimum Checks By Task Type

| Task | Required validation |
| --- | --- |
| Prediction/fitting | baseline comparison, train/test or rolling validation when possible, residual inspection, MAE/RMSE/MAPE/R2 as appropriate |
| Optimization/scheduling | solver/search status, objective value, constraint violation or feasibility table, baseline scheme comparison, sensitivity to key parameters; heuristic/iterative searches must save an iteration trace |
| Evaluation/ranking | indicator direction check, normalization check, weight perturbation, ranking stability, alternative weighting comparison |
| Simulation/propagation | boundary cases, parameter sensitivity, repeated stochastic runs, peak/final-state interpretation |
| Classification | confusion matrix, accuracy/recall/F1 or ROC-AUC, threshold rationale, error case analysis, feature or rule interpretation |
| Clustering | silhouette/CH/DBI or stability, cluster interpretation, sensitivity to K/parameters |

## Failure Recovery

## Optimization Evidence

For grid search, coordinate search, genetic algorithms, simulated annealing,
particle swarm, or other non-exact solvers:

- save an iteration/search trace with decision variables, objective value,
  accepted/rejected action, and stopping status;
- save a feasibility table or include feasibility columns in the result table:
  capacity, time window, boundary order, group size, target rate, or other
  problem constraints;
- compare against a simple baseline;
- write the conclusion as "current candidate set / current parameters /
  feasible preferred scheme" unless global optimality is certified.

## Screening Classification Evidence

For medical, safety, or screening-style classification:

- do not report only accuracy;
- include ROC-AUC, confusion matrix, sensitivity, specificity, and threshold
  selection rule;
- when cross-validation is used, select thresholds inside training folds and
  evaluate on held-out folds to avoid leakage;
- if output is a risk score, include Brier score or calibration evidence when
  sample size allows;
- use screening language, not diagnosis language.

When code fails:

1. inspect the traceback;
2. fix the smallest local error;
3. rerun the same command;
4. if it fails twice, switch to a justified smaller-scope fallback model or
   produce a reproducible blocker report;
5. never write final numerical conclusions from failed code.

Record failures in `results/validation_report.md`:

```markdown
## Error 001
Command:
Traceback:
Cause:
Fix:
Rerun result:
Remaining risk:
```

## Validation Report

Write `results/validation_report.md` with:

- model or script checked;
- metric or feasibility item;
- result;
- pass/fail/blocker status;
- source file;
- consequence for the paper conclusion.

For optimization rows also record objective value, feasibility status, baseline
comparison, trace file, sensitivity item, and optimality limitation. For
screening/classification rows also record threshold, ROC-AUC, sensitivity,
specificity, confusion matrix source, and cross-validation or calibration status.
