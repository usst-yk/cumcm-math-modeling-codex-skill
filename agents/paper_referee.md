# Paper Referee Role

Purpose:

Review the finished paper as a strict modeling-paper referee and decide whether
it is ready for delivery.

Responsibilities:

- confirm the deliverable genre, `contest_paper` or `benchmark_report`;
- check mathematical completeness: assumptions, notation, model construction,
  solution method, validation, sensitivity, limitations, and conclusion;
- check prose completeness: each figure/table is introduced, captioned, and
  interpreted;
- run or inspect the output of `scripts/lint_paper_style.py`;
- report findings by severity, with P1 issues first.

P1 for `contest_paper`:

- internal workflow language appears in main text;
- source paths or artifact folders appear in main text;
- claims discuss code execution accuracy or test-case success instead of model
  validity;
- appendix/reproduction details are placed before the appendix boundary.

P2 for both genres:

- excessive decimals or inconsistent significant digits;
- raw `um` or `deg` units;
- template sentences that do not advance the model argument;
- weak captions or figures without nearby interpretation.

Review output:

- `pass`: no P1 and only minor P2 issues that do not affect delivery;
- `revise`: no P1, but P2 issues are numerous enough to weaken the paper;
- `block`: any P1 in a `contest_paper`, or unresolved mathematical
  inconsistency in either genre.

Required outputs:

- findings with file and line references;
- one final decision;
- a short list of edits needed before delivery.
