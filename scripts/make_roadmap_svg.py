#!/usr/bin/env python3
"""Generate an editable SVG technical roadmap from task_plan.json."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def load_nodes(task_plan: Path) -> list[str]:
    if not task_plan.exists():
        return [
            "题目任务",
            "数据与指标",
            "建模思路",
            "核心模型",
            "模型求解",
            "验证分析",
            "结论输出",
        ]
    plan = json.loads(task_plan.read_text(encoding="utf-8"))
    nodes = ["题目任务", "数据审计"]
    for q in plan.get("subquestions", []):
        qid = q.get("id", "Q")
        task_type = q.get("task_type", "建模")
        nodes.append(f"{qid} {task_type}")
    nodes.extend(["结果验证", "论文输出"])
    return nodes


def svg(nodes: list[str], width: int = 1200) -> str:
    box_w = 150
    box_h = 58
    gap = 30
    margin = 40
    per_row = max(1, (width - 2 * margin + gap) // (box_w + gap))
    rows = (len(nodes) + per_row - 1) // per_row
    height = margin * 2 + rows * box_h + (rows - 1) * 70
    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">'
        ),
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        (
            '<defs><marker id="arrow" markerWidth="10" markerHeight="10" '
            'refX="9" refY="3" orient="auto">'
            '<path d="M0,0 L0,6 L9,3 z" fill="#334155"/></marker></defs>'
        ),
        (
            '<style>text{font-family:Arial,"PingFang SC","Microsoft YaHei",sans-serif;'
            "font-size:18px;fill:#0f172a}.box{fill:#f8fafc;stroke:#2563eb;"
            "stroke-width:2;rx:8}.arrow{stroke:#334155;stroke-width:2;fill:none;"
            "marker-end:url(#arrow)}</style>"
        ),
        f'<text x="{width/2}" y="28" text-anchor="middle" font-size="22" font-weight="700">技术路线图</text>',
    ]
    centers: list[tuple[int, int]] = []
    for i, label in enumerate(nodes):
        row = i // per_row
        col = i % per_row
        x = margin + col * (box_w + gap)
        y = margin + row * (box_h + 70)
        centers.append((x + box_w // 2, y + box_h // 2))
        parts.append(
            f'<rect class="box" x="{x}" y="{y}" width="{box_w}" height="{box_h}"/>'
        )
        safe = html.escape(label)
        parts.append(
            f'<text x="{x + box_w / 2}" y="{y + box_h / 2 + 6}" '
            f'text-anchor="middle">{safe}</text>'
        )
    for (x1, y1), (x2, y2) in zip(centers, centers[1:]):
        parts.append(
            f'<path class="arrow" d="M{x1 + box_w / 2 - 6},{y1} '
            f'L{x2 - box_w / 2 + 6},{y2}"/>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate roadmap SVG from task_plan.json.")
    parser.add_argument("--task-plan", default="problem/task_plan.json", help="Task plan JSON.")
    parser.add_argument("--output", default="figures/roadmap.svg", help="Output SVG.")
    args = parser.parse_args()

    nodes = load_nodes(Path(args.task_plan).expanduser().resolve())
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg(nodes), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
