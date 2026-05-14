# Paper Assembly

Use this reference when the task asks for a complete paper, complete benchmark,
full-problem report, final TeX, or contest deliverable.

## Core Rule

A complete solved paper must be TeX. Use `paper/main.tex` as the only paper
file for full reports, benchmark cases, and single-question paper requests.
Markdown is acceptable only for draft notes, section outlines, README examples,
or quick discussion; it must not be the final paper artifact.

Paper quality comes before speed. The assembler must preserve the full modeling
chain from `examples/README.md`: staged parsing, multiple modeling rounds,
assumption justification, solving, validation, body writing, and abstract last.

A complete paper is not a list of solved questions. It must read like one
coherent modeling work:

题目理解 -> 建模主线 -> 合理假设 -> 数学符号 -> 数据审计 -> 模型建立 ->
算法求解 -> 结果解释 -> 验证分析 -> 模型评价 -> 结论。

If the paper only concatenates Q1/Q2/Q3 fragments or depends on
`paper/sections/*.tex`, mark it incomplete.

The paper must not be figure/table dominated. Figures and tables are evidence
for a written argument; they are not the argument itself. If removing the
figures and tables leaves only a thin method list and result list, mark the
paper incomplete and expand the prose before adding more visuals.

## Required Structure

For full CUMCM-style papers, `paper/main.tex` should contain these sections or
clear equivalents:

1. 摘要
2. 问题重述
3. 问题分析
4. 模型假设
5. 符号说明
6. 数据审计与预处理
7. 模型建立、求解与结果
8. 模型检验与敏感性分析
9. 模型评价与推广
10. 结论
11. 复现说明

Subquestion content belongs directly inside `paper/main.tex` under “模型建立、
求解与结果” unless the contest paper deliberately uses one top-level section
per question with equivalent global sections before and after.

## Per-Question Fullness

Each solved subquestion should include:

- problem role: what this question contributes to the whole paper;
- route and baseline reasoning: why the selected model is stronger than the
  baseline and why the fallback remains deliverable;
- variables and parameters used in the model;
- assumption purpose: what each active assumption resolves and what limitation
  it creates;
- mathematical expression: equation, objective, decision rule, recurrence,
  geometry criterion, or scoring formula;
- constraints and feasibility conditions;
- algorithm or solving process, including seed/status when relevant;
- result table/figure and a paragraph explaining what the result means, which
  question requirement it answers, and which headline value should enter the
  abstract or conclusion;
- validation, sensitivity, boundary check, and limitation;
- handoff to later questions or the final conclusion.

A thin subquestion part with only “we computed X, see figure Y” is not acceptable.

## Writing Density Gate

For a full paper:

- explain every important figure and table in prose;
- write the model chain in paragraph form before inserting dense tables:
  problem fact -> variable -> mechanism -> equation/criterion -> algorithm ->
  result -> validation -> limitation;
- keep each solved subquestion dense enough to stand as a judge-facing paper
  section: role, variables, derivation, algorithm, result interpretation,
  validation, limitation, and handoff;
- keep正文文字 as the main carrier of reasoning. Do not let a section become a
  sequence of figures, tables, captions, and one-sentence comments;
- do not leave the model as code-only logic;
- avoid method-name lists without equations or variables;
- include the route comparison or model-selection reasoning that led to the
  final model;
- state why assumptions make the problem solvable without changing the problem;
- connect later questions to earlier results and shared assumptions;
- write the conclusion as an answer to the original problem, not as a file list.

## Assembly Workflow

1. Read `results/validation_report.md`.
2. Read every solved `modeling/qx_modeling_idea.md`, especially the gradual
   derivation and code reverse-check. Do not write from final result tables
   alone.
3. Read generated figures/tables and any existing `paper/main.tex` draft.
4. Build or update the global sections first: restatement, analysis,
   assumptions, notation, data audit.
5. Write subquestion content directly under model/solution and normalize the
   heading level inside `paper/main.tex`.
6. For each inserted figure/table, write a before-and-after explanation:
   why it is needed, what it shows, what conclusion it supports, and how it
   relates to baseline or validation.
7. Remove repeated or decorative figures/tables; move large intermediate
   outputs to appendix or saved artifacts.
8. Add validation, evaluation, conclusion, and appendix.
9. Only after the body is coherent, write the final abstract using
   `agents/abstract_writer.md`.
10. Run `scripts/validate_results.py --mode full` and fix any paper-structure
   or traceability findings.
11. If the only paper artifact is Markdown, mark the report incomplete and
   assemble `paper/main.tex` before handoff.
12. If `paper/sections/*.tex` exists for a new deliverable, merge the content
   into `paper/main.tex` and remove the fragments before handoff.
