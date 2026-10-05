import json
import re
import sys

raw = sys.stdin.buffer.read().decode("utf-8").lstrip("\ufeff")
data = json.loads(raw)
command = data.get("tool_input", {}).get("command", "")

patterns = [
    r"\brm\b[^|;&\n]*\s-(?:[a-zA-Z]*[rR]|-recursive)",
    r"\b(remove-item|rm|ri|del|erase|rd|rmdir)\b"
    r"[^|;&\n]*\s-r(ecurse)?\b",
    r"\b(rmdir|rd|del|erase)\s+/s",
]
if any(re.search(p, command, re.IGNORECASE) for p in patterns):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            "폴더째 지우는 명령은 훅이 막습니다. "
            "파일을 하나씩 지우거나 사람에게 먼저 물어보세요."),
    }}))
sys.exit(0)
