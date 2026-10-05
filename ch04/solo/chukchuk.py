"""chukchuk.py - 아침 브리핑 비서 '척척이'(4장 완성본)"""
import argparse
import asyncio
import sys
from datetime import date
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions

import runlog
from chukchuk_tools import REPORTS_DIR, chukchuk_server
from runlog import run_with_retry

ROOT = Path(__file__).resolve().parent
# runlog.py 는 상대 경로를 쓴다. 어디서 실행해도
# chukchuk-agent/logs 에 쌓이게 고정한다.
runlog.LOG = ROOT / "logs" / "sessions.jsonl"

# 척척 실습 31·32에서 정한 한도. 설치한 SDK에 없는 옵션은
# build_options 에서 자동으로 뺀다.
LIMITS = {"max_turns": 8, "max_budget_usd": 0.50}
# 쓸 수 있는 기본 도구는 읽기뿐. 저장은 save_report 로만 한다.
TOOLS = ["Read", "Glob"]

SYSTEM_PROMPT = """너는 아침 브리핑 비서 '척척이'다.
- 입력은 지정된 inbox 폴더의 메모와 sources.md 뿐이다.
  웹에는 접속하지 않는다.
- 없는 사실을 지어내지 않는다. 모르면 '[확인 필요]'라고 쓴다.
- 브리핑 제목은 이 순서로 쓴다.
  '# 아침 브리핑 YYYY-MM-DD'
  '## 한 줄 요약'
  '## 오늘의 소식'
  '## 메모별 요약'
  '## 해야 할 일'
  '## 출처'
  '## 확인하지 못한 것'
- '## 오늘의 소식'은 주소가 적힌 소식만 최대 5개, 이 꼴로 쓴다.
  '1. 제목 — 한 줄 설명 ([출처 이름](주소))'
  5개가 안 되면 있는 만큼만 쓰고
  이유를 '## 확인하지 못한 것'에 적는다.
- '## 메모별 요약'은 '- [파일명] 요약' 꼴로 쓰고
  메모를 빠뜨리지 않는다.
- 다 쓰면 save_report 도구로 저장하고,
  저장 결과를 한 줄로 알린다."""

# 종료 코드: 0 성공 / 1 끝내 실패 / 2 인자 오류
#            3 한도 초과 / 4 저장 확인 실패
EXIT_OK, EXIT_FAILED, EXIT_ARGS = 0, 1, 2
EXIT_LIMIT, EXIT_NOT_SAVED = 3, 4


def parse_args():
    parser = argparse.ArgumentParser(
        description="아침 브리핑 비서 '척척이'")
    parser.add_argument(
        "--inbox", default="inbox",
        help="메모 폴더(chukchuk-agent 안의 폴더, 기본 inbox)")
    parser.add_argument(
        "--max-turns", type=int, default=LIMITS["max_turns"],
        help=f"최대 턴 수(기본 {LIMITS['max_turns']})")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="API를 부르지 않고 계획만 출력")
    return parser.parse_args()


def next_report_name(today):
    """오늘 날짜 파일명. 이미 있으면 -2, -3 을 붙인다
    (save_report 이름 규칙과 같음)."""
    name, n = f"{today}.md", 1
    while (REPORTS_DIR / name).exists():
        n += 1
        name = f"{today}-{n}.md"
    return name


def build_options():
    supported = ClaudeAgentOptions.__dataclass_fields__
    return dict(
        cwd=str(ROOT),
        model="claude-sonnet-5",
        system_prompt=SYSTEM_PROMPT,
        tools=TOOLS,
        mcp_servers={"chukchuk": chukchuk_server},
        allowed_tools=TOOLS + ["mcp__chukchuk__save_report"],
        permission_mode="dontAsk",
        **{k: v for k, v in LIMITS.items() if k in supported},
    )


def fail(message, code):
    print(message, file=sys.stderr)
    return code


async def main():
    args = parse_args()

    inbox = (ROOT / args.inbox).resolve()
    if ROOT not in inbox.parents and inbox != ROOT:
        msg = f"--inbox 는 {ROOT} 안의 폴더여야 합니다."
        return fail(msg, EXIT_ARGS)
    if args.max_turns < 1:
        msg = "--max-turns 는 1 이상이어야 합니다."
        return fail(msg, EXIT_ARGS)
    if not list(inbox.glob("*.md")):
        print(f"{inbox.name}/ 에 메모(.md)가 없습니다. "
              "메모를 넣고 다시 실행하세요.")
        return EXIT_OK

    today = date.today().isoformat()
    filename = next_report_name(today)
    rel_inbox = inbox.relative_to(ROOT).as_posix() or "."
    prompt = (
        f"오늘은 {today}이다. {rel_inbox}/ 의 메모를 모두 읽고 "
        "sources.md 도 참고해 브리핑을 만들어 "
        f"{filename} 로 저장해줘."
    )
    options = build_options()
    options["max_turns"] = args.max_turns

    if args.dry_run:
        print("[dry-run] 저장할 파일:", f"reports/{filename}")
        print("[dry-run] 프롬프트:", prompt)
        limits = {k: options[k] for k in LIMITS if k in options}
        print("[dry-run] 한도:", limits)
        return EXIT_OK

    agent_options = ClaudeAgentOptions(**options)
    result = await run_with_retry(prompt, agent_options)
    if result is None:
        msg = ("끝내 실패했습니다. "
               "logs/sessions.jsonl 을 확인하세요.")
        return fail(msg, EXIT_FAILED)
    print(result.result or "")
    sid, why = result.session_id, result.subtype
    print("세션:", sid, "| 끝난 이유:", why)
    if result.subtype in runlog.LIMIT_SUBTYPES:
        msg = ("한도에 걸려 중단됐습니다. "
               "--max-turns 를 올리거나 지시를 줄이세요.")
        return fail(msg, EXIT_LIMIT)
    if not (REPORTS_DIR / filename).exists():
        msg = f"reports/{filename} 이 생기지 않았습니다."
        return fail(msg, EXIT_NOT_SAVED)
    print(f"완료: reports/{filename}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
