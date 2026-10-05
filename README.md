# 《척척 에이전트》 실습 꾸러미

책 《척척 에이전트》의 실습에서 쓰는 파일을 장과 실습 번호별로 모아 둔 곳입니다. 책에 실린 코드와 글자 하나까지 같습니다.

## 받는 법

PowerShell에서 한 줄이면 됩니다(깃이 설치되어 있어야 합니다. 1장 1-3 참고).

```powershell
git clone https://github.com/MSSJ-AI-ACADEMY/chukchuk-agent-practice $env:USERPROFILE\chukchuk-practice
```

깃이 없으면 이 쪽 위의 초록 단추 **Code → Download ZIP**으로 받아 `내 홈\chukchuk-practice`에 풉니다.

## 쓰는 법

실습마다 책에 「예제 파일」 표시가 있습니다. 예를 들어 `ch04/lab28/hello_chukchuk.py`이면, 작업실(`chukchuk-agent`)에서 클로드 코드를 켜고 이렇게 시킵니다.

> 실습 꾸러미의 ch04/lab28/hello_chukchuk.py 를 작업실로 복사해 줘.

손으로 옮겨 적지 않아도 됩니다. 파일을 꺼내는 일도 '척척이'에게 맡기는 연습입니다.

`_home` 폴더에 든 파일은 작업실이 아니라 **내 홈 폴더**에 놓는 파일입니다(예: `_home/.codex/config.toml` → `내 홈\.codex\config.toml`).

## 폴더

| 폴더 | 장 |
|---|---|
| `ch02` | 2장 클로드 코드로 첫 에이전트 만들기 |
| `ch03` | 3장 클로드 코드 하네스 확장하기 |
| `ch04` | 4장 Agent SDK로 내 에이전트 코딩하기 |
| `ch05` | 5장 코덱스로 같은 에이전트 만들기 |

`labNN`은 책의 「척척 실습 NN」, `solo`는 그 장의 「혼자 해보기」입니다.

## 내 파일이 책과 같은지 확인하기

`manifest.json`에 파일마다 지문(sha256 앞 16자리)이 있습니다. 클로드 코드에 「manifest.json 의 지문과 내 작업실 파일을 비교해 줘」라고 시키면 됩니다.

## 알려 둘 것

- API 키나 토큰은 이 꾸러미에 없습니다. 키는 책의 안내대로 내 창에만 넣습니다.
- 책과 다른 점을 찾으면 이 저장소의 Issues에 남겨 주세요.
