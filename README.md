# Playwright 기반의 ITSCOPE 화면 분석 및 Audit 자동화

## 프로젝트 개요

### 기능 요약
- ITSCOPE 표준산출물(메뉴구조도)에 근거해 재활용성이 높은 Menu Tree JSON을 뽑아낸다.
- AI 기반의 도구를 활용해 최적의 프롬프트로 입력한 URL의 화면 분석을 요청/처리한다.
- *Playwright* (, *BrowserTools*) 등의 자동화 테스트/크롤링 도구를 활용하여 자동으로 runtime 화면을 분석한다.
- 화면의 분석 결과를 매뉴얼 등에 활용할 수 있도록 마크다운 파일(.md)로 리포트를 생성한다.
- (Future Work) 생성된 마크다운 리포트를 활용할 수 있도록 메뉴트리와 마크다운 렌더러를 포함한 웹 앱을 개발한다.

### 기타 상세 정보

- 상세 내용은 다음 Notion URL (내부공개)에서 확인할 수 있습니다.(https://www.notion.so/solutionlink-platform/Playwright-BrowserTools-Audit-203bff1e3bd3800ab662da14b9d2eaa1?pvs=4)

---

## 사전 준비 사항

### 실행 환경
- *Cursor* 사용
- *Cursor* 내 *BrowserTools MCP* 연결

### 프로젝트 구조
- 프로젝트 루트 디렉토리 내 다음 디렉토리 세팅
    - `.cursor\rules`: Cursor Agent에게 제공하는 규칙 및 명령 포함
    - `01_inputs`: 분석할 대상 메뉴구조도 JSON 파일
    - `02_outputs`: 분석 결과 생성되는 마크다운 리포트 저장 경로
    - `02_outputs\src`: 분석 결과 생성되는 스크린샷 저장 경로
    - `03_ref`: 분석 수행을 위해 과정 중 필요한 참고 자료
    - `04_programs`: 본 프로젝트와 관련된 파이썬 프로그램
- 핵심 파일/명령
    - `.cursor\rules\analyze-screen.mdc`: 화면 분석을 수행하기 위한 <작업 개요>, <작업 절차>, <분석 보고서 작성 Rule> 등을 포함하는 Cursor Rule 문서

---

## 자동 분석 수행

### 입력 세팅

1. `.cursor\rules\analyze-screen.mdc` 파일 내 경로 세팅
    - Input JSON 파일 세팅 (1개)
    - Output Markdown Report 경로 세팅 (기본: `./02_outputs/`)
    - Output Screenshot 경로 세팅 (기본: `./02_outputs/screenshots/`)
    - Template Markdown 파일 세팅 (기본: `03_ref\report_md_template.md`)
        - AI Agent가 분석 결과 마크다운 리포트를 생성할 때 템플릿으로 활용하는 문서 (mdc 내에 자세한 Rule 포함)
2. `01_inputs\*.json`: 분석 대상 JSON 파일로써, 메뉴구조도를 기반으로 계층적으로 구성되어 있으며, leaf node는 *BrowserTools*가 자동으로 탐색하게 될 0..N개의 `includedScreens`를 포함
    - 현재 성능 이슈로 2레벨 단위로 분해되어 있음 (38개)

### BrowserTools 실행 및 자동 분석

- `analyze-screen-rule.mdc` 파일을 입력 프롬프트에 문맥으로 넣고, 다음과 같이 프롬프팅
    ```
    > @analyze-screen-rule.mdc 를 상세히 숙지하고, 기술된 절차대로 체계적으로 수행해줘.
    ```
- AI Agent의 자동 실행 결과 검토 및 단계별 권한 허용 (및 Tool Run)
    - 필요한 파일 읽기
    - 특정 화면에 대한 Navigate, Evaluate
    - 특정 화면에 대한 GetVisibleHtml, ScreenShot


### 실행 후 절차

- 생성 결과 파일 확인
    - 화면별 마크다운 리포트 (*.md)
    - 화면별 스크린샷 파일 (*.png)
- `02_outputs` 디렉토리를 초기화하고 싶을 경우, 기존 데이터를 백업한 후 `04_programs\clean_outputs.py`를 실행 (해당 파일을 열어 실행 버튼 클릭 혹은 아래의 터미널 명령어로 실행)
   ```shell
   Python clean_outputs.py
   ```