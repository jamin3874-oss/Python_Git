# 공부주머니 · Study Pocket

특정 과목에 종속되지 않는 PDF 시험 공부 앱입니다. 여러 PDF를 모아 전체 노트를 만들고 질문을 이어갑니다. **HTML/CSS/JavaScript + Python 3.12 이상**으로 동작하며 프론트 프레임워크와 외부 CDN이 없습니다. PDF 파싱·그림 렌더링은 함께 제공하는 Mozilla PDF.js를 사용합니다.

## 실행

Node.js 22.13 이상과 Python 3.12 이상을 설치한 뒤 이 폴더에서 실행합니다. 별도 npm/pip 라이브러리 설치는 필요하지 않습니다.

```powershell
npm run build
python -B server.py
```

브라우저에서 `http://127.0.0.1:8788`을 엽니다. `run.ps1`도 동일한 작업을 합니다. HTTP 로컬호스트에서 PWA 개발이 가능하며 휴대폰 설치는 HTTPS 배포 주소를 사용하세요.

## 사용

1. 자료실에서 여러 PDF를 선택합니다. 각 150MB 이하이며 원본을 IndexedDB에 저장합니다.
2. API 설정에서 **본인의 Codyssey 키**와 사용 가능한 모델 ID를 입력합니다. 기본 모델 ID `claude-opus-4-8`은 기존 프로젝트 설정을 이어받은 값입니다. 실제 계정에서 지원하는지는 연결 확인으로 검증해야 합니다.
3. 공부 노트에서 원하는 설명 방식·분량·제외 범위 등을 적고 **PDF 전체로 공부 노트 만들기**를 누릅니다.
4. 전체 내용을 자동으로 읽고 계층적으로 연결한 단일 노트를 받습니다. 중단 후 같은 설정으로 이어갈 수 있습니다.
5. 작은 손글씨는 원본 보기에서 영역을 드래그해 확대 판독하고, 수정 후 다음 전체 노트에 반영합니다.
6. AI 대화에서 일반 질문 또는 선택한 완성 노트에 관한 후속 질문을 보냅니다.
7. 잘못 올린 PDF는 파일 옆 ×로 삭제합니다. 그 자료가 포함된 통합 노트·진행 기록·프로젝트 대화도 제거합니다. PC 원본 파일은 삭제하지 않습니다.

## API 키

브라우저에 입력한 키는 현재 탭 메모리에만 있습니다. localStorage·IndexedDB·내보내기·소스에 저장하지 않습니다. AI 실행 시 이 앱의 서버를 거쳐 고정 주소 `https://copa.codyssey.kr/v1/messages`에 전달합니다. Anthropic Messages 규약의 `x-api-key`, `anthropic-version: 2023-06-01`을 사용합니다. 리디렉션과 자동 유료 재시도는 차단합니다.

공유 서비스는 방문자가 각자 키를 입력하는 방식이 기본입니다. 개인 서버 환경변수를 이용하려면 배포 환경에 `CODYSSEY_API_KEY`와 **충분히 긴 별도의 `STUDY_APP_ACCESS_TOKEN`을 둘 다** 설정하고 앱 설정의 서버 접근 암호에 후자를 입력합니다. 서버 키만 설정한 공개 앱에서는 익명 방문자가 그 키를 사용할 수 없습니다. 키·접근 암호는 GitHub나 이 문서에 넣지 마세요. PC 환경변수는 Vercel이나 Sites로 자동 복사되지 않습니다.

## 모바일 설치·저장

- Android Chrome: 메뉴 → 앱 설치/홈 화면에 추가.
- iPhone Safari: 공유 → 홈 화면에 추가.
- PWA manifest, 192/512px 아이콘, maskable 아이콘, 서비스 워커, 모바일 하단 메뉴 및 safe area를 포함합니다.
- 앱 셸과 저장된 노트는 설치·최초 로딩 이후 오프라인에서 열 수 있습니다. PDF.js의 추가 폰트/압축 해독 리소스는 한 번 사용해 캐시한 이후 오프라인 사용이 가능하며, 모든 형식의 PDF 오프라인 렌더링을 보장하지 않습니다.
- PDF·노트·대화는 **이 기기의 브라우저**에 저장됩니다. 계정 및 기기 간 자동 동기화는 없습니다. 브라우저 데이터 삭제·저장 용량 부족·OS의 저장소 정리로 자료가 사라질 수 있어 노트 다운로드를 권장합니다.
- 앱 공유는 사이트 주소만 공유합니다. 다른 사람에게 내 PDF와 노트가 자동 공개되지 않습니다.

## 전체 PDF 처리 구조와 한계

PDF 원본 저장 때 모든 페이지 이미지를 미리 생성하거나 서버로 올리지 않습니다. 분석 시작 때 쪽수를 확인하고 필요한 페이지를 순서대로 렌더링합니다. 한 요청당 최대 4쪽, 이미지 합계 2.35MB, 요청 JSON 3.8MB로 제한합니다. 전체 쪽수에는 150쪽 같은 고정 중단 조건이 없습니다. 중간 노트를 최대 4개·58,000자씩 통합하여 마지막 한 권으로 만듭니다. 501쪽 전체 흐름은 모의 모델로 검증했습니다.

완료한 묶음마다 IndexedDB에 체크포인트를 저장합니다. Web Locks로 같은 브라우저의 중복 AI 작업을 막고, 저장 직전 원본·요청 버전을 재검사합니다. 탭을 닫거나 휴대폰이 앱을 절전하면 실행이 중단될 수 있습니다. 응답 수신 후 저장 전에 앱이 종료되면 그 한 요청은 재실행될 수 있습니다. 유료 요청을 서버 백그라운드에서 계속 돌리는 구조는 아닙니다.

기본 155 DPI, 정밀 200 DPI, 전체 페이지 긴 변 최대 2400px입니다. 작은 필기 영역은 원본에서 최대 300 DPI·1800px로 렌더링합니다. DPI는 픽셀 밀도이며 실제 인식 정확도를 보장하지 않습니다. 스캔 글자·필기·그림을 이미지로 보내는 비전 분석이며 별도의 Tesseract OCR 엔진을 사용하지 않습니다. 선명한 텍스트 레이어도 보조 입력으로 전달합니다. X는 사용자가 개인 범위 제외를 요청했을 때 적용하며 OX 문항 답과 구별하도록 지시합니다.

대용량 PDF는 기기 메모리와 저장 공간의 영향을 받습니다. 저사양 휴대폰에서 150MB 문서가 항상 열리는 것은 아닙니다. 수백 쪽은 여러 유료 호출이 필요하고 통합 과정에서 세부 정보가 요약될 수 있습니다.

## Vercel 배포

이 폴더를 GitHub 저장소 루트에 올리고 Vercel에서 Import합니다. Framework는 Other, Build Command는 `npm run build`, Output Directory는 `dist/public`입니다. `vercel.json`이 함께 제공됩니다. `/api/ai`는 `api/ai.py`로 처리합니다. Python 함수 최대 실행 시간을 300초로 선언했고 API 자체 타임아웃은 135초입니다. 실제 적용 가능 시간·요청 한도는 계정 플랜과 Vercel의 현재 설정에 따릅니다.

공식 참고: [Vercel Python runtime](https://vercel.com/docs/functions/runtimes/python), [Vercel configuration](https://vercel.com/docs/project-configuration/vercel-json), [MDN PWA 설치 조건](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable).

## 검사

```powershell
npm test
python -B -m unittest discover -s tests -p "test_*.py" -v
# 로컬 서버를 실행한 뒤:
python -B tests/http_check.py http://127.0.0.1:8788
```

JavaScript 27개, Python 14개 테스트가 모의 API로 검증합니다. 실제 키의 유효성, 모델 답변의 학습 정확도, 휴대폰 설치 완료는 별도 확인이 필요합니다.

`worker/api.mjs`와 빌드 시 생성하는 `dist/server/index.js`는 Sites용 추가 호스팅 어댑터입니다. Vercel에서는 사용하지 않습니다. `.openai/hosting.json`은 이 Sites 실행본의 식별 설정이며, 새로운 제출 저장소에 복사할 필요는 없습니다.

## 외부 라이브러리

`vendor/pdfjs/`는 기존 프로젝트에 설치되어 있던 `pdfjs-dist` 5.7.284의 legacy 호환 빌드을 복사한 정적 배포 파일입니다. Apache License 2.0이며 `vendor/pdfjs/LICENSE`를 포함합니다. 나머지 앱 런타임은 브라우저 API 및 Python 표준 라이브러리입니다.
