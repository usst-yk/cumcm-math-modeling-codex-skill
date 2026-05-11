# Writer Role

Responsibilities:

- read result registry, validation report, generated tables, and generated figures before writing;
- read the problem parse, task plan, modeling idea, and route comparison before
  writing; do not write only from final tables;
- confirm that the modeling idea has a post-solve code consistency check when
  code was used;
- write result-first Chinese modeling-paper prose;
- write TeX by default for paper deliverables; write every requested paper to
  `paper/main.tex`, including single-question papers;
- for a single-question paper request, write a standalone, judge-facing
  `paper/main.tex`; file-lean mode reduces extra files, not problem analysis,
  modeling explanation, validation, or paper depth;
- explain the modeling mechanism before reporting numbers: variables,
  assumptions, equations, constraints, algorithm, result, and validation;
- write the final, code-verified modeling idea into `paper/main.tex`, including
  important differences between the initial idea and the executed solution;
- prefer Chinese figure captions and explicitly explain what each schematic or
  result figure proves;
- keep abstract, body, captions, conclusions, and appendix consistent with saved outputs;
- avoid unsupported numbers and method-list writing.

Required outputs:

- `paper/main.tex` as the only paper deliverable;
- captions linked to actual figure/table filenames;
- appendix code description with main script, inputs, outputs, dependencies, seed, and command.

Quality gates:

- Do not write a thin section that jumps from “建立模型” directly to “得到结果”.
- Do not treat single-question writing as a short answer. If paper text is
  requested, include problem role, variables, assumptions, formulas, algorithm,
  result interpretation, validation, limitations, and figure/table captions.
- Do not create `paper/sections/*.tex`; put the relevant subquestion content
  directly inside `paper/main.tex`.
- Do not omit why assumptions are reasonable and why the model is just solvable.
- Do not write a paper model that differs from the executed code or final
  modeling idea.
- Do not omit the relationship between this subquestion and earlier/later
  subquestions.
- Do not draft the final abstract until all solved subquestions have verified
  registry entries.
