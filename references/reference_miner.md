# Reference Miner

Use this when a contest problem needs outside facts, formulas, material
constants, official background, or method benchmarks.

## Mining Targets

- official problem statement, attachment notes, and contest requirements;
- physical laws and derivations needed by the model;
- material constants, refractive-index ranges, and validity bands;
- comparable contest papers or official reviews;
- numerical methods used for the same observable;
- figure and validation conventions in the domain.

## Evidence Rules

- Prefer official, textbook, peer-reviewed, or manufacturer/standards sources.
- For award papers and public paper packs, read `award-paper-learning.md` first.
- For time-sensitive or uncertain facts, verify with current web sources.
- Record source title, URL or bibliographic cue, accessed date when relevant,
  and the specific fact used.
- Never import a constant or formula without its unit, validity range, and role
  in the model.
- Separate "used in computation" from "background explanation".
- Mine structure, method progression, validation logic, and figure function;
  do not copy reference-paper prose, figures, final numbers, or data.

## Output Template

Create a compact evidence table:

| claim_or_fact | source | unit/range | used_where | risk |
| --- | --- | --- | --- | --- |

Then write a route implication note:

- which formulas become admissible;
- which assumptions need sensitivity analysis;
- which facts are too weak for final numerical use.
- which reference-paper habits should become a current-paper rework task.

## B-Problem Prompts

For 2025 B-type thin-film work, search or verify:

- Snell-law geometry for thin-film optical path;
- Fresnel coefficients and phase conventions;
- Cauchy dispersion form and material-specific validity;
- Airy multi-beam interference formula;
- refractive-index values for the material and spectral band;
- numerical fitting practices for reflectance/transmittance spectra.

## C-Problem NIPT Prompts

For 2025 C-type NIPT timing and fetal abnormality work, search or verify:

- official four-question structure and data-column meaning before reducing the
  task into a smaller synthetic case;
- fetal fraction definition, platform-dependent threshold ranges, and the role
  of the common 4% quality-control cutoff;
- evidence that fetal fraction is affected by gestational age, BMI or maternal
  weight, age, and sequencing/sample quality;
- low-fetal-fraction, no-call, and false-negative risks, with clear wording
  that NIPT is a screening test rather than a diagnostic conclusion;
- male-fetus routes that use Y concentration only after data-quality checks;
- female-fetus routes that do not treat missing/zero Y concentration as
  abnormality evidence, and instead use chromosome Z-scores, X-chromosome
  signals, GC correction, read-depth/unique-read/filtering quality indicators,
  ROC, sensitivity, specificity, PPV/NPV when a valid label and prevalence are
  available;
- threshold, BMI-boundary, weight, and measurement-error sensitivity needed to
  defend a recommended NIPT timing plan.
