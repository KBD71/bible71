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
                                <p><strong>의미:</strong> 전치사 '베(בְּ)'와 명사 '야드(יָד, 손)', 2인칭 접미어가 결합하여 '당신의 손 안에'를 뜻합니다. 완벽한 통제와 보호를 상징합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אַפְקִיד <span onclick="playOriginalAudio('אַפְקִיד', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(아프키드)</span></p>
                                <p><strong>의미:</strong> 동사 '파카드(פָּקַד)'의 히필(사역형) 미완료로 '내가 맡깁니다, 위탁합니다'라는 뜻입니다. 귀중품을 은행에 맡기듯 영혼을 철저히 의탁하는 행위입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">רוּחִי <span onclick="playOriginalAudio('רוּחִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(루히)</span></p>
                                <p><strong>의미:</strong> 명사 '루아흐(רוּחַ, 영, 바람)'에 1인칭 접미어가 붙어 '나의 영'입니다. 생명의 가장 본질적인 중심을 뜻합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">פָּדִיתָה <span onclick="playOriginalAudio('פָּדִיתָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(파디타)</span></p>
                                <p><strong>의미:</strong> 동사 '파다(פָּדָה, 속량하다, 값을 치르고 구하다)'의 완료형입니다. 과거에 구원하신 확신을 근거로 현재를 의탁합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אוֹתִי <span onclick="playOriginalAudio('אוֹתִי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(오티)</span></p>
                                <p><strong>의미:</strong> 목적격 소사 '에트(אֵת)'에 1인칭 접미어가 붙어 '나를'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">יְהוָה <span onclick="playOriginalAudio('יְהוָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(야훼)</span></p>
                                <p><strong>의미:</strong> 언약의 신실하신 이름, '여호와'입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אֵל <span onclick="playOriginalAudio('אֵל', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(엘)</span></p>
                                <p><strong>의미:</strong> '능력의 하나님'을 뜻하는 명사입니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">אֱמֶת <span onclick="playOriginalAudio('אֱמֶת', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(에메트)</span></p>
                                <p><strong>의미:</strong> '진리, 신실함'을 뜻합니다. 하나님의 변함없는 속성입니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">בְּיָדְךָ אַפְקִיד רוּחִי פָּדִיתָה אוֹתִי יְהוָה אֵל אֱמֶת <span onclick="playOriginalAudio('בְּיָדְךָ אַפְקִיד רוּחִי פָּדִיתָה אוֹתִי יְהוָה אֵל אֱמֶת', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[직역]</strong> "당신의 손에 내가 나의 영을 맡깁니다. 나를 속량하셨습니다, 오 여호와 진리의 하나님이여."</p>
                            <h4>④ 언약 신학적 묵상</h4>
                            <p>예수님께서 십자가에서 마지막으로 하신 말씀입니다. 철저한 버림받음 속에서도 하나님의 신실하심(에메트)을 굳게 믿고 가장 안전한 손에 전 존재를 맡기는 위대한 신앙의 승리입니다.</p>
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
                                <p><strong>의미:</strong> '복되도다(Oh, the blessedness of)'라는 감탄사적 명사 연계형입니다. 하나님과의 관계에서 누리는 지극한 행복을 뜻합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">נְשׂוּי־ <span onclick="playOriginalAudio('נְשׂוּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(네수이)</span></p>
                                <p><strong>의미:</strong> 동사 '나사(נָשָׂא, 들어올리다, 가져가다)'의 수동 분사 연계형입니다. 무거운 짐이 누군가에 의해 치워진 상태를 말합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">פֶּשַׁע <span onclick="playOriginalAudio('פֶּשַׁע', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(페샤)</span></p>
                                <p><strong>의미:</strong> '반역, 허물'입니다. 하나님의 권위에 대한 의도적인 반역을 뜻합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">כְּסוּי <span onclick="playOriginalAudio('כְּסוּי', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(케수이)</span></p>
                                <p><strong>의미:</strong> 동사 '카사(כָּסָה, 덮다, 가리다)'의 수동 분사 연계형입니다. 보이지 않게 완전히 덮여버린 상태를 의미합니다.</p>
                            </div>
                            <div style="background:#fff; border:1px solid #dee2e6; border-radius:12px; padding:1.5rem; margin-bottom:1.2rem;">
                                <p style="font-size:1.8rem; font-weight:bold; color:#1a5c9a;">חֲטָאָה <span onclick="playOriginalAudio('חֲטָאָה', 'he-IL')" style="cursor:pointer;">🔊</span> <span style="font-size:1rem; color:#868e96; margin-left:10px;">(하타아)</span></p>
                                <p><strong>의미:</strong> '죄, 과녁에서 빗나감'을 뜻합니다. 하나님의 기준에서 벗어난 모든 상태입니다.</p>
                            </div>

                            <h4>③ 원어 구절 전체 분석</h4>
                            <div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; text-align:center;">
                                <p style="font-size:1.4rem; font-weight:bold; direction:rtl;">אַשְׁרֵי נְשׂוּי־פֶּשַׁע כְּסוּי חֲטָאָה <span onclick="playOriginalAudio('אַשְׁרֵי נְשׂוּי־פֶּשַׁע כְּסוּי חֲטָאָה', 'he-IL')" style="cursor:pointer;">🔊</span></p>
                            </div>
                            <p><strong>[직역]</strong> "그의 반역이 치워진 자, 그의 죄가 덮여진 자는 복이 있도다."</p>
                            <h4>④ 언약 신학적 묵상</h4>
                            <p>진정한 행복(아쉬레)은 재물이나 건강이 아니라, '죄의 문제'가 해결되는 데 있습니다. 내 스스로의 힘으로는 치울 수도 덮을 수도 없는 반역의 짐을 그리스도께서 십자가에서 대신 짊어지셨고, 그 보혈로 완전히 덮어(속죄) 주셨습니다.</p>
                            <div class="button-group">
                                <button class="btn btn-secondary listen-audio-btn" data-key="PSA_32" data-title="시편 32편">성경 듣기</button>
                            </div>
                        </div>
                    </article>
                </div>
"""
}

# The remaining files (0422-0427) will follow the same pattern
# To save space and run it immediately, I will generate them in batches.

import sys
for file_name, new_content in files_content.items():
    path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the entire <div id="content-hebrew"...> to the end of that div
        pattern = r'<div id="content-hebrew".*?</article>\s*</div>'
        new_text = re.sub(pattern, new_content.strip(), content, flags=re.DOTALL)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"Updated {file_name}")

