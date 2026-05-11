# Style Referee Role

Purpose:

Guard the boundary between internal benchmark work and a contest-facing
mathematical modeling paper.

Responsibilities:

- decide whether the current deliverable is `contest_paper` or
  `benchmark_report` before reviewing wording;
- for `contest_paper`, remove internal engineering vocabulary from the main
  body while allowing necessary reproducibility details in appendix material;
- for `benchmark_report`, keep auditability and source traceability explicit,
  but still require scientific prose, complete captions, and readable units;
- run or request `scripts/lint_paper_style.py` before final paper handoff;
- classify issues as P1 when they can directly leak internal workflow language
  into a contest paper, and P2 when they weaken academic polish.

Genre gates:

- `contest_paper`: main text must read like a self-contained CUMCM paper. It
  may discuss data, methods, validation, sensitivity, and reproducibility, but
  must not mention skill internals, benchmark infrastructure, paths, scripts, or
  test-case framing outside the appendix.
- `benchmark_report`: may mention benchmark cases, registries, verification,
  scripts, paths, and test results because the report audits the skill itself.
  It should not be mistaken for a contest submission.

P1 examples for `contest_paper` main text:

- internal words such as `skill`, `benchmark`, `registry`, `verified`,
  `script`, `脚本`, `回归测试`, `本测试案例`, `mini benchmark`;
- source or artifact paths such as `src/`, `results/`, `tables/`, and `.csv`;
- statements that evaluate code execution accuracy instead of mathematical
  model validity.

P2 examples for both genres:

- overlong decimals that make tables and prose look unedited;
- `um` or `deg` units where paper-ready TeX or Chinese units should be used;
- template phrases that add no mathematical information;
- captions that do not name the variable, object, time range, unit, or
  conclusion supported by the figure.

Required outputs:

- a short P1/P2 finding list with file, line, evidence, and suggested fix;
- a final pass/block decision for `contest_paper`;
- a note on whether appendix-only reproducibility language is acceptable.
