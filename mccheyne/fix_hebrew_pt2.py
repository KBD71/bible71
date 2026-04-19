import os
import re

files_content = {
    "mc0422.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 33:6</h3>
                            <div class="key-question-box">
                                <p>"여호와의 말씀으로 하늘이 지음이 되었으며 그 만상을 그의 입기운으로 이루었도다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>ד (달렛)</strong>: 문 모양의 '드' 발음입니다. <strong>ר (레쉬)</strong>: 머리 모양의 '르' 발음입니다. <strong>צ (짜데)</strong>: 낚시 바늘 모양의 '쯔' 발음입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">בִּדְבַר <span onclick="playOriginalAudio('בִּדְבַר', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(비드바르)</span></p>
                                <p><strong>본래 의미:</strong> 전치사 베(בְּ, ~으로)와 명사 다바르(דָּבָר, 말씀, 일)의 연계형으로 '말씀으로'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 천지 창조가 인간의 물리적 노동이 아니라 오직 인격적인 의지의 표명(말씀)으로 이루어졌음을 선포합니다.</p>
                                <p><strong>신학적 의미:</strong> 요한복음 1:1의 태초의 '말씀(로고스)'과 연결되며, 제2위 성자 하나님이신 그리스도가 창조의 주체요 수단이심을 예표합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>본래 의미:</strong> 이스라엘의 언약적 신, '여호와'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 창조주 하나님이 곧 이스라엘과 언약을 맺으신 구원자와 동일한 분임을 보여줍니다.</p>
                                <p><strong>신학적 의미:</strong> 구속사(Redemptive History)의 주체인 여호와가 창조계 전체의 주인이심을 확증합니다. 곧 언약의 신실하심이 온 우주의 보존으로 이어집니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">שָׁמַיִם <span onclick="playOriginalAudio('שָׁמַיִם', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(샤마임)</span></p>
                                <p><strong>본래 의미:</strong> '하늘들'을 뜻하는 쌍수(또는 복수) 명사입니다. 광대한 우주 공간 전체를 가리킵니다.</p>
                                <p><strong>문맥적 의미:</strong> 인간이 가장 경외하는 대자연의 웅장함조차 피조물에 불과함을 보여줍니다.</p>
                                <p><strong>신학적 의미:</strong> 고대 근동의 이방 종교들이 하늘(해, 달, 별)을 신으로 숭배했던 것과 달리, 하늘은 창조주의 권능에 의해 지어진 장막일 뿐임을 선포하는 반(反)우상숭배적 선언입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">נַעֲשׂוּ <span onclick="playOriginalAudio('נַעֲשׂוּ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(나아수)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '아사(עָשָׂה, 만들다, 행하다)'의 닢팔(수동태) 완료형으로 '지어졌다'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 하늘이 스스로 진화하거나 자연 발생한 것이 아니라 지음 받은 결과물임을 명시합니다.</p>
                                <p><strong>신학적 의미:</strong> 무에서 유를 창조하신(Creatio ex nihilo) 하나님의 절대적 권능을 드러내는 피동사입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וּבְרוּחַ <span onclick="playOriginalAudio('וּבְרוּחַ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(우베루아흐)</span></p>
                                <p><strong>본래 의미:</strong> 접속사 '베(וְ, 그리고)', 전치사 '베(בְּ, ~으로)', 명사 '루아흐(רוּחַ, 영, 기운, 호흡)'의 연계형 결합입니다.</p>
                                <p><strong>문맥적 의미:</strong> 하나님의 입에서 나오는 강력한 숨결, 생기를 부여하는 능력을 뜻합니다.</p>
                                <p><strong>신학적 의미:</strong> 창세기 1:2의 수면 위를 운행하시는 '하나님의 영(성령)'을 가리킵니다. 성령 하나님이 창조의 생명력을 불어넣으신 주역임을 보여줍니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">פִּיו <span onclick="playOriginalAudio('פִּיו', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(피우)</span></p>
                                <p><strong>본래 의미:</strong> 명사 '페(פֶּה, 입)'에 3인칭 단수 접미어가 붙어 '그의 입의'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 말씀(다바르)과 기운(루아흐)이 나오는 출처로서 인격적인 하나님의 입술을 의인화합니다.</p>
                                <p><strong>신학적 의미:</strong> 생명은 물질의 결합에서 오는 것이 아니라 하나님의 입에서 나오는 인격적 호흡에서 비롯됨을 강조합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">כָּל־ <span onclick="playOriginalAudio('כָּל', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(콜)</span></p>
                                <p><strong>본래 의미:</strong> '모든(all)'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 창조계 내에 예외가 단 하나도 없음을 보여주는 포괄적인 수식어입니다.</p>
                                <p><strong>신학적 의미:</strong> 우주의 어떤 별이나 영적 존재도 하나님의 피조계 외부에 존재할 수 없다는 철저한 유일신 사상을 담고 있습니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">צְבָאָם <span onclick="playOriginalAudio('צְבָאָם', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(체바암)</span></p>
                                <p><strong>본래 의미:</strong> 명사 '차바(צָבָא, 군대, 무리)'에 3인칭 복수 접미어가 붙어 '그것들의 무리가'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 밤하늘에 끝없이 펼쳐진 수많은 별들과 천체들을 진열된 군대처럼 질서 정연하게 묘사합니다.</p>
                                <p><strong>신학적 의미:</strong> 해와 달과 별들이 독립적인 신성이 아니라 우주를 다스리시는 만군의 여호와(야훼 체바오트)의 지휘 아래 있는 피조된 군대에 불과함을 선언합니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">בִּדְבַר יְהוָה שָׁמַיִם נַעֲשׂוּ וּבְרוּחַ פִּיו כָּל־צְבָאָם <span onclick="playOriginalAudio('בִּדְבַר יְהוָה שָׁמַיִם נַעֲשׂוּ וּבְרוּחַ פִּיו כָּל־צְבָאָם', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>בִּדְבַר(비드바르: 말씀으로) יְהוָה(야훼: 여호와의) שָׁמַיִם(샤마임: 하늘들이) נַעֲשׂוּ(나아수: 지어졌다) וּבְרוּחַ(우베루아흐: 그리고 기운으로) פִּיו(피우: 그의 입의) כָּל־(콜: 모든) צְבָאָם(체바암: 그것들의 만상이)</p>
                            <p><strong>[직역]</strong> "여호와의 말씀으로 하늘들이 지어졌으며, 그의 입의 기운으로 하늘의 모든 만상이 지어졌다."</p>
                            <p><strong>[문법 해설]</strong> 문장은 완벽한 동의적 평행법(Synonymous Parallelism)을 취하고 있습니다. 전반절의 '말씀(다바르)'은 후반절의 '입의 기운(루아흐)'과 평행을 이루며, '하늘들(샤마임)'은 '모든 만상(체바암)'과 평행합니다. 수동태 동사 '나아수(지어졌다)'는 전반절에만 있지만, 후반절까지 그 의미가 확장되어 걸립니다. 창조 행위가 성부의 뜻, 성자(말씀), 성령(루아흐)의 완벽한 삼위일체적 사역임을 시적인 압축미로 보여주는 위대한 구절입니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>시편 기자는 세상의 웅장함 앞에서 두려워하지 말라고 권면합니다. 이방인들은 밤하늘의 촘촘한 별들(만상)과 거대한 바다를 보며 그것들을 신으로 숭배하고 두려워했습니다. 그러나 이스라엘에게 주신 계시는 명확합니다. 저 끝을 알 수 없는 우주와 해와 달은 그저 하나님의 '말씀(로고스)' 한 마디와 '입김(성령)'으로 만들어진 작은 조형물에 불과합니다. 창조주 여호와는 세상을 손으로 빚기 위해 땀 흘리지 않으시고, 오직 주권적인 명령만으로 무에서 유를 이끌어내셨습니다.</p>
                            <p>이 위대한 창조주가 바로 지금 나의 기도를 들으시고 나와 언약을 맺으신 나의 아버지이십니다. 내 인생의 수많은 문제와 장벽이 태산처럼 거대해 보일지라도, 온 우주를 한숨결로 지으신 하나님의 입기운 앞에서는 먼지에 불과합니다. 새 창조(중생) 역시 이 동일한 말씀(복음)과 성령(기운)으로 내 영혼에 임했습니다. 오늘 내 상황이 칠흑 같은 무질서(혼돈) 속에 있을지라도, 창조의 빛을 명하신 여호와의 말씀이 내 안에 임할 때 새 생명의 질서가 창조됨을 굳게 믿읍시다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_33" data-title="시편 33편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
""",
    "mc0423.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 34:8</h3>
                            <div class="key-question-box">
                                <p>"너희는 여호와의 선하심을 맛보아 알지어다 그에게 피하는 자는 복이 있도다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>ט (테트)</strong>: 뱀 또는 바구니 모양에서 유래한 '트' 발음입니다. <strong>ע (아인)</strong>: 눈 모양에서 온 후음. <strong>ר (레쉬)</strong>: 머리 모양의 '르' 발음입니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">טַעֲמוּ <span onclick="playOriginalAudio('טַעֲמוּ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(타아무)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '타암(טָעַם, 맛보다, 인지하다)'의 복수 명령형으로 '너희는 맛보아라'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 음식을 혀로 직접 느껴보는 행위처럼, 하나님의 은혜를 머리로만 아는 것이 아니라 전인격적인 체험으로 깨달으라는 강력한 초청입니다.</p>
                                <p><strong>신학적 의미:</strong> 참된 신앙은 객관적 교리에 머물지 않고 주관적인 은혜의 체득(Experiential knowledge)으로 나아가야 함을 보여줍니다. 다윗 자신이 미친 체하여 죽음의 위기를 벗어난(삼상 21장) 극적인 구원을 체험한 후 터져나온 고백입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וּרְאוּ <span onclick="playOriginalAudio('וּרְאוּ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(우레우)</span></p>
                                <p><strong>본래 의미:</strong> 접속사 바브(그리고)와 동사 '라아(רָאָה, 보다, 알아차리다)'의 복수 명령형이 결합하여 '그리고 너희는 보아라'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 육신의 눈으로 보는 것을 넘어 영적인 통찰로 하나님의 선하심을 확증하라는 의미입니다.</p>
                                <p><strong>신학적 의미:</strong> '맛보다'라는 미각적 체험 뒤에 '보다'라는 시각적 확신이 뒤따릅니다. 하나님을 인격적으로 경험할 때 영안이 열려 그분의 섭리를 명확히 깨닫게 됨을 시사합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">כִּי־ <span onclick="playOriginalAudio('כִּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(키)</span></p>
                                <p><strong>본래 의미:</strong> '~함을', '왜냐하면'을 뜻하는 접속사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 무엇을 맛보고 보아야 하는지 목적어절을 이끕니다.</p>
                                <p><strong>신학적 의미:</strong> 체험의 목적이 감정주의가 아니라 명확한 언약의 속성(선하심)을 확인하는 데 있음을 명시합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">טוֹב <span onclick="playOriginalAudio('טוֹב', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(토브)</span></p>
                                <p><strong>본래 의미:</strong> '선한, 좋은, 아름다운'을 뜻하는 형용사입니다.</p>
                                <p><strong>문맥적 의미:</strong> 나를 벼랑 끝에서 건져내시는 흠 없고 완전하신 선하심을 찬양합니다.</p>
                                <p><strong>신학적 의미:</strong> 선하심(토브)은 하나님의 본질적 속성입니다. 비록 현재 내 상황이 최악(블레셋 가드 왕 앞에서의 수치)이라 할지라도, 그분이 허락하신 결론은 궁극적으로 내 영혼에 가장 유익한 선(Goodness)이라는 확신입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>본래 의미:</strong> 여호와입니다.</p>
                                <p><strong>문맥적 의미:</strong> 다윗을 미치광이의 수치에서 건져내신 실질적인 구원자의 이름입니다.</p>
                                <p><strong>신학적 의미:</strong> 체험적 지식의 대상은 종교적 관념이 아니라 스스로 계시는 인격적 구원자 야훼입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אַשְׁרֵי <span onclick="playOriginalAudio('אַשְׁרֵי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아쉬레)</span></p>
                                <p><strong>본래 의미:</strong> '복되도다(Oh, the happiness of)'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 세상에서 누리는 안락함이 아니라, 극심한 위기 속에서 주님 품에 안긴 자만이 아는 참된 지복입니다.</p>
                                <p><strong>신학적 의미:</strong> 복의 근원이 환경의 평탄함에 있지 않고, 하나님과의 언약적 관계 안에 있음을 선언합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">הַגֶּבֶר <span onclick="playOriginalAudio('הַגֶּבֶר', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하게베르)</span></p>
                                <p><strong>본래 의미:</strong> 정관사 헤(ה)와 '힘센 자, 사나이'를 뜻하는 명사 게베르(גֶּבֶר)의 결합으로 '그 사람은'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 스스로 강하다고 생각하지만 사실은 절대적 피난처가 필요한 나약한 인간 존재를 강조합니다.</p>
                                <p><strong>신학적 의미:</strong> 다윗은 용사 중의 용사였으나 자기 힘(게베르)으로 살 수 없음을 깨달았습니다. 인간의 참된 강함은 내 능력을 포기하고 하나님의 능력에 의존할 때 시작됨을 암시합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יֶחֱסֶה־ <span onclick="playOriginalAudio('יֶחֱסֶה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(예헤세)</span></p>
                                <p><strong>본래 의미:</strong> 동사 '하사(חָסָה, 피난처를 구하다, 숨다, 피하다)'의 미완료 3인칭 단수형으로 '피하는 자는'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 폭풍우를 피해 바위 틈으로 숨어 들어가는 병아리처럼, 위협적인 세상 속에서 날개 그늘 아래로 달려가는 절박한 행동입니다.</p>
                                <p><strong>신학적 의미:</strong> 칭의를 얻는 '믿음'의 구약적 표현입니다. 내 의지와 힘을 다 내려놓고 오직 그리스도의 십자가 공로 뒤로 숨는 것, 그것이 가장 완벽한 피난(하사)입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">בּוֹ <span onclick="playOriginalAudio('בּוֹ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(보)</span></p>
                                <p><strong>본래 의미:</strong> 전치사 베(בְּ, ~안에, ~에게)와 3인칭 접미어가 결합하여 '그에게'입니다.</p>
                                <p><strong>문맥적 의미:</strong> 피난의 목적지가 다름 아닌 여호와 자신임을 명시합니다.</p>
                                <p><strong>신학적 의미:</strong> 성도의 피난처는 교리나 종교 의식이 아니라 인격적이신 하나님 한 분뿐입니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">טַעֲמוּ וּרְאוּ כִּי־טוֹב יְהוָה אַשְׁרֵי הַגֶּבֶר יֶחֱסֶה־בּוֹ <span onclick="playOriginalAudio('טַעֲמוּ וּרְאוּ כִּי־טוֹב יְהוָה אַשְׁרֵי הַגֶּבֶר יֶחֱסֶה־בּוֹ', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[단어별 음역 및 직역 병기]</strong></p>
                            <p>טַעֲמוּ(타아무: 맛보아라) וּרְאוּ(우레우: 그리고 보아라) כִּי(키: ~함을) טוֹב(토브: 선하심) יְהוָה(야훼: 여호와께서) אַשְׁרֵי(아쉬레: 복되도다) הַגֶּבֶר(하게베르: 그 사람은) יֶחֱסֶה־(예헤세: 피하는 자는) בּוֹ(보: 그에게)</p>
                            <p><strong>[직역]</strong> "여호와께서 선하시다는 것을 맛보고 보아라. 그분 안으로 피난하는 그 사람은 참으로 복되도다!"</p>
                            <p><strong>[문법 해설]</strong> 문장은 두 부분으로 나뉩니다. 전반부는 두 개의 강렬한 명령법('맛보라', '보라')을 통해 백성들을 경험적 신앙으로 초청하는 선지자적 외침이며, 후반부는 명사구('복되도다 그 사람')와 관계대명사 절('그에게 피하는 자')을 통해 그 초청에 응답하는 자의 영광스러운 결론(행복)을 선포하는 지혜 문학적 선언입니다. 미완료 동사 '예헤세(피하다)'는 단회적 도피가 아니라 매일의 삶 속에서 주님을 지속적인 피난처로 삼는 습관적 신앙 태도를 시사합니다.</p>

                            <h4>④ 언약 신학적 묵상</h4>
                            <p>이 시편의 배경은 다윗의 생애 중 가장 비참했던 순간입니다. 사울을 피해 가드 왕 아기스에게로 도망쳤던 다윗은, 정체가 발각될 위기에 처하자 침을 수염에 흘리며 미친 체하는 굴욕을 겪습니다(삼상 21장). 세상의 위대한 용사(게베르)의 체면이 산산조각 나는 그 절망의 밑바닥에서 다윗은 기적적인 구원을 경험합니다. 그리고 그는 깨닫습니다. 하나님의 선하심(토브)은 평탄한 궁궐에서가 아니라, 내 의지와 자존심이 다 꺾인 벼랑 끝에서 주님의 날개 그늘로 숨어들(하사) 때 가장 달콤하게 맛보아진다(타암)는 사실을 말입니다.</p>
                            <p>그리스도의 십자가는 이 선하심의 가장 완벽한 성취입니다. 하나님은 우리를 죄의 심판에서 건지시기 위해 당신의 독생자를 수치스러운 십자가의 벼랑 끝으로 몰아넣으셨습니다. 세상은 그것을 미련하고 약한 것이라 조롱하지만, 그 십자가 뒤로 몸을 숨기는(피하는) 자마다 영원한 생명의 지복(아쉬레)을 누리게 됩니다. 오늘 내 삶의 조건이 어떠하든, 스스로의 강함을 내려놓고 겸손히 주님의 십자가를 피난처로 삼으십시오. 그때 비로소 당신의 영혼은 "하나님은 참으로 선하시다"라는 고백을 미각적 희열로 노래하게 될 것입니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_34" data-title="시편 34편">성경 듣기</button>
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

