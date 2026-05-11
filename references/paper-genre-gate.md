# Paper Genre Gate

This reference separates two deliverable modes that often share the same
project files but must not share the same prose.

## Genres

`contest_paper` is the competition submission. Its main body should read as a
mathematical modeling paper written by contestants. It may mention data,
models, algorithms, validation, robustness, and limitations, but it must not
expose internal skill, benchmark, registry, script, path, or test-case language
before the appendix.

`benchmark_report` is an internal or maintainer-facing evaluation report. It
may mention benchmark sources, registries, verification status, scripts, paths,
case identities, and test outcomes because those are the objects being audited.
It still needs clear scientific prose, readable units, and useful captions.

## Contest Paper Main-Body Ban List

The following terms are P1 when they appear in the main body of a
`contest_paper`. For an official submission, they should not appear in the
submitted appendix either; keep command/path details in internal reproduction
notes instead.

- `skill`
- `benchmark`
- `registry`
- `verified`
- `script`
- `脚本`
- `代码执行准确性`
- `回归测试`
- `本测试案例`
- `本案例`
- `mini benchmark`
- `src/`
- `results/`
- `tables/`
- `.csv`

Treat close variants and obvious path forms as P1 when they reveal internal
workflow rather than mathematical content.

## Appendix Boundary

Appendix text begins after one of these signals:

- TeX `\appendix`
- `\begin{appendices}`
- a section title containing `附录`, `Appendix`, `复现`, or `Reproduction`
- a section file whose name contains `appendix`, `repro`, or `supplement`

Official appendices should use paper-facing wording: data口径, calculation口径,
result consistency, and limitations. Commands, data filenames, scripts,
environment notes, seeds, and output paths belong in internal reproduction notes
or project reports, not the submitted paper.

## Severity

P1 blocks `contest_paper` delivery. It usually means the paper leaks the
internal workflow, exposes artifact paths in the main body, or frames the result
as a test case instead of a mathematical solution.

P2 does not automatically block delivery but should be fixed before final
polishing. Common P2 issues are overlong decimals, raw `um` or `deg` units,
template phrases, and captions too weak to support the figure.

## Practical Rewrite Rules

- Replace "the script verified the result" with "the residual and sensitivity
  analysis support the stability of the result" only when the paper actually
  contains that evidence.
- Replace artifact paths with paper objects: "Table 3", "Figure 4", "the
  cleaned data set", or "the appendix reproduction files".
- Replace benchmark language with problem-facing language: "representative
  scenario", "historical sample", "validation set", or "comparison baseline".
- Move commands, file names, seeds, package versions, and folder names out of
  the submitted paper and into internal reproduction notes.
