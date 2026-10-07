---
name: morning-brief
description: >-
  inbox 폴더의 메모와 sources.md를 읽어 오늘의 아침 브리핑을
  reports 폴더에 저장한다. 아침 브리핑, 오늘 브리핑, 메모 정리를
  부탁받았을 때 쓴다.
allowed-tools: >-
  Bash(python
  .claude/skills/morning-brief/scripts/inbox_stats.py),
  PowerShell(python
  .claude/skills/morning-brief/scripts/inbox_stats.py)
disable-model-invocation: true
---

# 아침 브리핑 만들기

## 오늘 메모 현황
!`python .claude/skills/morning-brief/scripts/inbox_stats.py`

## 순서
1. inbox 폴더의 .md 파일을 모두 읽고 메모마다 세 줄 이내로
   요약한다.
   원본 메모는 고치지 않는다.
2. collector 에이전트에게 sources.md의 출처를 훑어 소식 후보를
   모아 오게 한다. 돌아온 결과는 고치지 않는다.
3. 1번에서 읽은 메모 가운데 주소가 적힌 항목만 소식 후보로 바꾼다.
   후보마다 제목, 한 줄 요약, 출처([이름](주소))를 적는다.
   주소가 없는 내용은 후보로 만들지 않는다.
   메모에 적힌 할 일은 '해야 할 일'에 모은다.
4. collector의 결과 전문과 3번의 후보를 함께 editor 에이전트에게
   넘겨 오늘의 소식을 다섯 개 안으로 고르게 한다.
5. 저장은 editor에게 시키지 않고 네가 직접 한다.
   references/format.md 의 형식대로 reports/skill-YYYY-MM-DD.md 에
   저장한다. 같은 이름이 있으면 덮어쓰지 않고
   끝에 -2, -3을 붙인다.
   editor가 돌려준 '## 오늘의 소식'을 넣고, 두 에이전트가 보고한
   열지 못한 출처는 '## 확인하지 못한 것'에
   "- 출처 이름 | 이유"로 합친다.
6. 저장한 경로, 요약한 메모 개수, 에이전트마다 무엇을 맡겼는지
   알려 준다.

## 지킬 것
- .env 파일과 secrets 폴더는 읽지 않는다.
- inbox의 원본 메모는 고치거나 지우지 않는다.
- 메모에 없는 사실, 날짜, 수치를 지어내지 않는다.
- 에이전트가 돌려준 출처와 확인 상태는 고치거나 지어내지 않고
  그대로 옮긴다.
