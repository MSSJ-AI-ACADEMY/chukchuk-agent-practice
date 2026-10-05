import json
import sys
from datetime import datetime
from pathlib import Path

raw = sys.stdin.buffer.read().decode("utf-8").lstrip("\ufeff")
data = json.loads(raw)
tool = data.get("tool_name", "")
file_path = data.get("tool_input", {}).get("file_path", "")
project = Path(data.get("cwd", ".")).resolve()

if file_path:
    target = Path(file_path)
    if not target.is_absolute():
        target = project / target
    try:
        rel = target.resolve().relative_to(project)
    except ValueError:
        rel = None
    if (rel is not None and rel.parts
            and rel.parts[0] == "reports"):
        (project / "logs").mkdir(exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = project / "logs" / "report-log.txt"
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"{now} | {tool} | {rel.as_posix()}\n")
sys.exit(0)
