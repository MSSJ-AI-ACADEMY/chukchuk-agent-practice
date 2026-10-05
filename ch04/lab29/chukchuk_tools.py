"""chukchuk_tools.py - '척척이'가 쓰는 나만의 도구"""
import re
from pathlib import Path
from typing import Any

from claude_agent_sdk import create_sdk_mcp_server, tool

# 이 파일이 있는 폴더(작업실) 안의 reports 만 쓴다
REPORTS_DIR = Path(__file__).resolve().parent / "reports"
# 받아 주는 이름: 2026-10-02.md 또는 2026-10-02-2.md
NAME_RULE = re.compile(r"^\d{4}-\d{2}-\d{2}(-\d+)?\.md$")


def _text(message: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": message}]}


def _error(message: str) -> dict[str, Any]:
    return {**_text(message), "is_error": True}


@tool(
    "save_report",
    "완성된 아침 브리핑을 reports 폴더에 마크다운 파일로 "
    "저장한다. filename은 YYYY-MM-DD.md 꼴(같은 날 두 번째부터는 "
    "YYYY-MM-DD-2.md)이어야 한다. 이미 있는 파일은 덮어쓰지 "
    "않는다. 본문을 다 쓴 뒤 마지막에 한 번만 부른다.",
    {"filename": str, "content": str},
)
async def save_report(args: dict[str, Any]) -> dict[str, Any]:
    filename = args["filename"].strip()
    content = args["content"]
    if not NAME_RULE.match(filename):
        return _error(
            f"파일 이름 '{filename}'은 규칙에 맞지 않습니다. "
            "YYYY-MM-DD.md 꼴로 다시 부르세요."
        )
    if not content.strip():
        return _error(
            "content가 비어 있습니다. "
            "브리핑 본문을 채워 다시 부르세요."
        )
    target = (REPORTS_DIR / filename).resolve()
    if target.parent != REPORTS_DIR:
        return _error("reports 폴더 밖에는 저장할 수 없습니다.")
    if target.exists():
        return _error(
            f"reports/{filename} 이 이미 있어 "
            "덮어쓰지 않았습니다. "
            "이름 끝에 -2를 붙여 다시 부르세요."
        )
    REPORTS_DIR.mkdir(exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return _text(f"저장했습니다: reports/{filename}")


chukchuk_server = create_sdk_mcp_server(
    name="chukchuk", version="1.0.0", tools=[save_report]
)
