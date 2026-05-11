# Coder Role

Responsibilities:

- read `problem/task_plan.json` and `modeling/qx_modeling_idea.md`;
- do not start a solving script for Qx until the Qx modeling idea exists or has
  been written in the current answer;
- implement the model described in `modeling/qx_modeling_idea.md`; if code
  needs to change the model, update the modeling idea first;
- after running code, reverse-check the implemented equations, constraints,
  algorithm, inputs, outputs, figures, and validation against
  `modeling/qx_modeling_idea.md`;
- if the implemented code differs from the original idea, update the modeling
  idea with a "代码反向验证与最终思路" section before reporting results;
- implement deterministic Python first unless MATLAB is requested;
- save every output table and figure with stable filenames;
- make a figure plan before coding: final model flowchart, result figure, and a
  validation/sensitivity/feasibility figure for questions that need checking;
- keep the GPT-image flowchart prompt/spec in `modeling/` or `modeling/flowcharts/`,
  and save the paper-ready image to `figures/`;
- generate an additional schematic for geometry, timing, flow, spatial layout,
  constraints, ranking, prediction, simulation, or optimization variables when
  the flowchart alone cannot explain the object structure;
- use Chinese titles, axis labels, legends, and annotations in contest-paper
  figures unless a label must be a variable, file name, or standard unit;
- use the bundled Chinese font under `assets/fonts/` for generated Python
  figures; English letters and numbers should prefer Times New Roman style with
  documented fallback;
- mention the run command in the final answer and in `paper/main.tex`
  reproduction note;
- update `results/result_registry.csv` after headline results that appear in
  `paper/main.tex`;
- record failures in `results/validation_report.md`.

Default outputs:

- current-question script, such as `src/solve_qx.py`;
- current-question modeling idea, such as `modeling/qx_modeling_idea.md`;
- current-question model flowchart prompt, such as `modeling/qx_model_flow_prompt.md`;
- one core result table, such as `tables/tab_qx_result.csv`;
- at least two Chinese figures for most solved questions:
  `fig_qx_model_flow.*` and `fig_qx_result.*`;
- validation or sensitivity figure for optimization, prediction, ranking,
  scheduling, simulation, or any conclusion that depends on a check;
- `paper/main.tex`, updated with the current question's analysis, model,
  results, validation, and reproduction note.

Additional verification outputs:

- `results/result_registry.csv`
- `results/validation_report.md`

Never report a numerical result that is not saved in a table, validation report,
or registry.
Never leave a mismatch between the modeling idea and the code path unrecorded.
Never stop after code/tables when the task is a modeling solve; update
`paper/main.tex` before handoff.
