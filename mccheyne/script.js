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
        
        /* 히브리어 심화 레이아웃 */
        .hebrew-grid { display: flex; flex-direction: column; gap: 1.5rem; margin: 2rem 0; }
        .hebrew-entry { background: #fff; border: 1px solid #dee2e6; border-radius: 12px; padding: 1.5rem; border-right: 6px solid #1a5c9a; direction: ltr; position: relative; }
        .hebrew-word-row { display: flex; align-items: baseline; gap: 15px; margin-bottom: 12px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
        .h-word { font-size: 2.5rem; font-weight: bold; color: #1a5c9a; font-family: 'Times New Roman', serif; }
        .h-label { font-size: 0.9rem; color: #888; font-weight: bold; }
        .h-section { margin-top: 10px; }
        .h-title { font-weight: 700; color: #444; margin-right: 5px; }
        .h-desc { font-size: 1rem; line-height: 1.7; color: #333; }
        .h-desc b { color: #d93025; }
        
        .pronounce-btn { background: #f8f9fa; border: 1px solid #ddd; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; position: absolute; right: 20px; top: 20px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
        .pronounce-btn:hover { background: #e9ecef; }
        
        .verse-footer { background: #e7f3ff; padding: 1.5rem; border-radius: 8px; margin-top: 2rem; border: 1px solid #b3d7ff; direction: ltr; }
        .original-text { font-size: 1.6rem; font-weight: bold; color: #1a5c9a; margin-top: 10px; display: block; text-align: right; direction: rtl; line-height: 1.5; }
        .sentence-desc { font-size: 1.05rem; line-height: 1.8; color: #333; margin-top: 15px; }
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
                <button class="tab-btn active" data-color="overview" onclick="switchTab(0)">전체 개요</button>
                <button class="tab-btn" data-color="book4" onclick="switchTab(1)">원어 심층 분석</button>
                <button class="tab-btn" data-color="book1" onclick="switchTab(2)">레위기 22장</button>
                <button class="tab-btn" data-color="book2" onclick="switchTab(3)">시편 28-29편</button>
                <button class="tab-btn" data-color="book3" onclick="switchTab(4)">전도서 5장</button>
                <button class="tab-btn" data-color="book4" onclick="switchTab(5)">디모데후서 1장</button>
                <button class="tab-btn" data-color="integration" onclick="switchTab(6)">종합 묵상</button>
            </nav>

            <main>
                <div id="content-overview" class="tab-content active">
                    <article class="chapter-card card-overview">
                        <div class="card-content">
                            <h3>4월 18일 성경읽기 안내 </h3>
                            <p>오늘은 성결의 규례와 하나님의 엄위하신 소리, 예배자의 마땅한 경외심과 복음을 향한 사도적 소명을 묵상합니다.</p>
                            <ul>
                                <li><strong>레위기 22장:</strong> 성물을 다루는 제사장의 성결과 흠 없는 제물의 규례[cite: 9].</li>
                                <li><strong>시편 28-29편:</strong> 반석 되신 하나님을 향한 부르짖음과 폭풍 가운데 임하는 여호와의 소리[cite: 19].</li>
                                <li><strong>전도서 5장:</strong> 하나님 앞에서 말을 삼가며, 재물의 허무를 깨닫고 하나님을 경외하는 지혜[cite: 19].</li>
                                <li><strong>디모데후서 1장:</strong> 성령의 능력으로 복음과 함께 고난을 받으며 신앙의 유산을 지키라는 권면[cite: 19].</li>
                            </ul>
                        </div>
                    </article>
                </div>

                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 심층 주해: 시편 29편 2절 [cite: 19]</h3>
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
                                    <div class="h-section">
                                        <span class="h-title">[사전적 뜻]:</span>
                                        <span class="h-desc">'가져오다', '주다', '바치다'를 뜻하는 동사 '야합(יָהַב)'의 명령형입니다[cite: 19].</span>
                                    </div>
                                    <div class="h-section">
                                        <span class="h-title">[신학적 해설]:</span>
                                        <span class="h-desc">예배는 인간이 하나님께 새로운 영광을 보태는 것이 아니라, <b>본래 하나님의 것인 주권과 가치</b>를 인정하여 다시 그분께 돌려드리는 행위입니다.</span>
                                    </div>
                                </div>

                                <div class="hebrew-entry">
                                    <button class="pronounce-btn" onclick="speakHebrew('כָּבוֹד')">🔊</button>
                                    <div class="hebrew-word-row">
                                        <span class="h-word">כָּבוֹד</span>
                                        <span class="h-label">(Kavod)</span>
                                    </div>
                                    <div class="h-section">
                                        <span class="h-title">[사전적 뜻]:</span>
                                        <span class="h-desc">'무거움', '중량'을 뜻하는 '카바드(כָּבַד)'에서 유래하여 '명예'와 '존귀'를 의미합니다[cite: 19].</span>
                                    </div>
                                    <div class="h-section">
                                        <span class="h-title">[신학적 해설]:</span>
                                        <span class="h-desc">하나님을 영광스럽게 한다는 것은 그분을 우리 삶에서 <b>가장 무게감 있고 가치 있는 분</b>으로 대우하는 것입니다.</span>
                                    </div>
                                </div>
                            </div>

                            <div class="verse-footer">
                                <h5>[전체 문장 해설 및 원문]</h5>
                                <span class="original-text">הָב֣וּ לַ֭יהוָה כְּב֣오ֹד שְׁמ֑וֹ הִשְׁתַּחֲו֥וּ לַ֝יהוָ֗ה בְּהַדְרַת־קֹֽדֶשׁ׃</span>
                                <p class="sentence-desc">시편 기자는 만물을 향해 여호와의 이름, 즉 그분의 모든 성품에 걸맞은 최고의 무게감을 인정하며(Havu Kavod), 구별된 거룩함으로 그분 앞에 굴복할 것을 명령하고 있습니다[cite: 19].</p>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-book1" class="tab-content">
                    <article class="chapter-card card-book1">
                        <div class="card-content">
                            <h3>레위기 22장: 성물과 제물의 거룩함 [cite: 9]</h3>
                            <div class="key-question-box"><p>질문: 흠 없는 제물은 우리에게 어떤 영적 완벽성을 요구하는가? [cite: 9]</p></div>
                            <h4>역사적 문맥과 제사장의 정결</h4>
                            <p>제사장들은 부정한 상태에서 성물을 먹을 수 없었으며, 이는 하나님의 성소를 더럽히지 않기 위한 엄격한 지침이었습니다[cite: 9]. 하나님께 가까이 나아가는 직분자일수록 더 높은 수준의 성결이 요구됨을 보여줍니다[cite: 9].</p>
                            <h4>흠 없는 제물: 그리스도의 예표</h4>
                            <p>신체적 결함이 있는 짐승은 결코 제물이 될 수 없었습니다[cite: 9]. 이는 장차 오실 <b>'흠 없고 점 없는 어린 양'</b>이신 예수 그리스도의 완전한 대속을 예표합니다[cite: 9]. 우리는 우리의 정성이 아닌 그리스도의 완전한 의를 힘입어 하나님께 나아갑니다.</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/LEV_22.html" data-title="레위기 22장">본문 보기</button>
                                <button class="btn btn-secondary listen-audio-btn" data-key="LEV_22" data-title="레위기 22장">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-book2" class="tab-content">
                    <article class="chapter-card card-book2">
                        <div class="card-content">
                            <h3>시편 28-29편: 폭풍 속에 임재하시는 하나님 [cite: 19]</h3>
                            <div class="key-question-box"><p>질문: 만물을 진동시키는 '여호와의 소리'가 성도에게 주는 평강은 무엇인가? [cite: 19]</p></div>
                            <h4>28편: 반석을 향한 비명</h4>
                            <p>다윗은 침묵하시는 것 같은 하나님을 향해 부르짖으며 '나의 반석'이 되어 주시길 간구합니다[cite: 19]. 성도의 기도는 하나님의 신실하심이라는 반석 위에 우리를 고정시키는 과정입니다[cite: 19].</p>
                            <h4>29편: 영광의 하나님과 그 소리</h4>
                            <p>'여호와의 소리'가 일곱 번 반복되며 폭풍우 속에서도 만물을 통치하시는 창조주의 위엄을 노래합니다[cite: 19]. 이 두려운 권능의 소리는 결국 자기 백성에게 평강의 복을 주시는 약속으로 귀결됩니다[cite: 19].</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/PSA_28.html,https://kbd71.github.io/bible71/bible_html/PSA_29.html" data-title="시편 28-29편">본문 보기</button>
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_28_29" data-title="시편 28-29편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-book3" class="tab-content">
                    <article class="chapter-card card-book3">
                        <div class="card-content">
                            <h3>전도서 5장: 예배와 재물에 대한 지혜 [cite: 19]</h3>
                            <div class="key-question-box"><p>질문: '하나님 앞에서 말을 적게 하라'는 권고는 어떤 경외심을 뜻하는가? [cite: 19]</p></div>
                            <h4>예배자의 자세: 경청과 서원</h4>
                            <p>하나님의 집에 들어갈 때 발을 삼가고 경솔한 서원을 금해야 합니다[cite: 19]. 예배는 나의 요구를 쏟아놓는 자리가 아니라, 하나님의 광대하심 앞에 우리를 굴복시키는 자리입니다[cite: 19].</p>
                            <h4>재물의 허무와 하나님의 선물</h4>
                            <p>은을 사랑하는 자는 만족이 없으나, 하나님이 주신 복을 누리고 즐거워하는 것은 하나님의 선물입니다[cite: 19]. 자족함은 소유의 양이 아닌 공급하시는 분과의 관계에서 옵니다[cite: 19].</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/ECC_05.html" data-title="전도서 5장">본문 보기</button>
                                <button class="btn btn-secondary listen-audio-btn" data-key="ECC_5" data-title="전도서 5장">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-book4" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>디모데후서 1장: 복음과 함께 고난을 받으라 [cite: 19]</h3>
                            <div class="key-question-box"><p>질문: 우리 안에 거하시는 성령은 복음을 지키는 데 어떤 역할을 하는가? [cite: 19]</p></div>
                            <h4>신앙의 전수와 은사</h4>
                            <p>바울은 디모데의 어머니와 외조모로부터 이어진 '거짓 없는 믿음'을 상기시키며 그 안의 은사를 다시 불붙이게 합니다[cite: 19]. 신앙은 언약적 가문과 공동체 내에서 성령의 능력으로 계승됩니다[cite: 19].</p>
                            <h4>두려움을 이기는 사랑</h4>
                            <p>하나님이 주신 것은 두려워하는 마음이 아니라 능력과 사랑과 절제하는 마음입니다[cite: 19]. 복음의 가치를 아는 자는 감옥에 갇힌 바울을 부끄러워하지 않고 복음과 함께 기꺼이 고난을 받습니다[cite: 19].</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/2TI_01.html" data-title="디모데후서 1장">본문 보기</button>
                                <button class="btn btn-secondary listen-audio-btn" data-key="2TI_1" data-title="디모데후서 1장">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="content-integration" class="tab-content">
                    <article class="integration-card">
                        <div class="card-content">
                            <h3>종합 묵상: "영광의 무게 중심" </h3>
                            <p>오늘의 모든 말씀은 우리 존재의 무게 중심을 하나님께 두라고 촉구합니다. 레위기는 예배의 성결을, 시편은 창조주의 권능을, 전도서는 예배자의 경외를, 디모데후서는 복음의 사명을 가르칩니다. 하나님을 가장 무거운 분(Kavod)으로 대우할 때, 우리 삶에 참된 평강이 임합니다.</p>
                            <div class="button-group">
                                <a href="#top" class="btn btn-primary" onclick="switchTab(0); return false;">맨 위로 돌아가기</a>
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
            <div class="modal-header"><h2 id="modal-title"></h2><button class="modal-close-btn" id="modal-close" onclick="closeModal()">&times;</button></div>
            <div class="modal-body"><iframe id="modal-iframe" src=""></iframe></div>
        </div>
    </div>
    
    <div id="player-container"></div>
    <div id="audio-player" style="position:fixed;bottom:0;left:0;right:0;background:rgba(0,0,0,0.9);backdrop-filter:blur(10px);padding:12px 20px;display:flex;align-items:center;justify-content:space-between;z-index:1001;color:white;transition:transform 0.3s;transform:translateY(100%);">
        <span id="player-info" style="font-size:0.9rem;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">재생 대기 중...</span>
        <div style="display:flex;gap:12px;align-items:center;">
            <button id="play-pause-btn" style="background:none;border:none;color:white;font-size:1.3rem;cursor:pointer;">▶</button>
            <button id="close-player-btn" style="background:none;border:none;color:#aaa;font-size:1.1rem;cursor:pointer;" onclick="document.getElementById('audio-player').style.transform='translateY(100%)'">✕</button>
        </div>
    </div>

    <script>
        // 탭 전환 시스템 (ID 정합성 해결)
        function switchTab(index) {
            const tabs = [
                'content-overview', 'content-hebrew', 'content-book1', 
                'content-book2', 'content-book3', 'content-book4', 'content-integration'
            ];
            
            document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            
            const targetId = tabs[index];
            const targetContent = document.getElementById(targetId);
            if(targetContent) targetContent.style.display = 'block';
            
            const targetBtn = document.querySelectorAll('.tab-btn')[index];
            if(targetBtn) targetBtn.classList.add('active');
            
            window.scrollTo(0, 0);
        }

        // 본문 보기 모달 제어
        document.querySelectorAll('.view-text-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const path = this.getAttribute('data-path').split(',')[0];
                const title = this.getAttribute('data-title');
                document.getElementById('modal-title').innerText = title;
                document.getElementById('modal-iframe').src = path;
                document.getElementById('text-modal').style.display = 'flex';
            });
        });

        function closeModal() {
            document.getElementById('text-modal').style.display = 'none';
            document.getElementById('modal-iframe').src = '';
        }

        // 히브리어 발음 (Web Speech API)
        function speakHebrew(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'he-IL';
                window.speechSynthesis.speak(utterance);
            }
        }
    </script>
    <script src="script.js"></script>
</body>
</html>
