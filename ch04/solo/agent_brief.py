"""agent_brief.py - 목표만 주고 '척척이'가 검사하고 고치게 한다"""
import asyncio
from datetime import date
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    query,
)

from chukchuk import SYSTEM_PROMPT
from chukchuk_tools import chukchuk_server
from report_check import check_server

ROOT = Path(__file__).resolve().parent
GOAL = (
    "오늘은 {today}이다. inbox 의 메모로 오늘의 브리핑을 "
    "만들어 {today}.md 로 저장해. 저장한 뒤에는 "
    "check_report 로 검사하고, 문제가 나오면 고쳐서 "
    "이름 끝에 -2, -3 을 붙여 새로 저장한 다음 다시 검사해. "
    "통과하면 끝내고, 세 번 고쳐도 안 되면 멈춰."
)
SERVERS = {"chukchuk": chukchuk_server, "check": check_server}
ALLOWED = [
    "Read",
    "Glob",
    "mcp__chukchuk__save_report",
    "mcp__check__check_report",
]


async def main():
    today = date.today().isoformat()
    options = ClaudeAgentOptions(
        cwd=str(ROOT),
        model="claude-sonnet-5",
        system_prompt=SYSTEM_PROMPT,
        tools=["Read", "Glob"],
        mcp_servers=SERVERS,
        allowed_tools=ALLOWED,
        permission_mode="dontAsk",
        max_turns=20,
        max_budget_usd=0.50,
    )
    goal = GOAL.format(today=today)
    async for message in query(prompt=goal, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "name"):
                    print(f"도구: {block.name}")
        elif isinstance(message, ResultMessage):
            print(message.result)
            print(f"끝: {message.subtype}",
                  f"| 턴: {message.num_turns}")


asyncio.run(main())
