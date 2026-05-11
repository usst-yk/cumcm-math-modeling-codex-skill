# First-Prize-Oriented Modeling Rubric

This rubric is for judge-style review. It estimates whether a solution has the
ingredients of a strong CUMCM paper. It cannot guarantee an award.

## Award-Critical Notes

The evaluated product is the paper. Code, tables, and figures matter because
they make the paper traceable and credible, but they cannot replace clear
judge-facing writing. A route should not be treated as award-ready until the
paper explains the model, assumptions, equations, algorithm, results,
validation, limitations, and cross-question logic in one coherent narrative.

For award-oriented work, paper planning starts during modeling:

- each subquestion should produce paper-ready equations, figures, captions,
  result interpretation, and validation wording as soon as it is solved;
- abstract writing stays last, after body text, figures, tables, validation, and
  saved tables, figures, code outputs, and validation notes agree;
- a mathematically strong solution with a thin, fragmented, or inconsistent
  paper should be downgraded before a simpler but clearer complete paper.

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
| Traceability | Numbers cannot be traced | Some key numbers traceable | Every headline number traces to data, table, code output, or saved tables, figures, code outputs, and validation notes |
| Paper readiness | Chat-like or placeholder text | Mostly usable but inconsistent | Judge-facing Chinese prose with consistent abstract, body, tables, figures, and appendix |

## Gate Rules

- If any item scores 0, mark the answer incomplete.
- If core mechanism, validation, traceability, or paper readiness scores below
  2, do not call the work "first-prize level".
- Strong solutions usually score at least 16/20 and have no 0 item.

## Official Benchmark Use

When the user asks whether a solution is high-level, compare against
`references/official-benchmark.md`:

1. Identify the nearest official problem review or paper showcase.
2. Extract the expected modeling mechanism and validation style.
3. Score the current route with the table above.
4. Report blockers before praise.
