# Code To Paper

Use this reference when code, logs, tables, figures, or notebooks already exist.

## Workflow

1. Inventory outputs: list generated CSV/XLSX/JSON/log/figure files and modification times.
2. Read the actual output tables or logs before writing result text.
3. Create or update a result registry with `scripts/result_registry.py`.
4. Map each headline number to one source: output file, equation, problem condition, or explicit assumption.
5. Write model establishment, solution, result analysis, validation, and captions using only traceable outputs.
6. If code and existing paper text disagree, flag the inconsistency and use the saved output as the default source of truth unless the user says otherwise.

## Paper Text Pattern

For each subquestion:

- Model object: what is being predicted, optimized, evaluated, classified, or simulated.
- Input and preprocessing: only the steps that affect the model.
- Core equations or objective/constraints.
- Algorithm and parameters.
- Results with source table/figure.
- Validation, sensitivity, or feasibility check.
- Limitation if validation is missing.

## Common Failure Modes

- Copying numbers from memory instead of outputs.
- Writing "计算得到" when the output file does not contain the value.
- Captions describing trends not visible in the figure.
- Abstract values differing from tables.
- Appendix run command missing dependencies, seed, or input path.
