# 심평원 비급여조사 (HIRA OpenAPI 비급여 검색 스크립트)

이 프로젝트는 공공데이터포털(data.go.kr)의 **'건강보험심사평가원_비급여진료비정보조회서비스'** 및 관련 비급여 OpenAPI를 사용하여 특정 의료 행위의 비급여 가격 정보와 통계를 실시간으로 파싱하고 검색하기 위한 파이썬 스크립트입니다.

## 🚀 사용법 (Usage)

### 1. 비급여 항목 코드 리스트 조회
명칭과 분류 코드를 구하기 위해 전체 리스트를 조회합니다.

```bash
python search_npay.py getNonPaymentItemCodeList --numOfRows 500 > npay_codes.json
```

### 2. 특정 시술 항목의 병원별 가격 조회
특정 `itemCd` 또는 병원명(`yadmNm`) 등을 기반으로 병원별 가격 정보를 찾아봅니다.

```bash
python search_npay.py getNonPaymentItemHospList --itemCd [CODE] --numOfRows 20
```

*사용 가능한 매개변수(parameter):*
- `--pageNo` : 페이지 번호 (기본: 1)
- `--numOfRows` : 한 번에 불러올 개수 (기본: 10)
- `--itemCd` : 비급여 항목 코드
- `--npayCd` : 비급여 코드 
- `--sidoCd` / `--sgguCd` : 시도 / 시군구 코드
- `--yadmNm` : 병원명 검색어

## 🔑 필수 환경 변수 설정
이 스크립트는 공공데이터포털의 API 키가 필요합니다. 터미널 환경변수에 반드시 발급받으신 **일반 인증키(Encoding)**를 설정해 주십시오.

```bash
# Windows (PowerShell)
$env:HIRA_OPENAPI_KEY="본인의_API_KEY"

# Linux/Mac
export HIRA_OPENAPI_KEY="본인의_API_KEY"
```

## 🚨 유의사항
- HIRA OpenAPI의 경우 엔드포인트 파라미터 규칙이 변경될 수 있으므로, 결과값이 `<totalCount>0</totalCount>`일 경우 `itemCd` 대신 `npayCd` 등으로 매개변수를 교체하여 시도하시기 바랍니다.
