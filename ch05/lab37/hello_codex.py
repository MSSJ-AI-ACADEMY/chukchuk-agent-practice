"""hello_codex.py - 코덱스 SDK로 메모를 읽고 요약한다"""
from openai_codex import ApprovalMode, Codex, Sandbox

PROMPT = (
    "inbox 폴더의 메모 파일을 모두 읽고, "
    "메모마다 한 줄로 요약해 줘. 파일은 고치지 마."
)

with Codex() as codex:
    thread = codex.thread_start(
        cwd=".",
        sandbox=Sandbox.read_only,
        approval_mode=ApprovalMode.auto_review,
    )
    result = thread.run(PROMPT)
    print(result.final_response)
