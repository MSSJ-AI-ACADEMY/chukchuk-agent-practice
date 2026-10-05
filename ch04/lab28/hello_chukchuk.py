import asyncio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    query,
)


async def main():
    async for message in query(
        prompt=(
            "inbox 폴더의 메모 파일을 모두 읽고, "
            "메모마다 한 줄로 요약해 줘. 파일은 고치지 마."
        ),
        options=ClaudeAgentOptions(
            # 쓸 모델(정하지 않으면 비싼 기본 모델)
            model="claude-sonnet-5",
            # 쓸 수 있는 도구: 읽기와 파일 찾기뿐
            tools=["Read", "Glob"],
            # 그 둘은 묻지 않고 쓴다
            allowed_tools=["Read", "Glob"],
            # 지금 폴더(작업실)에서 일한다
            cwd=".",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"도구: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"끝: {message.subtype}")


asyncio.run(main())
