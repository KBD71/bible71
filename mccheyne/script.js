<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>4월 18일 맥체인 성경읽기</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* 맥체인 5.0 추가 스타일 */
        :root { --overview-color: #6c757d; }
        .tab-btn[data-color="overview"].active { background-color: var(--overview-color); color: white; }
        .card-overview { border-color: var(--overview-color); }
        .card-overview h3 { color: var(--overview-color); }
        
        /* 히브리어 심화 레이아웃 */
        .hebrew-grid { display: flex; flex-direction: column; gap: 1.5rem; margin: 2rem 0; }
        .hebrew-entry { background: #fff; border: 1px solid #dee2e6; border-radius: 12px; padding: 1.5rem; border-right: 6px solid #1a5c9a; direction: ltr; position: relative; }
        .hebrew-word-row { display: flex; align-items: baseline; gap: 15px; margin-bottom: 12px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
        .h-word { font-size: 2.8rem; font-weight: bold; color: #1a5c9a; font-family: 'Times New Roman', serif; }
        .h-label { font-size: 0.95rem; color: #888; font-weight: bold; }
        .h-section { margin-top: 10px; }
        .h-title { font-weight: 700; color: #444; margin-right: 8px; border-left: 3px solid #1a5c9a; padding-left: 8px; }
        .h-desc { font-size: 1.05rem; line-height: 1.8; color: #333; }
        .h-desc b { color: #d93025; }
        
        .pronounce-btn { background: #f8f9fa; border: 1px solid #ddd; border-radius: 50%; width: 42px; height: 42px; cursor: pointer; position: absolute; right: 20px; top: 20px; display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .pronounce-btn:hover { background: #e9ecef; transform: scale(1.1); }
        
        .verse-footer { background: #fdfdfe; padding: 2rem; border-radius: 12px; margin-top: 2rem; border: 1px solid #e0e0e0; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); }
        .original-text { font-size: 1.8rem; font-weight: bold; color: #1a5c9a; margin: 15px 0; display: block; text-align: right; direction: rtl; line-height: 1.6; font-family: 'SBL Hebrew', 'Times New Roman', serif; }
        .sentence-desc { font-size: 1.1rem; line-height: 1.9; color: #444; margin-top: 20px; padding: 15px; background: #fff; border-radius: 8px; border-left: 5px solid #c89200; }
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
                <div id="tab-0" class="tab-content active">
                    <article class="chapter-card card-overview">
                        <div class="card-content">
                            <h3>오늘의 거룩한 여정</h3>
                            <p>오늘은 성결의 규례와 하나님의 엄위하신 권능, 예배자의 경외심과 복음을 향한 사명을 묵상합니다. 구약의 제사법부터 신약의 복음 전수까지 관통하는 주제는 '하나님의 거룩한 주권'입니다.</p>
                            <ul>
                                <li><strong>레위기 22장:</strong> 성물을 다루는 자의 성결과 제물의 완전성에 대하여.</li>
                                <li><strong>시편 28-29편:</strong> 반석 되신 하나님을 향한 부르짖음과 만물을 진동시키는 여호와의 소리.</li>
                                <li><strong>전도서 5장:</strong> 하나님 앞에서 말을 삼가며, 자족의 은혜를 누리는 지혜.</li>
                                <li><strong>디모데후서 1장:</strong> 복음과 함께 고난을 받으며 신앙의 유산을 지키는 사명.</li>
                            </ul>
                        </div>
                    </article>
                </div>

                <div id="tab-1" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 심층 주해: 시편 29편 2절</h3>
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
                                        <span class="h-title">사전적 의미</span>
                                        <span class="h-desc">'가져오다', '주다', '바치다'를 뜻하는 동사 '야합(יָהַב)'의 명령형입니다. 본래 상대방에게 속한 권리나 몫을 정당하게 되돌려주는 행위를 의미합니다.</span>
                                    </div>
                                    <div class="h-section">
                                        <span class="h-title">신학적 해설</span>
                                        <span class="h-desc">예배는 인간이 하나님께 새로운 가치를 부여하는 것이 아니라, <b>본래 하나님의 것인 주권과 영광</b>을 피조물이 마땅히 인정하여 그분께 귀속시키는 '신앙적 반환'입니다.</span>
                                    </div>
                                </div>

                                <div class="hebrew-entry">
                                    <button class="pronounce-btn" onclick="speakHebrew('כָּבוֹ드')">🔊</button>
                                    <div class="hebrew-word-row">
                                        <span class="h-word">כָּבוֹ드</span>
                                        <span class="h-label">(Kavod)</span>
                                    </div>
                                    <div class="h-section">
                                        <span class="h-title">사전적 의미</span>
                                        <span class="h-desc">'무거움', '중량'을 뜻하는 '카바드(כָּבַד)'에서 유래했습니다. 고대에는 가치 있는 것일수록 무거웠기에 '존귀', '부요', '영광'을 뜻합니다.</span>
                                    </div>
                                    <div class="h-section">
                                        <span class="h-title">신학적 해설</span>
                                        <span class="h-desc">하나님을 영화롭게 한다는 것은 그분을 우리 삶에서 <b>가장 무겁고 가치 있는 분</b>으로 대우하는 것입니다. 세상을 가볍게 여기고 하나님을 가장 무겁게 대우하는 것이 경외함의 본질입니다.</span>
                                    </div>
                                </div>
                            </div>

                            <div class="verse-footer">
                                <h5>[문장 주해 및 원문]</h5>
                                <span class="original-text">הָב֣וּ לַ֭יהוָה כְּב֣וֹד שְׁמ֑וֹ הִשְׁתַּחֲו֥וּ לַ֝יהוָ֗회 בְּהַדְרַת־קֹֽדֶשׁ׃</span>
                                <div class="sentence-desc">
                                    본문은 여호와의 이름(성품과 인격)에 걸맞은 최고의 무게감을 인정하며(Havu Kavod), 구별된 거룩함의 예복을 입고 그분 앞에 전적으로 굴복할 것을 명령합니다. 이는 창조주를 향한 피조물의 가장 아름다운 질서입니다.
                                </div>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="tab-2" class="tab-content">
                    <article class="chapter-card card-book1">
                        <div class="card-content">
                            <h3>레위기 22장: 성결의 규례와 흠 없는 제물</h3>
                            <div class="key-question-box"><p>질문: 흠 있는 제물을 금지하신 원리는 오늘날 우리의 예배 태도에 어떤 도전을 주는가?</p></div>
                            <p>레위기 22장은 제사장들이 거룩한 성물을 다룰 때 지켜야 할 엄격한 지침과 하나님께 드려질 제물의 자격을 규정합니다. 제사장이 부정할 때 성물을 먹는 행위는 하나님의 성호를 욕되게 하는 것으로 간주되었습니다. 이는 하나님께 가까이 나아가는 자일수록 더 높은 수준의 정결함이 요구됨을 보여줍니다.</p>
                            <p>특히 신체적 결함이 있는 짐승을 제물로 드리지 못하게 하신 명령은 하나님은 '남는 것'이나 '병든 것'을 받으시는 분이 아님을 분명히 합니다. 이 '흠 없음'의 규례는 장차 오실 <b>'흠 없고 점 없는 어린 양'</b>이신 예수 그리스도를 예표합니다. 우리는 그리스도의 완전한 의를 덧입어 하나님께 나아갈 수 있습니다.</p>
                            <p>개혁주의 신학은 이 본문을 통해 예배의 외적 형식보다 드리는 자의 마음이 하나님의 거룩한 기준에 부합하는지를 점검하게 합니다. 최상의 것을 드리는 것은 하나님을 하나님답게 인정하는 실제적인 고백입니다.</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/LEV_22.html" data-title="레위기 22장">본문 보기</button>
                                <button class="btn btn-secondary listen-audio-btn" data-key="LEV_22" data-title="레위기 22장">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="tab-3" class="tab-content">
                    <article class="chapter-card card-book2">
                        <div class="card-content">
                            <h3>시편 28-29편: 반석과 권능의 소리</h3>
                            <div class="key-question-box"><p>질문: 대자연의 폭풍 속에서 하나님의 영광을 발견하는 성도의 유익은 무엇인가?</p></div>
                            <p>28편에서 다윗은 침묵하시는 것 같은 하나님을 향해 부르짖으며 '나의 반석'이 되어 주시길 간구합니다. 반석은 변하지 않는 하나님의 신실하심을 상징합니다. 기도는 하나님의 계획을 바꾸는 것이 아니라, 기도자가 하나님의 신실한 통치라는 반석 위에 자신을 견고히 세우는 과정입니다.</p>
                            <p>이어지는 29편은 분위기가 반전되어 대자연의 폭풍 속에서 드러나는 하나님의 위엄을 찬양합니다. '여호와의 소리'가 일곱 번이나 반복되며 백향목을 꺾고 광야를 진동시키는 말씀의 능력을 형상화합니다. 가나안 사람들이 폭풍을 바알의 힘으로 두려워할 때, 다윗은 그 폭풍의 주관자가 바로 여호와이심을 선포합니다.</p>
                            <p>장엄하고 두려운 하나님의 권능은 결국 '자기 백성에게 평강의 복을 주시리로다'라는 축복으로 귀결됩니다. 창조주를 경외하는 자만이 세상의 그 어떤 폭풍 속에서도 참된 안식을 누릴 수 있음을 가르쳐 줍니다.</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/PSA_28.html,https://kbd71.github.io/bible71/bible_html/PSA_29.html" data-title="시편 28-29편">본문 보기</button>
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_28_29" data-title="시편 28-29편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="tab-4" class="tab-content">
                    <article class="chapter-card card-book3">
                        <div class="card-content">
                            <h3>전도서 5장: 예배와 재물에 관한 지혜</h3>
                            <div class="key-question-box"><p>질문: '하나님은 하늘에 계시고 너는 땅에 있음이니라'는 사실이 예배자의 언어를 어떻게 변화시키는가?</p></div>
                            <p>전도자는 하나님의 집에 들어갈 때 발을 삼가고, 함부로 입을 열어 서원하지 말라고 엄히 경고합니다. 예배는 나의 욕구를 관철시키는 자리가 아니라 하나님의 말씀을 듣는 자리입니다. 인간의 유한함과 하나님의 초월성을 인식하는 것이 예배의 시작이자 경외함의 본질입니다.</p>
                            <p>또한 재물의 허무함을 통찰력 있게 묘사합니다. 은을 사랑하는 자는 은으로 만족하지 못하며, 소유의 증가는 오히려 근심을 더할 수 있습니다. 그러나 하나님은 자기가 수고한 것을 즐거워하는 마음을 '선물'로 주십니다. 재물 자체가 복이 아니라, 그것을 주신 분과의 관계에서 누리는 자족함이 진정한 복입니다.</p>
                            <p>개혁주의적 관점에서 자족은 하나님의 주권적 공급을 신뢰하는 구체적인 신앙의 열매입니다. 우리는 땅의 소유보다 하늘의 풍성함을 사모하며 주어진 몫에 감사해야 합니다.</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/ECC_05.html" data-title="전도서 5장">본문 보기</button>
                                <button class="btn btn-secondary listen-audio-btn" data-key="ECC_5" data-title="전도서 5장">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="tab-5" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>디모데후서 1장: 복음과 함께 받는 고난</h3>
                            <div class="key-question-box"><p>질문: 성령의 능력이 신앙의 유산을 지키는 데 어떻게 역사하는가?</p></div>
                            <p>바울은 감옥에서 죽음을 앞두고 사랑하는 아들 디모데에게 마지막 권면을 전합니다. 그는 디모데의 어머니와 외조모로부터 이어진 '거짓 없는 믿음'을 상기시킵니다. 이는 신앙의 전수가 언약적 가정 내에서 얼마나 중요한지를 보여줍니다. 바울은 안수를 통해 주어진 은사를 다시 불붙이듯 활성화하라고 독려합니다.</p>
                            <p>하나님이 우리에게 주신 것은 두려워하는 마음이 아닙니다. 오직 능력과 사랑과 절제하는 마음입니다. 복음의 영광을 아는 자는 세상의 비난이나 고난을 부끄러워하지 않습니다. 바울은 오네시보로의 신실함을 칭찬하며, 진정한 충성이란 고난 중에 있는 형제를 외면하지 않는 것임을 증명합니다.</p>
                            <p>우리는 우리 안에 거하시는 성령을 의지하여 복음의 아름다운 부탁을 지켜내야 합니다. 복음은 고난 없이 전수되지 않으며, 그 고난은 하나님의 은혜 안에서 영광으로 승화됩니다.</p>
                            <div class="button-group">
                                <button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/2TI_01.html" data-title="디모데후서 1장">본문 보기</button>
                                <button class="btn btn-secondary listen-audio-btn" data-key="2TI_1" data-title="디모데후서 1장">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>

                <div id="tab-6" class="tab-content">
                    <article class="integration-card">
                        <div class="card-content">
                            <h3>종합 묵상: "하나님 경외의 회복"</h3>
                            <p>오늘의 모든 본문은 우리 존재의 무게 중심을 하나님께 두라고 촉구합니다. 레위기는 예배의 성결을, 시편은 창조주의 권능을, 전도서는 예배자의 경외를, 디모데후서는 복음의 사명을 가르칩니다.</p>
                            <p>우리가 하나님을 가장 무거운 분(Kavod)으로 대우할 때, 세상의 염려와 재물의 유혹은 가볍게 날아가게 됩니다. 오늘 하루, 하나님의 이름에 합당한 영광을 돌리며 우리 삶의 현장에서 거룩한 예배자로 살아가는 은혜가 있기를 소망합니다.</p>
                            <div class="button-group">
                                <a href="#top" class="btn btn-primary" onclick="switchTab(0); return false;">처음으로 돌아가기</a>
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
        // 탭 전환 시스템 (ID: tab-0 ~ tab-6)
        function switchTab(index) {
            // 모든 탭 숨기기
            document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
            // 모든 버튼 비활성화
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            
            // 대상 탭 보이기
            const targetId = 'tab-' + index;
            const targetContent = document.getElementById(targetId);
            if(targetContent) {
                targetContent.style.display = 'block';
            }
            
            // 대상 버튼 활성화
            const targetBtn = document.querySelectorAll('.tab-btn')[index];
            if(targetBtn) {
                targetBtn.classList.add('active');
            }
            
            window.scrollTo(0, 0);
        }

        // 본문 보기 모달 제어
        document.querySelectorAll('.view-text-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const paths = this.getAttribute('data-path').split(',');
                const title = this.getAttribute('data-title');
                document.getElementById('modal-title').innerText = title;
                document.getElementById('modal-iframe').src = paths[0]; // 첫 번째 장 우선 로드
                document.getElementById('text-modal').style.display = 'flex';
            });
        });

        function closeModal() {
            document.getElementById('text-modal').style.display = 'none';
            document.getElementById('modal-iframe').src = '';
        }

        // 히브리어 발음 기능
        function speakHebrew(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'he-IL';
                window.speechSynthesis.speak(utterance);
            }
        }
        
        // 초기 로드 시 탭 0 활성화 확인
        window.onload = function() {
            switchTab(0);
        };
    </script>
    <script src="script.js"></script>
</body>
</html>
