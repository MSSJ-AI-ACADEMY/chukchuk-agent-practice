import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

inbox = Path("inbox")
if not inbox.is_dir():
    print("inbox 폴더를 찾지 못했습니다. "
          "작업실에서 켰는지 확인하세요.")
    raise SystemExit(0)

files = sorted(inbox.glob("*.md"))
print(f"inbox 메모 {len(files)}개")
for f in files:
    text = f.read_text(encoding="utf-8-sig")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    links = text.count("http://") + text.count("https://")
    if lines:
        title = lines[0].lstrip("# ").strip()
    else:
        title = "(빈 파일)"
    print(f"- {f.name} | {title} | "
          f"내용 {len(lines)}줄 | 링크 {links}개")
