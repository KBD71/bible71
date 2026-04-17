<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>4월 18일 맥체인 성경읽기</title>
    <link rel="stylesheet" href="style.css">
    <style>
        :root { --overview-color: #6c757d; }
        .tab-btn[data-color="overview"].active { background-color: var(--overview-color); color: white; }
        .card-overview { border-color: var(--overview-color); }
        .card-overview h3 { color: var(--overview-color); }
        .key-question-box { background-color: #f1f3f5; border-left: 4px solid #495057; padding: 1.5rem; margin-bottom: 2rem; border-radius: 8px; }
        .key-question-box p { margin: 0; font-weight: 700; color: #212529; font-size: 1.1rem; }
        
        /* 원어 분석 심화 레이아웃 */
        .hebrew-grid { display: flex; flex-direction: column; gap: 1.5rem; margin: 2rem 0; }
        .hebrew-entry { background: #fff; border: 1px solid #dee2e6; border-radius: 12px; padding: 1.5rem; border-right: 6px solid #1a5c9a; direction: ltr; position: relative; }
        .hebrew-word-row { display: flex; align-items: baseline; gap: 15px; margin-bottom: 12px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
        .h-word { font-size: 2.2rem; font-weight: bold; color: #1a5c9a; font-family: 'Times New Roman', serif; }
        .h-label { font-size: 0.9rem; color: #888; font-weight: bold; text-transform: uppercase; }
        .h-content { font-size: 1rem; line-height: 1.7; color: #333; margin-top: 5px; }
        .h-content b { color: #d93025; }
        .pronounce-btn { background: #f8f9fa; border: 1px solid #ddd; border-radius: 50%; width: 32px; height: 32px; cursor: pointer; font-size: 14px; position: absolute; right: 20px; top: 20px; display: flex; align-items: center; justify-content: center; transition: background 0.2s; }
        .pronounce-btn:hover { background: #e9ecef; }
        
        .sentence-summary { background: #e7f3ff; padding: 1.5rem; border-radius: 8px; margin-top: 2rem; border: 1px solid #b3d7ff; direction: ltr; }
        .sentence-summary h5 { margin: 0 0 10px 0; font-size: 1.1rem; color: #0056b3; }
        .original-verse { font-size: 1.5rem; font-weight: bold; color: #1a5c9a; margin-top: 10px; display: block; text-align: right; direction: rtl; }
    </style>
</head>
<body>
    <div class="progress-container"><div class="progress-bar" id="reading-progress"></div></div>

    <div class="container">
        <div class="content-wrapper">
            <header>
                <h4>M'Cheyne Bible Reading Plan</h4>
                <h1>4월 18일</h1>
            </header>

            <nav class="tabs">
                <button class="tab-btn active" data-target="content-overview" data-color="overview" onclick="switchTab(0)">전체 개요</button>
                <button class="tab-btn" data-target="content-hebrew" data-color="book4" onclick="switchTab(1)">원어 깊이 읽기</button>
                <button class="tab-btn" data-target="content-book1" data-color="book1" onclick="switchTab(2)">레위기 22장</button>
                <button class="tab-btn" data-target="content-book2" data-color="book2" onclick="switchTab(3)">시편 28-29편</button>
                <button class="tab-btn" data-target="content-book3" data-color="book3" onclick="switchTab(4)">전도서 5장</button>
                <button class="tab-btn" data-target="content-book4" data-color="book4" onclick="switchTab(5)">디모데후서 1장</button>
                <button class="tab-btn" data-target="content-integration" data-color="integration" onclick="switchTab(6)">종합 묵상</button>
            </nav>

            <main>
                <div id="content-overview" class="tab-content active">
                    <article class="chapter-card card-overview">
                        <div class="card-content">
                            <h3>오늘의 성경적 권면</h3>
                            <p>오늘은 거룩한 성물을 다루는 제사장의 성결함과 자연의 경이로움 속에 울려 퍼지는 하나님의 위엄 있는 소리, 그리고 복음을 지키기 위한 사도적 고난을 묵상합니다.</p>
                            <ul>
                                <li><strong>레위기 22장:</strong> 성결 규례와 흠 없는 제물의 의미를 살핍니다.</li>
                                <li><strong>시편 28-29편:</strong> 간구에 응답하시는 반석과 폭풍 가운데 임하는 여호와의 소리를 찬양합니다.</li>
                                <li><strong>전도서 5장:</strong> 하나님 앞에서 말을 삼가며 경외함으로 예배할 것을 배웁니다.</li>
                                <li><strong>디모데후서 1장:</strong> 성령의 능력으로 복음과 함께 고난을 받으라는 권면을 듣습니다.</li>
                            </ul>
                        </div>
                    </article>
                </div>

                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 심층 분석: 시편 29편 2절</h3>
                            <div class="key-question-box">
                                <p>“여호와께 그의 이름에 합당한 영광을 돌리며 거룩한 옷을 입고 여호와께 예배할지어다”</p>
                            </div>

                            <div class="hebrew-grid">
                                <div class="hebrew-entry">
                                    <button class="pronounce-btn" onclick="speakHebrew('הָבוּ')">🔊</button>
                                    <div class="hebrew-word-row">
                                        <span class="h-word">הָבוּ</span>
                                        <span class="h-label">(Havu)</span>
                                    </div>
                                    <p class="h-content"><strong>원래 뜻:</strong> '가져오다', '주다', '바치다'는 뜻을 가진 동사 '야합(יָהַב)'의 명령형입니다. 본래 다른 이에게 속한 정당한 몫을 되돌려주는 행위를 지칭합니다.</p>
                                    <p class="h-content"><strong>신학적 해설:</strong> 예배는 우리가 새로운 영광을 하나님께 보태는 것이 아니라, 원래 하나님의 것인 영광을 <b>인정하여 돌려드리는 것</b>입니다. 이는 창조주에 대한 피조물의 당연한 의무를 선포합니다.</p>
                                </div>

                                <div class="hebrew-entry">
                                    <button class="pronounce-btn" onclick="speakHebrew('כָּבוֹד')">🔊</button>
                                    <div class="hebrew-word-row">
                                        <span class="h-word">כָּבוֹד</span>
                                        <span class="h-label">(Kavod)</span>
                                    </div>
                                    <p class="h-content"><strong>원래 뜻:</strong> '무겁다', '중량이 나가다'는 의미의 '카바드(כָּבַד)'에서 유래했습니다. 고대 세계에서 가치는 곧 무게로 측정되었기에 '풍요'와 '존귀'를 동시에 뜻합니다.</p>
                                    <p class="h-content"><strong>신학적 해설:</strong> 하나님을 영광스럽게 하는 것은 그분을 우리 삶에서 <b>가장 무거운 분</b>으로 대우하는 것입니다. 세상을 가볍게 여기고 하나님을 가장 가치 있게 여기는 것이 경외함의 본질입니다.</p>
                                </div>

                                <div class="hebrew-entry">
                                    <button class="pronounce-btn" onclick="speakHebrew('בְּהַדְרַת־קֹדֶשׁ')">🔊</button>
                                    <div class="hebrew-word-row">
                                        <span class="h-word">בְּהַדְרַת־קֹדֶשׁ</span>
                                        <span class="h-label">(Be-hadrat-qodesh)</span>
                                    </div>
                                    <p class="h-content"><strong>원래 뜻:</strong> '아름다움' 혹은 '화려한 장식'을 뜻하는 '하다라'와 '구별됨'의 '코데쉬'가 결합했습니다. 성소의 거룩한 예복과 엄숙한 분위기를 뜻합니다.</p>
                                    <p class="h-content"><strong>신학적 해설:</strong> 예배자는 외적인 화려함이 아니라 <b>하나님의 거룩함이라는 장식</b>을 입어야 합니다. 거룩함은 예배자가 갖추어야 할 유일하고도 필수적인 예복입니다.</p>
                                </div>
                            </div>

                            <div class="sentence-summary">
                                <h5>[심층 해설 및 원문]</h5>
                                <p>이 구절은 여호와의 이름, 즉 그분의 모든 속성과 인격에 걸맞은 최고의 무게감을 인정하며 구별된 태도로 굴복할 것을 명령합니다. 이는 만물의 왕이신 하나님 앞에 서는 피조물의 정당한 반응입니다.</p>
                                <span class="original-verse">הָב֣וּ לַ֭יהוָה כְּב֣וֹ드 שְׁמ֑וֹ הִשְׁתַּחֲו֥וּ לַ֝יהוָ֗ה בְּהַדְרַת־קֹֽדֶשׁ׃</span>
                            </div>
                            
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_28_29" data-title="시편 28-29편">오디오 재생</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-book1" class="tab-content">
                    <article class="chapter-card card-book1">
                        <div class="card-content">
                            <h3>레위기 22장: 성결의 규례와 흠 없는 제물</h3>
                            <div class="key-question-box">
                                <p>질문: 왜 하나님은 흠 있는 짐승을 드리는 것을 가증하게 여기셨는가?</p>
                            </div>
                            <h4>역사적 배경과 제사장의 책임</h4>
                            <p>레위기 22장은 제사장들이 거룩한 성물을 다룰 때 요구되는 엄격한 정결 규례를 명시합니다. 제사장은 부정한 상태에서 성물을 먹을 수 없었으며, 이는 하나님의 성호(聖號)를 욕되게 하지 않기 위함이었습니다. 하나님의 직분자가 먼저 정결해야 한다는 이 원리는 현대 교회의 지도자와 성도들에게 동일하게 적용됩니다.</p>
                            <h4>흠 없는 제물의 구속사적 의미</h4>
                            <p>하나님은 신체적 결함이 있는 짐승을 제물로 드리는 행위를 엄히 금하셨습니다. 이는 장차 우리의 죄를 대속하시기 위해 오실 <b>'흠 없고 점 없는 어린 양'</b>이신 예수 그리스도를 예표합니다. 우리가 드리는 최상의 제물이라 할지라도 결국 그리스도의 완벽한 의를 덧입지 않고서는 하나님께 열납될 수 없음을 가르칩니다.</p>
                            <h4>신학적 적용</h4>
                            <p>칼빈은 본문을 주해하며 예배자가 하나님께 나아갈 때 '남은 것'을 드리는 태도를 강력히 경계했습니다. 예배의 중심은 드리는 자의 정성 이전에, 하나님께서 요구하시는 거룩한 기준에 부합하는가에 있습니다.</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/LEV_22.html" data-title="레위기 22장">본문 보기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-book2" class="tab-content">
                    <article class="chapter-card card-book2">
                        <div class="card-content">
                            <h3>시편 28-29편: 반석과 영광의 소리</h3>
                            <div class="key-question-box">
                                <p>질문: 자연의 거대한 폭풍 속에서 하나님의 영광을 어떻게 발견할 수 있는가?</p>
                            </div>
                            <h4>28편: 침묵을 뚫는 탄원</h4>
                            <p>다윗은 침묵하시는 것 같은 하나님을 향해 부르짖습니다. 그에게 하나님은 '반석'이시며, 이 반석은 변하지 않는 하나님의 작정과 신실하심을 상징합니다. 개혁주의 신학에서 기도는 하나님의 계획을 바꾸는 것이 아니라, 기도자가 하나님의 신실한 통치(반석) 위로 옮겨지는 과정입니다.</p>
                            <h4>29편: 폭풍우 속의 여호와</h4>
                            <p>29편은 '여호와의 소리'가 일곱 번이나 반복되며 창조주의 장엄함을 선포합니다. 가나안 사람들이 폭풍을 바알의 위력으로 두려워할 때, 다윗은 그 폭풍의 근원이 여호와의 목소리라고 선포합니다. 만물을 복종시키시는 하나님의 말씀은 결국 자기 백성에게 평강을 주시는 구원의 방편이 됩니다.</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/PSA_28.html,https://kbd71.github.io/bible71/bible_html/PSA_29.html" data-title="시편 28-29편">본문 보기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-book3" class="tab-content">
                    <article class="chapter-card card-book3">
                        <div class="card-content">
                            <h3>전도서 5장: 예배자의 경외심과 자족의 지혜</h3>
                            <div class="key-question-box">
                                <p>질문: '하나님은 하늘에 계시고 너는 땅에 있음이니라'는 선언이 주는 교훈은 무엇인가?</p>
                            </div>
                            <h4>경거망동을 금하는 예배</h4>
                            <p>전도자는 하나님의 집에 들어갈 때 발을 삼가라고 권고합니다. 예배는 많은 말을 쏟아붓는 시간이 아니라 하나님의 말씀을 경청하는 시간입니다. 인간의 유한함을 인정하고 하나님의 초월성을 경외하는 것이 참된 지혜의 시작입니다.</p>
                            <h4>재물의 허무와 하나님의 선물</h4>
                            <p>은을 사랑하는 자는 은으로 만족할 수 없습니다. 소유의 증가가 평안을 보장하지 않음을 강조하며, 하나님이 주신 몫을 기쁨으로 누리는 것 자체가 '하나님의 선물'임을 역설합니다. 이는 자본주의 사회 속에서도 신자가 누려야 할 자족의 개혁주의적 태도를 보여줍니다.</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/ECC_05.html" data-title="전도서 5장">본문 보기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-book4" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>디모데후서 1장: 복음을 부끄러워하지 않는 믿음</h3>
                            <div class="key-question-box">
                                <p>질문: 사역자가 '두려워하는 마음'을 극복하는 유일한 길은 무엇인가?</p>
                            </div>
                            <h4>신앙의 유산과 성령의 능력</h4>
                            <p>바울은 로이스와 유니게로부터 흐른 디모데의 신앙 유산을 상기시킵니다. 신앙은 성령의 능력 안에서 계승됩니다. 하나님이 주신 것은 두려워하는 마음이 아니라 오직 능력과 사랑과 절제하는 마음입니다. 우리는 우리 안에 거하시는 성령을 의지하여 복음의 아름다운 부탁을 지켜내야 합니다.</p>
                            <h4>고난의 영광</h4>
                            <p>바울은 쇠사슬에 매인 자신을 부끄러워하지 말고 오직 하나님의 능력을 따라 복음과 함께 고난을 받으라고 명령합니다. 복음의 가치를 발견한 자는 세상의 수치를 넉넉히 이길 수 있는 담대함을 얻게 됩니다.</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/2TI_01.html" data-title="디모데후서 1장">본문 보기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-integration" class="tab-content">
                    <article class="integration-card">
                        <div class="card-content">
                            <h3>종합 묵상: "경외함으로 열리는 평강의 문"</h3>
                            <p>오늘의 네 본문은 우리가 하나님을 '가장 무거운 분(영광)'으로 대우할 때 비로소 우리 삶의 질서가 바로 잡힘을 보여줍니다. 흠 없는 제물로 그분의 가치를 인정하고(레위기), 폭풍우 속에서도 그분의 목소리를 들으며(시편), 입을 닫고 그분의 광대하심을 경외하며(전도서), 그 영광스러운 복음을 위해 기꺼이 고난을 지는 것(디모데후서). 이것이 오늘 우리에게 요구되는 하나님 경외의 삶입니다.</p>
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

    <script>
        // 히브리어 발음 기능
        function speakHebrew(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'he-IL'; // 히브리어 설정
                speechSynthesis.speak(utterance);
            } else {
                alert("이 브라우저는 발음 듣기를 지원하지 않습니다.");
            }
        }

        // 본문 보기 디버깅용 이벤트 (기존 script.js와 충돌 방지를 위해 별도 정의)
        document.querySelectorAll('.view-text-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const path = this.getAttribute('data-path');
                console.log("요청된 성경 경로:", path);
            });
        });
    </script>
    <script src="script.js"></script>
</body>
</html>
