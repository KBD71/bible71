# 성경 도우미 챗봇 - API 연동 가이드

## 개요

성경 도우미 챗봇은 전통적 개혁신학 관점에서 성경 관련 질문에 답변하는 AI 챗봇입니다. Claude API (기본)와 OpenAI API를 지원하여 정확하고 신학적으로 건전한 답변을 제공합니다.

## 주요 특징

- ✅ **전통적 개혁신학** 관점의 답변
- ✅ **성경 전용** 질문 필터링
- ✅ **웨스트민스터 신앙고백서** 기반 답변
- ✅ **응급상황 감지** (자살 위험 등)
- ✅ **플로팅 UI**로 모든 페이지에서 접근 가능
- ✅ **대화 히스토리** 유지 (최근 5개 대화)

## API 키 설정

### 1. Claude API 키 발급 (권장)

1. [Anthropic Console](https://console.anthropic.com/)에 가입/로그인
2. API 키 생성 (크레딧 구매 필요)
3. 생성된 API 키 복사

### 2. OpenAI API 키 발급 (대안)

1. [OpenAI 웹사이트](https://platform.openai.com/)에 가입/로그인
2. API 키 생성 (Billing 설정 필요)
3. 생성된 API 키 복사

### 3. config.js 파일 수정

#### Claude API 사용 (기본 설정):

```javascript
const CONFIG = {
    // Claude API 키 설정
    CLAUDE_API_KEY: 'sk-ant-your-actual-api-key-here',
    API_SERVICE: 'claude',

    // 모델 선택
    MODEL: 'claude-sonnet-4-20250514',    // Claude Sonnet 4 (최신 최고 성능)
    // MODEL: 'claude-3-5-haiku-20241022',    // 빠르고 경제적
    // MODEL: 'claude-3-5-sonnet-20241022', // 더 정확, 비싸

    MAX_TOKENS: 1000,
    TEMPERATURE: 0.3
};
```

#### OpenAI API 사용 시:

```javascript
const CONFIG = {
    // OpenAI API 키 설정
    OPENAI_API_KEY: 'sk-your-actual-openai-key-here',
    API_SERVICE: 'openai',

    MODEL: 'gpt-4o-mini',    // 또는 'gpt-4'
    MAX_TOKENS: 1000,
    TEMPERATURE: 0.3
};
```

### 4. 보안 주의사항

⚠️ **중요**: API 키는 민감한 정보입니다.

- **절대 GitHub나 공개 저장소에 올리지 마세요**
- 가능하면 서버사이드에서 API 호출 처리
- 환경변수 또는 별도 config 파일로 관리
- `.gitignore`에 config.js 추가 권장

## Claude vs OpenAI 비교

### 보안성

| 항목 | Claude | OpenAI |
|------|--------|--------|
| **데이터 보관** | 더 짧은 기간 | 30일간 보관 |
| **학습 사용** | 사용자 데이터로 학습 안함 | 옵트아웃 가능 |
| **프라이버시** | 더 강한 개인정보 보호 | 표준적 보호 |
| **EU/한국 규정** | 더 준수적 | 표준 준수 |

**🔒 보안 관점에서 Claude가 더 안전합니다.**

### 성능 및 비용

| 모델 | 용도 | 입력 토큰당 비용 | 출력 토큰당 비용 |
|------|------|----------------|----------------|
| **Claude Sonnet 4** ⭐ | 최고 품질 신학 해석 | $0.003 | $0.015 |
| **Claude 3.5 Sonnet** | 복잡한 추론 | $0.003 | $0.015 |
| **Claude 3.5 Haiku** | 빠른 일반 대화 | $0.00025 | $0.00125 |
| **GPT-4o** | 복잡한 추론 | $0.0025 | $0.01 |
| **GPT-4o-mini** | 빠른 일반 대화 | $0.00015 | $0.0006 |

**💰 비용: GPT-4o-mini < Claude Haiku < GPT-4o < Claude Sonnet 3.5 ≈ Sonnet 4**

## 신학적 설정

### 개혁신학 원칙

챗봇은 다음 원칙에 따라 답변합니다:

1. **성경의 권위와 무오성**
2. **삼위일체 하나님의 주권**
3. **전적 부패와 원죄**
4. **무조건적 선택과 예정**
5. **제한적 속죄**
6. **불가항력적 은혜**
7. **성도의 견인**
8. **오직 믿음, 오직 은혜, 오직 그리스도**

### 참고 문헌

- 웨스트민스터 신앙고백서
- 웨스트민스터 대요리문답
- 웨스트민스터 소요리문답
- 존 칼빈, 루터 등 종교개혁자들의 가르침

## 질문 필터링

### 허용되는 질문

- 성경 해석 및 연구
- 신앙생활 상담
- 교리 및 신학 질문
- 기도, 예배, 교회생활
- 구원, 칭의, 성화 등

### 차단되는 질문

- 정치, 선거, 정당 관련
- 주식, 투자, 재테크
- 연애, 결혼 상담 (일반적인)
- 타종교 비교
- 게임, 연예, 스포츠

## 파일 구조

```
bible71/
├── config.js              # API 설정
├── theology-system.js     # 개혁신학 프롬프트
├── question-filter.js     # 질문 필터링
├── api-handler.js         # API 호출 처리
├── chatbot-trigger.js     # iframe용 트리거
├── proxy-server.py        # CORS 문제 해결용 프록시 서버
└── index.html            # 메인 챗봇 (업데이트됨)
```

## 실행 방법

### 1. 프록시 서버 실행 (중요!)

브라우저의 CORS 정책으로 인해 Claude API 호출을 위한 프록시 서버가 필요합니다.

**터미널 1: 프록시 서버 실행**
```bash
cd /Users/kbd/Desktop/bible/bible71
python3 proxy-server.py
```

### 2. 웹 서버 실행

**터미널 2: 웹 서버 실행**
```bash
cd /Users/kbd/Desktop/bible/bible71
python3 -m http.server 8000
```

### 3. 챗봇 사용

브라우저에서 `http://localhost:8000`을 열어 챗봇을 사용하세요.

⚠️ **두 서버 모두 실행되어야 합니다**:
- 프록시 서버: `localhost:8001` (Claude API 통신용)
- 웹 서버: `localhost:8000` (챗봇 UI용)

## 사용법

### 1. 메인 페이지에서

- 우측 하단 챗봇 버튼 클릭
- 질문 입력 후 Enter 또는 전송
- 빠른 질문 버튼 활용

### 2. iframe 페이지에서

- 우측 하단 트리거 버튼 클릭
- 키보드 단축키: `Ctrl + /` (또는 `Cmd + /`)
- 메인 페이지의 챗봇이 열림

## API 없이 사용

API 키가 없어도 기본적인 답변은 제공됩니다:

- 미리 정의된 성경 구절
- 기본적인 신앙 상담
- 성경 읽기 계획 안내

하지만 더 정확하고 개인화된 답변을 위해서는 API 키 설정을 권장합니다.

## 비용 관리

### 일반적인 성경 질문 비용 (평균 입력 100토큰, 출력 300토큰)

#### Claude API:
- **Claude 3.5 Haiku**: 질문당 약 $0.0004 (권장)
- **Claude 3.5 Sonnet**: 질문당 약 $0.0075

#### OpenAI API:
- **GPT-4o-mini**: 질문당 약 $0.0003 (가장 저렴)
- **GPT-4o**: 질문당 약 $0.0055

### 권장 설정

1. **개발/테스트**: GPT-4o-mini (가장 저렴)
2. **일반 사용**: Claude 3.5 Haiku (균형잡힌 성능/가격)
3. **고품질 답변**: Claude 3.5 Sonnet (최고 품질)

## 문제해결

### 1. API 오류

#### Claude API:
```
API 오류 (401): Authentication failed
```
→ config.js에서 CLAUDE_API_KEY 확인

#### OpenAI API:
```
API 오류 (401): Invalid API key
```
→ config.js에서 OPENAI_API_KEY 확인

### 2. 질문 차단

```
성경이나 신앙생활과 관련된 질문만 답변드릴 수 있습니다.
```
→ 더 구체적인 성경 관련 질문으로 다시 시도

### 3. 로딩 계속됨

- 네트워크 상태 확인
- API 키 유효성 확인
- 브라우저 콘솔에서 오류 확인

## 커스터마이징

### 1. 신학적 관점 수정

`theology-system.js`에서 CORE_PRINCIPLES 및 시스템 프롬프트 수정

### 2. 필터링 키워드 추가

`question-filter.js`에서 bibleKeywords, prohibitedTopics 배열 수정

### 3. 응답 스타일 변경

`api-handler.js`에서 temperature, 토큰 수, 프롬프트 조정

## 지원 및 문의

기술적 문제나 신학적 질문이 있으시면:

1. 브라우저 개발자 도구에서 콘솔 오류 확인
2. API 키 및 네트워크 상태 확인
3. 필요시 목회진과 상담

---

**"모든 성경은 하나님의 감동으로 된 것으로 교훈과 책망과 바르게 함과 의로 교육하기에 유익하니" (딤후 3:16)**