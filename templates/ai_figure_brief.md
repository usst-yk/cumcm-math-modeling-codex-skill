# AI Figure Brief: {figure_name}

- Subquestion: {subquestion}
- Task type: {task_type}
- Intended file: `{figure_name}`
- Required output: {required_output}
- Validation: {validation}

## Figure Goal

State what the figure must communicate and which paper claim it supports.

## Content Requirements

- Match symbols, labels, units, and terminology used in the model.
- Keep visual style clean enough for a CUMCM paper or defense slide.
- Prefer readable annotations over decorative effects.
- Do not add numerical values that are absent from source data, scripts, tables, or the result registry.

## Data And Evidence

- Input data: {input_data}
- Related tables: {tables_needed}

## Suggested Prompt

Create a clean CUMCM modeling figure for `{figure_name}`. It should support {subquestion}, communicate the required output "{required_output}", and remain consistent with the validation requirement "{validation}".

## Review Checklist

- [ ] Filename and caption match the paper reference.
- [ ] Axes, units, legends, and labels are readable.
- [ ] The figure agrees with the registered result or source table.
- [ ] No unsupported numerical claim is introduced.
