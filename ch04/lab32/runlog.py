"""runlog.py - 실행 기록과 재시도(척척 실습 32)"""
import asyncio
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ResultMessage,
    ToolUseBlock,
    query,
)

LOG = Path("logs/sessions.jsonl")
LIMIT_SUBTYPES = {"error_max_turns", "error_max_budget_usd"}


def now():
    return datetime.now().isoformat(timespec="seconds")


def append_log(record):
    LOG.parent.mkdir(exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def last_session_id():
    if not LOG.exists():
        return None
    lines = LOG.read_text(encoding="utf-8").splitlines()
    for line in reversed(lines):
        sid = json.loads(line).get("session_id")
        if sid:
            return sid
    return None


async def run_once(prompt, options):
    tools, result = [], None
    try:
        stream = query(prompt=prompt, options=options)
        async for message in stream:
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, ToolUseBlock):
                        tools.append(block.name)
            elif isinstance(message, ResultMessage):
                result = message
    except Exception:
        # 결과를 못 받았을 때만 진짜 실패로 봅니다
        if result is None:
            raise
    return result, tools


async def run_with_retry(prompt, options, tries=3, delay=2):
    error = "결과 없음"
    for attempt in range(1, tries + 1):
        try:
            result, tools = await run_once(prompt, options)
            ok = result is not None and (
                not result.is_error
                or result.subtype in LIMIT_SUBTYPES
            )
            if ok:
                append_log({
                    "time": now(),
                    "prompt": prompt[:40],
                    "session_id": result.session_id,
                    "subtype": result.subtype,
                    "turns": result.num_turns,
                    "tools": dict(Counter(tools)),
                    "cost_usd": result.total_cost_usd,
                })
                return result
            why = result.result if result else "없음"
            error = f"오류 결과: {why}"
        except Exception as e:
            error = f"{type(e).__name__}: {e}"
        print(f"시도 {attempt}/{tries} 실패 - {error}")
        if attempt < tries:
            await asyncio.sleep(delay * attempt)
    append_log({
        "time": now(),
        "prompt": prompt[:40],
        "subtype": "failed",
        "error": error,
    })
    return None
