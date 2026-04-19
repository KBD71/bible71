import os
import re

files_content = {
    "mc0424.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 디도서 3:5</h3>
                            <div class="key-question-box">
                                <p>"중생의 씻음과 성령의 새롭게 하심으로 하셨나니"</p>
                            </div>
                            <h4>① 헬라어 가이드</h4>
                            <p><strong>π (피)</strong>: 입술소리 '프' 발음입니다. <strong>λ (람다)</strong>: 혀끝을 윗니에 대는 'ㄹ' 발음입니다. <strong>ἀ (알파)</strong>: 헬라어 알파벳의 첫 글자입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">διὰ <span onclick="playOriginalAudio('διὰ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(디아)</span></p>
                                <p><strong>본래 의미:</strong> 속격과 결합하여 '~를 통하여(through)', '~를 수단으로 하여(by means of)'를 뜻하는 전치사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 구원이 인간의 선행이나 의로운 행위(에르곤)가 아니라 철저히 외부에서 주어지는 신적 수단에 의해 이루어졌음을 강력히 지시합니다.</p>
                                <p><strong>신학적 의미:</strong> 성도의 구원은 하나님이 마련하신 단 하나의 통로(중생과 성령)를 통해서만 성취되는 배타적 은혜임을 선언합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">λουτροῦ <span onclick="playOriginalAudio('λουτροῦ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(루트루)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '루오(λούω, 씻다, 목욕하다)'에서 유래한 명사로 '목욕, 씻음, 물두멍'을 뜻합니다.</p>
                                <p><strong>문맥적 의미:</strong> 더러운 몸을 물로 깨끗하게 씻어내는 행위로, 영혼의 전면적인 정결을 비유합니다.</p>
                                <p><strong>신학적 의미:</strong> 구약시대 제사장이 성소에 들어가기 전 물두멍에서 씻었던 규례의 영적 성취이며, 신약의 세례(Baptism)가 지니는 영적 실재, 즉 그리스도의 피로 인한 완전한 죄 사함을 상징합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">παλιγγενεσίας <span onclick="playOriginalAudio('παλιγγενεσίας', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(팔링게네시아스)</span></p>
                                <p><strong>본래 의미:</strong> '팔린(πάλιν, 다시)'과 '게네시스(γένεσις, 출생, 기원)'의 합성어로 '다시 태어남(Regeneration)'을 뜻합니다.</p>
                                <p><strong>문맥적 의미:</strong> 타락으로 죽었던 영혼이 생명을 부여받아 새로운 피조물로 재창조되는 단회적이고 근본적인 사건입니다.</p>
                                <p><strong>신학적 의미:</strong> 구원은 도덕적 수양이나 개선(Improvement)이 아니라 본질적인 영적 재출생입니다. 니고데모에게 "거듭나야 하겠다"(요 3장)고 하신 예수님의 선언과 일치하는 구원론의 핵심 단어입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">καὶ <span onclick="playOriginalAudio('καὶ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(카이)</span></p>
                                <p><strong>본래 의미:</strong> '그리고(and), 또한'을 뜻하는 등위 접속사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 앞의 '중생의 씻음'과 뒤의 '성령의 새롭게 하심'을 대등하게 연결하여 두 가지가 동전의 양면처럼 불가분의 관계임을 보여줍니다.</p>
                                <p><strong>신학적 의미:</strong> 칭의(과거적 사건)와 성화(현재적 과정)가 서로 분리될 수 없는 단일한 구원의 과정임을 문법적으로 묶어줍니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">ἀνακαινώσεως <span onclick="playOriginalAudio('ἀνακαινώσεως', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아나카이노세오스)</span></p>
                                <p><strong>본래 의미:</strong> '아나(ἀνά, 위로, 다시)'와 '카이노스(καινός, 본질적으로 새로운)'의 합성 명사로 '지속적인 갱신, 새롭게 됨(Renewal)'을 뜻합니다.</p>
                                <p><strong>문맥적 의미:</strong> 단회적인 출생(중생) 이후에 이어지는 성도의 점진적이고 매일매일의 영적 성장 과정을 말합니다.</p>
                                <p><strong>신학적 의미:</strong> 구원은 한 번의 영접으로 끝나는 것이 아닙니다. 타락한 본성의 잔재와 싸우며 매일 그리스도의 형상을 닮아가는 치열하고 영광스러운 성화(Sanctification)의 과정이 우리에게 요구됩니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">πνεύματος <span onclick="playOriginalAudio('πνεύματος', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(프뉴마토스)</span></p>
                                <p><strong>본래 의미:</strong> 명사 '프뉴마(πνεῦμα, 영, 바람, 호흡)'의 속격형으로 '영의'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 인간의 영혼이 아니라 하나님의 영이심을 가리킵니다.</p>
                                <p><strong>신학적 의미:</strong> 새롭게 하심(갱신)의 동력이 인간의 결단이나 노력이 아니라 전적인 성령 하나님의 사역임을 못 박습니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">ἁγίου <span onclick="playOriginalAudio('ἁγίου', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하기우)</span></p>
                                <p><strong>본래 의미:</strong> '하기오스(ἅγιος, 거룩한, 분리된)'의 속격형입니다.</p>
                                <p><strong>문맥적 의미:</strong> 프뉴마토스를 수식하여 '성령(Holy Spirit)'이라는 신격의 명칭을 완성합니다.</p>
                                <p><strong>신학적 의미:</strong> 성령의 사역은 결국 성도를 세상과 구별된 '거룩한(하기오스)' 상태로 만들어가는 것임을 그분의 이름 자체가 증명합니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold;">διὰ λουτροῦ παλιγγενεσίας καὶ ἀνακαινώσεως πνεύματος ἁγίου <span onclick="playOriginalAudio('διὰ λουτροῦ παλιγγενεσίας καὶ ἀνακαινώσεως πνεύματος ἁγίου', 'el-GR')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>διὰ(디아: ~를 통하여) λουτροῦ(루트루: 씻음을) παλιγγενεσίας(팔링게네시아스: 다시 태어남의) καὶ(카이: 그리고) ἀνακαινώσεως(아나카이노세오스: 새롭게 하심을) πνεύματος(프뉴마토스: 영의) ἁγίου(하기우: 거룩한)</p>
                            <p><strong>[직역]</strong> "... 거룩한 영의 새롭게 하심과 다시 태어남의 씻음을 통하여 (우리를 구원하셨으니)."</p>
                            <p><strong>[문법 해설]</strong> 전치사 '디아(διὰ, ~를 통하여)'는 두 개의 소유격 명사절('다시 태어남의 씻음'과 '성령의 새롭게 하심')을 지배하고 있습니다. 두 명사구 사이의 접속사 '카이(καὶ)'는 Epexegetic(설명적) 용법으로 쓰여, '씻음(단회적 중생)'과 '새롭게 하심(점진적 성화)'이 사실상 성령 하나님이 주도하시는 하나의 연속된 구원 역사임을 강조합니다. 즉 구원의 수단은 율법적 행위가 아니라 철저히 신적 사역(성령의 내주하심)임을 헬라어 문법 구조가 치밀하게 증언합니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>이 구절은 바울 서신에 나타난 가장 완벽하고 압축된 성령론적 구원론입니다. 바울은 우리가 구원받은 이유가 "우리가 행한 바 의로운 행위(Works of righteousness)로 말미암지 아니하고 오직 그의 긍휼하심을 따라" 이루어졌다고 선언합니다. 종교적 열심이나 도덕적 선행은 찢어진 옷을 기워 입는 것과 같습니다. 하나님이 요구하시는 구원의 조건은 수선(Repair)이 아니라 완전한 재창조(Regeneration)입니다.</p>
                            <p>성령님은 먼저 우리 영혼의 치명적인 죄악을 씻어내시고 새 생명을 잉태케 하십니다(팔링게네시아스). 그러나 이것이 끝이 아닙니다. 태어난 생명은 자라나야 합니다. 내 안에 내주하시는 거룩한 영은 세속에 물든 우리의 가치관과 기질을 매일매일 그리스도를 닮은 모습으로 새롭게 갱신(아나카이노세오스)해 가십니다. 이 거룩한 영적 수술대 위에 나 자신을 온전히 내어드리는 것, 그것이 바로 참된 은혜의 복음을 아는 성도의 마땅한 삶입니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="TIT_3" data-title="디도서 3장">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
""",
    "mc0425.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 36:9</h3>
                            <div class="key-question-box">
                                <p>"진실로 생명의 원천이 주께 있사오니 주의 빛 안에서 우리가 빛을 보리이다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>מ (멤)</strong>: 물결 모양에서 유래한 '므' 발음입니다. <strong>ח (헤트)</strong>: 울타리 모양의 거친 '흐' 발음입니다. <strong>א (알레프)</strong>: 소 머리 모양으로 묵음이나 모음값을 갖습니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">כִּי־ <span onclick="playOriginalAudio('כִּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(키)</span></p>
                                <p><strong>본래 의미:</strong> '왜냐하면(For, Because)'을 뜻하는 접속사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 앞선 7-8절에서 성도가 주의 날개 그늘 아래 피하며 주의 집의 살진 것으로 풍족함을 누릴 수 있는 근본적이고 논리적인 이유를 제시합니다.</p>
                                <p><strong>신학적 의미:</strong> 참된 만족과 보호의 원인이 환경이 아니라 하나님 당신의 본성 자체에 있음을 선언합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">עִמְּךָ <span onclick="playOriginalAudio('עִמְּךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(임메카)</span></p>
                                <p><strong>본래 의미:</strong> 전치사 '임(עִם, ~와 함께)'에 2인칭 단수 접미어가 결합하여 '주와 함께', '주님 곁에', '주님 안에'를 뜻합니다.</p>
                                <p><strong>문맥적 의미:</strong> 생명이라는 절대적 가치가 존재하는 유일무이한 위치, 곧 하나님의 임재 그 자체를 가리킵니다.</p>
                                <p><strong>신학적 의미:</strong> 세상의 수많은 우상과 철학이 생명을 약속하지만, 그것은 모두 거짓 우물에 불과합니다. 생명은 오직 하나님 '안에(עִמְּךָ)' 독점적으로 보관되어 있습니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">מְקוֹר <span onclick="playOriginalAudio('מְקוֹר', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(메코르)</span></p>
                                <p><strong>본래 의미:</strong> 명사 '마코르(מָקוֹר, 솟아나는 샘, 수원지, 근원)'의 연계형입니다. 파낸 우물이 아니라 땅속에서 끊임없이 물이 뿜어져 나오는 활기찬 샘을 뜻합니다.</p>
                                <p><strong>문맥적 의미:</strong> 하나님의 은혜와 생명이 결코 고갈되지 않고 무한히 솟구쳐 오르는 역동성을 묘사합니다.</p>
                                <p><strong>신학적 의미:</strong> 예레미야 2:13의 "생수의 근원(מְקוֹר מַיִם חַיִּים)"이신 하나님을 버린 이스라엘의 죄와 대비되며, 그리스도께서 사마리아 여인에게 약속하신 "영생하도록 솟아나는 샘물"(요 4:14)을 예표합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">חַיִּים <span onclick="playOriginalAudio('חַיִּים', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하임)</span></p>
                                <p><strong>본래 의미:</strong> '생명'을 뜻하는 복수형 명사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 단순한 생물학적 호흡(Bios)을 넘어선, 하나님과의 영적 교제 안에서 누리는 풍성한 삶(Zoe)의 총체입니다.</p>
                                <p><strong>신학적 의미:</strong> 히브리어에서 생명이 복수형으로 쓰이는 것은 그 본질이 지닌 충만함, 역동성, 그리고 다양한 차원(육적, 영적, 영원한 생명)을 아우르기 때문입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">בְּאוֹרְךָ <span onclick="playOriginalAudio('בְּאוֹרְךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(베오르카)</span></p>
                                <p><strong>본래 의미:</strong> 전치사 베(בְּ, ~안에서)와 명사 '오르(אוֹר, 빛)', 2인칭 접미어가 결합하여 '주의 빛 안에서'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 생명의 샘을 찾고 진리를 분별할 수 있게 만드는 매질(Medium)이자 계시의 근원입니다.</p>
                                <p><strong>신학적 의미:</strong> 태양 빛이 아니라 하나님의 진리, 공의, 그리고 은혜의 현현을 상징합니다. 하나님의 계시가 없이는 인간은 철저한 영적 흑암 속에 갇혀 있음을 의미합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">נִרְאֶה־ <span onclick="playOriginalAudio('נִרְאֶה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(니르에)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '라아(רָאָה, 보다, 깨닫다)'의 칼(단순 능동) 미완료 1인칭 복수형으로 '우리가 봅니다'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 단순히 시각적으로 사물을 인지하는 것을 넘어, 영적인 눈이 열려 진리의 참모습을 꿰뚫어 보는 지적, 영적 각성을 뜻합니다.</p>
                                <p><strong>신학적 의미:</strong> 인간 스스로의 이성적 탐구나 학문적 노력으로 진리를 도출해내는 것이 아니라, 하나님의 빛이 비췰 때 비로소 우리가 진리를 '수동적으로 발견'하게 됨을 보여주는 계시 의존적 인식론의 정수입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אוֹר <span onclick="playOriginalAudio('אוֹר', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(오르)</span></p>
                                <p><strong>본래 의미:</strong> 앞서 쓰인 동일한 명사 '오르(빛)'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 여기서는 하나님이 비추시는 매질(빛)을 통해 비로소 우리가 보게 되는 결과물, 곧 '참된 진리와 구원의 실재'로서의 빛입니다.</p>
                                <p><strong>신학적 의미:</strong> "빛이 세상에 왔으되 사람들이 자기 행위가 악하므로 빛보다 어둠을 더 사랑한 것이니라"(요 3:19)의 그 생명의 빛, 곧 성육신하신 그리스도를 예표합니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">כִּי־עִמְּךָ מְקוֹר חַיִּים בְּאוֹרְךָ נִרְאֶה־אוֹר <span onclick="playOriginalAudio('כִּי־עִמְּךָ מְקוֹר חַיִּים בְּאוֹרְךָ נִרְאֶה־אוֹר', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>כִּי־(키: 왜냐하면) עִמְּךָ(임메카: 주님과 함께) מְקוֹר(메코르: 샘이) חַיִּים(하임: 생명의) בְּאוֹרְךָ(베오르카: 당신의 빛 안에서) נִרְאֶה־(니르에: 우리가 봅니다) אוֹר(오르: 빛을)</p>
                            <p><strong>[직역]</strong> "왜냐하면 당신 안에 생명의 샘이 있기 때문입니다. 당신의 빛 안에서 우리가 빛을 봅니다."</p>
                            <p><strong>[문법 해설]</strong> 문장은 '생명(하임)'과 '빛(오르)'이라는 요한문헌의 핵심 모티프를 완벽한 병행 구조로 배열하고 있습니다. 전반절은 생명의 '근원(메코르)'이 철저히 여호와께 종속(임메카)되어 있음을 소유격 연계형으로 못 박으며, 후반절은 인식의 조건(베오르카)과 그 인식의 결과(오르)가 동어 반복을 통해 일치됨을 보여줍니다. 즉, 빛(하나님의 계시)이 없이는 빛(참된 진리)을 볼 수 없다는 철저한 신본주의적 인식론을 명확한 히브리어 신택스로 입증하고 있습니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>이 구절은 개혁파 신학자 코넬리우스 반틸(C. Van Til)이 그토록 강조했던 '계시 의존적 사색'의 가장 완벽한 성경적 근거입니다. 태양이 떠올라 그 빛을 비추어 주어야만 우리가 비로소 태양의 존재를 볼 수 있고 세상 만물의 색깔을 구별할 수 있듯이, 영적으로 죽어 흑암에 갇힌 인간은 스스로 진리(하나님)를 더듬어 찾을 수 없습니다. 오직 성령께서 말씀(주의 빛)을 통해 우리 영혼에 조명(Illumination)을 비추어 주실 때만, 비로소 우리는 나 자신의 비참함을 깨닫고 십자가라는 찬란한 은혜의 빛을 볼 수 있습니다.</p>
                            <p>세상은 우물을 파면 그 아래 어딘가에 생명의 물이 있을 거라 착각하며 인본주의 철학과 과학, 쾌락의 땅을 깊이 파내려 갑니다. 그러나 생명의 원천은 땅 아래 있지 않고 하늘 보좌 우편(주와 함께)에 있습니다. 오늘 내 삶이 메말라 죽어가는 것 같다면 썩은 물을 내는 세상의 웅덩이를 버려두고 생수의 근원이신 그리스도께로 돌아가십시오. 주님의 계시의 빛 앞에 잠잠히 머무를 때, 내 인생의 어두운 그림자들이 물러가고 영원토록 솟구치는 기쁨의 샘이 내 영혼을 적시게 될 것입니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_36" data-title="시편 36편">성경 듣기</button>
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

