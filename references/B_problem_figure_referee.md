# 2025 B Problem Figure Referee

Use this before finalizing B-problem plots, schematics, captions, or paper
figure references.

## Minimum Figure Set

- Data overview: raw spectrum for each attachment/sample with units.
- Pipeline evidence: cleaned spectrum or detected extrema with rejected/accepted
  markers when extrema drive a baseline estimate.
- Model schematic: incident angle, refraction angle, film thickness, interfaces,
  and optical path.
- Fit result: measured spectrum versus fitted curve for each final model.
- Residual evidence: residual curve or residual distribution.
- Route comparison: baseline versus formal model results and error metrics.
- Problem 3: single-beam versus Airy multi-beam comparison.

## Figure Quality Checks

- Axes name the physical quantity and unit.
- Legends distinguish data, baseline, formal model, and validation curves.
- Captions state what evidence the figure proves, not just what it shows.
- Any smoothing, normalization, or interpolation is visible in caption or label.
- Residual plots use the same spectral axis as the fitted spectrum.
- Colors and markers remain readable in grayscale or PDF print.
- No figure cites a result that is absent from saved data or code output.

## Referee Rejections

Reject or revise a figure if:

- it is decorative and does not support a claim;
- it hides model disagreement by over-smoothing;
- it overlays curves with incompatible units or spectral axes;
- it lacks units, sample labels, or angle labels;
- it uses AI-generated imagery as quantitative evidence;
- it shows only the final fit without residuals or comparison.

## Caption Pattern

Use a concise caption structure:

1. data source and preprocessing state;
2. model or comparison shown;
3. key quantitative conclusion;
4. validation implication.
