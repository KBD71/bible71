# API 키 설정 가이드

## 🔐 보안 중요 사항

**절대 API 키를 GitHub에 업로드하지 마세요!**

## 설정 방법

### 1단계: API 키 취득
- [Anthropic Console](https://console.anthropic.com/)에서 새 API 키 생성
- 기존 키가 GitHub에 노출되었다면 즉시 삭제하고 새 키 생성

### 2단계: 로컬 설정 파일 생성
```bash
cp config-example.js config-local.js
```

### 3단계: API 키 입력
`config-local.js` 파일에서 API 키 입력:
```javascript
CLAUDE_API_KEY: 'sk-ant-api03-여기에_실제_API_키_입력',
```

### 4단계: 확인
브라우저에서 웹사이트를 열어 챗봇이 정상 작동하는지 확인

## 파일 설명

- `config.js`: GitHub에 업로드되는 공개 설정 (API 키 없음)
- `config-local.js`: 로컬에만 있는 개인 설정 (API 키 포함)
- `config-example.js`: 설정 파일 템플릿
- `.gitignore`: config-local.js가 실수로 커밋되지 않도록 방지

## 트러블슈팅

### 챗봇이 작동하지 않는 경우
1. 브라우저 개발자 도구 확인 (F12)
2. 콘솔에서 API 키 관련 오류 메시지 확인
3. config-local.js 파일 존재 및 내용 확인

### GitHub Pages에서 사용하는 경우
- GitHub Pages는 정적 호스팅이므로 API 키를 서버사이드에서 숨길 수 없음
- 프로덕션 환경에서는 별도의 백엔드 서버 필요
- 현재는 개발/테스트 용도로만 사용 권장