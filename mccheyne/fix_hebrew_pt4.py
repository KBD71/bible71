import os
import re

files_content = {
    "mc0426.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 37:4</h3>
                            <div class="key-question-box">
                                <p>"또 여호와를 기뻐하라 그가 네 마음의 소원을 네게 이루어 주시리로다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>ו (바브)</strong>: '그리고'를 뜻하는 접속사입니다. <strong>ע (아인)</strong>: 눈 모양에서 유래한 후음입니다. <strong>ג (기멜)</strong>: 낙타 모양의 '그' 발음입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וְהִתְעַנַּג <span onclick="playOriginalAudio('וְהִתְעַנַּג', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(베히트아나그)</span></p>
                                <p><strong>본래 의미:</strong> 접속사 바브(그리고)와 동사 '아나그(עָנַג, 섬세하다, 즐기다, 호사를 누리다)'의 히트파엘(재귀 강조형) 명령법입니다.</p>
                                <p><strong>문맥적 의미:</strong> 세상의 악인들이 형통하는 것을 보며 불평하지 말고(1절), 오히려 하나님 안에서 네 영혼이 최고급 식사를 하듯 최고의 사치를 누리며 기뻐하라는 뜻입니다.</p>
                                <p><strong>신학적 의미:</strong> 기독교 희락주의(Christian Hedonism)의 성경적 기초입니다. 하나님을 기뻐하는 것은 종교적 의무가 아니라 성도가 누려야 할 특권이자 가장 가치 있는 탐닉입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">עַל־ <span onclick="playOriginalAudio('עַל', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(알)</span></p>
                                <p><strong>본래 의미:</strong> '~위에서, ~에 근거하여, ~로 인하여'를 뜻하는 전치사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 내 기쁨과 호사의 근거가 환경이나 소유에 있지 않고 오직 뒤에 오는 대상에 철저히 기초하고 있음을 보여줍니다.</p>
                                <p><strong>신학적 의미:</strong> 우상숭배는 피조물 '위에서' 기뻐하는 것이지만, 참된 신앙은 창조주 '위에서' 기뻐하는 것입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>본래 의미:</strong> 이스라엘의 언약적 신, 여호와입니다.</p>
                                <p><strong>문맥적 의미:</strong> 내 영혼이 기뻐해야 할 유일하고도 영원한 대상입니다.</p>
                                <p><strong>신학적 의미:</strong> 그분이 주시는 선물(응답) 때문이 아니라, 선물을 주시는 분 자체(여호와)가 기쁨의 대상이 되어야 함을 웅변합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וְיִתֶּן־ <span onclick="playOriginalAudio('וְיִתֶּן', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(베이텐)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '나탄(נָתַן, 주다, 허락하다)'의 칼 미완료 3인칭 단수형으로 '그리하면 그가 주실 것이다'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 하나님을 온전히 기뻐하는 자에게 뒤따르는 확실한 결과를 나타냅니다.</p>
                                <p><strong>신학적 의미:</strong> 기복신앙적 거래가 아닙니다. 내 기쁨의 영점 조준이 하나님께 맞춰질 때, 하나님은 전능자의 권능으로 내 기도를 응답하신다는 약속입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">לְךָ <span onclick="playOriginalAudio('לְךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(레카)</span></p>
                                <p><strong>본래 의미:</strong> 전치사 '레(לְ, ~에게)'와 2인칭 단수 접미어가 결합하여 '너에게'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 응답이 허공에 흩어지지 않고, 하나님을 기뻐하는 바로 그 사람(너)에게 정확히 하달됨을 보여줍니다.</p>
                                <p><strong>신학적 의미:</strong> 언약 관계의 인격적 밀착을 나타냅니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">מִשְׁאֲלֹת <span onclick="playOriginalAudio('מִשְׁאֲלֹת', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(미쉬알로트)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '샤알(שָׁאַל, 묻다, 요구하다)'에서 파생된 명사의 복수 연계형으로 '요청들, 소원들'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 내면 깊은 곳에서 하나님을 향해 쏟아내는 여러 가지 간절한 기도 제목들을 가리킵니다.</p>
                                <p><strong>신학적 의미:</strong> 하나님은 단지 영적인 필요뿐 아니라 우리 삶의 구체적인 필요(요청들)를 세밀하게 아시고 채워주시는 분이십니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">לִבֶּךָ <span onclick="playOriginalAudio('לִבֶּךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(리베카)</span></p>
                                <p><strong>본래 의미:</strong> 명사 '레브(לֵב, 마음, 지성과 감정과 의지의 좌소)'에 2인칭 접미어가 결합하여 '네 마음의'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 입술로만 급조된 기도가 아니라 존재의 가장 깊은 중심(마음)에서 우러나온 진실한 갈망입니다.</p>
                                <p><strong>신학적 의미:</strong> 내 마음(레브)이 하나님을 기뻐함(히트아나그)으로 가득 찰 때, 내 마음의 소원 역시 세속적 정욕을 벗어나 거룩한 하나님의 뜻과 완벽하게 일치하게 됩니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">וְהִתְעַנַּג עַל־יְהוָה וְיִתֶּן־לְךָ מִשְׁאֲלֹת לִבֶּךָ <span onclick="playOriginalAudio('וְהִתְעַנַּג עַל־יְהוָה וְיִתֶּן־לְךָ מִשְׁאֲלֹת לִבֶּךָ', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>וְהִתְעַנַּג(베히트아나그: 그리고 네 자신을 기쁘게 하라) עַל־(알: 위에서) יְהוָה(야훼: 여호와) וְיִתֶּן־(베이텐: 그리하면 그가 주실 것이다) לְךָ(레카: 너에게) מִשְׁאֲלֹת(미쉬알로트: 소원들을) לִבֶּךָ(리베카: 네 마음의)</p>
                            <p><strong>[직역]</strong> "그리고 너는 여호와로 인하여 네 자신을 기쁘게 하라, 그리하면 그가 네 마음의 소원들을 네게 주실 것이다."</p>
                            <p><strong>[문법 해설]</strong> 문장은 '명령법(Imperative)' + '미완료 동사(Imperfect)'의 전형적인 조건-결과 구문입니다. '네 자신을 기쁘게 하라'는 재귀형(히트파엘) 명령은 기쁨이 우연한 감정이 아니라 의지적인 훈련과 몰입을 요하는 영적 전투임을 보여줍니다. 이 영광스러운 훈련에 성공하여 하나님 그분을 내 소원으로 삼을 때, 뒤에 오는 '이루어 주실 것이다(이텐)'는 반드시 성취되는 필연적 결과로 주어집니다. 내 마음(레브)이 하나님으로 채워졌으므로 그 마음의 소원이 응답받는 것은 완벽한 논리적 귀결입니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>존 파이퍼(John Piper)는 이 구절을 자신의 신학적 뼈대인 '기독교 희락주의'의 모토로 삼았습니다. "하나님은 우리가 그분 안에서 가장 크게 만족할 때, 우리를 통해 가장 크게 영광을 받으신다." 악인들이 불법을 저질러 부를 축적하는 것을 볼 때, 우리의 본성은 그들을 질투하며 속을 끓입니다. 그러나 시편 기자는 불평의 불을 끄고 거룩한 기쁨의 불을 지피라고 명령합니다. 세상의 찌꺼기 같은 쾌락에 만족하지 말고, 영원한 샘물(여호와)을 마시며 최고급 영적 사치를 누리라는 것입니다.</p>
                            <p>우리가 하나님 그분을 내 인생의 최고 보물로 삼고 기뻐할 때 놀라운 기적이 일어납니다. 내 마음의 소원(미쉬알로트)이 정화되어 세속적인 탐욕이 떨어져 나가고 하나님의 뜻과 일치하게 됩니다. 조지 뮬러는 "나의 첫 번째 사명은 내 영혼을 하나님 안에서 행복하게 만드는 것"이라고 했습니다. 오늘 수많은 기도 제목을 늘어놓기 전에 먼저 나침반을 재조정하십시오. 내가 원하는 것은 주님이 주실 선물이 아니라 십자가에서 나를 다 사랑하신 예수 그리스도 한 분뿐임을 고백할 때, 아버지께서는 당신의 모든 필요를 가장 완벽하게 채워주실 것입니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_37" data-title="시편 37편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
""",
    "mc0427.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 히브리서 2:18</h3>
                            <div class="key-question-box">
                                <p>"그가 시험을 받아 고난을 당하셨은즉 시험 받는 자들을 능히 도우실 수 있느니라"</p>
                            </div>
                            <h4>① 헬라어 가이드</h4>
                            <p><strong>π (피)</strong>: 입술 파열음 '프' 발음입니다. <strong>β (베타)</strong>: '브' 발음입니다. <strong>θ (쎄타)</strong>: 혀를 이 사이에 물고 내는 '쓰' 발음입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">ἐν <span onclick="playOriginalAudio('ἐν', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(엔)</span></p>
                                <p><strong>본래 의미:</strong> '~안에서(in)'를 뜻하는 처소적 전치사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 뒤에 오는 관계대명사와 결합하여 그리스도께서 겪으신 '바로 그 고난의 영역 안에서'라는 범위를 한정합니다.</p>
                                <p><strong>신학적 의미:</strong> 그리스도의 도우심이 관념적이지 않고 그가 직접 통과하신 구체적인 역사적 경험에 근거함을 보여줍니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">ᾧ <span onclick="playOriginalAudio('ᾧ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(호)</span></p>
                                <p><strong>본래 의미:</strong> 관계대명사 '호스(ὅς)'의 여격 단수형입니다.</p>
                                <p><strong>문맥적 의미:</strong> 앞선 구절에서 언급된 육신을 입고 겪으신 모든 생애의 상황을 받습니다.</p>
                                <p><strong>신학적 의미:</strong> '엔 호(ἐν ᾧ, in that which)'는 '그 점에 있어서 바로 그것 때문에'라는 원인과 영역을 동시에 강조합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">γὰρ <span onclick="playOriginalAudio('γὰρ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(가르)</span></p>
                                <p><strong>본래 의미:</strong> '왜냐하면(for)'을 뜻하는 접속사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 그리스도가 자비롭고 신실한 대제사장이 되신(17절) 이유를 논리적으로 설명합니다.</p>
                                <p><strong>신학적 의미:</strong> 우리의 구원이 맹목적 믿음이 아니라 그리스도의 대속적 고난이라는 확실한 객관적 근거에 터하고 있음을 입증합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">πέπονθεν <span onclick="playOriginalAudio('πέπονθεν', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(페폰덴)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '파스코(πάσχω, 고난받다, 경험하다)'의 완료 능동 3인칭 단수형으로 '그가 (치명적인) 고난을 겪으셨다'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 십자가의 극심한 고통을 포함하여 성육신 기간 동안 당하신 모든 육체적, 정신적 형벌을 의미합니다.</p>
                                <p><strong>신학적 의미:</strong> 고난의 결과가 현재까지도 효력을 미치고 있음(완료형)을 나타냅니다. 그리스도의 못 박힌 손자국은 여전히 그가 우리의 고난을 공감하시는 영원한 징표입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">αὐτὸς <span onclick="playOriginalAudio('αὐτὸς', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아우토스)</span></p>
                                <p><strong>본래 의미:</strong> '그(he)' 또는 강조 용법으로 '그 자신이(himself)'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 천사나 대리인이 아니라, 창조주 성자 하나님 '그분 자신이 직접' 육체를 입고 오셨음을 강조합니다.</p>
                                <p><strong>신학적 의미:</strong> 성육신(Incarnation)의 놀라운 신비이자 복음의 핵심입니다. 주권자가 피조물의 자리까지 친히 내려오신 자기 비하(Kenosis)입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">πειρασθείς <span onclick="playOriginalAudio('πειρασθείς', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(페이라스데이스)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '페이라조(πειράζω, 시험하다, 유혹하다)'의 과거 수동 분사로 '시험을 받으시어'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 광야의 시험부터 겟세마네 동산까지, 사탄과 죄인들로부터 끊임없이 외부적 압박과 유혹에 노출되셨음을 나타냅니다.</p>
                                <p><strong>신학적 의미:</strong> 죄는 없으시지만, 우리와 동일한 한계 속에서 유혹의 무게를 고스란히 견뎌내셨기에 우리의 연약함을 체휼(Sympathize)하실 수 있습니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">δύναται <span onclick="playOriginalAudio('δύναται', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(뒤나타이)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '뒤나마이(δύναμαι, 할 수 있다, 능력이 있다)'의 현재 중간수동태 3인칭 단수형입니다.</p>
                                <p><strong>문맥적 의미:</strong> 고난과 시험을 통과하심으로 획득하신 대제사장적 권능과 자격을 확언합니다.</p>
                                <p><strong>신학적 의미:</strong> 예수님의 도우심은 단순한 동정심이 아니라 문제를 완벽히 해결할 수 있는 신적 권능(Dynamis)을 동반합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">τοῖς <span onclick="playOriginalAudio('τοῖς', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(토이스)</span></p>
                                <p><strong>본래 의미:</strong> 정관사의 여격 복수형으로 '~하는 자들에게'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 분사와 결합하여 도우심의 대상을 지칭합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">πειραζομένοις <span onclick="playOriginalAudio('πειραζομένοις', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(페이라조메노이스)</span></p>
                                <p><strong>본래 의미:</strong> 앞선 '페이라조' 동사의 현재 수동 분사 여격형으로 '(지금 계속해서) 시험받고 있는'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 성도들이 이 땅에서 겪는 환난과 유혹이 1회성이 아니라 현재 진행형임을 보여줍니다.</p>
                                <p><strong>신학적 의미:</strong> 매일 넘어지고 유혹에 시달리는 비참한 상태에 있는 자야말로 대제사장의 긍휼을 입을 1순위 대상임을 위로합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">βοηθῆσαι <span onclick="playOriginalAudio('βοηθῆσαι', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(보에데사이)</span></p>
                                <p><strong>본래 의미:</strong> '보아에(βοή, 부르짖음)'와 '데오(θέω, 달려가다)'가 합성된 동사 '보에데오(βοηθέω)'의 부정사로 '구원하려고 달려가 돕다'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 물에 빠진 자가 살려달라고 비명 지를 때, 지체 없이 물속으로 뛰어들어 건져내는 역동적인 구조 행위입니다.</p>
                                <p><strong>신학적 의미:</strong> 하늘 보좌에 가만히 앉아 구경하시는 분이 아니라, 성도가 고통 중에 부르짖을 때 즉각적으로 비명을 듣고 달려오시는 능동적 구원자이십니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold;">ἐν ᾧ γὰρ πέπονθεν αὐτὸς πειρασθείς, δύναται τοῖς πειραζομένοις βοηθῆσαι <span onclick="playOriginalAudio('ἐν ᾧ γὰρ πέπονθεν αὐτὸς πειρασθείς, δύναται τοῖς πειραζομένοις βοηθῆσαι', 'el-GR')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>ἐν(엔: ~안에서) ᾧ(호: 그 자신이) γὰρ(가르: 왜냐하면) πέπονθεν(페폰덴: 고난을 겪으셨으므로) αὐτὸς(아우토스: 그 자신이 직접) πειρασθείς(페이라스데이스: 시험을 받으시어) δύναται(뒤나타이: 그는 능력이 있으시다) τοῖς(토이스: ~하는 자들에게) πειραζομένοις(페이라조메노이스: 시험받고 있는) βοηθῆσαι(보에데사이: 달려와 도우실)</p>
                            <p><strong>[직역]</strong> "왜냐하면 그 자신이 시험을 받아 고난을 겪으셨으므로, 그는 지금 시험받고 있는 자들을 능히 달려와 도우실 수 있기 때문입니다."</p>
                            <p><strong>[문법 해설]</strong> 문장은 '원인절(가르 페폰덴...)'과 '결과절(뒤나타이... 보에데사이)'로 구성되어 그리스도의 대제사장적 직무 수행의 확실성을 논증합니다. 예수님이 당하신 과거의 시험('페이라스데이스', 과거 분사)이, 우리가 겪는 현재의 시험('페이라조메노이스', 현재 분사)을 완벽하게 덮고 공감할 수 있는 근거가 됩니다. 핵심 동사 '보에데오(달려와 돕다)'는 능력이 있다는 '뒤나타이'에 걸리는 보충 부정사로서, 그리스도의 긍휼이 감상주의에 그치지 않고 실제적인 구원 행위로 나타남을 헬라어 수사학을 통해 역동적으로 보여줍니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>고대 헬라 철학자들은 신의 가장 큰 속성을 '아파테이아(Apatheia, 무감각/고통을 느끼지 못함)'라고 믿었습니다. 신이 고통을 느낀다면 완벽하지 않다고 본 것입니다. 그러나 성경이 증언하는 하나님은 전혀 다릅니다. 이 땅에 오신 예수 그리스도는 배고픔과 피곤, 배신과 조롱, 찢어지는 육체의 고통을 피부로 다 느끼셨습니다. 그분은 우리와 동떨어진 진공상태에 계신 분이 아니라, 우리와 똑같은 눈물 골짜기에서 피 흘리며 싸우신 분입니다.</p>
                            <p>내가 죄의 유혹 앞에 비참하게 흔들릴 때, 혹은 이유를 알 수 없는 고난의 늪에 빠져 "살려달라"고 비명 지를 때(보아에), 주님은 "내가 다 안다" 하시며 지체 없이 내게 달려오십니다(데오). 그분 손에 있는 못 자국이 바로 "나도 그 시험을 겪었으며 내가 이미 승리했다"는 영원한 보증입니다. 나의 연약함을 탓하지 마시고, 우리의 모든 아픔을 체휼하신 크고 자비로우신 대제사장, 예수 그리스도의 옷자락을 굳게 붙잡으시길 바랍니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="HEB_2" data-title="히브리서 2장">성경 듣기</button>
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

