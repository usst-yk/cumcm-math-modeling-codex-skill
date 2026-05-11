# 2025 B Problem Validation Gate

Use this gate before accepting B-problem numerical results or final paper claims.

## Gate Inputs

- data inventory and fit-ready tables;
- model formulas and parameter definitions;
- fitted parameter table with units, bounds, initial values, and solver status;
- residual/error tables and figures;
- route comparison table covering baseline and formal models.

## Required Checks

- Dimensional check: every thickness formula and fitted parameter has consistent
  units.
- Angle check: Snell correction is applied where the optical path depends on
  internal angle.
- Dispersion check: constant refractive index is compared against Cauchy or a
  justified dispersion law.
- Phase/amplitude check: Fresnel effects are considered, not silently absorbed
  into arbitrary scale factors.
- Nonlinear fit check: report objective function, bounds, convergence status,
  residual pattern, and parameter uncertainty or sensitivity.
- Cross-sample check: compare results across attachments, materials, or angles
  when available.
- Baseline check: single-beam dominant-frequency estimates are labeled baseline
  and not used as the sole final answer.
- Problem 3 check: Airy multi-beam interference is compared with single-beam
  interference and judged by residuals, stability, and physical plausibility.

## Failure Conditions

Mark the result as blocked if:

- final thickness is copied from a formula without data traceability;
- a nonlinear fit converges but residuals show systematic fringe mismatch;
- angle, wavelength/wavenumber, or refractive-index units are unclear;
- the model comparison only reports one method;
- Problem 3 omits Airy multi-beam comparison;
- a paper claim says the model is accurate without an error metric,
  residual figure, or comparison baseline.

## Handoff Standard

Accepted results need a short validation paragraph:

- what was checked;
- which table/figure contains the evidence;
- what residual risk remains;
- why the selected model is stronger than the baseline.
