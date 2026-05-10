# Selling Point Design

Selling points are the paper's defensible strengths. They should shape the
abstract, figures, validation, and final review, but they must be earned by the
work already done.

## Valid Selling Points

Good selling points usually come from:

- a clear mechanism model instead of method stacking;
- an assumption that simplifies the problem without changing its essence;
- a baseline comparison that shows improvement;
- validation, sensitivity analysis, constraint checks, or robustness tests;
- interpretable figures that make the model or result easy to judge;
- cross-question reuse of variables, parameters, or strategy outputs;
- reproducible code and traceable result tables.

Weak selling points:

- "advanced algorithm" without baseline or explanation;
- many figures that do not support conclusions;
- high accuracy without data split, metric, or error definition;
- decorative AI images unrelated to modeling evidence;
- award-level claims not supported by results.

## Design Flow

1. For each subquestion, name one result claim and one validation claim.
2. Choose the figure or table that best proves each claim.
3. Decide whether the abstract should mention method, result, validation, or
   limitation.
4. Check that the claim traces to saved code output, data, table, figure,
   problem fact, or explicit assumption.
5. Remove any selling point that cannot survive judge questioning.

## Output Template

| Item | Claim | Evidence | Used in abstract | Used in figure/caption | Risk |
| --- | --- | --- | --- | --- | --- |
| Qx | concise claim | table/figure/code/source | yes/no | file or caption | blocker or caveat |

## Figure And Abstract Alignment

- The abstract should mention only the strongest traceable points.
- Captions should state what the figure proves, not only what it displays.
- Validation figures should be tied to error, feasibility, stability, or
  sensitivity claims.
- If a point is only illustrative, keep it out of the result claim.
