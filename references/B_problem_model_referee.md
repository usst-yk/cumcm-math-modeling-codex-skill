# 2025 B Problem Physics Model Referee

Use this reference to review model cards, code plans, and paper claims for
thin-film optical thickness problems.

## Model Ladder

1. Baseline: single-beam dominant-frequency or adjacent-extrema thickness
   estimate. Use for sanity check and comparison only.
2. Angle-corrected model: apply Snell law to convert incident angle to internal
   propagation angle.
3. Dispersion-aware model: compare constant refractive index with Cauchy or
   another justified refractive-index law.
4. Fresnel-aware model: include interface reflection/transmission amplitude and
   phase effects when they affect fringe contrast or phase.
5. Nonlinear spectral fit: fit physical parameters directly against the measured
   spectrum with explicit objective function and bounds.
6. Problem 3 multi-beam model: compare Airy-form multi-beam interference against
   the single-beam approximation.

## Referee Questions

- What observable is the model fitting: extrema spacing, phase, reflectance,
  transmittance, or normalized intensity?
- Which variables are measured, fixed from literature, estimated, or fitted?
- Are incidence angle and internal refraction angle separated?
- Does the model use wavelength, frequency, or wavenumber consistently?
- Does the refractive index vary across the measured band?
- Are Fresnel coefficients physically meaningful for the material interfaces?
- Are fitted parameters identifiable from the available data?
- Does the objective function weight all spectral regions appropriately?

## Route Comparison Table

Require a compact table with columns:

- route name;
- physics included;
- fitted parameters;
- data used;
- error metric;
- thickness result;
- advantages;
- limitations;
- decision.

## Hard Blocks

- Treating the baseline single-beam estimate as the final model without
  comparison.
- Claiming dispersion is negligible without a calculation or sensitivity check.
- Using a refractive-index value from memory without citation or stated source.
- Fitting many free parameters without bounds, initialization, or identifiability
  discussion.
- Omitting Airy multi-beam comparison in Problem 3.

## Paper Wording

Use restrained language: "baseline estimate", "angle-corrected fit",
"dispersion-aware nonlinear fit", "multi-beam comparison". Avoid saying a model
is superior unless the validation gate shows lower residuals, better stability,
or stronger physical consistency.
