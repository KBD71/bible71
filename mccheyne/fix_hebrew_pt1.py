import os
import re

files_content = {
    "mc0420.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 31:5</h3>
                            <div class="key-question-box">
                                <p>"내가 나의 영을 주의 손에 부탁하나이다 진리의 하나님 여호와여 나를 속량하셨나이다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>ב (베트)</strong>: 집 모양에서 유래한 '브' 발음입니다. <strong>ר (레쉬)</strong>: 머리 모양의 '르' 발음입니다. <strong>א (알레프)</strong>: 소 머리 모양으로 묵음이나 '아' 발음입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">בְּיָדְךָ <span onclick="playOriginalAudio('בְּיָדְךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(베야데카)</span></p>
                                <p><strong>본래 의미:</strong> 전치사 '베(בְּ, ~안에)'와 명사 '야드(יָד, 손)', 2인칭 접미어가 결합하여 '당신의 손 안에'를 뜻합니다.</p>
                                <p><strong>문맥적 의미:</strong> 원수들의 그물과 핍박 속에서 유일하게 안전한 피난처로서의 하나님의 주권과 보호를 상징합니다.</p>
                                <p><strong>신학적 의미:</strong> 성도의 궁극적인 안전망입니다. 세상의 손이 나를 해치려 할지라도, 전능자의 손이 나를 붙들고 계심을 확신하는 신앙입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אַפְקִיד <span onclick="playOriginalAudio('אַפְקִיד', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아프키드)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '파카드(פָּקַד, 방문하다, 돌보다, 맡기다)'의 히필(사역형) 미완료 1인칭 단수형으로 '내가 맡깁니다, 위탁합니다'라는 뜻입니다.</p>
                                <p><strong>문맥적 의미:</strong> 귀중품을 가장 안전한 은행에 보관하듯, 내 생명을 철저히 하나님께 의탁하는 주도적인 행위입니다.</p>
                                <p><strong>신학적 의미:</strong> 믿음은 단순한 지적 동의가 아니라 내 전 존재를 던지는 의탁(Commitment)입니다. 십자가에서 예수님이 마지막으로 자신의 영혼을 성부께 던지신 위대한 순종의 단어입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">רוּחִי <span onclick="playOriginalAudio('רוּחִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(루히)</span></p>
                                <p><strong>본래 의미:</strong> 명사 '루아흐(רוּחַ, 영, 바람, 호흡)'에 1인칭 접미어가 붙어 '나의 영'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 육체적 생명을 넘어선, 하나님과 교제하는 나의 가장 본질적이고 내밀한 자아를 뜻합니다.</p>
                                <p><strong>신학적 의미:</strong> 인간이 소유한 가장 가치 있는 것은 재물이나 명예가 아니라 생명의 호흡(루아흐)입니다. 이를 창조주께 돌려드리는 것이 참된 안식의 시작입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">פָּדִיתָה <span onclick="playOriginalAudio('פָּדִיתָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(파디타)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '파다(פָּדָה, 속량하다, 값을 치르고 구하다)'의 완료형입니다.</p>
                                <p><strong>문맥적 의미:</strong> '주께서 이미 나를 속량하셨습니다'라는 과거의 구원 사건에 대한 확신입니다.</p>
                                <p><strong>신학적 의미:</strong> 우리가 미래와 현재를 주님께 맡길 수 있는 근거는 십자가에서 '이미(Already)' 치러진 대속의 은혜 때문입니다. 구속은 철저히 값(피)을 지불하고 사오는 것입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אוֹתִי <span onclick="playOriginalAudio('אוֹתִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(오티)</span></p>
                                <p><strong>본래 의미:</strong> 목적격 소사 '에트(אֵת)'에 1인칭 접미어가 붙어 '나를'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 구원의 대상이 막연한 다수가 아니라 바로 나 자신임을 지목합니다.</p>
                                <p><strong>신학적 의미:</strong> 대속의 개별적 적용입니다. 구원은 개인적이고 인격적인 관계 안에서 성취됩니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>본래 의미:</strong> '여호와'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 자기 백성을 향한 언약을 끝까지 지키시는 이름입니다.</p>
                                <p><strong>신학적 의미:</strong> 상황이 변해도 여호와는 영원히 존재하시는 신실하신 구원자이십니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אֵל <span onclick="playOriginalAudio('אֵל', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(엘)</span></p>
                                <p><strong>본래 의미:</strong> '능력의 하나님'을 뜻하는 명사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 원수들의 그물을 찢고 나를 건지실 수 있는 무한한 힘을 가진 전능자입니다.</p>
                                <p><strong>신학적 의미:</strong> 우리의 영혼을 맡길 분은 나약한 피조물이 아니라 온 우주를 주관하시는 강한 통치자이십니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אֱמֶת <span onclick="playOriginalAudio('אֱמֶת', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(에메트)</span></p>
                                <p><strong>본래 의미:</strong> '진리, 신실함, 확고함'을 뜻합니다. 동사 '아만(확실하다)'에서 파생되었습니다.</p>
                                <p><strong>문맥적 의미:</strong> 엘(하나님)을 수식하여 '진리의 하나님, 신실하신 하나님'이라는 호칭을 완성합니다.</p>
                                <p><strong>신학적 의미:</strong> 거짓이 없고 하신 약속을 반드시 지키시는 하나님의 본성입니다. 우리가 전 존재를 의탁할 수 있는 궁극적 이유는 그분이 절대적으로 믿을 만한(신실한) 분이기 때문입니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">בְּיָדְךָ אַפְקִיד רוּחִי פָּדִיתָה אוֹתִי יְהוָה אֵל אֱמֶת <span onclick="playOriginalAudio('בְּיָדְךָ אַפְקִיד רוּחִי פָּדִיתָה אוֹתִי יְהוָה אֵל אֱמֶת', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>בְּיָדְךָ(베야데카: 당신의 손에) אַפְקִיד(아프키드: 내가 맡깁니다) רוּחִי(루히: 나의 영을) פָּדִיתָה(파디타: 주께서 속량하셨습니다) אוֹתִי(오티: 나를) יְהוָה(야훼: 여호와여) אֵל(엘: 하나님) אֱמֶת(에메트: 진리의)</p>
                            <p><strong>[직역]</strong> "당신의 손에 내가 나의 영을 맡깁니다. 나를 속량하셨습니다, 오 여호와 진리의 하나님이여."</p>
                            <p><strong>[문법 해설]</strong> 문장의 앞부분 '아프키드(맡깁니다)'는 미완료형으로 현재와 미래의 지속적 행위를 나타내고, 뒷부분 '파디타(속량하셨다)'는 완료형으로 이미 성취된 과거의 사실을 나타냅니다. 즉, 과거에 이미 이루어진 확실한 구속(속량)의 역사적 사실에 근거하여, 현재와 미래의 삶 전체를 온전히 위탁한다는 논리적 구조를 취하고 있습니다. 엘 에메트(진리의 하나님)는 이 모든 과정이 가능하게 하는 토대입니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>이 고백은 다윗의 개인적인 부르짖음이었으나, 결국 골고다 언덕 위에서 예수 그리스도의 십자가 상의 마지막 칠언 중 하나(눅 23:46)로 완벽하게 성취되었습니다. 예수님은 철저한 버림받음의 어둠 속에서도 하나님 아버지를 끝까지 '진리(에메트)'로 신뢰하시며, 자신의 전 존재(루히)를 그분의 손(야드)에 던지셨습니다. 이는 단순한 체념이 아니라 가장 적극적인 믿음의 도약이었습니다.</p>
                            <p>우리도 매일의 삶 속에서 원수의 그물과 절망의 밤을 마주합니다. 그러나 우리는 혼자가 아닙니다. 이미 그리스도의 보혈로 우리를 '속량(파다)'하신 진리의 하나님이 우리를 붙들고 계십니다. 나의 건강, 재산, 자녀, 그리고 가장 깊은 영혼까지도 그 전능자의 손에 의탁하십시오. 가장 안전한 금고는 세상의 권력이 아니라 피 묻은 십자가를 통과한 우리 주님의 못 박힌 두 손입니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_31" data-title="시편 31편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
""",
    "mc0421.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 32:1</h3>
                            <div class="key-question-box">
                                <p>"허물의 사함을 받고 자신의 죄가 가려진 자는 복이 있도다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>א (알레프)</strong>: 소 머리 모양으로 묵음이나 '아' 발음입니다. <strong>פ (페)</strong>: 입 모양에서 유래한 '프' 발음입니다. <strong>ח (헤트)</strong>: 울타리 모양의 거친 '흐' 발음입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אַשְׁרֵי <span onclick="playOriginalAudio('אַשְׁרֵי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아쉬레)</span></p>
                                <p><strong>본래 의미:</strong> '복되도다(Oh, the blessedness of)'라는 감탄사적 명사 연계형입니다. 올바른 길을 걷는 충만한 상태를 의미합니다.</p>
                                <p><strong>문맥적 의미:</strong> 세상이 말하는 조건적 행복(바라크)이 아니라, 죄 사함을 받은 영혼이 누리는 궁극적이고 영적인 지복(至福)을 선포합니다.</p>
                                <p><strong>신학적 의미:</strong> 하나님과의 단절(죄)이 회복될 때 인간이 누릴 수 있는 최고의 상태를 뜻합니다. 이는 산상수훈의 팔복(마카리오스)과 직접적으로 연결됩니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">נְשׂוּי־ <span onclick="playOriginalAudio('נְשׂוּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(네수이)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '나사(נָשָׂא, 들어올리다, 가져가다)'의 수동 분사 연계형입니다.</p>
                                <p><strong>문맥적 의미:</strong> 내 스스로 감당할 수 없던 무거운 짐(죄책감)이 외부의 어떤 권능자에 의해 완전히 치워진 수동적 은혜의 상태를 말합니다.</p>
                                <p><strong>신학적 의미:</strong> 레위기 16장의 '아사셀 염소'가 백성의 죄를 짊어지고(나사) 광야로 떠나는 것을 연상시킵니다. 예수 그리스도께서 세상 죄를 '지고 가는' 어린 양이심을 예표합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">פֶּשַׁע <span onclick="playOriginalAudio('פֶּשַׁע', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(페샤)</span></p>
                                <p><strong>본래 의미:</strong> '반역, 허물'입니다. 하나님의 법을 알면서도 고의로 깨뜨린 주권 침해적 범죄입니다.</p>
                                <p><strong>문맥적 의미:</strong> 도덕적 결함 정도가 아니라, 왕이신 하나님을 향한 치명적인 반역 행위로서 인간의 전적 타락을 나타냅니다.</p>
                                <p><strong>신학적 의미:</strong> 죄의 가장 근본적인 형태는 하나님과의 언약을 고의로 파기한 반역(Rebellion)에 있음을 지적합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">כְּסוּי <span onclick="playOriginalAudio('כְּסוּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(케수이)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '카사(כָּסָה, 덮다, 가리다)'의 수동 분사 연계형입니다.</p>
                                <p><strong>문맥적 의미:</strong> 추악한 것이 보이지 않게 완전히 덮여버린 상태로, 하나님께서 우리의 죄를 더 이상 주목하지 않으시겠다는 의지적 선언입니다.</p>
                                <p><strong>신학적 의미:</strong> 속죄소(카포레트)의 피가 언약궤 안의 율법을 덮듯, 그리스도의 의로운 피가 우리의 불의를 덮어 의롭다 칭하시는 '칭의(Justification)'의 핵심 교리입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">חֲטָאָה <span onclick="playOriginalAudio('חֲטָאָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하타아)</span></p>
                                <p><strong>본래 의미:</strong> '죄, 과녁에서 빗나감'을 뜻합니다. 동사 '하타'에서 유래했습니다.</p>
                                <p><strong>문맥적 의미:</strong> 하나님의 거룩한 기준(과녁)에 도달하지 못하고 실패한 모든 불완전한 상태를 총칭합니다.</p>
                                <p><strong>신학적 의미:</strong> 인간의 선행이나 도덕적 노력은 결국 하나님의 영광이라는 과녁에 도달하지 못합니다(롬 3:23). 이 실패가 은혜의 덮개(케수이)로만 가려질 수 있음을 선포합니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">אַשְׁרֵי נְשׂוּי־פֶּשַׁע כְּסוּי חֲטָאָה <span onclick="playOriginalAudio('אַשְׁרֵי נְשׂוּי־פֶּשַׁע כְּסוּי חֲטָאָה', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>אַשְׁרֵי(아쉬레: 복되도다) נְשׂוּי(네수이: 치워진 자는) פֶּשַׁע(페샤: 반역이) כְּסוּי(케수이: 가려진 자는) חֲטָאָה(하타아: 죄가)</p>
                            <p><strong>[직역]</strong> "그의 반역이 치워진 자, 그의 죄가 덮여진 자는 참으로 복되도다!"</p>
                            <p><strong>[문법 해설]</strong> 본문은 감탄사 '아쉬레(복되도다)' 뒤에 두 개의 수동 분사('네수이', '케수이')가 각각 명사('페샤', '하타아')와 연계형(construct state)으로 묶인 완벽한 평행법 구조입니다. 능동태가 아닌 수동태가 쓰였다는 것은 인간 스스로 자신의 죄(반역과 실패)를 치우거나 덮을 능력이 없으며, 구원이 오직 하나님 편에서 주어지는 전적인 은혜임을 문법적으로 강력하게 증거합니다. 사도 바울은 로마서 4장에서 이 구절을 인용하여 행위가 아닌 믿음으로 말미암는 칭의 교리를 확립했습니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>우리는 세상에서 물질, 건강, 성공을 행복의 척도로 삼기 쉽지만, 다윗은 밧세바 범죄 이후 가장 비참한 수렁에서 진정한 행복(아쉬레)의 실체를 발견했습니다. 그것은 내 스스로의 힘으로 하나님을 향한 거대한 반역(페샤)과 실패(하타아)를 해결할 수 없음을 인정하고, 그 무거운 짐을 내게서 들어 옮겨주시는(나사) 분의 은혜를 입는 것입니다. 다윗의 이 고백은 훗날 이사야의 예언("여호와께서는 우리 무리의 죄악을 그에게 담당시키셨도다")을 거쳐 갈보리 언덕에서 완벽하게 성취되었습니다.</p>
                            <p>성도의 가장 큰 무기는 죄를 짓지 않는 무결점이 아니라, 지은 죄를 피 묻은 십자가 아래로 정직하게 가지고 나아가는 것입니다. 내가 내 죄를 숨기려 하면 뼈가 쇠하는 고통을 겪지만(3절), 내 죄를 자복하고 드러낼 때 그리스도의 의의 겉옷이 내 죄를 영원히 덮어(케수이) 주십니다. 하나님의 기준에서 빗나간 나의 연약함조차 그리스도의 십자가 아래서 속량 받았음을 기뻐하며, 은혜로 칭의 된 자의 담대한 평안을 누리는 하루가 됩시다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_32" data-title="시편 32편">성경 듣기</button>
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

