#!/usr/bin/env python3
"""Export AI figure brief markdown files from problem/task_plan.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def slugify(value: str) -> str:
    stem = Path(value).stem or value
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", stem).strip("_")
    return slug or "figure"


def as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def load_template(path: Path | None) -> str:
    if path and path.exists():
        return path.read_text(encoding="utf-8")
    return """# AI Figure Brief: {figure_name}

- Subquestion: {subquestion}
- Task type: {task_type}
- Intended file: `{figure_name}`
- Required output: {required_output}
- Validation: {validation}

## Figure Goal
Explain what this figure must prove or communicate in the paper.

## Content Requirements
- Use labels, units, and legends that match the mathematical model.
- Make the caption defensible from registered results or reproducible scripts.
- Avoid decorative elements that do not support the solution.

## Data And Evidence
- Input data: {input_data}
- Related tables: {tables_needed}

## Suggested Prompt
Create a clean CUMCM paper figure for `{figure_name}`. It should support {subquestion} and show the result or model relationship implied by: {required_output}.

## Review Checklist
- [ ] Filename and caption match the paper reference.
- [ ] Axes, units, and symbols are readable.
- [ ] No unsupported numerical claim is introduced by the image.
"""


def render(template: str, context: dict[str, str]) -> str:
    text = template
    for key, value in context.items():
        text = text.replace("{" + key + "}", value)
    return text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate figure brief markdown files from task_plan.json.")
    parser.add_argument("--plan", default="problem/task_plan.json", help="Input task_plan.json path.")
    parser.add_argument("--output-dir", default="modeling", help="Output directory for markdown briefs.")
    parser.add_argument("--template", default="templates/ai_figure_brief.md", help="Optional brief template.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing brief files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_path = Path(args.plan).expanduser()
    if not plan_path.exists():
        raise SystemExit(f"Task plan not found: {plan_path}")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    outdir = Path(args.output_dir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)
    template = load_template(Path(args.template).expanduser())

    written = 0
    skipped = 0
    for subq in plan.get("subquestions", []):
        qid = str(subq.get("id", "Q"))
        figures = as_list(subq.get("figures_needed"))
        for figure in figures:
            filename = f"{qid.lower()}_{slugify(figure)}.md"
            path = outdir / filename
            if path.exists() and not args.overwrite:
                skipped += 1
                continue
            context = {
                "figure_name": str(figure),
                "subquestion": qid,
                "task_type": str(subq.get("task_type", "")),
                "required_output": "; ".join(as_list(subq.get("required_output"))) or "TBD",
                "validation": "; ".join(as_list(subq.get("validation"))) or "TBD",
                "input_data": "; ".join(as_list(subq.get("input_data"))) or "TBD",
                "tables_needed": "; ".join(as_list(subq.get("tables_needed"))) or "TBD",
            }
            path.write_text(render(template, context).rstrip() + "\n", encoding="utf-8")
            written += 1

    print(f"AI figure briefs written: {written}")
    print(f"Skipped existing briefs: {skipped}")
    print(f"Output directory: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
