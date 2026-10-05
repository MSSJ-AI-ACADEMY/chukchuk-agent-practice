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
(4단계의 요청 전문을 여기에)
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
