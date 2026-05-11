#!/usr/bin/env python3
"""Append project progress events and optionally render/open progress.html."""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append(
                {
                    "time": "",
                    "stage": "parse_error",
                    "message": line,
                    "status": "invalid",
                    "retry_reason": f"logs/progress.jsonl line {line_number} is not valid JSON",
                }
            )
    return rows


def event_files(event: dict, *keys: str) -> list[str]:
    values = []
    for key in keys or ("files", "generated_files", "evidence"):
        files = event.get(key, [])
        if isinstance(files, list):
            values.extend(str(item) for item in files if str(item).strip())
        elif isinstance(files, str):
            values.extend(split_csv(files))
    return values


def link_path(value: str, html_dir: Path) -> str:
    path_text = value.strip()
    if not path_text:
        return ""
    path = Path(path_text)
    if path.is_absolute():
        try:
            path_text = str(path.resolve().relative_to(html_dir.resolve()))
        except ValueError:
            path_text = path.name
    normalized = path_text.replace("\\", "/")
    return "/".join(quote(part) for part in normalized.split("/"))


def files_html(event: dict, html_dir: Path) -> str:
    links = []
    for file_name in event_files(event, "files", "generated_files"):
        label = html.escape(file_name.replace("\\", "/"))
        href = html.escape(link_path(file_name, html_dir), quote=True)
        links.append(f'<a href="{href}">{label}</a>' if href else label)
    return ", ".join(links)


def short_field(event: dict, *names: str) -> str:
    values = [str(event.get(name, "")).strip() for name in names if str(event.get(name, "")).strip()]
    return " / ".join(values)


def current_stage(events: list[dict]) -> str:
    for event in reversed(events):
        stage = str(event.get("current_stage") or event.get("stage") or "").strip()
        if stage:
            return stage
    return "not started"


def read_task_plan(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    rows = []
    for item in payload.get("subquestions", []):
        revision = item.get("revision_status", {}) if isinstance(item.get("revision_status"), dict) else {}
        rows.append(
            {
                "id": str(item.get("id", "")),
                "status": str(item.get("status") or revision.get("state") or ""),
                "owner": str(revision.get("owner", "")),
                "next_action": str(revision.get("next_action", "")),
            }
        )
    return rows


def read_registry_summary(path: Path) -> dict[str, int | str]:
    if not path.exists():
        return {}
    counts: dict[str, int | str] = {"path": str(path)}
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                status = str(row.get("status", "unknown")).strip().lower() or "unknown"
                counts[status] = int(counts.get(status, 0)) + 1
                counts["total"] = int(counts.get("total", 0)) + 1
    except OSError:
        return {}
    return counts


def event_detail(event: dict) -> str:
    known = {
        "time",
        "stage",
        "current_stage",
        "status",
        "worker",
        "message",
        "files",
        "generated_files",
        "blocker",
        "blockers",
        "retry_reason",
        "score",
        "rubric_status",
        "evidence",
        "question",
        "agent_role",
        "event_type",
        "task",
        "step",
        "action",
        "owner",
        "next_action",
        "agent",
        "checkpoint",
        "attempt",
        "rework_round",
        "gate_id",
        "decision",
        "issue",
        "expected_fix",
        "target_rubric_item",
        "evidence_needed",
    }
    parts = []
    for key in (
        "question",
        "agent_role",
        "event_type",
        "task",
        "step",
        "action",
        "owner",
        "next_action",
        "agent",
        "checkpoint",
        "attempt",
        "rework_round",
        "gate_id",
        "decision",
        "issue",
        "expected_fix",
        "target_rubric_item",
        "evidence_needed",
    ):
        value = str(event.get(key, "")).strip()
        if value:
            parts.append(f"{key}: {value}")
    extras = {key: value for key, value in event.items() if key not in known and key not in {"task", "step", "action", "owner", "agent", "checkpoint"}}
    if extras:
        parts.append(json.dumps(extras, ensure_ascii=False, sort_keys=True))
    return "；".join(parts)


def render_html(
    events: list[dict],
    output: Path,
    task_plan: list[dict[str, str]] | None = None,
    registry_summary: dict[str, int | str] | None = None,
) -> None:
    status_class = {
        "done": "done",
        "blocked": "blocked",
        "revise": "blocked",
        "risk": "risk",
        "working": "working",
        "todo": "todo",
        "skipped": "todo",
        "invalid": "blocked",
    }
    rows = []
    html_dir = output.parent
    for event in reversed(events):
        status = str(event.get("status", "working"))
        css = status_class.get(status.lower(), "working")
        blocker = short_field(event, "blocker", "blockers", "retry_reason")
        rubric = short_field(event, "score", "rubric_status")
        detail = event_detail(event)
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(event.get('time', '')))}</td>"
            f"<td>{html.escape(str(event.get('current_stage') or event.get('stage', '')))}</td>"
            f"<td><span class=\"pill {css}\">{html.escape(status)}</span></td>"
            f"<td>{html.escape(str(event.get('worker', '')))}</td>"
            f"<td>{html.escape(str(event.get('message', '')))}</td>"
            f"<td>{html.escape(detail)}</td>"
            f"<td>{html.escape(blocker)}</td>"
            f"<td>{html.escape(rubric)}</td>"
            f"<td>{files_html(event, html_dir)}</td>"
            "</tr>"
        )
    body = "\n".join(rows) or '<tr><td colspan="9">No progress events yet.</td></tr>'
    recent_generated = []
    for event in reversed(events):
        for file_name in event_files(event, "generated_files"):
            label = html.escape(file_name.replace("\\", "/"))
            href = html.escape(link_path(file_name, html_dir), quote=True)
            recent_generated.append(f'<a href="{href}">{label}</a>' if href else label)
        if len(recent_generated) >= 8:
            break
    generated_html = ", ".join(recent_generated) if recent_generated else "No generated files recorded yet."
    task_plan_rows = []
    for row in task_plan or []:
        task_plan_rows.append(
            "<tr>"
            f"<td>{html.escape(row.get('id', ''))}</td>"
            f"<td>{html.escape(row.get('status', ''))}</td>"
            f"<td>{html.escape(row.get('owner', ''))}</td>"
            f"<td>{html.escape(row.get('next_action', ''))}</td>"
            "</tr>"
        )
    task_plan_html = "\n".join(task_plan_rows) or '<tr><td colspan="4">No task plan status loaded.</td></tr>'
    registry_items = []
    if registry_summary:
        for key, value in sorted(registry_summary.items()):
            if key == "path":
                continue
            registry_items.append(f"{html.escape(str(key))}: {html.escape(str(value))}")
    registry_html = "；".join(registry_items) if registry_items else "No registry summary loaded."
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="5">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Project Progress</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 1280px; margin: 0 auto; padding: 32px 20px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    .meta {{ margin: 0 0 24px; color: #64748b; }}
    .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 0 0 20px; }}
    .summary div {{ background: #fff; border: 1px solid #e5e7eb; padding: 12px; }}
    .label {{ display: block; color: #64748b; font-size: 12px; margin-bottom: 4px; }}
    .generated {{ background: #fff; border: 1px solid #e5e7eb; padding: 12px; margin: 0 0 20px; font-size: 14px; }}
    .task-grid {{ display: grid; grid-template-columns: minmax(280px, 1fr) minmax(280px, 1fr); gap: 12px; margin: 0 0 20px; }}
    .panel {{ background: #fff; border: 1px solid #e5e7eb; padding: 12px; }}
    .panel table {{ border: 0; }}
    .panel th, .panel td {{ padding: 7px 8px; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid #e5e7eb; background: #fff; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #e5e7eb; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid #e5e7eb; text-align: left; vertical-align: top; font-size: 14px; }}
    td:nth-child(5) {{ min-width: 320px; }}
    td:nth-child(6) {{ min-width: 180px; color: #475569; }}
    th {{ background: #f1f5f9; color: #334155; }}
    a {{ color: #2563eb; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .pill {{ display: inline-block; min-width: 64px; padding: 2px 8px; border-radius: 999px; text-align: center; font-size: 12px; }}
    .done {{ background: #dcfce7; color: #166534; }}
    .blocked {{ background: #fee2e2; color: #991b1b; }}
    .risk {{ background: #fef3c7; color: #92400e; }}
    .working {{ background: #dbeafe; color: #1e40af; }}
    .todo {{ background: #e5e7eb; color: #374151; }}
    @media (max-width: 760px) {{ .task-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
<main>
  <h1>Project Progress</h1>
  <p class="meta">Generated from logs/progress.jsonl.</p>
  <section class="summary">
    <div><span class="label">Current stage</span>{html.escape(current_stage(events))}</div>
    <div><span class="label">Events</span>{len(events)}</div>
    <div><span class="label">Last updated</span>{html.escape(str(events[-1].get("time", "")) if events else "")}</div>
    <div><span class="label">Refresh</span>Every 5 seconds while this file is open</div>
  </section>
  <section class="generated"><span class="label">Recent generated files</span>{generated_html}</section>
  <section class="task-grid">
    <div class="panel">
      <span class="label">Question status</span>
      <table>
        <thead><tr><th>Question</th><th>Status</th><th>Owner</th><th>Next action</th></tr></thead>
        <tbody>
{task_plan_html}
        </tbody>
      </table>
    </div>
    <div class="panel">
      <span class="label">Registry summary</span>
      {registry_html}
    </div>
  </section>
  <div class="table-wrap">
  <table>
    <thead><tr><th>Time</th><th>Stage</th><th>Status</th><th>Worker</th><th>Message</th><th>Details</th><th>Blocker / Retry</th><th>Score / Rubric</th><th>Files</th></tr></thead>
    <tbody>
{body}
    </tbody>
  </table>
  </div>
</main>
</body>
</html>
""",
        encoding="utf-8",
    )


def open_file(path: Path) -> None:
    target = path.expanduser().resolve()
    if sys.platform.startswith("win"):
        if hasattr(os, "startfile"):
            os.startfile(str(target))  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["powershell", "-NoProfile", "-Command", "Start-Process", str(target)])
        return
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.Popen([opener, str(target)])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append logs/progress.jsonl and render a static progress page.")
    parser.add_argument("--log", default="logs/progress.jsonl", help="Progress JSONL path.")
    parser.add_argument("--stage", default="", help="Current stage, e.g. parsing, modeling, writing.")
    parser.add_argument("--current-stage", default="", help="Explicit current stage label; defaults to --stage.")
    parser.add_argument("--status", default="working", help="working, done, blocked, risk, etc.")
    parser.add_argument("--message", default="", help="Progress message to append.")
    parser.add_argument("--worker", default="", help="Worker or role name.")
    parser.add_argument("--question", default="", help="Question id, e.g. Q1, Q2, or ALL.")
    parser.add_argument("--agent-role", default="", help="Agent role, e.g. supervisor, explorer, writer.")
    parser.add_argument("--event-type", default="", help="Event type, e.g. agent_start, gate, edit, verification.")
    parser.add_argument("--owner", default="", help="Owner responsible for the next action.")
    parser.add_argument("--next-action", default="", help="Next action or handoff note.")
    parser.add_argument("--attempt", default="", help="Attempt number for retry loops.")
    parser.add_argument("--rework-round", default="", help="Rework round identifier.")
    parser.add_argument("--evidence", default="", help="Comma-separated evidence files.")
    parser.add_argument("--gate-id", default="", help="Supervisor gate id, e.g. G5-validation.")
    parser.add_argument("--decision", default="", choices=["", "pass", "revise", "block"], help="Supervisor gate decision.")
    parser.add_argument("--issue", default="", help="Supervisor issue found at this gate.")
    parser.add_argument("--expected-fix", default="", help="Expected fix before recheck.")
    parser.add_argument("--target-rubric-item", default="", help="Rubric item affected by this gate.")
    parser.add_argument("--evidence-needed", default="", help="Evidence required to close a revise/block gate.")
    parser.add_argument("--files", default="", help="Comma-separated touched or relevant files.")
    parser.add_argument("--generated-files", default="", help="Comma-separated generated files; kept separate for dashboards.")
    parser.add_argument("--blocker", default="", help="Current blocker or revise reason.")
    parser.add_argument("--retry-reason", default="", help="Reason a stage is being retried.")
    parser.add_argument("--score", default="", help="Score or score gate summary, e.g. 16/20.")
    parser.add_argument("--rubric-status", default="", help="Rubric gate status, e.g. no-zero-items.")
    parser.add_argument("--meta", default="", help="Optional JSON object with extra fields.")
    parser.add_argument("--render", action="store_true", help="Render progress.html after reading/appending events.")
    parser.add_argument("--html", default="progress.html", help="Rendered HTML output path.")
    parser.add_argument("--task-plan", default="problem/task_plan.json", help="Task plan JSON used for dashboard summary.")
    parser.add_argument("--registry", default="results/result_registry.csv", help="Result registry CSV used for dashboard summary.")
    parser.add_argument("--no-render", action="store_true", help="Do not render progress.html after appending.")
    parser.add_argument("--open", action="store_true", help="Open the rendered progress.html in the default browser.")
    parser.add_argument("--watch", action="store_true", help="Keep rendering progress.html when the log changes.")
    parser.add_argument("--poll-seconds", type=float, default=2.0, help="Polling interval used by --watch.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log_path = Path(args.log).expanduser()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    should_append = any(
        [
            args.stage,
            args.current_stage,
            args.message,
            args.worker,
            args.question,
            args.agent_role,
            args.event_type,
            args.owner,
            args.next_action,
            args.attempt,
            args.rework_round,
            args.evidence,
            args.gate_id,
            args.decision,
            args.issue,
            args.expected_fix,
            args.target_rubric_item,
            args.evidence_needed,
            args.files,
            args.generated_files,
            args.blocker,
            args.retry_reason,
            args.score,
            args.rubric_status,
        ]
    )
    if should_append:
        if args.decision in {"revise", "block"}:
            missing = [
                name
                for name, value in [
                    ("--gate-id", args.gate_id),
                    ("--owner", args.owner),
                    ("--issue", args.issue),
                    ("--expected-fix", args.expected_fix),
                    ("--evidence-needed", args.evidence_needed),
                ]
                if not value.strip()
            ]
            if missing:
                raise SystemExit(
                    f"{args.decision} gate events require: " + ", ".join(missing)
                )
        if args.decision == "pass" and not (args.evidence.strip() or args.files.strip() or args.generated_files.strip()):
            raise SystemExit("pass gate events require --evidence, --files, or --generated-files.")
        event = {
            "time": now_iso(),
            "stage": args.stage,
            "current_stage": args.current_stage or args.stage,
            "status": args.status,
            "worker": args.worker,
            "question": args.question,
            "agent_role": args.agent_role,
            "event_type": args.event_type,
            "owner": args.owner,
            "next_action": args.next_action,
            "attempt": args.attempt,
            "rework_round": args.rework_round,
            "gate_id": args.gate_id,
            "decision": args.decision,
            "issue": args.issue,
            "expected_fix": args.expected_fix,
            "target_rubric_item": args.target_rubric_item,
            "evidence_needed": args.evidence_needed,
            "message": args.message,
            "files": split_csv(args.files),
            "generated_files": split_csv(args.generated_files),
            "evidence": split_csv(args.evidence),
            "blocker": args.blocker,
            "retry_reason": args.retry_reason,
            "score": args.score,
            "rubric_status": args.rubric_status,
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
    html_path = Path(args.html).expanduser()
    should_render = (should_append and not args.no_render) or args.render or args.open or args.watch
    task_plan_path = Path(args.task_plan).expanduser()
    registry_path = Path(args.registry).expanduser()
    if should_render:
        render_html(events, html_path, read_task_plan(task_plan_path), read_registry_summary(registry_path))
        print(f"Rendered progress page: {html_path}")
        if args.open:
            open_file(html_path)
            print(f"Opened progress page: {html_path}")
    if args.watch:
        last_signature = None
        try:
            while True:
                try:
                    stat = log_path.stat()
                    signature = (stat.st_mtime_ns, stat.st_size)
                except FileNotFoundError:
                    signature = None
                if signature != last_signature:
                    events = read_jsonl(log_path)
                    render_html(events, html_path, read_task_plan(task_plan_path), read_registry_summary(registry_path))
                    last_signature = signature
                    print(f"{now_iso()} rendered {len(events)} events")
                time.sleep(max(args.poll_seconds, 0.2))
        except KeyboardInterrupt:
            print("Stopped progress watcher.")
            return 0
    if not should_append and not args.render and not args.open and not args.watch:
        print(f"Progress events: {len(events)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
