# Paper Quality Standard

Use this reference for every complete paper, benchmark paper, or request that
asks for a paper deliverable. The standard is intentionally stricter than a
format check: the final paper is the main contest product.

## Priority

Paper quality comes before speed. A complete TeX paper with clear modeling
logic is preferred over a quick result summary. Do not compress away the
mathematics, assumptions, validation, figure interpretation, or abstract to
finish faster.

## Required Writing Chain

Before writing the final paper, make sure the work has passed this chain:

1. problem parse: subquestions, inputs, outputs, constraints, units, risk words;
2. route comparison: baseline, primary route, fallback route;
3. modeling deepening: at least three rounds of idea checking, and a fourth
   mandatory round for the final route;
4. assumptions: each important assumption has necessity, reason, and possible
   effect;
5. solving: code or derivation produces traceable tables and figures;
6. validation: baseline, feasibility, sensitivity, error, or boundary check;
7. paper body: problem analysis, model, results, validation, evaluation;
8. final abstract: written only after the body and registry are consistent.

## Full Paper Non-Negotiables

A full paper must:

- be written in TeX, normally `paper/main.tex`;
- contain global sections before and after the subquestion content;
- explain why the model matches the real problem mechanism;
- state variables, parameters, objective/decision rule, constraints, and
  algorithm in mathematical language;
- explain why assumptions make the problem just solvable rather than over-simple;
- connect subquestions through shared assumptions, variables, parameters,
  outputs, or strategy handoff;
- explain every important figure and table in prose;
- state validation results and limitations honestly;
- write the abstract last and include methods, numbers, validation, and limits.

## Rejection Rules

Mark the paper incomplete if any of these happens:

- the final artifact is Markdown instead of TeX;
- the paper only stitches together per-question fragments;
- the body says only “建立模型并求解得到结果” without mathematical detail;
- a subquestion has no equation, objective, recurrence, decision rule, or clear
  mathematical criterion;
- figures are inserted without explaining what conclusion they support;
- assumptions are listed but not used in the model;
- the abstract has numbers not found in the registry, tables, code output, or
  problem facts;
- the paper hides that the model is a best-found or benchmark result and
  overclaims global optimality.

## Minimum Subquestion Section Shape

Each solved subquestion should include:

1. role in the whole paper;
2. modeling object and decision variables;
3. assumptions and constraints specific to the question;
4. mathematical formulation or decision rule;
5. solving algorithm and reproducibility details;
6. result table/figure and a paragraph explaining the result;
7. validation or sensitivity check;
8. connection to the next question or final conclusion.
