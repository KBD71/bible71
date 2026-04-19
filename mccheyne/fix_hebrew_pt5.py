import os
import re

files_content = {
    "mc0428.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 39:7</h3>
                            <div class="key-question-box">
                                <p>"주여 이제 내가 무엇을 바라리요 나의 소망은 주께 있나이다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>ו (바브)</strong>: '그리고'를 뜻하는 접속사입니다. <strong>ע (아인)</strong>: 목구멍에서 나는 후음입니다. <strong>ק (코프)</strong>: 목구멍 깊은 곳의 '크' 발음입니다. <strong>ת (타브)</strong>: 십자가 모양에서 유래한 '트' 발음으로 히브리어의 마지막 알파벳입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וְעַתָּה <span onclick="playOriginalAudio('וְעַתָּה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(베아타)</span></p>
                                <p><strong>본래 의미:</strong> 접속사 바브(וְ)와 '이제, 지금(עַתָּה)'의 결합으로 '그리고 이제', '그러므로 지금'을 뜻합니다.</p>
                                <p><strong>문맥적 의미:</strong> 인생이 그림자같이 헛되고(6절) 재물을 쌓으나 누가 거둘지 모르는 허무함을 철저히 깨달은 뒤에 맞이하는 영적 전환점을 알립니다.</p>
                                <p><strong>신학적 의미:</strong> 회개(돌이킴)의 시간적 출발점입니다. 세상의 헛됨을 직시한 성도는 더 이상 과거의 미련에 묶이지 않고 '지금 이 순간' 영원한 가치를 향해 방향을 틉니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">מַה־ <span onclick="playOriginalAudio('מַה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(마)</span></p>
                                <p><strong>본래 의미:</strong> '무엇을(What)'을 뜻하는 의문 대명사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 뒤에 오는 동사와 결합하여 내가 기다릴 만한 대상이 이 세상에는 전혀 없음을 강조하는 수사의문문을 만듭니다.</p>
                                <p><strong>신학적 의미:</strong> 인간이 스스로 부여잡고 있던 피조물에 대한 모든 헛된 기대의 포기를 선언하는 단어입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">קִּוִּיתִי <span onclick="playOriginalAudio('קִּוִּיתִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(키비티)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '카바(קָוָה, 기다리다, 소망하다, 줄을 팽팽하게 당기다)'의 피엘(강조형) 1인칭 단수 완료형입니다.</p>
                                <p><strong>문맥적 의미:</strong> 활시위를 당기듯 내 영혼의 모든 에너지를 모아 '내가 간절히 기다려왔는가?'를 자문합니다.</p>
                                <p><strong>신학적 의미:</strong> 인간은 본질적으로 무언가를 갈망하며 기다리는(카바) 존재입니다. 문제는 그 갈망의 줄이 생명 없는 우상(재물, 건강, 명예)을 향하고 있었다는 것에 있습니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אֲדֹנָי <span onclick="playOriginalAudio('אֲדֹנָי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아도나이)</span></p>
                                <p><strong>본래 의미:</strong> '나의 주님(My Lord)'을 뜻합니다. 하나님의 통치와 주권을 강조하는 호칭입니다.</p>
                                <p><strong>문맥적 의미:</strong> 죽음이라는 한계 앞에서 인간의 무능을 절감하고, 생사화복을 주관하시는 분을 찾습니다.</p>
                                <p><strong>신학적 의미:</strong> 인생의 주인이 내가 아님을 고백합니다. 재물을 주인으로 섬기던 우상숭배에서 벗어나 참된 주권자에게 영혼을 의탁하는 칭의적 선언입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">תּוֹחַלְתִּי <span onclick="playOriginalAudio('תּוֹחַלְתִּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(토할티)</span></p>
                                <p><strong>본래 의미:</strong> 명사 '토헬레트(תּוֹחֶלֶת, 소망, 기대)'에 1인칭 단수 접미어가 붙어 '나의 소망'입니다. 동사 '야할(견디며 기다리다)'에서 파생되었습니다.</p>
                                <p><strong>문맥적 의미:</strong> 세상에서 실망한 내 영혼이 유일하게 닻을 내리는 확고한 기대를 뜻합니다.</p>
                                <p><strong>신학적 의미:</strong> 기독교의 소망은 막연한 낙관주의나 상황의 호전이 아니라, 인격적인 대상(하나님)의 약속에 대한 언약적 기대입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">לְךָ <span onclick="playOriginalAudio('לְךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(레카)</span></p>
                                <p><strong>본래 의미:</strong> 전치사 '레(לְ, ~에게, ~를 향하여)'와 2인칭 단수 접미어의 결합으로 '당신에게, 주님께'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 소망의 방향과 목적지가 오직 여호와(You) 한 분뿐임을 한정합니다.</p>
                                <p><strong>신학적 의미:</strong> 방향성의 궁극적 전환(회심)입니다. 세상을 향하던 눈을 돌려, 영원한 생명이신 그리스도만을 바라보게 되는 구원의 이정표입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">הִיא <span onclick="playOriginalAudio('הִיא', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(히)</span></p>
                                <p><strong>본래 의미:</strong> 3인칭 여성 단수 대명사 '그녀(she, it)'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 앞의 여성 명사 '소망(토헬레트)'을 받는 대명사로서, '그 소망은 바로 당신께 있습니다'라는 be동사의 역할을 합니다.</p>
                                <p><strong>신학적 의미:</strong> 문장을 흔들림 없이 확정 짓는 단어입니다. 내 영혼의 안전지대가 다른 어떤 곳이 아닌 오직 '주님 그분'이라는 사실을 못 박는 신앙의 쐐기입니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">וְעַתָּה מַה־קִּוִּיתִי אֲדֹנָי תּוֹחַלְתִּי לְךָ הִיא <span onclick="playOriginalAudio('וְעַתָּה מַה־קִּוִּיתִי אֲדֹנָי תּוֹחַלְתִּי לְךָ הִיא', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>וְעַתָּה(베아타: 그러므로 이제) מַה(마: 무엇을) קִּוִּיתִי(키비티: 내가 갈망하리요) אֲדֹנָי(아도나이: 오 주여) תּוֹחַלְתִּי(토할티: 나의 소망은) לְךָ(레카: 오직 주님께) הִיא(히: 그것이 있습니다)</p>
                            <p><strong>[직역]</strong> "그러므로 이제 오 주여, 내가 무엇을 간절히 기다리겠습니까? 나의 소망, 그것은 오직 당신께 있습니다."</p>
                            <p><strong>[문법 해설]</strong> 전반부는 동사 '카바(기다리다, 당기다)'의 완료형을 사용한 수사의문문으로, 세상의 헛됨 속에서 기대할 것이 아무것도 없음을 강하게 부정합니다. 후반부는 '주어(나의 소망) + 전치사구(주님께) + 대명사(그것이 있다)' 형태의 명사문(Nominal clause)으로 구성되어 있습니다. 히브리어에서 동사 없이 명사만으로 이루어진 문장은 시간적 제약을 뛰어넘는 절대적 진리나 불변의 사실을 선포할 때 사용됩니다. 즉 세상의 소망은 시간이 지나면 변하지만, 하나님께 둔 나의 소망은 영원히 변치 않는다는 강력한 선언입니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>다윗은 이 시편의 전반부에서 인생의 허무함을 처절하게 노래했습니다. 사람의 날이 한 뼘 길이에 불과하고, 든든히 서 있는 것 같으나 사실은 입김(헤벨)처럼 아무것도 아니라는 사실입니다. 그림자처럼 지나가는 인생 속에서 사람들은 헛되이 소란을 피우며 재물을 쌓지만, 그것을 누가 거둘지 알지 못합니다(6절). 이 지독한 허무주의의 심연에서, 성도는 세상을 향해 팽팽하게 당기고 있던 갈망의 줄(카바)을 툭 끊어버립니다. 그리고 "이제(베아타)" 방향을 돌려 유일한 반석이신 주님께로 영혼의 닻을 내립니다.</p>
                            <p>세상의 절망은 우리를 하나님께로 인도하는 가장 탁월한 나침반입니다. 병들고 늙고 가진 것을 잃어버리는 과정은 슬프지만, 그것은 세상이 피난처가 될 수 없음을 깨닫게 하시는 하나님의 거룩한 수술입니다. 죽음이라는 한계 앞에서 "나의 소망은 주께 있나이다"라고 외칠 수 있는 자만이 십자가에서 죽으시고 부활하신 참된 소망, 예수 그리스도를 온전히 영접하게 됩니다. 오늘 인생의 한계와 좌절을 마주하고 있다면, 그 허무함을 통해 유일한 구원자이신 주님을 굳게 붙잡으라는 하늘의 초청으로 받아들이십시오.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_39" data-title="시편 39편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
""",
    "mc0429.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 40:1</h3>
                            <div class="key-question-box">
                                <p>"내가 여호와를 기다리고 기다렸더니 귀를 기울이사 나의 부르짖음을 들으셨도다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>ק (코프)</strong>: 목구멍 깊은 곳의 '크' 발음입니다. <strong>ו (바브)</strong>: '브' 또는 '우/오' 모음 역할을 합니다. <strong>ט (테트)</strong>: 바구니 모양의 '트' 발음입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">קַוֹּה <span onclick="playOriginalAudio('קַוֹּה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(카보)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '카바(קָוָה, 팽팽하게 당기다, 간절히 기다리다)'의 피엘(강조형) 절대 부정사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 뒤에 오는 동일한 동사를 꾸며주어 '기다리고 또 기다렸다', '지독하게 기다렸다'는 최상급의 인내를 표현합니다.</p>
                                <p><strong>신학적 의미:</strong> 응답이 지연되는 캄캄한 웅덩이 속에서도, 내 영혼의 줄을 끊지 않고 하나님을 향해 극도로 팽팽하게 당기고 있는 치열한 영적 전투의 상태입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">קִוִּיתִי <span onclick="playOriginalAudio('קִוִּיתִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(키비티)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '카바'의 피엘 1인칭 단수 완료형입니다.</p>
                                <p><strong>문맥적 의미:</strong> 과거의 어느 시점부터 응답이 온 순간까지 내가 끝까지 포기하지 않고 '기다려왔다'는 성취의 고백입니다.</p>
                                <p><strong>신학적 의미:</strong> 성도의 기다림(카바)은 막연한 시간 낭비가 아니라 하나님의 뜻이 이루어지기 위해 반드시 채워져야 하는 믿음의 분량입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>본래 의미:</strong> 언약의 신, 여호와입니다.</p>
                                <p><strong>문맥적 의미:</strong> 팽팽하게 당겨진 내 영혼의 줄이 묶여 있는 유일하고 견고한 반석이십니다.</p>
                                <p><strong>신학적 의미:</strong> 환난 날에 사람이나 수단을 의지하지 않고, 오직 언약에 신실하신 구원자 하나님만을 전적으로 신뢰함을 보여줍니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וַיֵּט <span onclick="playOriginalAudio('וַיֵּט', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(바예트)</span></p>
                                <p><strong>본래 의미:</strong> 와우 연속법과 동사 '나타(נָטָה, 뻗다, 굽히다, 기울이다)'의 칼 미완료 3인칭 단수형으로 '그래서 그가 몸을 기울이셨다'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 높고 거룩하신 보좌에서 웅덩이 아래로 몸을 굽혀 내 작은 신음소리를 듣기 위해 귀를 가까이 대시는 하나님의 다급한 동작입니다.</p>
                                <p><strong>신학적 의미:</strong> 성육신(Incarnation)의 본질을 보여줍니다. 지극히 높으신 분이 비천한 죄인의 울음소리를 듣기 위해 스스로 가장 낮은 곳으로 굽히시는(나타) 위대한 자기 비하의 은혜입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אֵלַי <span onclick="playOriginalAudio('אֵלַי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(엘라이)</span></p>
                                <p><strong>본래 의미:</strong> 전치사 '엘(אֶל, ~에게, ~를 향하여)'에 1인칭 접미어가 결합하여 '나를 향하여'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 하나님이 몸을 기울이신 정확한 표적이 바로 먼지 같은 '나(me)'임을 명시합니다.</p>
                                <p><strong>신학적 의미:</strong> 하나님의 구원은 추상적이지 않고 극도로 개인적이고 인격적인 사랑에 기초하고 있음을 증명합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וַיִּשְׁמַע <span onclick="playOriginalAudio('וַיִּשְׁמַע', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(바이스마)</span></p>
                                <p><strong>본래 의미:</strong> 와우 연속법과 동사 '샤마(שָׁמַע, 듣다, 응답하다)'의 결합으로 '그래서 그가 들으셨다'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 소리가 고막을 울렸다는 뜻이 아니라, 내 부르짖음을 접수하시고 즉각적으로 구원 행동을 개시하셨다는 뜻입니다.</p>
                                <p><strong>신학적 의미:</strong> 하나님이 '들으심(샤마)'은 곧 구원 역사의 시작입니다. 이스라엘이 애굽에서 부르짖을 때 하나님이 들으시고 모세를 보내신 것과 같은 구속의 패턴입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">שַׁוְעָתִי <span onclick="playOriginalAudio('שַׁוְעָתִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(샤브아티)</span></p>
                                <p><strong>본래 의미:</strong> 명사 '샤바(שָׁוְעָה, 살려달라는 절규, 부르짖음)'에 1인칭 접미어가 붙어 '나의 부르짖음을'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 점잖은 기도가 아니라, 물에 빠져 죽어가는 자가 생명을 구걸하며 터뜨리는 처절한 비명입니다.</p>
                                <p><strong>신학적 의미:</strong> 하나님은 화려한 미사여구에 응답하시는 것이 아니라, 파산한 심령(Broken heart)으로 십자가의 은혜만을 구하는 처절한 비명을 결코 외면하지 않으심을 보여줍니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">קַוֹּה קִוִּיתִי יְהוָה וַיֵּט אֵלַי וַיִּשְׁמַע שַׁוְעָתִי <span onclick="playOriginalAudio('קַוֹּה קִוִּיתִי יְהוָה וַיֵּט אֵלַי וַיִּשְׁמַע שַׁוְעָתִי', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>קַוֹּה(카보: 간절히 기다림으로) קִוִּיתִי(키비티: 내가 기다려왔다) יְהוָה(야훼: 여호와를) וַיֵּט(바예트: 그러자 그가 몸을 굽히셨다) אֵלַי(엘라이: 나를 향하여) וַיִּשְׁמַע(바이스마: 그리고 그가 들으셨다) שַׁוְעָתִי(샤브아티: 나의 절규를)</p>
                            <p><strong>[직역]</strong> "내가 여호와를 간절히 애타게 기다려왔다. 그러자 그가 나를 향하여 몸을 구부리셨고, 마침내 내 처절한 비명을 들으셨다."</p>
                            <p><strong>[문법 해설]</strong> 첫 단어 '카보 카비티(간절히 기다렸다)'는 동일한 어근의 절대 부정사와 정동사를 겹쳐 쓰는 전형적인 히브리어 강조 용법(Infinitive Absolute)으로, 인간이 감당할 수 있는 한계점까지 기다렸다는 시간의 극대화를 표현합니다. 반면 하반절에 연속해서 등장하는 '바예트(몸을 기울이셨다)'와 '바이스마(들으셨다)'는 '와우 연속법(Waw-consecutive)'을 사용하여, 그 기나긴 기다림 끝에 마침내 터져 나온 하나님의 응답이 얼마나 신속하고 역동적으로 일어났는지를 극적으로 대조해 줍니다. 긴 인내의 밤과 벼락처럼 임하는 구원의 아침을 문법 구조만으로도 완벽하게 그려내고 있습니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>다윗은 기가 막힐 웅덩이와 수렁에 빠져 있었습니다. 아무리 발버둥 쳐도 빠져나올 수 없는 절망의 바닥이었습니다. 그러나 그는 원망하지 않고 오직 영혼의 줄(카바)을 여호와께 팽팽히 묶고 '기다리고 기다렸습니다'. 응답이 지연되는 것은 하나님이 우리를 버리신 것이 아닙니다. 내 힘으로 구덩이를 빠져나올 수 있다는 육신의 마지막 남은 교만마저 다 빠져나가고, 오직 "주여 나를 살려주소서(샤바)"라는 가난한 비명만 남을 때까지 기다리시는 하나님의 거룩한 세공 작업입니다.</p>
                            <p>우리의 부르짖음이 극에 달할 때, 놀라운 일이 벌어집니다. 지극히 높으신 하나님께서 그 보좌에서 벌떡 일어나 그 웅덩이 입구까지 달려오시어 몸을 깊숙이 굽히십니다(나타). 그리고 십자가라는 거대한 구원의 밧줄을 내리사 나를 끌어올려 반석 위에 두십니다. 이 예수 그리스도의 성육신과 대속의 은혜야말로 하늘 보좌를 굽혀 진흙탕 속에 있는 우리를 끌어올리신 위대한 구원 사건입니다. 오늘 응답의 지연 속에서 지쳐가고 있다면, 줄을 놓지 마십시오. 몸을 굽히사 우리의 신음소리에 귀를 대시는 그 사랑의 하나님이 지금도 당신 곁에 계십니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_40" data-title="시편 40편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
""",
    "mc0430.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 41:4</h3>
                            <div class="key-question-box">
                                <p>"내가 말하기를 여호와여 내게 은혜를 베푸소서 내가 주께 범죄하였사오니 나를 고치소서 하였나이다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>א (알레프)</strong>: 소 머리 모양으로 묵음이나 모음값을 갖습니다. <strong>ח (헤트)</strong>: 울타리 모양의 거친 '흐' 발음입니다. <strong>ר (레쉬)</strong>: 머리 모양의 '르' 발음입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אֲנִי־ <span onclick="playOriginalAudio('אֲנִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아니)</span></p>
                                <p><strong>본래 의미:</strong> 1인칭 단수 인칭대명사 '나(I)'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 문장 맨 앞에 독립적으로 위치하여 다른 누구도 아닌 바로 '나 자신'이 은혜가 필요한 장본인임을 강력히 강조합니다.</p>
                                <p><strong>신학적 의미:</strong> 회개의 주체성입니다. 죄의 책임을 환경이나 타인에게 전가하지 않고, 하나님 앞에 단독자로 서서 스스로의 영적 파산을 직면하는 태도입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אָמַרְתִּי <span onclick="playOriginalAudio('אָמַרְתִּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아마르티)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '아마르(אָמַר, 말하다)'의 1인칭 단수 완료형입니다.</p>
                                <p><strong>문맥적 의미:</strong> 마음속으로만 생각한 것이 아니라, 분명한 의지를 담아 입술로 소리 내어 고백했다는 의미입니다.</p>
                                <p><strong>신학적 의미:</strong> 마음으로 믿어 의에 이르고 입으로 시인하여 구원에 이르는(롬 10:10), 구체적이고 능동적인 신앙 고백의 행위를 보여줍니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>본래 의미:</strong> 여호와, 이스라엘의 언약적 하나님입니다.</p>
                                <p><strong>문맥적 의미:</strong> 절망 속에서 호소할 단 하나의 대상입니다.</p>
                                <p><strong>신학적 의미:</strong> 율법의 심판자가 아닌, 언약적 자비와 긍휼을 베푸시는 구원자의 이름으로 부르고 있습니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">חָנֵּנִי <span onclick="playOriginalAudio('חָנֵּנִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하네니)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '하난(חָנַן, 불쌍히 여기다, 은혜를 베풀다)'의 명령형에 1인칭 접미어가 결합하여 '나를 불쌍히 여기소서'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 내게는 구원받을 공로나 자격이 티끌만큼도 없으니, 오직 주권적인 자비(은혜)만을 구걸한다는 절대적 의존의 호소입니다.</p>
                                <p><strong>신학적 의미:</strong> 성경적 기도의 본질은 내 권리를 주장하는 것이 아니라, 거지처럼 빈손을 들고 하나님의 무조건적인 긍휼에 호소하는 것임을 보여줍니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">רְפָאָה <span onclick="playOriginalAudio('רְפָאָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(레파아)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '라파(רָפָא, 고치다, 치료하다)'의 명령형으로 '치료하소서'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 다윗이 처한 극심한 질병과 고통을 고쳐달라는 간구입니다.</p>
                                <p><strong>신학적 의미:</strong> 여호와 라파(치료하시는 하나님)에 대한 신뢰입니다. 이 질병의 근원이 죄에 있음을 깨달았기에, 참된 의사이신 주님만이 근원적인 치유를 주실 수 있음을 고백합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">נַפְשִׁי <span onclick="playOriginalAudio('נַפְשִׁי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(나프쉬)</span></p>
                                <p><strong>본래 의미:</strong> 명사 '네페쉬(נֶפֶשׁ, 생명, 영혼, 존재 전체)'에 1인칭 접미어가 붙어 '나의 영혼을'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 단순한 육체의 질병 치료를 넘어 내 존재의 가장 깊은 본질적 회복을 원한다는 의미입니다.</p>
                                <p><strong>신학적 의미:</strong> 성도의 구원은 몸의 안위를 넘어 영혼 전체가 하나님과의 관계 속에서 온전히 회복(Shalom)되는 전인적 구원입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">כִּי־ <span onclick="playOriginalAudio('כִּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(키)</span></p>
                                <p><strong>본래 의미:</strong> '왜냐하면'을 뜻하는 접속사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 영혼의 치유를 간구해야만 하는 원인, 즉 가장 근본적인 질병의 실체를 밝힙니다.</p>
                                <p><strong>신학적 의미:</strong> 내 고난의 원인이 다른 사람의 저주가 아니라 나의 본질적 죄악에 있음을 인정하는 진실한 원인 규명입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">חָטָאתִי <span onclick="playOriginalAudio('חָטָאתִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하타티)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '하타(חָטָא, 표적을 빗나가다, 범죄하다)'의 1인칭 단수 완료형입니다.</p>
                                <p><strong>문맥적 의미:</strong> '내가 하나님의 기준에서 벗어나 죄를 지었습니다'라는 전적인 항복 선언입니다.</p>
                                <p><strong>신학적 의미:</strong> 모든 치유와 구원의 첫 관문입니다. 죄인 됨의 철저한 자각 없이는 은혜(하난)도, 치유(라파)도 주어질 수 없음을 웅변합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">לָךְ <span onclick="playOriginalAudio('לָךְ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(라크)</span></p>
                                <p><strong>본래 의미:</strong> 전치사 '레(לְ)'와 2인칭 단수 접미어가 결합하여 '당신에게, 주님께'를 뜻합니다.</p>
                                <p><strong>문맥적 의미:</strong> 내가 지은 죄의 궁극적인 피해자요 대상이 바로 창조주 하나님이심을 지목합니다.</p>
                                <p><strong>신학적 의미:</strong> 다윗은 우리아와 밧세바에게 죄를 지었으나, "내가 주께만 범죄하여"(시 51:4)라고 고백합니다. 모든 죄의 본질은 도덕적 실수를 넘어 거룩하신 하나님의 주권에 대한 정면 도전이기 때문입니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">אֲנִי־אָמַרְתִּי יְהוָה חָנֵּנִי רְפָאָה נַפְשִׁי כִּי־חָטָאתִי לָךְ <span onclick="playOriginalAudio('אֲנִי־אָמַרְתִּי יְהוָה חָנֵּנִי רְפָאָה נַפְשִׁי כִּי־חָטָאתִי לָךְ', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>אֲנִי־(아니: 나는) אָמַרְתִּי(아마르티: 말하였습니다) יְהוָה(야훼: 오 여호와여) חָנֵּנִי(하네니: 나를 불쌍히 여기소서) רְפָאָה(레파아: 고쳐 주소서) נַפְשִׁי(나프쉬: 나의 영혼을) כִּי־(키: 왜냐하면) חָטָאתִי(하타티: 내가 범죄하였기 때문입니다) לָךְ(라크: 주님께)</p>
                            <p><strong>[직역]</strong> "나로 말할 것 같으면 내가 부르짖었습니다, 오 여호와여, 내게 은혜를 베푸소서! 나의 영혼을 치유하소서! 왜냐하면 내가 주님께 죄를 지었기 때문입니다."</p>
                            <p><strong>[문법 해설]</strong> 문장은 '아니(나)'라는 독립 인칭 대명사로 시작하여 다윗의 철저한 자기 주도적 회개를 강조합니다. 이어서 두 개의 강렬한 명령법 동사 '하네니(은혜를 베푸소서)'와 '레파아(치료하소서)'가 병치되어 하나님의 긴급한 개입을 호소합니다. 마지막 '키(왜냐하면)' 절은 내가 왜 아프며, 왜 은혜가 필요한지에 대한 영적 진단을 내립니다. 질병(고통)의 근본 원인이 '하나님을 향한(라크) 표적 빗나감(하타티)'에 있음을 인과관계 구문으로 명확히 선언함으로써, 치유는 오직 죄 사함의 은혜를 통해서만 온다는 구원론의 진수를 문법적으로 입증합니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>본문은 극심한 질병과 대적들의 저주(5절), 심지어 가장 신뢰하던 친구의 배신(9절) 속에서 다윗이 터뜨린 위대한 영적 승리의 기도입니다. 고난이 닥치면 인간의 본성은 하나님을 원망하거나 주변 사람들을 탓하기 쉽습니다. 그러나 다윗은 이 고통의 화살표를 타인이 아닌 정확히 자기 자신의 '죄'로 향하게 합니다(하타티 라크). 내 육신의 고통보다 더 무서운 것은 영혼이 하나님과의 관계에서 빗나가 죽어가는(네페쉬) 병이었습니다. 이 영적 암 덩어리를 고치는 유일한 처방전은 율법적 변명이나 선행이 아니라, 주권적인 은혜(하난)를 구걸하는 것뿐이었습니다.</p>
                            <p>그리스도인은 고난을 해석하는 방식이 세상과 달라야 합니다. 질병이나 실패의 밑바닥에서 우리는 "왜 나에게 이런 일이?"라고 묻기 전에, 십자가의 은혜 없이는 단 하루도 살 수 없는 전적 타락한 죄인임을 자각해야 합니다. 내가 겪는 고난은 징벌이 아니라, 나를 십자가 밑으로 끌고 가 영혼의 치명적인 질병을 고치시는(라파) 위대한 의사이신 하나님의 사랑의 메스입니다. 오늘 질병의 고통과 인간관계의 배신 속에 찢어져 있습니까? 은혜의 보좌 앞에 무릎을 꿇고 정직하게 내 영혼의 실패를 자백하십시오. 십자가에서 흘리신 그리스도의 보혈이 당신의 영혼을 가장 완전하게 치유하실 것입니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_41" data-title="시편 41편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
"""
}

for file_name, new_content in files_content.items():
    path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = r'<div id="content-hebrew".*?</article>\s*</div>'
        new_text = re.sub(pattern, new_content.strip(), content, flags=re.DOTALL)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)

