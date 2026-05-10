#!/usr/bin/env python3
"""Generate an editable SVG technical roadmap from task_plan.json."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


TASK_TYPE_LABELS = {
    "prediction": "预测",
    "optimization": "优化",
    "evaluation": "评价",
    "simulation": "仿真",
    "classification": "分类",
    "clustering": "聚类",
    "unknown": "建模",
}


def load_plan(task_plan: Path) -> dict:
    if not task_plan.exists():
        return {}
    return json.loads(task_plan.read_text(encoding="utf-8"))


def load_nodes(task_plan: Path) -> list[str]:
    plan = load_plan(task_plan)
    if not plan:
        return ["题面解析", "附件审计", "建模路线", "模型求解", "结果验证", "论文输出"]
    nodes = ["题面解析", "附件审计", "路线比较"]
    for q in plan.get("subquestions", []):
        qid = q.get("id", "Q")
        task_type = q.get("task_type", "建模")
        nodes.append(f"{qid} {TASK_TYPE_LABELS.get(task_type, task_type)}")
    nodes.extend(["结果验证", "论文输出"])
    return nodes


def question_nodes(question: dict) -> list[str]:
    qid = question.get("id", "Q")
    task_type = question.get("task_type", "unknown")
    label = TASK_TYPE_LABELS.get(task_type, task_type)
    outputs = question.get("required_output", [])
    output_label = str(outputs[0])[:18] if outputs else "输出结果"
    return [
        f"{qid} 题意解析",
        "输入和约束",
        f"{label}模型",
        "代码求解",
        "结果图表",
        "验证检查",
        output_label,
    ]


def wrap_label(label: str, max_chars: int = 9, max_lines: int = 3) -> list[str]:
    text = str(label).strip()
    lines = [text[i : i + max_chars] for i in range(0, len(text), max_chars)] or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .。") + "..."
    return lines


def svg(nodes: list[str], width: int = 1200) -> str:
    wrapped = [wrap_label(node) for node in nodes]
    line_h = 18
    box_w = 170
    box_h = max(64, max(len(lines) for lines in wrapped) * line_h + 24)
    gap = 30
    margin_x = 40
    margin_y = 58
    row_gap = 70
    per_row = max(1, (width - 2 * margin_x + gap) // (box_w + gap))
    rows = (len(nodes) + per_row - 1) // per_row
    height = margin_y + rows * box_h + (rows - 1) * row_gap + 36
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
    rects: list[dict[str, int]] = []
    for i, lines in enumerate(wrapped):
        row = i // per_row
        col = i % per_row
        x = margin_x + col * (box_w + gap)
        y = margin_y + row * (box_h + row_gap)
        rects.append({"row": row, "x": x, "y": y, "cx": x + box_w // 2, "cy": y + box_h // 2})
        parts.append(
            f'<rect class="box" x="{x}" y="{y}" width="{box_w}" height="{box_h}"/>'
        )
        start_y = y + box_h / 2 - (len(lines) - 1) * line_h / 2 + 6
        text_parts = [
            f'<text x="{x + box_w / 2}" y="{start_y}" text-anchor="middle">'
        ]
        for idx, line in enumerate(lines):
            dy = 0 if idx == 0 else line_h
            text_parts.append(f'<tspan x="{x + box_w / 2}" dy="{dy}">{html.escape(line)}</tspan>')
        text_parts.append("</text>")
        parts.append("".join(text_parts))
    for current, nxt in zip(rects, rects[1:]):
        if current["row"] == nxt["row"]:
            parts.append(
                f'<path class="arrow" d="M{current["x"] + box_w - 6},{current["cy"]} '
                f'L{nxt["x"] + 6},{nxt["cy"]}"/>'
            )
            continue
        mid_y = current["y"] + box_h + row_gap // 2
        parts.append(
            f'<path class="arrow" d="M{current["cx"]},{current["y"] + box_h - 4} '
            f'L{current["cx"]},{mid_y} L{nxt["cx"]},{mid_y} L{nxt["cx"]},{nxt["y"] + 4}"/>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate roadmap SVG from task_plan.json.")
    parser.add_argument("--task-plan", default="problem/task_plan.json", help="Task plan JSON.")
    parser.add_argument("--output", default="figures/roadmap.svg", help="Output SVG.")
    parser.add_argument(
        "--per-question-dir",
        help="Optional directory for per-question roadmap SVG files, e.g. figures/roadmaps.",
    )
    args = parser.parse_args()

    task_plan = Path(args.task_plan).expanduser().resolve()
    nodes = load_nodes(task_plan)
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg(nodes), encoding="utf-8")
    print(f"Wrote {out}")
    if args.per_question_dir:
        plan = load_plan(task_plan)
        per_question_dir = Path(args.per_question_dir).expanduser().resolve()
        per_question_dir.mkdir(parents=True, exist_ok=True)
        for question in plan.get("subquestions", []):
            qid = str(question.get("id", "q")).lower()
            q_out = per_question_dir / f"roadmap_{qid}.svg"
            q_out.write_text(svg(question_nodes(question), width=1000), encoding="utf-8")
            print(f"Wrote {q_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
