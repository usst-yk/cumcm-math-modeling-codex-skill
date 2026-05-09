# Validation

Use this reference after code has generated outputs and before writing final paper conclusions.

## Minimum Checks By Task Type

| Task | Required validation |
| --- | --- |
| Prediction/fitting | baseline comparison, train/test or rolling validation when possible, residual inspection, MAE/RMSE/MAPE/R2 as appropriate |
| Optimization/scheduling | solver status, objective value, constraint violation table, baseline scheme comparison, sensitivity to key parameters |
| Evaluation/ranking | indicator direction check, normalization check, weight perturbation, ranking stability, alternative weighting comparison |
| Simulation/propagation | boundary cases, parameter sensitivity, repeated stochastic runs, peak/final-state interpretation |
| Classification | confusion matrix, accuracy/recall/F1, error case analysis, feature or rule interpretation |
| Clustering | silhouette/CH/DBI or stability, cluster interpretation, sensitivity to K/parameters |

## Failure Recovery

When code fails:

1. inspect the traceback;
2. fix the smallest local error;
3. rerun the same command;
4. if it fails twice, simplify the model or produce a reproducible blocker report;
5. never write final numerical conclusions from failed code.

Record failures in `logs/error_log.md`:

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
