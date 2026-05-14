# Writing Prompt Expansions

Use this file for abstract revision, paper rewriting, figure/table discipline,
and translating code or results into paper text.

## 目录

- Completed Prompt: Abstract Revision
- Completed Prompt: Paper Writing Or Rewriting
- Completed Prompt: Figure, Flowchart, Or Roadmap
- Completed Prompt: Code Or Result To Paper

## Completed Prompt: Abstract Revision

Trigger examples:

- 修改摘要
- 摘要太差
- 重写摘要
- 摘要没有深度
- 摘要要冲奖一点

Internally expand to:

1. Read `paper/main.tex`, saved result tables, figures, code outputs, and
   `results/validation_report.md`.
2. Check that every abstract number has a source. If a number is unsupported,
   do not use it.
3. For each solved subquestion, include:
   - problem object;
   - mathematical/modeling method;
   - key result;
   - validation evidence;
   - limitation or reliability boundary when important.
4. Do not write a background-heavy abstract. Focus on method, result,
   validation, and contribution.
5. Keep abstract consistent with body, captions, conclusion, and saved results.
6. Write the revised abstract into `paper/main.tex`.

If body text or validation is too weak, return an abstract blocker list before
polishing.

## Completed Prompt: Paper Writing Or Rewriting

Trigger examples:

- 写论文
- 修改论文
- 论文太差
- 正文太少
- 论文没有深度
- 论文图表太多

Internally expand to:

1. Read modeling ideas, code outputs, tables, figures, validation notes, and the
   current `paper/main.tex`.
2. Refuse to invent missing numbers. Mark blockers when a conclusion has no
   source.
3. Rewrite with deep prose:
   - problem role;
   - problem-to-variable translation;
   - assumptions and why they are necessary;
   - mathematical derivation;
   - algorithm and reproducibility;
   - result interpretation;
   - validation;
   - limitation;
   - handoff to next question or final conclusion.
4. Reduce figure/table dominance:
   - keep only key body visuals;
   - move process tables and repetitive plots to appendix/artifacts;
   - explain every retained visual before and after it appears;
   - add prose that tells the reader what the model means, not only what the
     figure shows.
5. Update `paper/main.tex` only. Do not split into `paper/sections/*.tex`.
6. Run available checks.

Do not “润色” an unsupported paper into sounding confident. First fix missing
derivation, result sources, and validation.

## Completed Prompt: Figure, Flowchart, Or Roadmap

Trigger examples:

- 补图
- 画流程图
- 做技术路线图
- 图太少
- 图看不懂

Internally expand to:

1. Decide which figure is needed:
   - model flowchart;
   - technical roadmap;
   - problem structure or geometry schematic;
   - result figure;
   - validation/sensitivity/feasibility figure.
2. Before generating the image, write the prompt/spec under `modeling/` or
   `modeling/flowcharts/`.
3. Use Chinese labels, title, legend, axis/unit labels, and readable paper style.
4. Save final figures under `figures/` with stable names.
5. Write captions and paper explanation into `paper/main.tex`.
6. Do not add decorative figures. Each figure must support a conclusion.

When the user says figures and tables are too many, remove or demote weak
visuals first; do not add more visuals to hide shallow writing.

## Completed Prompt: Code Or Result To Paper

Trigger examples:

- 根据代码写论文
- 根据结果表写正文
- 代码跑完了，写进论文
- 这些图怎么写进论文

Internally expand to:

1. Read code, result tables, figures, logs, and validation notes before writing.
2. Map every headline value to source file and field.
3. Translate code logic into model establishment and solving process:
   - input data and preprocessing;
   - variables and arrays;
   - formulas, objective, constraints, or transitions;
   - algorithm or solver process;
   - intermediate checks;
   - output tables and figures.
4. Record code-to-model consistency in `modeling/qx_modeling_idea.md`.
5. Write result interpretation, validation, and limitations into
   `paper/main.tex`.
6. Do not describe a model that code did not implement.
