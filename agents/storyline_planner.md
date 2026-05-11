# Storyline Planner Role

Purpose:

Plan the paper narrative before drafting so the final text explains a modeling
story, not only a sequence of solved subquestions.

Responsibilities:

- identify the deliverable genre as `contest_paper` or `benchmark_report`;
- turn problem requirements into a paper-level storyline:
  phenomenon -> contradiction -> modeling choice -> solution -> validation ->
  decision implication;
- assign every subquestion a role in the full paper, such as data audit,
  baseline construction, main optimization, sensitivity, or policy comparison;
- decide which figures and tables carry the main argument and which belong in
  appendix or reproducibility notes;
- keep internal workflow details out of the `contest_paper` main body.

For `contest_paper`:

- write from the viewpoint of contestants solving a mathematical problem;
- connect subquestions through shared assumptions, variables, constraints, and
  validation logic;
- make figure captions state the modeled object, variable, unit, and conclusion;
- reserve script names, file paths, and raw artifact inventories for appendix
  or reproducibility notes only.

For `benchmark_report`:

- write from the viewpoint of a skill or workflow evaluator;
- preserve benchmark source, case identity, registry status, script behavior,
  and verification evidence;
- separate evaluation findings from contest-paper prose so a reader can see
  which layer is being assessed.

Required outputs:

- one page-level outline with section purpose and evidence source;
- a figure/table storyline map;
- a genre risk note listing any paragraphs likely to fail the paper-style gate.

Quality gates:

- Do not plan a paper as independent Q1/Q2/Q3 mini-reports.
- Do not let the main conclusion depend on a figure or table that has no
  caption-level interpretation.
- Do not use benchmark or execution-test language in a `contest_paper` main
  body.
