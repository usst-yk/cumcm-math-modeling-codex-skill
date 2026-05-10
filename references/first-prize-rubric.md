# First-Prize-Oriented Modeling Rubric

This rubric is for judge-style review. It estimates whether a solution has the
ingredients of a strong CUMCM paper. It cannot guarantee an award.

Score each item 0-2:

| Item | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Problem coverage | Missing or misreads a subquestion | Covers most questions but leaves vague outputs | Every subquestion has direct input-model-output-validation mapping |
| Core mechanism | Method is chosen by name only | Mechanism is partly explained | Model captures the main physical, operational, statistical, or evaluation logic |
| Baseline | No baseline | Baseline exists but is not used | Baseline is used to justify improvement or sanity-check results |
| Model formulation | Variables/constraints unclear | Some variables and assumptions are clear | Variables, objective/equations, constraints, assumptions, and outputs are complete |
| Data and units | Data/sheets/units ignored | Data checked partially | All required files, sheets, units, time ranges, and exclusions are audited |
| Validation | No real validation | One weak check | Task-matched validation: feasibility, error metric, sensitivity, boundary case, or stability |
| Robustness | Single fragile result | Mentions uncertainty only | Tests key parameters or scenarios and explains result stability |
| Figures | Few or decorative figures | Figures show results but not mechanism | Chinese schematic, result, and validation figures directly support conclusions |
| Traceability | Numbers cannot be traced | Some key numbers traceable | Every headline number traces to data, table, code output, or registry |
| Paper readiness | Chat-like or placeholder text | Mostly usable but inconsistent | Judge-facing Chinese prose with consistent abstract, body, tables, figures, and appendix |

## Gate Rules

- If any item scores 0, mark the answer incomplete.
- If core mechanism, validation, or traceability scores below 2, do not call the
  work "first-prize level".
- Strong solutions usually score at least 16/20 and have no 0 item.

## Official Benchmark Use

When the user asks whether a solution is high-level, compare against
`references/official-benchmark.md`:

1. Identify the nearest official problem review or paper showcase.
2. Extract the expected modeling mechanism and validation style.
3. Score the current route with the table above.
4. Report blockers before praise.
