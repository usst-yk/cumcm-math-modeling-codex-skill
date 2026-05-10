# Correctness Ladder

Use this reference before trusting any major result in a CUMCM solution.

## Ladder

1. Baseline.
   - Build a simple, interpretable comparison point first.
   - Examples: analytical expression, simplified case, upper/lower bound, naive
     predictor, greedy rule, manual sample check, or small hand-computed case.

2. Main model.
   - Define variables, parameters, objective or evaluation criterion,
     constraints, assumptions, algorithm, and output form.
   - Keep the model tied to the requested subquestion, not to a method name.

3. Cross-check.
   - Check feasibility, dimensions, units, boundary cases, and direction of the
     result.
   - When possible, compare with an alternative formulation, small-case brute
     force, independent recomputation, or residual/error metric.

4. Stress test.
   - Perturb conclusion-driving inputs, weights, constraints, or parameters.
   - Report whether the main conclusion is stable, changes slightly, or fails.

## Required Use

Apply the ladder to:

- optimal decisions and objective values;
- forecast headline values and error metrics;
- evaluation rankings and weights;
- simulation peaks, thresholds, and final states;
- policy recommendations and contest-paper conclusions.

If a ladder step cannot be completed, mark it as a limitation or blocker instead
of writing a confident final conclusion.

