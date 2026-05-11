# Award Paper Learning

Use this when the user provides award-paper packs, official display links,
public GitHub paper repositories, or contest paper examples for skill/paper
improvement.

## Workflow

Run the learning loop before rewriting a final paper:

```text
reference source -> structured mining -> transferable rules -> current-paper
gap table -> rework tasks -> regenerated paper artifacts -> referee check
```

Do not let reference papers flow directly into the draft. They only inform the
rules, gap table, and rework plan.

## Mining Template

For each reference, record:

| field | note |
| --- | --- |
| paper_id | stable local id or source title |
| source | official page, public repo, journal page, or user-provided file |
| problem_structure | how the paper turns questions into a progression |
| model_chain | baseline -> main model -> correction/extension |
| data_pipeline | raw data, preprocessing, feature extraction, fit-ready data |
| validation_pipeline | baseline comparison, residuals, sensitivity, uncertainty |
| figure_functions | what each figure proves |
| writing_features | abstract, section flow, model evaluation style |
| skill_rules_to_add | executable rule or gate |
| do_not_copy | text, figures, data, code, or final numbers |

## Transferable Rules

- Abstracts should name the object, difficulty, model chain, data/algorithm,
  key result, validation, and residual limitation.
- Problem analysis should define observable variables, target variables,
  contradictions, and why the next model layer is needed.
- Every nontrivial result needs at least one evidence artifact: data figure,
  result table, residual diagnostic, sensitivity figure, method comparison, or
  cited physical/standard basis.
- Fitted or predicted results need a baseline, a formal model, and a comparison
  metric; the final model cannot only compare with itself.
- Figure captions must state the judgment supported by the figure, not merely
  describe what is drawn.
- Model evaluation must bind strengths and weaknesses to assumptions, data
  limits, parameter identifiability, or residual evidence.

## Anti-Plagiarism Gate

Block the rework if any of these occur:

- copied sentences or paragraph order from a reference paper;
- recreated reference figures with only labels changed;
- reused non-problem data, final numbers, or code without license/source;
- redistributed PDFs, official display images, or paywalled material;
- claims in the current paper that cannot be traced to current data, current
  code, current problem facts, or a cited source.

Allowed learning: structure, method progression, validation logic, figure
function, result-table design, and restrained scientific tone.
