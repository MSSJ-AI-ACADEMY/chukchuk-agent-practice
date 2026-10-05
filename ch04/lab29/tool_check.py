"""tool_check.py - save_report 를 혼자 불러 본다(요금 없음)"""
import asyncio
from chukchuk_tools import save_report


async def main():
    tries = [
        ("2000-01-01.md", "# 시험 브리핑"),
        ("2000-01-01.md", "한 번 더"),
        ("../evil.md", "x"),
        ("2000-01-01.txt", "x"),
        ("2000-01-02.md", "   "),
    ]
    for name, text in tries:
        args = {"filename": name, "content": text}
        result = await save_report.handler(args)
        print(name, "→", result["content"][0]["text"])


asyncio.run(main())
