# 2025 B Problem Data Pipeline Auditor

Use this reference before fitting or writing results for thin-film spectral
thickness tasks. The goal is to make the data-to-result chain auditable.

## Required Inventory

- List every attachment, sheet, column, row count, unit, and measurement role.
- Identify independent variables, observed response, sample/material label,
  incidence angle, and any repeated measurements.
- Confirm whether the spectral axis is wavelength, frequency, wavenumber, or
  another convention; convert explicitly and keep units in table headers.
- Record excluded rows, missing values, duplicate points, non-monotonic axes,
  saturated points, and obvious instrument artifacts.

## Preprocessing Rules

- Preserve a raw copy. All cleaned tables must keep a source-file/sheet marker.
- Do not smooth before checking whether smoothing shifts extrema or fringe
  spacing.
- If interpolation is used, state the grid and verify it does not create extra
  extrema.
- Peak/trough detection must report thresholds, minimum spacing, prominence, and
  rejected candidates.
- Any baseline correction, normalization, or detrending must be justified by a
  physical or instrument reason.

## Fit-Ready Table

Each fit-ready table should contain:

- sample/material identifier;
- incident angle and unit;
- spectral variable and unit;
- measured reflectance/transmittance/intensity and unit or normalization state;
- preprocessing flags;
- source row or interval identifier.

## Audit Checklist

- Raw and cleaned data counts match expected exclusions.
- Units are consistent across formulas, plots, and tables.
- Incidence angle is not mixed with refraction angle.
- Spectral ordering is explicit after conversion.
- Extrema or fringe features used for a baseline estimate can be traced to
  concrete data points.
- Fitting code reads the cleaned table, not manually typed values.
- Result tables include parameter bounds and initial values when nonlinear
  fitting is used.

Block downstream modeling if any key unit, sample label, or angle definition is
ambiguous.
