# Advanced Mathematical Modeling

Use this reference when the problem has real mechanisms behind the data, or
when the user asks for more mathematically substantial modeling. The goal is to
raise modeling depth without forcing decorative formulas.

## Core Rule

Prefer the deepest mathematical model that is still:

- implied by the problem mechanism or data-generating process;
- identifiable or calibratable from given data, problem constants, or defensible
  assumptions;
- solvable within contest time;
- validated by a baseline, conservation law, boundary case, residual/error
  metric, sensitivity check, or small exact case;
- explainable in `paper/main.tex`.

If a high-level model is not identifiable, use it as an explanatory correction,
upper/lower bound, or validation model instead of pretending it is the main
source of exact results.

## Mathematical Depth Pass

Before finalizing each subquestion route, ask:

1. Is there a conservation law, balance equation, equilibrium, stability
   condition, or variational principle behind the process?
2. Can the problem be written as an ODE, PDE, difference equation, stochastic
   process, network flow, dynamic program, optimal control problem, or
   constrained optimization problem?
3. Can a simplified analytical model provide a threshold, bound, monotonicity
   result, or dimensionless parameter that explains the numerical result?
4. Are there hidden uncertainties, interventions, confounders, or feedback loops
   that require stochastic, robust, Bayesian, causal, or control modeling?
5. Which advanced model can enter the paper as:
   - main model for final calculation;
   - correction model to improve a baseline;
   - validation model to check direction, scale, or boundary behavior?

## Mechanism-To-Model Map

| Problem mechanism | Mathematical candidates | Paper value | Required checks |
| --- | --- | --- | --- |
| Flight, projectile, drag, interception | Kinematics, Newtonian dynamics, drag ODE, optimal control, geometric visibility | Converts motion wording into equations and constraints | Unit check, limiting case without drag, trajectory residual or boundary event check |
| Fluid, smoke, pollutant, heat, diffusion | Advection-diffusion PDE, Gaussian plume, reaction-diffusion, finite difference/finite volume | Adds physical mechanism beyond curve fitting | Conservation/mass balance, boundary conditions, grid convergence, parameter sensitivity |
| Epidemic, ecology, population evolution | ODE/difference systems, SIR/SEIR, Lotka-Volterra, stability analysis | Explains peaks, equilibria, thresholds | Equilibrium/stability, parameter identifiability, sensitivity, baseline comparison |
| Supply chain, logistics, production, inventory | Network flow, MILP, stochastic programming, robust optimization, queuing, inventory control | Makes constraints and tradeoffs explicit | Feasibility, dual/bound comparison, scenario stress test, service-level or capacity checks |
| Scheduling, routing, dispatch | MILP, CP-SAT, dynamic programming, VRP, shortest path, min-cost flow | Gives decision variables, objective, and hard constraints | Solver status, constraint violation table, greedy/small exact baseline |
| Causal intervention, policy evaluation | DAG, propensity score, difference-in-differences, IV, regression discontinuity, panel fixed effects | Distinguishes correlation from intervention effect | Identification assumptions, balance/placebo tests, robustness to confounders |
| Risk, uncertainty, reliability | Monte Carlo, Bayesian updating, Markov chain, survival analysis, chance constraints | Quantifies uncertainty and failure probability | Seed, confidence intervals, convergence, stress cases |
| Spatial coverage, sensing, facility layout | Voronoi, p-median, maximum coverage, spatial interpolation, geometric optimization | Links geometry to allocation or coverage decisions | Coordinate scale, boundary effects, distance metric sensitivity |

## How To Use Advanced Models In The Paper

When an advanced model is used, write these pieces explicitly:

1. **Why needed**: what simpler model misses.
2. **Mechanism**: the physical, statistical, operational, or causal law.
3. **Variables and parameters**: units, data source, bounds, and unknowns.
4. **Equations**: derive them from balance, force, probability, flow, or
   optimization logic.
5. **Simplification**: what is ignored and why it is acceptable.
6. **Solution**: discretization, solver, initial/boundary conditions, seed, and
   stopping/status where relevant.
7. **Validation**: conservation, residual, baseline, grid convergence, small
   exact case, placebo, sensitivity, or feasibility check.
8. **Interpretation**: what the mathematical structure explains about the result.

## Guardrails

- Do not add PDEs, causal graphs, Bayesian formulas, or optimal-control notation
  unless the problem has a mechanism requiring them.
- Do not use an advanced model if its parameters cannot be estimated, bounded,
  or justified.
- Do not replace validation with model complexity.
- Do not hide a simple answer behind a complex method. Use the advanced model to
  explain, improve, or validate the answer.
- If a high-level model is introduced but simplified for contest feasibility,
  say exactly which terms or constraints were simplified and test the effect
  when possible.
