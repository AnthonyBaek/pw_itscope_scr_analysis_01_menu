# Playwright 기반의 ITSCOPE 화면 분석 및 Audit 자동화

## 프로젝트 개요

### 기능 요약
- ITSCOPE 표준산출물(메뉴구조도)에 근거해 재활용성이 높은 Menu Tree JSON을 뽑아낸다.
- Menu JSON을 기준으로, (1)화면 자동 탐색을 수행하고, (2)메뉴 목차를 추출한다.

### (1) 메뉴 화면 자동 탐색
- AI 기반의 도구를 활용해 최적의 프롬프트로 입력한 URL의 화면 분석을 요청/처리한다.
- *Playwright* (, *BrowserTools*) 등의 자동화 테스트/크롤링 도구를 활용하여 자동으로 runtime 화면을 분석한다.
- 화면의 분석 결과를 매뉴얼 등에 활용할 수 있도록 마크다운 파일(.md)로 리포트를 생성한다.

### (2) 메뉴 목차 생성
- 생성된 Menu JSON 파일을 기준으로, 온라인 매뉴얼에서 사용할 메뉴 목차 마크다운 파일을 생성한다.
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
    - `.cursor/rules`: Cursor Agent에게 제공하는 규칙 및 명령 포함
    - `01_inputs`: 분석 대상 메뉴 구조도 JSON 파일 및 관련 입력 파일 저장
        - `01_inputs/menu_tree.json`: (선택 사항) `menu_json_decomposer.py`의 기본 입력 파일
        - `01_inputs/menu_json_all`: 병합된 전체 메뉴 JSON 파일 (`menu_all.json`) 저장
        - `01_inputs/menu_json_decomposed`: `menu_json_decomposer.py` 실행 결과 분리된 개별 메뉴 JSON 파일 저장
    - `02_outputs`: 자동 분석 및 기타 스크립트 실행 결과 생성 파일 저장
        - `02_outputs/reports`: 화면 분석 결과 생성되는 마크다운 리포트 저장
        - `02_outputs/screenshots`: 화면 분석 결과 생성되는 스크린샷 파일 저장
        - `02_outputs/toc`: `generate_toc_active_md.py` 실행 결과 생성되는 목차 파일 저장
    - `03_ref`: 분석 수행 및 스크립트 작성 시 참고 자료 저장
        - `03_ref/report_md_template.md`: 화면 분석 리포트 생성 시 사용되는 마크다운 템플릿
    - `04_programs`: 본 프로젝트의 유틸리티 파이썬 스크립트 저장
        - `04_programs/ref`: 스크립트 작성 시 참고용 예시 코드 또는 문서 저장
- 핵심 파일/명령
    - `.cursor/rules/analyze-screen.mdc`: 화면 분석을 수행하기 위한 <작업 개요>, <작업 절차>, <분석 보고서 작성 Rule> 등을 포함하는 Cursor Rule 문서

---

## (1) 자동 분석 수행

### 입력 세팅

1. `.cursor/rules/analyze-screen.mdc` 파일 내 경로 세팅
    - Input JSON 파일 세팅 (1개)
    - Output Markdown Report 경로 세팅 (기본: `./02_outputs/reports/`)
    - Output Screenshot 경로 세팅 (기본: `./02_outputs/screenshots/`)
        - ***주의! Absolute Path를 반드시 수정해야 함***
    - Template Markdown 파일 세팅 (기본: `03_ref/report_md_template.md`)
        - AI Agent가 분석 결과 마크다운 리포트를 생성할 때 템플릿으로 활용하는 문서 (mdc 내에 자세한 Rule 포함)
2. `01_inputs/menu_tree.json`: 분석 대상 JSON 파일로써, 메뉴구조도를 기반으로 계층적으로 구성되어 있으며, leaf node는 *BrowserTools*가 자동으로 탐색하게 될 0..N개의 `includedScreens`를 포함
    - 현재 성능 이슈로 2레벨 단위로 분해되어 있음 (38개)

### BrowserTools 실행 및 자동 분석

- *Cursor AI* 세팅: Auto-run 활성화
    - Cursor Setting > Chat > Auto-run
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
- `02_outputs` 디렉토리를 초기화하고 싶을 경우, 기존 데이터를 백업한 후 `04_programs/clean_outputs.py`를 실행 (해당 파일을 열어 실행 버튼 클릭 혹은 아래의 터미널 명령어로 실행)
   ```shell
   Python clean_outputs.py
   ```

---

## (2) 매뉴얼 목차 생성

### 사전 조건
- `.\01_inputs\menu_json_all\menu_all.json` 파일 존재
    - 포함시킬 메뉴에 대해 `isTestTarget`==true 설정
- `.\04_programs\generate_toc_active_md.py` 프로그램 경로 세팅

### 목차 생성
- `generate_toc_active_md.py` 실행
    ```
    Python .\generate_toc_active_md.py
    ```
- 실행 결과 확인: `.\02_outputs\toc\menu_toc_active.md`
   - Test Target 메뉴에 대해 *"2.2.2. 프로젝트 월간보고"* 식으로 출력되었으면 정상

---

## 포함 프로그램

### 입력 파일 관리
- `menu_json_decomposer.py`: 하나의 큰 메뉴 JSON 파일을 `menuLevel` 2 기준으로 여러 개의 작은 JSON 파일로 분리합니다.
    - 입력: `01_inputs/menu_tree.json` (스크립트에 하드코딩된 기본값) 또는 사용자 지정 경로
    - 출력: `01_inputs/menu_json_decomposed/decomposed_menu_XXX.json` (기본 접두사 "decomposed_menu" 사용 시)
- `merge_json.py`: `01_inputs/menu_json_decomposed` 폴더 내의 분리된 JSON 파일들을 병합하여 `menu_all.json` 파일을 생성합니다.
    - 입력: `01_inputs/menu_json_decomposed/decomposed_menu_*.json` (또는 스크립트 실행 시 지정된 패턴의 파일들)
    - 출력: `01_inputs/menu_json_all/menu_all.json`
- `input_menu_id.py`: `menu_all.json` 파일 내의 각 메뉴 항목에 규칙에 따라 `menuId` 값을 할당합니다.
    - 입력: `01_inputs/menu_json_all/menu_all.json`
    - 출력: `01_inputs/menu_json_all/menu_all.json` (파일 직접 수정)

### 탐색 범위 관리
- `enable_test_target.py`: 특정 접두사를 가진 JSON 파일 내 모든 메뉴의 `isTestTarget`을 `True`로 설정합니다.
    - 입력: `01_inputs/{prefix}_*.json` (스크립트 실행 시 `prefix` 인자 필요)
    - 출력: `01_inputs/{prefix}_*.json` (파일 직접 수정)
- `disable_test_target.py`: 특정 접두사를 가진 JSON 파일 내 모든 메뉴의 `isTestTarget`을 `False`로 설정합니다.
    - 입력: `01_inputs/{prefix}_*.json` (스크립트 실행 시 `prefix` 인자 필요)
    - 출력: `01_inputs/{prefix}_*.json` (파일 직접 수정)
- `enable_test_target_all.py`: `menu_all.json` 파일 내 모든 메뉴의 `isTestTarget`을 `True`로 설정합니다.
    - 입력: `01_inputs/menu_json_all/menu_all.json`
    - 출력: `01_inputs/menu_json_all/menu_all.json` (파일 직접 수정)

### 분석 결과 관리
- `clean_outputs.py`: `02_outputs` 폴더 내의 분석 결과 파일(*.md, *.png)들을 삭제하여 정리합니다.
    - 입력: 해당 없음 (지정된 폴더 `02_outputs/reports/`, `02_outputs/screenshots/`, `02_outputs/toc/` 를 대상으로 함)
    - 출력: 해당 없음 (파일 삭제)

### 목차 생성
- `generate_toc_active_md.py`: `menu_all.json` 파일을 읽어 `isTestTarget`이 `true`인 메뉴 항목들만 추출하여, 숫자 계층 형식의 목차를 `menu_toc_active.md` 파일로 생성합니다.
    - 입력: `01_inputs/menu_json_all/menu_all.json`
    - 출력: `02_outputs/toc/menu_toc_active.md`



## 저작권 및 문의

> 본 코드는 *Cursor AI*로 만들어졌습니다.

- 저작권: 2025 Copyright ⓒ Solution Link. All Rights Reserved.
- 문의: 백영민(ymbaek@sol-link.com), 최현규(hkchoi@sol-link.com)