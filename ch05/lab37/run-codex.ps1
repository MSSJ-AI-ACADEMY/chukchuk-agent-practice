# 코덱스로 오늘의 브리핑을 받는 스크립트.
# 작업실 파일이 바뀌면 실패로 끝낸다.
Set-Location "$HOME\chukchuk-agent"
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force reports, logs | Out-Null

$Date = Get-Date -Format "yyyy-MM-dd"
$Out = "reports\codex-$Date.md"; $n = 2
while (Test-Path $Out) {
    $Out = "reports\codex-$Date-$n.md"; $n++
}
$Log = "logs\codex-$Date.log"
$PromptFile = "logs\codex-prompt.txt"

$Prompt = @"
너는 내 아침 브리핑 비서 '척척이'야.
inbox/ 폴더의 .md 파일(지금은 memo-01.md, memo-02.md,
memo-03.md)을 모두 읽고, sources.md도 읽어서
오늘의 브리핑을 만들어 줘.

형식(제목과 순서를 그대로):
# 아침 브리핑 $Date
## 한 줄 요약 — 오늘 메모 전체를 한 문장으로
## 오늘의 소식 — 메모와 sources.md에 주소가 적힌 소식만 최대 5개.
  "1. 제목 — 한 줄 설명 ([출처 이름](주소))" 꼴의 번호 목록.
  없으면 "없음"
## 메모별 요약 — 메모마다 "- [파일명] 요약(3줄 이내)"
## 해야 할 일 — 메모에 적힌 할 일만 "- [ ] " 체크리스트로
## 출처 — 이 브리핑에 쓴 주소를 그대로. 없으면 "없음"
## 확인하지 못한 것 — 열어 보지 않은 링크, 메모에 없는 내용,
  애매한 부분, 소식이 5개가 안 된 이유. 없으면 "없음"

조건:
- 메모와 sources.md에 없는 내용은 지어내지 마.
  소식 5개를 채우려고 지어내지도 마.
- 링크는 열어 보지 마.
  열어 보지 않은 주소는 메모나 sources.md에 적힌 설명만 써.
- 확실하지 않은 내용은 "[확인 필요]"로 표시해.
- 파일은 만들거나 수정하지 마. 브리핑 본문만 답변으로 출력해.
"@
$PromptPath = Join-Path (Get-Location) $PromptFile
[IO.File]::WriteAllText($PromptPath, $Prompt)

$Mine = "?? $Out", "?? $Log", "?? $PromptFile" |
    ForEach-Object { $_.Replace("\", "/") }
$Before = git status --porcelain --untracked-files=all |
    Where-Object { $Mine -notcontains $_ }
$Cmd = "codex exec --approve-for-me -o $Out - < $PromptFile"
cmd /c "$Cmd > $Log 2>&1"
$Status = $LASTEXITCODE
$After = git status --porcelain --untracked-files=all |
    Where-Object { $Mine -notcontains $_ }

if ($Status -ne 0) {
  $Msg = "실패: codex가 종료 코드 $Status 로 끝났습니다."
  Write-Host "$Msg 로그: $Log"
  exit $Status
}
if (-not (Test-Path $Out) -or (Get-Item $Out).Length -eq 0) {
  Write-Host "실패: 결과 파일이 없거나 비어 있습니다: $Out"
  exit 2
}
if ((@($Before) -join "`n") -ne (@($After) -join "`n")) {
  $Msg = "실패: 결과 파일 말고도 작업실 파일이 바뀌었습니다."
  Write-Host "$Msg git status 로 확인하세요."
  exit 3
}
Write-Host "성공: $Out"
