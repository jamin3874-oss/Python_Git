# 국내 여행지 추천 프로그램 README

날짜를 입력하면 Gemini(LLM)가 여행하기 좋은 국내 지역을 추천하고, Kakao Local API로 해당 지역의 맛집을 검색한 뒤, 최종 여행 리포트(Markdown)를 자동으로 생성하는 CLI 프로그램입니다.

# 1. 사용 API

| 역할 | 제공자 | 비고 |
| --- | --- | --- |
| LLM API | Google Gemini (`gemini-3.6-flash`) | 1차 추천 JSON 생성 + 최종 리포트 Markdown 생성 |
| 지도/장소 검색 API | Kakao Local (Keyword Search) | 지역명 기반 맛집 검색 |

# 2. 설치

```bash
pip install requests python-dotenv
```

Python 3.10 이상이 필요합니다.

# 3. API 키 설정 방법 (필수)

**API 키는 절대 코드에 직접 작성하지 마세요.** 프로젝트 폴더에 `.env` 파일을 만들어 관리합니다.

`api.py`와 같은 폴더에 `.env` 파일을 만들고 아래처럼 작성하세요.

```
GEMINI_API_KEY=여기에_발급받은_제미나이_키
KAKAO_REST_API_KEY=여기에_발급받은_카카오_REST_API_키
```

- `=` 앞뒤로 공백을 넣지 않습니다.
- 따옴표는 넣지 않아도 됩니다.
- `.env` 파일은 절대 깃허브에 올리거나 다른 사람에게 공유하지 않습니다.

## 키를 얻는 곳

- **Gemini API 키**: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey) 에서 "Create API key" 클릭
- **Kakao REST API 키**:
    1. [https://developers.kakao.com](https://developers.kakao.com) 접속 → 로그인
    2. "내 애플리케이션" → "애플리케이션 추가하기"로 앱 생성
    3. 생성한 앱 → "앱 키" 메뉴에서 REST API 키 복사
    4. **주의**: 앱을 만든 것만으로는 검색이 안 됩니다. 왼쪽 메뉴의 "제품 설정" → "카카오맵"에서 활성화 설정을 ON으로 켜야 정상 작동합니다. (켜지 않으면 `NotAuthorizedError` 발생)

## 왜 `.env`를 쓰나요?

- 코드나 결과물에 키가 그대로 노출되어 공유 중 실수로 유출되는 것을 방지합니다.
- 키를 교체해도 코드를 수정할 필요가 없습니다.
- 과금이 걸린 서비스에서 사고를 예방합니다.

이 프로젝트의 README, 로그, `results/` 폴더 안 어떤 파일에도 실제 API 키 값이 포함되어서는 안 됩니다.

# 4. 실행 방법

```bash
python api.py --date "2026-03-15"
```

`--date`는 필수 옵션이며, `YYYY-MM-DD` 형식이 아니면 안내 메시지를 출력하고 종료합니다.

## 실행 예시

```
python api.py --date "2026-03-15"

{
    "recommended_city": "전라남도 광양시",
    "weather": "...",
    "events": ["광양매화축제", "..."],
    "reason": "..."
}
---
<class 'dict'>
전라남도 광양시
---
200
[ ... 맛집 5곳 ... ]
=== 최종 리포트 ===
# 2026-03-15 국내 여행 추천 리포트
...
results 폴더 생성 완료 (또는 이미 있음)
저장 완료: results\2026-03-15_travel_data.json
저장 완료: results\2026-03-15_travel_plan.md
```

# 5. 결과물 확인 방법

실행이 끝나면 `results/` 폴더에 아래 두 파일이 생성됩니다.

- `results/{date}_travel_data.json` — 1차 추천 결과(`recommendation`), 맛집 검색 결과(`restaurants`, 0건 가능), 오류 목록(`errors`)이 담긴 원본 데이터
- `results/{date}_travel_plan.md` — 추천 지역, 추천 이유, 날씨, 행사/축제, 맛집 리스트, 1일 일정 제안, 오류 요약이 담긴 최종 리포트

# 6. 오류 처리 정책

| 상황 | 동작 |
| --- | --- |
| `GEMINI_API_KEY` 또는 `KAKAO_REST_API_KEY` 미설정 | 프로그램 즉시 종료 + 설정 방법 안내 출력 |
| `--date` 형식이 `YYYY-MM-DD`가 아님 | 사용법 안내 출력 후 즉시 종료 |
| Kakao Local 인증 실패(401/403) | 맛집 섹션을 "데이터 없음"으로 처리하고 리포트 생성은 계속 진행 |
| Kakao Local 검색 결과 0건 | 프로그램 중단 없이 "데이터 없음"으로 다음 단계 진행 |
| Gemini 1차 추천 JSON 파싱 실패 | 순수 JSON만 다시 출력하도록 프롬프트를 수정해 최대 1회 재시도 |
| Gemini 리포트 생성 응답 이상(candidates 없음 등) | 최대 1회 재시도 |

발생한 모든 오류는 내부적으로 누적되어 원본 JSON의 `errors` 배열과 최종 리포트의 `## 오류 요약(errors)` 섹션에 함께 기록됩니다 (오류가 없으면 빈 배열 / "없음"으로 표기).

# 7. 프로젝트 구조

```
Python_API 활용/
├── api.py             # 메인 CLI 프로그램
├── .env                # 환경변수 (실제 키 값, 절대 공유 금지)
├── README.md           # 본 문서
└── results/             # 실행 결과 저장 폴더 (자동 생성)
```