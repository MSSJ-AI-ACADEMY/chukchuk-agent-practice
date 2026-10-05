"""chukchuk.py - 아침 브리핑 비서 '척척이'(4-2판)"""
import asyncio
from datetime import date
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    query,
)

from chukchuk_tools import chukchuk_server

ROOT = Path(__file__).resolve().parent

SYSTEM_PROMPT = """너는 아침 브리핑 비서 '척척이'다.
- 입력은 inbox 의 메모와 sources.md 뿐이다. 웹은 열지 않는다.
- 없는 사실을 지어내지 않는다. 모르면 '[확인 필요]'라고 쓴다.
- 제목은 이 순서로 쓴다.
  '# 아침 브리핑 YYYY-MM-DD'
  '## 한 줄 요약'
  '## 오늘의 소식'
  '## 메모별 요약'
  '## 해야 할 일'
  '## 출처'
  '## 확인하지 못한 것'
- '## 오늘의 소식'은 주소가 적힌 소식만 최대 5개, 이 꼴로 쓴다.
  '1. 제목 — 한 줄 설명 ([출처 이름](주소))'
  모자라면 있는 만큼만 쓰고 이유를 '## 확인하지 못한 것'에 적는다.
- '## 메모별 요약'은 '- [파일명] 요약' 꼴로 쓰고
  메모를 빠뜨리지 않는다.
- 다 쓰면 save_report 도구로 저장하고,
  저장 결과를 한 줄로 알린다."""


async def main():
    if not list((ROOT / "inbox").glob("*.md")):
        print("inbox 에 메모(.md)가 없습니다. "
              "메모를 넣고 다시 실행하세요.")
        return
    today = date.today().isoformat()
    options = ClaudeAgentOptions(
        cwd=str(ROOT),
        model="claude-sonnet-5",
        tools=["Read", "Glob"],
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"chukchuk": chukchuk_server},
        allowed_tools=[
            "Read", "Glob", "mcp__chukchuk__save_report",
        ],
    )
    prompt = (
        f"오늘은 {today}이다. inbox 의 메모를 모두 읽고 "
        f"브리핑을 만들어 {today}.md 로 저장해 줘."
    )
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"도구: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"끝: {message.subtype}")


asyncio.run(main())
