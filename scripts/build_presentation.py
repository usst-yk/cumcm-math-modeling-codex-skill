#!/usr/bin/env python3
"""Build a static HTML presentation from task plan, result registry, and figures."""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
from pathlib import Path


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"}


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_registry(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def find_figures(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(item for item in path.iterdir() if item.is_file() and item.suffix.lower() in IMAGE_SUFFIXES)


def relpath(path: Path, start: Path) -> str:
    return Path(os.path.relpath(path.resolve(), start.resolve())).as_posix()


def esc(value: object) -> str:
    return html.escape(str(value if value is not None else ""))


def join_list(value: object) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value or "")


def render(plan: dict, registry: list[dict], figures: list[Path], output: Path) -> str:
    root = output.parent
    subquestions = plan.get("subquestions", [])
    title = plan.get("problem_id") or "CUMCM Presentation"
    figure_cards = []
    for fig in figures:
        src = relpath(fig, root)
        figure_cards.append(
            f"<figure><img src=\"{esc(src)}\" alt=\"{esc(fig.name)}\"><figcaption>{esc(fig.name)}</figcaption></figure>"
        )
    result_rows = []
    for row in registry:
        result_rows.append(
            "<tr>"
            f"<td>{esc(row.get('id', ''))}</td>"
            f"<td>{esc(row.get('subquestion', ''))}</td>"
            f"<td>{esc(row.get('claim', ''))}</td>"
            f"<td>{esc(row.get('value', ''))} {esc(row.get('unit', ''))}</td>"
            f"<td>{esc(row.get('validation', ''))}</td>"
            "</tr>"
        )
    subq_sections = []
    for q in subquestions:
        expected = set(str(item) for item in q.get("figures_needed", []))
        q_figs = [fig for fig in figures if fig.name in expected or fig.stem in {Path(item).stem for item in expected}]
        fig_list = "".join(f"<li>{esc(fig.name)}</li>" for fig in q_figs) or "<li>No matching figure file found.</li>"
        subq_sections.append(
            "<section>"
            f"<h2>{esc(q.get('id', 'Question'))}: {esc(q.get('task_type', ''))}</h2>"
            f"<p><strong>Required output:</strong> {esc(join_list(q.get('required_output')))}</p>"
            f"<p><strong>Model route:</strong> {esc(q.get('primary_route', ''))}</p>"
            f"<p><strong>Validation:</strong> {esc(join_list(q.get('validation')))}</p>"
            f"<ul>{fig_list}</ul>"
            "</section>"
        )
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #172033; background: #f7f7f4; }}
    header {{ padding: 36px 28px 24px; background: #ffffff; border-bottom: 1px solid #ddd8cc; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 24px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    h2 {{ margin: 0 0 12px; font-size: 22px; }}
    .meta {{ color: #667085; margin: 0; }}
    section {{ margin: 0 0 20px; padding: 20px 0; border-bottom: 1px solid #ddd8cc; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }}
    figure {{ margin: 0; background: #fff; border: 1px solid #e5e0d6; padding: 10px; }}
    img {{ display: block; max-width: 100%; height: 180px; object-fit: contain; margin: 0 auto; }}
    figcaption {{ margin-top: 8px; font-size: 13px; color: #475467; word-break: break-all; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ padding: 9px 10px; border: 1px solid #e5e0d6; text-align: left; vertical-align: top; font-size: 14px; }}
    th {{ background: #f0eee8; }}
  </style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <p class="meta">Static presentation generated from task_plan, result_registry, and figures.</p>
</header>
<main>
  <section>
    <h2>Question Plan</h2>
    {subq_sections}
  </section>
  <section>
    <h2>Registered Results</h2>
    <table>
      <thead><tr><th>ID</th><th>Question</th><th>Claim</th><th>Value</th><th>Validation</th></tr></thead>
      <tbody>{result_rows}</tbody>
    </table>
  </section>
  <section>
    <h2>Figures</h2>
    <div class="grid">{figure_cards}</div>
  </section>
</main>
</body>
</html>
""".format(
        title=esc(title),
        subq_sections="\n".join(subq_sections) or "<p>No task plan subquestions found.</p>",
        result_rows="\n".join(result_rows) or "<tr><td colspan=\"5\">No registered results found.</td></tr>",
        figure_cards="\n".join(figure_cards) or "<p>No figure files found.</p>",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build presentation/index.html.")
    parser.add_argument("--plan", default="problem/task_plan.json", help="Input task_plan.json path.")
    parser.add_argument("--registry", default="results/result_registry.csv", help="Input result registry CSV path.")
    parser.add_argument("--figures", default="figures", help="Figure directory.")
    parser.add_argument("--output", default="presentation/index.html", help="Output HTML path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    plan = read_json(Path(args.plan).expanduser())
    registry = read_registry(Path(args.registry).expanduser())
    figures = find_figures(Path(args.figures).expanduser())
    output.write_text(render(plan, registry, figures, output), encoding="utf-8")
    print(f"Presentation written: {output}")
    print(f"Subquestions: {len(plan.get('subquestions', []))}")
    print(f"Results: {len(registry)}")
    print(f"Figures: {len(figures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
