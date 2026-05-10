# Paper Assembly

Use this reference when the task asks for a complete paper, complete benchmark,
full-problem report, final TeX, or contest deliverable.

## Core Rule

A complete solved paper must be TeX. Use `paper/main.tex` as the final entry
file for full reports and benchmark cases. Markdown is acceptable only for
draft notes, section outlines, README examples, or quick single-section
discussion; it must not be the final paper artifact.

A complete paper is not a list of solved questions. It must read like one
coherent modeling work:

题目理解 -> 建模主线 -> 合理假设 -> 数学符号 -> 数据审计 -> 模型建立 ->
算法求解 -> 结果解释 -> 验证分析 -> 模型评价 -> 结论。

If the paper only concatenates Q1/Q2/Q3 sections, mark it incomplete.

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
11. 附录或复现说明

Qx sections belong inside “模型建立、求解与结果” unless the contest paper
deliberately uses one top-level section per question with equivalent global
sections before and after.

## Per-Question Fullness

Each solved subquestion should include:

- problem role: what this question contributes to the whole paper;
- variables and parameters used in the model;
- mathematical expression: equation, objective, decision rule, recurrence,
  geometry criterion, or scoring formula;
- constraints and feasibility conditions;
- algorithm or solving process, including seed/status when relevant;
- result table/figure and a paragraph explaining what the result means;
- validation, sensitivity, boundary check, or limitation.

A thin Qx section with only “we computed X, see figure Y” is not acceptable.

## Writing Density Gate

For a full paper:

- explain every important figure and table in prose;
- do not leave the model as code-only logic;
- avoid method-name lists without equations or variables;
- state why assumptions make the problem solvable without changing the problem;
- connect later questions to earlier results and shared assumptions;
- write the conclusion as an answer to the original problem, not as a file list.

## Assembly Workflow

1. Read `results/result_registry.csv` and `results/validation_report.md`.
2. Read all Qx sections and generated figures/tables.
3. Build or update the global sections first: restatement, analysis,
   assumptions, notation, data audit.
4. Embed Qx sections under model/solution and normalize their heading level.
5. Add validation, evaluation, conclusion, and appendix.
6. Only after the body is coherent, write the final abstract using
   `agents/abstract_writer.md`.
7. Run `scripts/validate_results.py --mode full` and fix any paper-structure
   or traceability findings.
8. If the only paper artifact is Markdown, mark the report incomplete and
   assemble `paper/main.tex` before handoff.
