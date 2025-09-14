# 성경 챗봇 백엔드 서버 가이드

## 🚀 빠른 시작

### 1단계: 의존성 설치
```bash
npm install
```

### 2단계: 환경변수 설정
```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일을 열어서 API 키 입력
CLAUDE_API_KEY=sk-ant-api03-실제_API_키
```

### 3단계: 서버 실행
```bash
# 개발 모드 (자동 재시작)
npm run dev

# 프로덕션 모드
npm start
```

### 4단계: 브라우저에서 확인
- http://localhost:3000 에서 웹사이트 확인
- 챗봇이 백엔드 서버를 통해 작동

## 📂 파일 구조

```
bible71/
├── server.js              # 백엔드 서버 (Express.js)
├── package.json           # Node.js 설정
├── .env                   # 환경변수 (API 키 포함)
├── .env.example          # 환경변수 예시
│
├── index.html            # 메인 페이지
├── config-backend.js     # 백엔드용 설정
├── api-handler-backend.js # 백엔드 API 통신
│
└── (기타 프론트엔드 파일들...)
```

## 🔐 보안 기능

- ✅ API 키를 서버에서 안전하게 관리
- ✅ CORS 설정으로 허용된 도메인에서만 접근
- ✅ Rate Limiting으로 API 남용 방지
- ✅ 성경 관련 질문만 허용하는 필터링
- ✅ 입력 검증 및 길이 제한

## 🌐 배포 옵션

### Option 1: Heroku
```bash
# Heroku CLI 설치 후
heroku create your-app-name
heroku config:set CLAUDE_API_KEY=your-api-key
git push heroku main
```

### Option 2: Railway
1. Railway.app에 가입
2. GitHub 저장소 연결
3. 환경변수에 CLAUDE_API_KEY 설정
4. 자동 배포

### Option 3: Render
1. Render.com에 가입
2. Web Service 생성
3. GitHub 저장소 연결
4. 환경변수 설정

### Option 4: Vercel (서버리스)
1. Vercel.com에 가입
2. GitHub 저장소 연결
3. 환경변수 설정
4. 자동 배포

## 🔧 환경변수 설명

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `CLAUDE_API_KEY` | Anthropic Claude API 키 | 필수 |
| `CLAUDE_MODEL` | 사용할 Claude 모델 | `claude-sonnet-4-20250514` |
| `MAX_TOKENS` | 최대 토큰 수 | `300` |
| `TEMPERATURE` | 응답 창의성 | `0.3` |
| `PORT` | 서버 포트 | `3000` |
| `NODE_ENV` | 환경 모드 | `development` |

## 🚨 트러블슈팅

### 서버가 시작되지 않는 경우
1. Node.js 버전 확인 (16.0.0 이상 필요)
2. `npm install` 실행
3. `.env` 파일에 API 키 확인

### 챗봇이 응답하지 않는 경우
1. 브라우저 개발자 도구에서 네트워크 탭 확인
2. `http://localhost:3000/api/health` 접속해서 서버 상태 확인
3. 서버 콘솔에서 오류 메시지 확인

### API 키 오류
1. Anthropic Console에서 API 키 확인
2. `.env` 파일에 올바르게 설정되었는지 확인
3. 환경변수가 로드되는지 확인

## 📈 성능 최적화

- Rate limiting: 15분당 100회 요청 제한
- 응답 캐싱: 필요시 Redis 추가 가능
- 로드 밸런싱: PM2나 클러스터 모드 사용
- CDN: 정적 파일 배포시 CloudFlare 등 활용

## 🔒 추가 보안 설정

프로덕션 환경에서 권장사항:
- HTTPS 사용 필수
- 환경변수를 통한 허용 도메인 설정
- 로그 모니터링 설정
- 정기적인 의존성 업데이트