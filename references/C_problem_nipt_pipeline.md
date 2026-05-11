# C Problem NIPT Pipeline

Use this for 2025 C-type NIPT timing and fetal abnormality problems.

## Required Route

Do not compress the official problem into a thin three-part draft. Preserve the
four-question logic unless the user explicitly asks for a reduced demo:

1. Analyze male-fetus Y concentration against gestational week, BMI, maternal
   variables, and sequencing quality; include a simple baseline and significance
   or residual checks. Regression metrics alone are not enough: include
   coefficient interpretation, residual/robustness evidence, the 4% threshold
   connection, source tables, Chinese figures, and a paper-ready paragraph.
2. Use BMI groups to recommend NIPT timing by minimizing a risk function that
   balances early low-fetal-fraction failure and late clinical-window risk; add
   threshold sensitivity. Fixed-group timing must output a recommendation table,
   feasibility/constraint check, threshold and late-risk sensitivity table, and
   a statement that grid-search optimality is limited to the candidate grid.
3. Treat BMI boundaries and timing as joint decisions. Include maternal factors,
   measurement error, target qualified proportion, and an iterative or otherwise
   reproducible optimization trace. Q3 must include BMI-boundary/timing trace,
   qualified-rate feasibility check by group, minimum-group-size check, and an
   explicit local-search or candidate-set limitation when global optimality is
   not certified.
4. For female-fetus abnormality screening, do not use Y concentration as the
   main evidence. Use chromosome Z-scores, X-chromosome deviation, GC/read-depth
   quality variables, and screening metrics such as ROC, sensitivity,
   specificity, and confusion matrix. Threshold selection must be explained; in
   cross-validation choose the threshold inside training folds and report
   held-out AUC, sensitivity, specificity, and Brier/calibration when possible.

## Literature Gate

Before finalizing the route, record a compact literature note covering:

- fetal fraction definition and why it is a NIPT quality-control variable;
- evidence that gestational age and BMI/maternal weight affect fetal fraction;
- the status of 4% as a common but platform-dependent QC threshold;
- no-call / low-fetal-fraction implications and false-negative risk;
- female-fetus fetal-fraction estimation limitations and Z-score/GC correction;
- the boundary that NIPT is screening, not diagnostic testing.

Use peer-reviewed, official, or reputable clinical sources. Do not use
post-contest solution blogs as model evidence.

## Award-Paper Gap Check

Compare the current draft against award-paper structure without copying:

- object and contradiction are stated before algorithms;
- each question has baseline -> primary model -> robustness or correction;
- every headline number traces to a saved table, figure, code output, or result
  registry row;
- each solved question has a mechanism/flow figure, result figure, and
  validation or sensitivity figure;
- the abstract is written last and contains only verified numbers;
- limitations are tied to data scope, platform assumptions, measurement error,
  or screening/diagnosis boundary.

## Validation Gates

Block or revise if any item is missing:

- official four-question coverage, or a written reason for reduced scope;
- male concentration baseline comparison;
- Q2 threshold/late-risk sensitivity;
- Q2 feasibility check and parameter-source trace for threshold, target rate,
  search step, and risk weights;
- Q3 iterative optimization trace or equivalent reproducible search evidence,
  plus feasible group-size and qualified-rate checks;
- female-fetus ROC/confusion-matrix validation, threshold rationale,
  cross-validation, and screening-not-diagnosis wording;
- single `paper/main.tex` with paper-facing prose, not split fragments;
- no copied reference-paper prose, figures, data, or code.

## Paper Writing Notes

Prefer restrained clinical wording:

- write "screening risk", "high-risk indication", or "recommended follow-up";
- avoid "diagnose", "exclude abnormality", or individual medical conclusions;
- explain the 4% threshold as a modeling/QC cutoff unless the platform and
  source justify stronger wording;
- keep code paths and workflow details in internal reports, not in the main
  contest-paper body or official-submission appendix.
