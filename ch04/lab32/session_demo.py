"""session_demo.py - 이어 하기·갈라 보기·재시도 시험(실습 32)"""
import asyncio
import sys

from claude_agent_sdk import ClaudeAgentOptions

from runlog import last_session_id, run_with_retry

# 실습 31에서 배운 두 한도
LIMITS = {"max_turns": 8, "max_budget_usd": 0.50}

FIRST = (
    "inbox/ 폴더의 메모를 모두 읽고, "
    "메모마다 한 줄로 요약해 줘. 파일은 고치지 마."
)
FOLLOW = (
    "방금 요약한 메모 중 가장 급한 할 일 하나만 "
    "골라서 이유와 함께 말해 줘."
)
FORK = (
    "이번에는 반대로, 가장 미뤄도 되는 일 하나를 "
    "골라서 이유와 함께 말해 줘."
)


async def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "first"
    opts = dict(
        model="claude-sonnet-5",
        tools=["Read", "Glob", "Grep"],
        allowed_tools=["Read", "Glob", "Grep"],
        permission_mode="dontAsk",
        **LIMITS,
    )
    prompt = FIRST

    if cmd in ("resume", "fork"):
        opts["resume"] = last_session_id()
        prompt = FOLLOW if cmd == "resume" else FORK
        if cmd == "fork":
            opts["fork_session"] = True
    elif cmd == "broken":
        opts["env"] = {"ANTHROPIC_API_KEY": "wrong-key-for-test"}

    options = ClaudeAgentOptions(**opts)
    result = await run_with_retry(prompt, options)
    if result is None:
        print("끝내 실패했습니다. "
              "logs/sessions.jsonl을 확인하세요.")
    else:
        print(result.result)
        sid, why = result.session_id, result.subtype
        print("세션:", sid, "| 끝난 이유:", why)


asyncio.run(main())
