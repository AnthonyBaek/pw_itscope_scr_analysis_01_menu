# 화면 분석 보고서

## 화면 개요

- 화면 이름:
- 화면 접근 경로: 의사소통관리 → 보고관리 → 프로젝트 주간보고
- 화면 URL: `/report/report/list.do?CM=list&searchType=&menuId=852`
- 화면 요약:
    - 화면에 대해 간단하게 요약하여 설명합니다.
    - 화면에 대해 간단하게 요약하여 설명합니다.

---

## 화면 상세

### 화면 UI 구성

![화면 구성](./screenshot_sample.png)

### 화면 구성 컴포넌트

| 번호 | 컴포넌트명 | 컴포넌트 타입 | 설명 | 이벤트 유형 | 이벤트 동작 | 관련 Function |
|------|------------|----------------|------|-------------|-------------|---------------|
| 1 | 검색영역 | Container | 검색 조건을 입력하는 영역 | - | - | - |
| 1.1 | 기간선택 | DatePicker | 조회 기간을 선택 | change | 시작일/종료일 유효성 검증 | validateDateRange() |
| 1.2 | 검색버튼 | Button | 검색 조건에 맞는 데이터를 조회 | click | 검색 조건으로 데이터 조회 | searchData() |
| 2 | 목록영역 | Container | 조회된 데이터를 표시하는 영역 | - | - | - |
| 2.1 | 목록그리드 | Grid | 조회된 데이터 목록을 표시 | rowClick | 선택된 행의 상세정보 표시 | showDetail() |
| 2.1.1 | 상태컬럼 | Column | 처리상태를 아이콘으로 표시 | hover | 상태 설명 툴팁 표시 | showStatusTooltip() |
| 2.1.2 | 제목컬럼 | Column | 보고서 제목을 표시 | click | 상세 보기 팝업 오픈 | openDetailPopup() |

### 관련 Function 상세

| Function명 | 설명 | 입력값 | 반환값 |
|------------|------|--------|---------|
| validateDateRange() | 시작일과 종료일의 유효성을 검증하는 함수 | startDate: 시작일자(String)<br>endDate: 종료일자(String) | boolean - 유효성 검증 결과 |
| searchData() | 입력된 검색조건으로 데이터를 조회하는 함수 | searchParams: 검색조건 객체 | void |
| showDetail() | 선택된 행의 상세 정보를 표시하는 함수 | rowData: 선택된 행 데이터 객체 | void |
| showStatusTooltip() | 상태 아이콘에 마우스 오버시 툴팁을 표시하는 함수 | statusCode: 상태코드(String) | void |
| openDetailPopup() | 상세보기 팝업창을 여는 함수 | reportId: 보고서ID | void |
