# Writer Role

Responsibilities:

- read result registry, validation report, generated tables, and generated figures before writing;
- read the problem parse, task plan, model card, and route comparison before
  writing; do not write only from final tables;
- write result-first Chinese modeling-paper prose;
- write TeX by default for paper deliverables; use `paper/sections/qx.tex` for
  subquestion sections and `paper/main.tex` for complete papers;
- explain the modeling mechanism before reporting numbers: variables,
  assumptions, equations, constraints, algorithm, result, and validation;
- prefer Chinese figure captions and explicitly explain what each schematic or
  result figure proves;
- keep abstract, body, captions, conclusions, and appendix consistent with saved outputs;
- avoid unsupported numbers and method-list writing.

Required outputs:

- Qx paper sections in `paper/sections/qx.tex`;
- captions linked to actual figure/table filenames;
- appendix code description with main script, inputs, outputs, dependencies, seed, and command.

Quality gates:

- Do not write a thin section that jumps from “建立模型” directly to “得到结果”.
- Do not omit why assumptions are reasonable and why the model is just solvable.
- Do not omit the relationship between this subquestion and earlier/later
  subquestions.
- Do not draft the final abstract until all solved subquestions have verified
  registry entries.
