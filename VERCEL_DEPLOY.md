# 🚀 Vercel 배포 가이드

## 1단계: GitHub 푸시

현재 모든 파일이 준비되었으므로 GitHub에 푸시:

```bash
git add .
git commit -m "Add Vercel serverless functions"
git push origin main
```

## 2단계: Vercel 계정 생성 및 연결

1. **Vercel.com 가입**
   - GitHub 계정으로 로그인 권장

2. **프로젝트 가져오기**
   - "New Project" 클릭
   - GitHub 저장소 `KBD71/bible71` 선택
   - "Import" 클릭

## 3단계: 환경변수 설정

배포 설정 페이지에서 환경변수 추가:

```
Name: CLAUDE_API_KEY
Value: [여기에_실제_Claude_API_키_입력]
```

추가 환경변수 (선택사항):
```
CLAUDE_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=300
TEMPERATURE=0.3
```

## 4단계: 배포 실행

- "Deploy" 버튼 클릭
- 자동 빌드 및 배포 시작
- 3-5분 후 완료

## 5단계: 테스트

배포 완료 후:
1. 제공된 URL 접속 (예: `https://bible71.vercel.app`)
2. 우하단 Q&A 챗봇 클릭
3. "하나님의 주권에 대해 설명해주세요" 테스트

## 📂 Vercel 파일 구조

```
bible71/
├── api/
│   ├── chat.js         # 챗봇 API 엔드포인트
│   └── health.js       # 헬스체크 API
├── vercel.json         # Vercel 배포 설정
├── index.html          # 메인 페이지
├── config-vercel.js    # Vercel용 프론트엔드 설정
└── (기타 파일들...)
```

## 🔧 API 엔드포인트

배포 후 사용 가능한 API:

- `GET /api/health` - 헬스체크
- `POST /api/chat` - 챗봇 응답

## 🔒 보안 기능

- ✅ API 키가 Vercel 환경변수에서 안전하게 관리
- ✅ CORS 설정으로 모든 도메인에서 접근 가능
- ✅ 성경/신앙 관련 질문만 허용
- ✅ 입력 길이 제한 (500자)
- ✅ 서버리스로 자동 스케일링

## 🌐 도메인 설정 (선택사항)

Vercel에서 커스텀 도메인 설정:
1. 프로젝트 설정 → Domains
2. 원하는 도메인 입력
3. DNS 설정 안내에 따라 설정

## 🔄 자동 배포

- GitHub에 push할 때마다 자동 배포
- Pull Request 시 미리보기 배포
- 배포 히스토리 및 롤백 기능

## 🚨 트러블슈팅

### 1. 환경변수 설정 확인
**첫 번째 디버그 단계**:
1. 브라우저에서 `https://your-app.vercel.app/api/chat` 접속 (GET 요청)
2. 다음 정보 확인:
   ```json
   {
     "debug": {
       "hasApiKey": true,  // false면 환경변수 설정 안됨
       "apiKeyLength": 107, // API 키 길이 확인
       "model": "claude-sonnet-4-20250514"
     }
   }
   ```

**환경변수 설정이 안된 경우**:
1. Vercel 대시보드 → 프로젝트 → Settings → Environment Variables
2. `CLAUDE_API_KEY` 추가 (Production, Preview, Development 모두 체크)
3. 반드시 **Redeploy** 버튼 클릭하여 재배포

### 2. 환경변수가 설정되었는데도 안되는 경우
**가능한 원인들**:
- API 키에 공백이나 특수문자 포함
- 환경변수 이름 오타 (`CLAUDE_API_KEY` 정확히 입력)
- 재배포를 하지 않음

**해결 방법**:
1. API 키 재확인 (Anthropic Console에서 새 키 생성)
2. 환경변수 삭제 후 다시 추가
3. 반드시 Redeploy

### 3. API 호출 실패
```
Error: 500 Internal Server Error
```
→ Vercel Functions 로그 확인
→ `/api/chat` GET 요청으로 디버그 정보 확인

### 4. CORS 오류
```
Access to fetch blocked by CORS policy
```
→ 보통 자동으로 해결됨
→ 브라우저 새로고침

## 💡 최적화 팁

1. **함수 실행 시간**: 최대 30초 (vercel.json에서 설정)
2. **메모리 사용량**: 자동 최적화
3. **응답 속도**: 첫 호출 시 콜드 스타트로 약간 느릴 수 있음
4. **비용**: 월 100GB까지 무료

## 📊 모니터링

Vercel 대시보드에서 확인 가능:
- 함수 실행 로그
- 응답 시간
- 에러율
- 사용량 통계

배포 완료 후 URL을 알려주세요! 🎉