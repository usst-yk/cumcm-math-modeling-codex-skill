#!/usr/bin/env python3
"""Append project progress events and optionally render progress.html."""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"time": "", "stage": "parse_error", "message": line, "status": "invalid"})
    return rows


def render_html(events: list[dict], output: Path) -> None:
    status_class = {"done": "done", "blocked": "blocked", "risk": "risk", "working": "working"}
    rows = []
    for event in reversed(events):
        status = str(event.get("status", "working"))
        css = status_class.get(status.lower(), "working")
        files = ", ".join(event.get("files", [])) if isinstance(event.get("files"), list) else str(event.get("files", ""))
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(event.get('time', '')))}</td>"
            f"<td>{html.escape(str(event.get('stage', '')))}</td>"
            f"<td><span class=\"pill {css}\">{html.escape(status)}</span></td>"
            f"<td>{html.escape(str(event.get('worker', '')))}</td>"
            f"<td>{html.escape(str(event.get('message', '')))}</td>"
            f"<td>{html.escape(files)}</td>"
            "</tr>"
        )
    body = "\n".join(rows) or "<tr><td colspan=\"6\">No progress events yet.</td></tr>"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Project Progress</title>
  <style>
    body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #1f2937; background: #f8fafc; }
    main { max-width: 1120px; margin: 0 auto; padding: 32px 20px; }
    h1 { margin: 0 0 8px; font-size: 28px; }
    .meta { margin: 0 0 24px; color: #64748b; }
    table { width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #e5e7eb; }
    th, td { padding: 10px 12px; border-bottom: 1px solid #e5e7eb; text-align: left; vertical-align: top; font-size: 14px; }
    th { background: #f1f5f9; color: #334155; }
    .pill { display: inline-block; min-width: 64px; padding: 2px 8px; border-radius: 999px; text-align: center; font-size: 12px; }
    .done { background: #dcfce7; color: #166534; }
    .blocked { background: #fee2e2; color: #991b1b; }
    .risk { background: #fef3c7; color: #92400e; }
    .working { background: #dbeafe; color: #1e40af; }
  </style>
</head>
<body>
<main>
  <h1>Project Progress</h1>
  <p class="meta">Generated from logs/progress.jsonl.</p>
  <table>
    <thead><tr><th>Time</th><th>Stage</th><th>Status</th><th>Worker</th><th>Message</th><th>Files</th></tr></thead>
    <tbody>
"""
        + body
        + """
    </tbody>
  </table>
</main>
</body>
</html>
""",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append logs/progress.jsonl and render a static progress page.")
    parser.add_argument("--log", default="logs/progress.jsonl", help="Progress JSONL path.")
    parser.add_argument("--stage", default="", help="Current stage, e.g. parsing, modeling, writing.")
    parser.add_argument("--status", default="working", help="working, done, blocked, risk, etc.")
    parser.add_argument("--message", default="", help="Progress message to append.")
    parser.add_argument("--worker", default="", help="Worker or role name.")
    parser.add_argument("--files", default="", help="Comma-separated touched or relevant files.")
    parser.add_argument("--meta", default="", help="Optional JSON object with extra fields.")
    parser.add_argument("--render", action="store_true", help="Render progress.html after reading/appending events.")
    parser.add_argument("--html", default="progress.html", help="Rendered HTML output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log_path = Path(args.log).expanduser()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    should_append = any([args.stage, args.message, args.worker, args.files])
    if should_append:
        event = {
            "time": now_iso(),
            "stage": args.stage,
            "status": args.status,
            "worker": args.worker,
            "message": args.message,
            "files": split_csv(args.files),
        }
        if args.meta:
            try:
                meta = json.loads(args.meta)
                if isinstance(meta, dict):
                    event.update(meta)
                else:
                    event["meta"] = meta
            except json.JSONDecodeError:
                event["meta"] = args.meta
        with log_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
        print(f"Appended progress event to: {log_path}")

    events = read_jsonl(log_path)
    if args.render:
        html_path = Path(args.html).expanduser()
        render_html(events, html_path)
        print(f"Rendered progress page: {html_path}")
    if not should_append and not args.render:
        print(f"Progress events: {len(events)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
