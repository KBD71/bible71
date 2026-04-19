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
                            <p><strong>ד (달렛)</strong>: 문 모양의 '드' 발음입니다. <strong>ר (레쉬)</strong>: 머리 모양의 '르' 발음입니다. <strong>ר (루아흐)</strong>: 영, 기운을 뜻합니다.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">בִּדְבַר <span onclick="playOriginalAudio('בִּדְבַר', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(비드바르)</span></p>
                                <p><strong>의미:</strong> 전치사 베(בְּ, ~으로)와 다바르(דָּבָר, 말씀)의 연계형으로 '말씀으로'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>의미:</strong> '여호와의'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">שָׁמַיִם <span onclick="playOriginalAudio('שָׁמַיִם', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(샤마임)</span></p>
                                <p><strong>의미:</strong> '하늘들이'를 뜻하는 복수명사입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">נַעֲשׂוּ <span onclick="playOriginalAudio('נַעֲשׂוּ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(나아수)</span></p>
                                <p><strong>의미:</strong> 동사 아사(지어지다)의 닢팔(수동태) 완료형으로 '지어졌다'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וּבְרוּחַ <span onclick="playOriginalAudio('וּבְרוּחַ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(우베루아흐)</span></p>
                                <p><strong>의미:</strong> '그리고 기운(호흡/성령)으로'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">פִּיו <span onclick="playOriginalAudio('פִּיו', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(피우)</span></p>
                                <p><strong>의미:</strong> '그의 입의'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">כָּל־ <span onclick="playOriginalAudio('כָּל', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(콜)</span></p>
                                <p><strong>의미:</strong> '모든'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">צְבָאָם <span onclick="playOriginalAudio('צְבָאָם', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(체바암)</span></p>
                                <p><strong>의미:</strong> '그것들의 군대/만상이'입니다.</p>
                            </div>
                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">בִּדְבַר יְהוָה שָׁמַיִם נַעֲשׂוּ וּבְרוּחַ פִּיו כָּל־צְבָאָם <span onclick="playOriginalAudio('בִּדְבַר יְהוָה שָׁמַיִם נַעֲשׂוּ וּבְרוּחַ פִּיו כָּל־צְבָאָם', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[직역]</strong> "여호와의 말씀으로 하늘들이 지어졌고, 그의 입의 기운으로 그것들의 모든 만상이 (지어졌다)."</p>
                            <h4>④ 언약 신학적 묵상</h4>
                            <p>천지 창조에 성부, 성자(말씀), 성령(기운/루아흐) 삼위일체 하나님이 온전히 함께하셨음을 보여줍니다.</p>
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
                            <p><strong>ט (테트)</strong>: 뱀/바구니 모양에서 유래. <strong>ע (아인)</strong>: 눈 모양. <strong>ר (레쉬)</strong>: 머리 모양.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">טַעֲמוּ <span onclick="playOriginalAudio('טַעֲמוּ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(타아무)</span></p>
                                <p><strong>의미:</strong> 동사 '타암(맛보다)'의 복수 명령형으로 '너희는 맛보아라'입니다. 경험적 앎을 요구합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וּרְאוּ <span onclick="playOriginalAudio('וּרְאוּ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(우레우)</span></p>
                                <p><strong>의미:</strong> '그리고 너희는 보아라(알아라)'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">כִּי־ <span onclick="playOriginalAudio('כִּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(키)</span></p>
                                <p><strong>의미:</strong> '~함을' (that) 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">טוֹב <span onclick="playOriginalAudio('טוֹב', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(토브)</span></p>
                                <p><strong>의미:</strong> '선하심'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>의미:</strong> '여호와께서'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אַשְׁרֵי <span onclick="playOriginalAudio('אַשְׁרֵי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아쉬레)</span></p>
                                <p><strong>의미:</strong> '복되도다'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">הַגֶּבֶר <span onclick="playOriginalAudio('הַגֶּבֶר', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하게베르)</span></p>
                                <p><strong>의미:</strong> '그 사람은(the man)'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יֶחֱסֶה־ <span onclick="playOriginalAudio('יֶחֱסֶה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(예헤세)</span></p>
                                <p><strong>의미:</strong> '피하는 자는'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">בּוֹ <span onclick="playOriginalAudio('בּוֹ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(보)</span></p>
                                <p><strong>의미:</strong> '그에게'입니다.</p>
                            </div>
                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">טַעֲמוּ וּרְאוּ כִּי־טוֹב יְהוָה אַשְׁרֵי הַגֶּבֶר יֶחֱסֶה־בּוֹ <span onclick="playOriginalAudio('טַעֲמוּ וּרְאוּ כִּי־טוֹב יְהוָה אַשְׁרֵי הַגֶּבֶר יֶחֱסֶה־בּוֹ', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[직역]</strong> "여호와께서 선하시다는 것을 맛보고 보아라. 그에게 피난하는 그 사람은 복되도다!"</p>
                            <h4>④ 언약 신학적 묵상</h4>
                            <p>우리는 환난의 날에 여호와께 피할 때에만 비로소 그분의 십자가 은혜가 얼마나 달콤하고 선하신지를 인격적으로 맛보아 알게 됩니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_34" data-title="시편 34편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
""",
    "mc0424.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 디도서 3:5</h3>
                            <div class="key-question-box">
                                <p>"중생의 씻음과 성령의 새롭게 하심으로 하셨나니"</p>
                            </div>
                            <h4>① 헬라어 가이드</h4>
                            <p><strong>π (피)</strong>: 입술 파열음. <strong>λ (람다)</strong>: 혀끝을 윗니에 대는 발음. <strong>ἀ (알파)</strong>: 첫 글자.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">διὰ <span onclick="playOriginalAudio('διὰ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(디아)</span></p>
                                <p><strong>의미:</strong> '~를 통하여'라는 전치사입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">λουτροῦ <span onclick="playOriginalAudio('λουτροῦ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(루트루)</span></p>
                                <p><strong>의미:</strong> '씻음의'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">παλιγγενεσίας <span onclick="playOriginalAudio('παλιγγενεσίας', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(팔링게네시아스)</span></p>
                                <p><strong>의미:</strong> '중생(거듭남)의'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">καὶ <span onclick="playOriginalAudio('καὶ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(카이)</span></p>
                                <p><strong>의미:</strong> '그리고'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">ἀνακαινώσεως <span onclick="playOriginalAudio('ἀνακαινώσεως', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아나카이노세오스)</span></p>
                                <p><strong>의미:</strong> '새롭게 하심의'입니다. 지속적인 갱신입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">πνεύματος <span onclick="playOriginalAudio('πνεύματος', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(프뉴마토스)</span></p>
                                <p><strong>의미:</strong> '성령의'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">ἁγίου <span onclick="playOriginalAudio('ἁγίου', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하기우)</span></p>
                                <p><strong>의미:</strong> '거룩한'입니다. (성령을 뜻하는 형용사)</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold;">διὰ λουτροῦ παλιγγενεσίας καὶ ἀνακαινώσεως πνεύματος ἁγίου <span onclick="playOriginalAudio('διὰ λουτροῦ παλιγγενεσίας καὶ ἀνακαινώσεως πνεύματος ἁγίου', 'el-GR')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[직역]</strong> "... 거룩한 영의 새롭게 하심과 중생의 씻음을 통하여."</p>
                            <h4>④ 언약 신학적 묵상</h4>
                            <p>구원은 내 행위가 아니라 오직 삼위일체 하나님의 전적인 사역으로 인한 영적 재창조임을 보여줍니다.</p>
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
                            <p><strong>מ (멤)</strong>: 물결 모양 '므'. <strong>ח (헤트)</strong>: 울타리 '흐'. <strong>א (알레프)</strong>: 첫 글자.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">כִּי־ <span onclick="playOriginalAudio('כִּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(키)</span></p>
                                <p><strong>의미:</strong> '왜냐하면' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">עִמְּךָ <span onclick="playOriginalAudio('עִמְּךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(임메카)</span></p>
                                <p><strong>의미:</strong> '주와 함께(주께)' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">מְקוֹר <span onclick="playOriginalAudio('מְקוֹר', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(메코르)</span></p>
                                <p><strong>의미:</strong> '샘이, 원천이' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">חַיִּים <span onclick="playOriginalAudio('חַיִּים', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하임)</span></p>
                                <p><strong>의미:</strong> '생명의' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">בְּאוֹרְךָ <span onclick="playOriginalAudio('בְּאוֹרְךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(베오르카)</span></p>
                                <p><strong>의미:</strong> '주의 빛 안에서' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">נִרְאֶה־ <span onclick="playOriginalAudio('נִרְאֶה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(니르에)</span></p>
                                <p><strong>의미:</strong> '우리가 봅니다' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אוֹר <span onclick="playOriginalAudio('אוֹר', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(오르)</span></p>
                                <p><strong>의미:</strong> '빛을' 입니다.</p>
                            </div>
                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">כִּי־עִמְּךָ מְקוֹר חַיִּים בְּאוֹרְךָ נִרְאֶה־אוֹר <span onclick="playOriginalAudio('כִּי־עִמְּךָ מְקוֹר חַיִּים בְּאוֹרְךָ נִרְאֶה־אוֹר', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[직역]</strong> "왜냐하면 주께 생명의 샘이 있기 때문입니다. 주의 빛 안에서 우리가 빛을 봅니다."</p>
                            <h4>④ 언약 신학적 묵상</h4>
                            <p>오직 하나님의 계시의 빛이 있어야 우리가 진리를 볼 수 있다는 칼빈주의적 인식론을 보여줍니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_36" data-title="시편 36편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
""",
    "mc0426.html": """
                <div id="content-hebrew" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>원어 주해: 시편 37:4</h3>
                            <div class="key-question-box">
                                <p>"또 여호와를 기뻐하라 그가 네 마음의 소원을 네게 이루어 주시리로다"</p>
                            </div>
                            <h4>① 히브리어 가이드</h4>
                            <p><strong>ו (바브)</strong>: '그리고'. <strong>ה (헤)</strong>: 강조형 접두어. <strong>נ (눈)</strong>: 물고기. <strong>ג (기멜)</strong>: 낙타.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וְהִתְעַנַּג <span onclick="playOriginalAudio('וְהִתְעַנַּג', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(베히트아나그)</span></p>
                                <p><strong>의미:</strong> '그리고 네 자신을 최고로 기쁘게 하라' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">עַל־ <span onclick="playOriginalAudio('עַל', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(알)</span></p>
                                <p><strong>의미:</strong> '~안에서, ~로 인하여' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>의미:</strong> '여호와' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">וְיִתֶּן־ <span onclick="playOriginalAudio('וְיִתֶּן', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(베이텐)</span></p>
                                <p><strong>의미:</strong> '그리하면 그가 주실 것이다' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">לְךָ <span onclick="playOriginalAudio('לְךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(레카)</span></p>
                                <p><strong>의미:</strong> '너에게' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">מִשְׁאֲלֹת <span onclick="playOriginalAudio('מִשְׁאֲלֹת', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(미쉬알로트)</span></p>
                                <p><strong>의미:</strong> '소원들을' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">לִבֶּךָ <span onclick="playOriginalAudio('לִבֶּךָ', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(리베카)</span></p>
                                <p><strong>의미:</strong> '네 마음의' 입니다.</p>
                            </div>
                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">וְהִתְעַנַּג עַל־יְהוָה וְיִתֶּן־לְךָ מִשְׁאֲלֹת לִבֶּךָ <span onclick="playOriginalAudio('וְהִתְעַנַּג עַל־יְהוָה וְיִתֶּן־לְךָ מִשְׁאֲלֹת לִבֶּךָ', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[직역]</strong> "그리고 너는 여호와 안에서 네 자신을 기쁘게 하라, 그리하면 그가 네 마음의 소원들을 네게 주실 것이다."</p>
                            <h4>④ 언약 신학적 묵상</h4>
                            <p>기독교 희락주의의 핵심입니다. 여호와 안에서 최고로 기뻐할 때 내 소원이 하나님의 소원과 일치되어 반드시 이루어집니다.</p>
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
                            <p><strong>π (피)</strong>: 입술소리 '프'. <strong>β (베타)</strong>: '브' 발음.</p>

                            <h4>② 단어별 상세 해부</h4>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">ἐν <span onclick="playOriginalAudio('ἐν', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(엔)</span></p>
                                <p><strong>의미:</strong> '~안에서' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">ᾧ <span onclick="playOriginalAudio('ᾧ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(호)</span></p>
                                <p><strong>의미:</strong> 관계대명사 '그' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">γὰρ <span onclick="playOriginalAudio('γὰρ', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(가르)</span></p>
                                <p><strong>의미:</strong> '왜냐하면' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">πέπονθεν <span onclick="playOriginalAudio('πέπονθεν', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(페폰덴)</span></p>
                                <p><strong>의미:</strong> '고난을 당하셨기에' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">αὐτὸς <span onclick="playOriginalAudio('αὐτὸς', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아우토스)</span></p>
                                <p><strong>의미:</strong> '그 자신이' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">πειρασθείς <span onclick="playOriginalAudio('πειρασθείς', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(페이라스데이스)</span></p>
                                <p><strong>의미:</strong> '시험을 받으시어' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">δύναται <span onclick="playOriginalAudio('δύναται', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(뒤나타이)</span></p>
                                <p><strong>의미:</strong> '능력이 있으시다' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">τοῖς <span onclick="playOriginalAudio('τοῖς', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(토이스)</span></p>
                                <p><strong>의미:</strong> '~하는 자들을' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">πειραζομένοις <span onclick="playOriginalAudio('πειραζομένοις', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(페이라조메노이스)</span></p>
                                <p><strong>의미:</strong> '시험받고 있는' 입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">βοηθῆσαι <span onclick="playOriginalAudio('βοηθῆσαι', 'el-GR')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(보에데사이)</span></p>
                                <p><strong>의미:</strong> '(달려와서) 도우시기에' 입니다.</p>
                            </div>
                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold;">ἐν ᾧ γὰρ πέπονθεν αὐτὸς πειρασθείς, δύναται τοῖς πειραζομένοις βοηθῆσαι <span onclick="playOriginalAudio('ἐν ᾧ γὰρ πέπονθεν αὐτὸς πειρασθείς, δύναται τοῖς πειραζομένοις βοηθῆσαι', 'el-GR')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[직역]</strong> "왜냐하면 그 자신이 시험을 받아 고난을 겪으셨으므로, 그는 시험받고 있는 자들을 능히 도우실 수 있기 때문입니다."</p>
                            <h4>④ 언약 신학적 묵상</h4>
                            <p>우리 대제사장은 멀리서 명령만 하시는 분이 아니라 친히 내려와 모든 고통을 겪으시고, 비명을 듣고 달려와 구조해 주십니다.</p>
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
        print(f"Updated {file_name}")
