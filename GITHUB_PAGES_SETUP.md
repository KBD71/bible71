# 🚀 GitHub Pages 바로 사용하기

## ⚠️ 중요: API 키 보안 경고
GitHub이 푸시를 차단할 수 있습니다. 다음 방법으로 해결하세요:

## 방법 1: 로컬에서만 API 키 설정
```bash
# config-local.js에 API 키 설정 (GitHub에 업로드 안됨)
cp config-example.js config-local.js
# config-local.js 파일을 열어서 API 키 입력
```

## 방법 2: GitHub Secret Scanning 우회 (임시)
1. GitHub에서 push protection이 작동하면
2. 제공된 URL 클릭해서 "Allow this secret" 선택
3. 일시적으로 허용

## 방법 3: 수동 업로드 (권장)
1. GitHub 웹에서 config.js 파일 직접 수정
2. API 키 직접 입력 후 커밋
3. GitHub Pages 자동 배포

## 🔗 GitHub Pages 활성화
1. GitHub 저장소 → Settings → Pages
2. Source: Deploy from a branch → main 선택
3. Save 클릭
4. 5-10분 후 https://kbd71.github.io/bible71/ 에서 접근

## ✅ 테스트
- 웹사이트 로드 후 우하단 Q&A 챗봇 클릭
- "하나님의 주권에 대해 설명해주세요" 테스트

## 🔒 보안 고려사항
- **장점**: 바로 작동, 설정 간단
- **단점**: API 키가 공개적으로 노출됨
- **권장**: 개인 프로젝트나 테스트용으로만 사용

## 🎯 결론
복잡한 Vercel 설정 없이 바로 GitHub Pages에서 작동합니다!