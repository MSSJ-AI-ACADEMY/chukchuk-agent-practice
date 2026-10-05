"""report_check.py - 저장한 브리핑을 검사하는 도구(4장)"""
from pathlib import Path
from typing import Any

from claude_agent_sdk import create_sdk_mcp_server, tool

ROOT = Path(__file__).resolve().parent
HEADS = [
    "# 아침 브리핑",
    "## 한 줄 요약",
    "## 오늘의 소식",
    "## 메모별 요약",
    "## 해야 할 일",
    "## 출처",
    "## 확인하지 못한 것",
]
SUMMARY_MAX = 40   # 한 줄 요약은 40자까지


def _text(message: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": message}]}


def head_lines(lines):
    """제목마다 몇째 줄에 있는지(없으면 -1)."""
    found = []
    for h in HEADS:
        hits = [i for i, l in enumerate(lines) if l.startswith(h)]
        found.append(hits[0] if hits else -1)
    return found


def problems(text: str) -> list[str]:
    found = []
    lines = text.splitlines()
    pos = head_lines(lines)
    for h, p in zip(HEADS, pos):
        if p < 0:
            found.append(f"제목이 없음: {h}")
    if all(p >= 0 for p in pos) and pos != sorted(pos):
        found.append("제목 순서가 다름")
    if pos[1] >= 0:
        body = [l for l in lines[pos[1] + 1:] if l.strip()]
        n = len(body[0].strip()) if body else 0
        if n > SUMMARY_MAX:
            found.append(f"한 줄 요약이 {n}자"
                         f"(최대 {SUMMARY_MAX}자)")
    memos = len(list((ROOT / "inbox").glob("*.md")))
    if pos[3] >= 0:
        later = [p for p in pos[4:] if p > pos[3]]
        part = lines[pos[3]:later[0] if later else len(lines)]
        items = [l for l in part if l.startswith("- [")]
        if len(items) != memos:
            found.append(f"메모별 요약 {len(items)}개"
                         f"(메모 {memos}개)")
    return found


@tool(
    "check_report",
    "reports 폴더에 저장한 브리핑 하나를 검사한다. 문제가 없으면 "
    "'통과'를, 있으면 문제 목록을 돌려준다.",
    {"filename": str},
)
async def check_report(args: dict[str, Any]) -> dict[str, Any]:
    name = args["filename"].strip()
    target = (ROOT / "reports" / name).resolve()
    if target.parent != ROOT / "reports" or not target.exists():
        return _text(f"reports/{name} 이 없습니다.")
    found = problems(target.read_text(encoding="utf-8"))
    if not found:
        return _text(f"통과: reports/{name}")
    return _text("문제: " + " / ".join(found))


check_server = create_sdk_mcp_server(
    name="check", version="1.0.0", tools=[check_report]
)
