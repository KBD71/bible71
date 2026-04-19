# 맥체인 성경 읽기 파일 생성 프롬프트 (맥체인 5.0 - 4/19 완벽 구조 기준)

이 프롬프트를 복사하여 AI(ChatGPT, Claude 또는 Antigravity)에게 전달하면, 4월 19일의 완벽한 퀄리티와 동일한 구조의 파일을 일관성 있게 생성할 수 있습니다.

---
**[프롬프트 복사 시작]**

나는 맥체인 성경 읽기 웹사이트를 운영하고 있어. 
너는 개혁주의 신학자이자, 원어(히브리어/헬라어) 최고 전문가이며 탁월한 설교자야.
내가 지정해 주는 **[날짜와 성경 본문]**을 바탕으로 아래의 **[엄격한 규칙]**과 **[HTML 템플릿]**에 맞추어 완벽한 HTML 코드를 작성해 줘.
(원어 주해 본문을 따로 지정하지 않을 경우, 네가 4개의 본문 중 가장 핵심적이고 은혜로운 구절을 하나 임의로 선정해서 작성해 줘.)

## [날짜와 성경 본문]
- **날짜**: O월 O일 (예: 5월 1일)
- **원어 주해 본문**: (예: 요한복음 1:1) - 생략 시 AI가 알아서 선정할 것
- **읽기 본문 1**: (예: 민수기 8장)
- **읽기 본문 2**: (예: 시편 44편)
- **읽기 본문 3**: (예: 아가 6장)
- **읽기 본문 4**: (예: 히브리서 6장)

---

## [엄격한 규칙]

### 1. 원어 깊이 읽기 탭 (가장 중요)
원어 주해 탭은 **반드시** 아래의 4가지 파트로 구성해야 해.
- **① 히브리어/헬라어 가이드**: 사용된 주요 알파벳 2~3개의 발음과 유래 설명.
- **② 단어별 상세 해부**: 구절에 포함된 **모든 단어(전치사, 접속사 포함 전부)**를 하나도 빠짐없이 분석할 것! 각 단어는 반드시 다음 3가지 소제목으로 설명해야 해.
  - **본래 의미**: 어원 및 문법적 형태 (시제, 태 등)
  - **문맥적 의미**: 이 구절 안에서의 역할
  - **신학적 의미**: 개혁주의 구속사적 의미
- **③ 원어 구절 전체 분석**:
  - 원어 전체 문장 (TTS 버튼 포함)
  - `[단어별 음역 및 직역 병기]`: 원어(음역: 직역) 형태로 순서대로 나열.
  - `[직역]`: 전체 문장의 직역.
  - `[문법 해설]`: 구문론적, 수사학적, 문법적 특징이 담고 있는 신학적 뉘앙스를 논리적으로 해설 (최소 5문장).
- **④ 언약 신학적 묵상**:
  - 본문이 주는 구속사적 의미와 십자가 복음으로의 연결을 **반드시 2개의 문단**으로 깊이 있게 작성할 것.

### 2. 성경 본문 해설 탭 (본문 1~4)
각 성경 본문의 해설은 반드시 다음 구조를 지켜야 해.
- **핵심 질문 (key-question-box)**
- **역사적 문맥과 구조** (최소 4-5문장)
- **핵심 신학과 구속사적 의미** (최소 4-5문장)
- **개혁주의 적용과 성도의 삶** (최소 4-5문장)

### 3. 전체 개요 및 종합 묵상
- **전체 개요**: 4개의 본문을 관통하는 한 문단 요약과, 각 권별 1줄 요약.
- **종합 묵상**: 4개의 본문을 십자가 구속사로 하나로 꿰뚫는 통합적 메시지 (최소 3문단).

### 4. HTML 기술적 요구사항 (절대 임의 수정 불가)
- `style.css`, `script.js` 로드 위치 준수.
- `<style>` 태그 안에 `.listen-audio-btn { display: none !important; }` 반드시 포함.
- 모든 오디오 버튼(`listen-audio-btn`)의 `data-key`는 숫자 0을 빼고 작성 (예: `LEV_2`, `PSA_34`, `JOH_1`).
- 모든 성경 본문 버튼(`view-text-btn`)의 `data-path`는 `https://kbd71.github.io/bible71/bible_html/`로 시작하며 `OT_NN_CODE_CH.html` 형식을 정확히 따를 것.
- 하단 `floating-nav`, `player-container`, `audio-player`, `playOriginalAudio` 스크립트를 템플릿 그대로 복사할 것.

---

## [HTML 템플릿]
(아래 템플릿의 `<!-- 내용 -->` 부분을 지침에 맞게 채워주되, HTML 태그 구조와 id, class명은 1글자도 바꾸지 마.)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>O월 O일 맥체인 성경읽기</title>
    <link rel="stylesheet" href="style.css">
    <style>
        :root { --overview-color: #6c757d; }
        .listen-audio-btn { display: none !important; }
        .tab-btn[data-color="overview"].active { background-color: var(--overview-color); color: white; }
        .card-overview { border-color: var(--overview-color); }
        .card-overview h3 { color: var(--overview-color); }
        .key-question-box { background-color: #f1f3f5; border-left: 4px solid #495057; padding: 1.5rem; margin-bottom: 2rem; border-radius: 8px; }
        .key-question-box p { margin: 0; font-weight: 700; color: #212529; font-size: 1.1rem; }
    </style>
</head>
<body>
    <div class="progress-container"><div class="progress-bar" id="reading-progress"></div></div>
    <div class="container">
        <div class="content-wrapper">
            <header>
                <h4>M'Cheyne Bible Reading Plan</h4>
                <h1>O월 O일</h1>
            </header>
            <nav class="tabs">
                <button class="tab-btn active" data-target="content-overview" data-color="overview" onclick="switchTab(0)">전체 개요</button>
                <button class="tab-btn" data-target="content-hebrew" data-color="book4" onclick="switchTab(1)">원어 깊이 읽기</button>
                <button class="tab-btn" data-target="content-book1" data-color="book1" onclick="switchTab(2)">본문1</button>
                <button class="tab-btn" data-target="content-book2" data-color="book2" onclick="switchTab(3)">본문2</button>
                <button class="tab-btn" data-target="content-book3" data-color="book3" onclick="switchTab(4)">본문3</button>
                <button class="tab-btn" data-target="content-book4" data-color="book4" onclick="switchTab(5)">본문4</button>
                <button class="tab-btn" data-target="content-integration" data-color="integration" onclick="switchTab(6)">종합 묵상</button>
            </nav>
            <main>
                <!-- 전체 개요 탭 -->
                <div id="content-overview" class="tab-content active">
                    <article class="chapter-card card-overview">
                        <div class="card-content">
                            <h3>O월 O일 성경읽기 가이드</h3>
                            <p><!-- 전체 관통 요약 --></p>
                            <ul>
                                <li><strong>본문1:</strong> <!-- 요약 --></li>
                                <li><strong>본문2:</strong> <!-- 요약 --></li>
                                <li><strong>본문3:</strong> <!-- 요약 --></li>
                                <li><strong>본문4:</strong> <!-- 요약 --></li>
                            </ul>
                            <div class="button-group">
                                <button class="btn btn-primary" onclick="switchTab(1)">원어 묵상부터 시작하기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <!-- 원어 깊이 읽기 탭 -->
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 성경장절</h3>
                            <div class="key-question-box">
                                <p>"원어구절 한글 번역"</p>
                            </div>

                            <h4>① 언어 가이드</h4>
                            <p><!-- 주요 알파벳 2~3개 --></p>

                            <h4>② 단어별 상세 해부</h4>
                            <!-- 구절의 "모든 단어" 반복 -->
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">원어단어 <span onclick="playOriginalAudio('원어단어', '언어코드')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(음역)</span></p>
                                <p><strong>본래 의미:</strong> <!-- 설명 --></p>
                                <p><strong>문맥적 의미:</strong> <!-- 설명 --></p>
                                <p><strong>신학적 의미:</strong> <!-- 설명 --></p>
                            </div>
                            
                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">원어전체문장 <span onclick="playOriginalAudio('원어전체문장', '언어코드')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p><!-- 나열 --></p>
                            <p><strong>[직역]</strong> <!-- 직역 --></p>
                            <p><strong>[문법 해설]</strong> <!-- 5문장 이상 해설 --></p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p><!-- 문단 1 --></p>
                            <p><!-- 문단 2 --></p>

                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="키값" data-title="장절">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <!-- 본문 1 탭 -->
                <div id="content-book1" class="tab-content">
                    <article class="chapter-card card-book1">
                        <div class="card-content">
                            <h3>본문1 제목</h3>
                            <div class="key-question-box">
                                <p>질문: <!-- 질문 --></p>
                            </div>
                            <h4>역사적 문맥과 구조</h4>
                            <p><!-- 4-5문장 --></p>
                            <h4>핵심 신학과 구속사적 의미</h4>
                            <p><!-- 4-5문장 --></p>
                            <h4>개혁주의 적용과 성도의 삶</h4>
                            <p><!-- 4-5문장 --></p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="URL" data-title="제목">본문 보기</button>
                                <button class="btn btn-secondary listen-audio-btn" data-key="키값" data-title="제목">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
                <!-- 동일한 형식으로 본문2(content-book2), 본문3(content-book3), 본문4(content-book4) 작성 -->

                <!-- 종합 묵상 탭 -->
                <div id="content-integration" class="tab-content">
                    <article class="integration-card">
                        <div class="card-content">
                            <h3>주제 중심 신학적 종합: "<!-- 제목 -->"</h3>
                            <h4>관통하는 주제: <!-- 소제목 --></h4>
                            <p><!-- 문단 1 --></p>
                            <p><!-- 문단 2 --></p>
                            <p><!-- 문단 3 --></p>
                            <div class="button-group">
                                <a href="#top" class="btn btn-primary">맨 위로 돌아가기</a>
                            </div>
                        </div>
                    </article>
                </div>
            </main>
            <footer>
                <p>&copy; 2026 MacCheyne 5.0. All Rights Reserved.</p>
            </footer>
        </div>
    </div>
    
    <div class="modal-overlay" id="text-modal">
        <div class="modal-content">
            <div class="modal-header"><h2 id="modal-title"></h2><button class="modal-close-btn" id="modal-close">&times;</button></div>
            <div class="modal-body"><iframe id="modal-iframe" src=""></iframe></div>
        </div>
    </div>
    <div class="floating-nav" id="floating-nav">
        <button class="nav-btn" id="prev-tab"><span>◀</span></button>
        <div class="nav-info"><span class="current-tab" id="current-tab-info">1/7</span></div>
        <button class="nav-btn" id="next-tab"><span>▶</span></button>
    </div>
    <div id="player-container"></div>
    <div id="audio-player" style="position:fixed;bottom:0;left:0;right:0;background:rgba(0,0,0,0.9);backdrop-filter:blur(10px);padding:12px 20px;display:flex;align-items:center;justify-content:space-between;z-index:1001;color:white;transition:transform 0.3s;transform:translateY(100%);">
        <span id="player-info" style="font-size:0.9rem;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">재생 대기 중...</span>
        <div style="display:flex;gap:12px;align-items:center;">
            <button id="play-pause-btn" style="background:none;border:none;color:white;font-size:1.3rem;cursor:pointer;">▶</button>
            <button id="close-player-btn" style="background:none;border:none;color:#aaa;font-size:1.1rem;cursor:pointer;">✕</button>
        </div>
    </div>
    <script src="script.js"></script>
    <script>
        let audioUtterance = null;
        function playOriginalAudio(text, langCode) {
            if ('speechSynthesis' in window) {
                if (window.speechSynthesis.speaking || window.speechSynthesis.pending) window.speechSynthesis.cancel();
                setTimeout(() => {
                    audioUtterance = new SpeechSynthesisUtterance(text);
                    audioUtterance.lang = langCode;
                    window.speechSynthesis.speak(audioUtterance);
                }, 50);
            } else alert('TTS 미지원 브라우저입니다.');
        }
    </script>
</body>
</html>
```
**[프롬프트 복사 끝]**
