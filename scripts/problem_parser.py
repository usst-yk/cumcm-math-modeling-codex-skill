#!/usr/bin/env python3
"""Rule-based CUMCM problem statement parser.

The parser is intentionally lightweight and offline. It extracts a first-pass
task map that Codex can refine later.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHINESE_NUM = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}

RISK_WORDS = [
    "全部",
    "所有",
    "每个",
    "分别",
    "连续",
    "至少",
    "不超过",
    "不低于",
    "最大",
    "最小",
    "最优",
    "预测",
    "评价",
    "排序",
    "分类",
    "调度",
    "分配",
    "规划",
    "约束",
    "附件",
    "表",
    "给出",
    "比较",
    "检验",
    "分析",
    "灵敏度",
]

OUTPUT_WORDS = [
    "预测",
    "给出",
    "求",
    "计算",
    "确定",
    "设计",
    "评价",
    "排序",
    "分类",
    "比较",
    "分析",
    "建立",
    "绘制",
    "提出",
]

CONSTRAINT_WORDS = [
    "不超过",
    "不低于",
    "至少",
    "至多",
    "必须",
    "要求",
    "约束",
    "满足",
    "限制",
    "全部",
    "所有",
    "每个",
    "连续",
]

TASK_TYPE_KEYWORDS = [
    ("prediction", ["预测", "预报", "趋势", "回归", "时间序列", "未来"]),
    ("optimization", ["最优", "优化", "规划", "调度", "分配", "路径", "选址", "最小", "最大", "成本最小", "收益最大"]),
    ("evaluation", ["评价", "排序", "排名", "指标", "综合得分", "优先级"]),
    ("simulation", ["仿真", "模拟", "传播", "演化", "扩散", "动态"]),
    ("classification", ["分类", "识别", "判别", "等级"]),
    ("clustering", ["聚类", "分群", "划分"]),
]

UNIT_RE = re.compile(
    r"(?:\d+(?:\.\d+)?\s*)?(?:元|万元|亿元|(?<!附)件|个|吨|千克|公斤|克|公里|千米|米|平方米|亩|公顷|小时|分钟|秒|天|日|周|月|年|%|百分比|人|辆|次|台)"
)
TIME_RE = re.compile(
    r"(?:\d{4}\s*[-至到]\s*\d{4}\s*年?|\d+\s*[-至到]\s*\d+\s*(?:天|日|周|月|年|小时)|连续\s*\d+\s*(?:天|日|周|月|年|小时)|每\s*(?:天|日|周|月|年|小时)|第\s*\d+\s*(?:天|日|周|月|年|小时)|\d{4}\s*年)"
)
ATTACHMENT_LABEL_RE = re.compile(
    r"(?:附件|附录|表)\s*[一二三四五六七八九十\dA-Za-z_-]+(?:\s*[：:]\s*[\w\u4e00-\u9fff.-]+\.(?:xlsx|xls|csv|txt|json|mat|zip))?",
    re.IGNORECASE,
)
FILE_RE = re.compile(r"[\w\u4e00-\u9fff.-]+\.(?:xlsx|xls|csv|txt|json|mat|zip)", re.IGNORECASE)
QUESTION_MARK_RE = re.compile(
    r"(?P<label>问题\s*[一二三四五六七八九十\d]+|第\s*[一二三四五六七八九十\d]+\s*问|Q\s*\d+|[（(]\s*\d+\s*[）)])",
    re.IGNORECASE,
)


def unique(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        clean = re.sub(r"\s+", " ", str(item)).strip("，。；;:：、 ")
        if clean and clean not in seen:
            seen.add(clean)
            out.append(clean)
    return out


def extract_attachments(text: str) -> list[str]:
    items = ATTACHMENT_LABEL_RE.findall(text)
    items.extend(FILE_RE.findall(text))
    cleaned = unique(items)
    expanded_labels = [item for item in cleaned if "：" in item or ":" in item]
    result = []
    for item in cleaned:
        if any(item != label and item in label for label in expanded_labels):
            continue
        result.append(item)
    return result


def expand_attachments(items: list[str], all_attachments: list[str]) -> list[str]:
    expanded = []
    for item in items:
        replacement = item
        for full in all_attachments:
            if full.startswith(f"{item}：") or full.startswith(f"{item}:"):
                replacement = full
                break
        expanded.append(replacement)
    return unique(expanded)


def label_to_id(label: str, fallback: int) -> str:
    digits = re.findall(r"\d+", label)
    if digits:
        return f"Q{int(digits[0])}"
    for char, value in CHINESE_NUM.items():
        if char in label:
            return f"Q{value}"
    return f"Q{fallback}"


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[。！？；;])\s*", text)
    return [p.strip() for p in parts if p.strip()]


def split_subquestions(text: str) -> list[dict]:
    matches = list(QUESTION_MARK_RE.finditer(text))
    if not matches:
        return [{"id": "Q1", "title": "Q1", "text": text.strip()}]

    sections = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        raw = text[start:end].strip()
        qid = label_to_id(match.group("label"), idx + 1)
        sections.append({"id": qid, "title": match.group("label").strip(), "text": raw})

    deduped = []
    seen_ids = set()
    for section in sections:
        qid = section["id"]
        if qid in seen_ids:
            qid = f"Q{len(deduped) + 1}"
            section["id"] = qid
        seen_ids.add(qid)
        deduped.append(section)
    return deduped


def extract_by_words(text: str, words: list[str]) -> list[str]:
    sentences = split_sentences(text)
    return unique([s for s in sentences if any(word in s for word in words)])


def infer_task_type(text: str) -> str:
    scores = []
    for task_type, words in TASK_TYPE_KEYWORDS:
        score = sum(text.count(word) for word in words)
        if score:
            scores.append((score, task_type))
    if not scores:
        return "unknown"
    scores.sort(reverse=True)
    return scores[0][1]


def infer_decision_object(text: str, task_type: str) -> str:
    patterns = [
        r"(?:预测|预报)\s*([^，。；;]{2,30})",
        r"(?:评价|排序|排名)\s*([^，。；;]{2,30})",
        r"(?:优化|确定|给出|设计)\s*([^，。；;]{2,30})",
        r"(?:分配|调度|规划)\s*([^，。；;]{2,30})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip("的 ")
    fallback = {
        "prediction": "待预测对象",
        "optimization": "待优化决策方案",
        "evaluation": "待评价对象",
        "simulation": "待仿真系统状态",
        "classification": "待分类对象",
        "clustering": "待分组对象",
    }
    return fallback.get(task_type, "")


def extract_implicit_scoring(text: str, task_type: str) -> list[str]:
    points = []
    if task_type == "prediction":
        points.extend(["baseline comparison", "error metric"])
    if task_type == "optimization":
        points.extend(["feasibility check", "constraint violation check", "baseline scheme comparison"])
    if task_type == "evaluation":
        points.extend(["indicator direction check", "ranking stability"])
    if "灵敏度" in text or "敏感" in text:
        points.append("sensitivity analysis")
    if "比较" in text:
        points.append("route or baseline comparison")
    if "图" in text or "可视化" in text:
        points.append("paper-ready figure")
    return unique(points)


def extract_parse(text: str, problem_id: str) -> dict:
    attachments = extract_attachments(text)
    units = unique(UNIT_RE.findall(text))
    time_ranges = unique(TIME_RE.findall(text))
    risk_words = [word for word in RISK_WORDS if word in text]
    sections = split_subquestions(text)

    subquestions = []
    warnings = []
    for section in sections:
        qtext = section["text"]
        task_type = infer_task_type(qtext)
        q_attachments = expand_attachments(extract_attachments(qtext), attachments) or attachments
        q_units = unique(UNIT_RE.findall(qtext))
        q_time_ranges = unique(TIME_RE.findall(qtext))
        q_risk_words = [word for word in RISK_WORDS if word in qtext]
        required_output = extract_by_words(qtext, OUTPUT_WORDS)
        constraints = extract_by_words(qtext, CONSTRAINT_WORDS)
        input_data = [f"attachment:{item}" for item in q_attachments]
        decision_object = infer_decision_object(qtext, task_type)
        q_warnings = []

        if task_type == "unknown":
            q_warnings.append("task_type 未能由规则判断")
        if not required_output:
            q_warnings.append("required_output 为空，需要人工确认")
        if not decision_object:
            q_warnings.append("decision_object 为空，需要人工确认")
        if not input_data:
            q_warnings.append("input_data 未识别到附件依赖")
        if not constraints:
            q_warnings.append("constraints 未识别到明确约束")

        subquestions.append(
            {
                "id": section["id"],
                "title": section["title"],
                "text": qtext,
                "task_type": task_type,
                "input_data": input_data,
                "required_output": required_output,
                "decision_object": decision_object,
                "constraints": constraints,
                "units": q_units,
                "time_ranges": q_time_ranges,
                "attachments": q_attachments,
                "implicit_scoring_points": extract_implicit_scoring(qtext, task_type),
                "risk_words": q_risk_words,
                "warnings": q_warnings,
            }
        )
        warnings.extend([f"{section['id']}: {w}" for w in q_warnings])

    return {
        "contest": "CUMCM",
        "problem_id": problem_id,
        "question_count": len(subquestions),
        "attachments": attachments,
        "units": units,
        "time_ranges": time_ranges,
        "risk_words": risk_words,
        "subquestions": subquestions,
        "warnings": warnings,
    }


def write_markdown(parse: dict, path: Path) -> None:
    lines = [
        "# Problem Parse",
        "",
        f"- Contest: {parse['contest']}",
        f"- Problem: {parse.get('problem_id', '')}",
        f"- Question count: {parse['question_count']}",
        f"- Attachments: {', '.join(parse['attachments']) or '未识别'}",
        f"- Units: {', '.join(parse['units']) or '未识别'}",
        f"- Time ranges: {', '.join(parse['time_ranges']) or '未识别'}",
        f"- Risk words: {', '.join(parse['risk_words']) or '未识别'}",
        "",
        "## Subquestions",
        "",
    ]
    for q in parse["subquestions"]:
        lines.extend(
            [
                f"### {q['id']} {q['title']}",
                "",
                f"- Task type: {q['task_type']}",
                f"- Decision object: {q['decision_object'] or '待确认'}",
                f"- Input data: {', '.join(q['input_data']) or '待确认'}",
                f"- Required output: {'; '.join(q['required_output']) or '待确认'}",
                f"- Constraints: {'; '.join(q['constraints']) or '待确认'}",
                f"- Units: {', '.join(q['units']) or '未识别'}",
                f"- Time ranges: {', '.join(q['time_ranges']) or '未识别'}",
                f"- Attachments: {', '.join(q['attachments']) or '未识别'}",
                f"- Implicit scoring: {', '.join(q['implicit_scoring_points']) or '待确认'}",
                f"- Risk words: {', '.join(q['risk_words']) or '未识别'}",
                f"- Warnings: {'; '.join(q['warnings']) or 'None'}",
                "",
            ]
        )
    lines.extend(["## Warnings", ""])
    lines.extend([f"- {w}" for w in parse["warnings"]] or ["- None"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse a CUMCM problem statement without external APIs.")
    parser.add_argument("--problem", required=True, help="Problem statement text or markdown file.")
    parser.add_argument("--output-dir", default="problem", help="Output directory.")
    parser.add_argument("--problem-id", default="", help="Problem id, e.g. 2026A.")
    args = parser.parse_args()

    problem_path = Path(args.problem).expanduser()
    text = problem_path.read_text(encoding="utf-8")
    parsed = extract_parse(text, args.problem_id)

    outdir = Path(args.output_dir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    json_path = outdir / "problem_parse.json"
    md_path = outdir / "problem_parse.md"
    json_path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(parsed, md_path)

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    if parsed["warnings"]:
        print("Warnings:")
        for warning in parsed["warnings"]:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
