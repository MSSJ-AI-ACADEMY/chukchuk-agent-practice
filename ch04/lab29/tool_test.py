"""tool_test.py - save_report 하나만 붙여 보는 시험(실습 29)"""
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


async def main():
    today = date.today().isoformat()
    options = ClaudeAgentOptions(
        cwd=str(ROOT),
        model="claude-sonnet-5",
        tools=["Read"],
        mcp_servers={"chukchuk": chukchuk_server},
        allowed_tools=["Read", "mcp__chukchuk__save_report"],
    )
    prompt = (
        "inbox/memo-01.md 를 읽고 세 줄로 요약해서 "
        f"{today}.md 로 저장해 줘."
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
