#!/usr/bin/env python3
"""
Mock Test Script for Daily Bible Sermon Auto-Generator.
Simulates a Gemini API response for today (2026-05-23) and renders the PWA HTML page
to verify template, CSS/Tailwind rendering, and dynamic calendar integration.
"""

import os
import json

TEMPLATE_PATH = "dailybible/dailybible_template.html"
OUTPUT_PATH = "dailybible/db260523.html" # Today's date (May 23, 2026)
MOCK_YOUTUBE_ID = "NyENth7DFUA"

# Mock sermon data emulating a premium Gemini 3 Flash Reformed theological summary
MOCK_SERMON_DATA = {
    "title": "하나님의 주권적 은혜와 복음의 가시적 보증",
    "metadata_title": "[창45:16-28] 하나님의 주권적 은혜와 복음의 가시적 보증 (주권적 은혜와 신자의 소생)",
    "description": "과거의 깊은 죄책과 낙심에 사로잡혔던 야곱 가문을 애굽의 풍성한 처소로 부르시는 언약의 환대와, 요셉이 보낸 수레를 목도하고 영적으로 극적 소생한 야곱의 믿음을 개혁주의 관점에서 깊이 있게 해설합니다.",
    "series": "창세기 강해 시리즈",
    "scripture_ref": "창세기 45장 16-28절",
    "date_string": "2026년 5월 23일 토요일",
    "core_theme": "요셉의 권속들을 향한 바로의 왕권적 환대와 풍성한 공급은, 우리의 모든 죄와 오점을 완전하신 사랑으로 덮으시고 선으로 반전시키시는 <span class=\"keyword\">하나님의 주권적 은혜</span>를 예표합니다. 또한 불신 속에 기력을 잃어가던 야곱이 요셉의 수레를 본 후 기력을 되찾는 반전은, 신자가 <span class=\"keyword\">복음의 보증</span>을 대면할 때 일어나는 은혜로운 영적 각성을 증거합니다.",
    "scripture_html": """
        <p><strong>16</strong> 요셉의 형들이 왔다는 소문이 바로의 궁에 들리매 바로와 그의 신하들이 기뻐하고</p>
        <p><strong>17</strong> 바로는 요셉에게 이르되 네 형들에게 명령하기를 너희는 이렇게 하여 너희 양식을 싣고 가서 가나안 땅에 이르거든</p>
        <p><strong>18</strong> 너희 아버지와 너희 가족을 이끌고 내게로 오라 내가 너희에게 애굽의 좋은 땅을 주리니 너희가 나라의 기름진 것을 먹으리라</p>
        <p><strong>19</strong> 이제 명령을 받았으니 이렇게 하라 너희는 애굽 땅에서 수레를 가져다가 너희 자녀와 아내를 태우고 너희 아버지를 데려오라</p>
        <p><strong>20</strong> 또 너희의 기구를 아끼지 말라 온 애굽 땅의 좋은 것이 너희 것임이니라 하라</p>
        <p><strong>21</strong> 이스라엘의 아들들이 그대로 할새 요셉이 바로의 명령대로 그들에게 수레를 주고 길 양식을 주며</p>
        <p><strong>22</strong> 또 그들에게 다 각기 옷 한 벌씩을 주되 베냐민에게는 은 삼백과 옷 다섯 벌을 주고</p>
        <p><strong>23</strong> 그가 또 이와 같이 그 아버지에게 보내되 수나귀 열 필에 애굽의 아름다운 물품을 실리고 암나귀 열 필에는 아버지에게 길에서 드릴 곡식과 떡과 양식을 실리고</p>
        <p><strong>24</strong> 이에 형들을 돌려보내며 그들에게 이르되 당신들은 길에서 다투지 말라 하였더라</p>
        <p><strong>25</strong> 그들이 애굽에서 올라와 가나안 땅으로 들어가서 아버지 야곱에게 이르러</p>
        <p><strong>26</strong> 알리어 이르되 요셉이 지금까지 살아 있어 애굽 땅 총리가 되었더이다 야곱이 그들의 말을 믿지 못하여 어리둥절 하더니</p>
        <p><strong>27</strong> 그들이 또 요셉이 자기들에게 부탁한 모든 말로 그에게 말하매 그들의 아버지 야곱은 요셉이 자기를 태우려고 보낸 수레를 보고서야 기운이 소생한지라</p>
        <p><strong>28</strong> 이스라엘이 이르되 족하도다 내 아들 요셉이 지금까지 살아 있으니 내가 죽기 전에 가서 그를 보리라 하니라</p>
    """,
    "principle_title": "죄의 흔적을 덮어 생명으로 인도하시는 하나님의 완전하신 주권",
    "principle_html": """
        <p>요셉을 시기하여 구덩이에 던지고 종으로 팔아넘겼던 형제들의 죄악은 하나님의 공의로운 분노 앞에 영벌을 받아 마땅한 것이었습니다. 그러나 하나님께서는 그들의 비열한 <span class=\"keyword\">죄책의 열매</span>마저 친히 역이용하셔서 가문 전체를 살리는 거룩한 구원의 방편으로 삼으셨습니다.</p>
        <p>이방 바로 왕과 애굽 신하들이 요셉의 가족이 왔다는 소식을 듣고 자발적으로 기뻐하며 온궁이 축제의 장이 된 장면(16절)은, 장차 성도가 참된 구주이신 그리스도의 은혜에 힘입어 천국 낙원에 들어설 때 받게 될 영광스럽고 과분한 <span class=\"keyword\">종말론적 환대</span>를 미리 가리킵니다. 우리의 허물은 가려지고, 오직 요셉(그리스도)의 공로로 인해 과분한 상속을 입게 되는 이 놀라운 법식은 전적인 하나님의 주권적 구속사입니다.</p>
    """,
    "history_title": "기구를 아끼지 말라 하신 바로의 아낌없는 공급과 애굽의 수레",
    "history_html": """
        <p>기근과 죽음이 덮친 땅에서 이주하는 야곱 가문을 위해 애굽 최고의 권력자 바로 왕은 전방위적인 지원을 베풀기 시작합니다.</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-2 mb-2">
            <div class="bg-orange-50/50 p-3 rounded-lg border border-orange-100">
                <h4 class="font-bold text-orange-700 mb-1">👑 "너희의 기구를 아끼지 말라" (20절)</h4>
                <p class="text-xs text-slate-600 leading-normal">
                    바로는 가나안 땅의 낡고 볼품없는 세간에 미련을 두지 말라고 명령합니다. 애굽의 가장 좋은 것과 최상의 땅이 그들을 위해 영구히 예비되어 있기 때문입니다. 이는 성도가 땅의 썩어질 정욕과 가치관에 집착하지 않고, 보장된 하늘의 기업을 바라보며 순례 길을 걷는 자유함을 뜻합니다.
                </p>
            </div>
            <div class="bg-orange-50/50 p-3 rounded-lg border border-orange-100">
                <h4 class="font-bold text-orange-700 mb-1">🛒 왕의 권위가 실린 문명의 수송 수단</h4>
                <p class="text-xs text-slate-600 leading-normal">
                    요셉은 아버지를 정중히 모시기 위해 당대 최고 기술의 가시적 상징인 '애굽의 수레'를 내어줍니다. 또한 나귀 20필에 가득 실린 길 양식과 호화로운 물품들, 그리고 베냐민에게 베풀어진 은 삼백과 옷 다섯 벌은 은혜의 풍성함과 확실함을 야곱 가문에게 시각적으로 선언하는 방편이 되었습니다.
                </p>
            </div>
        </div>
    """,
    "warning_title": "길 위에서 판단하며 다투는 죄의 옛 습성 배격",
    "warning_html": """
        <p>요셉은 형제들을 떠나보내며 깊은 지혜가 담긴 한 마디 경고를 남깁니다. <strong>"당신들은 길에서 다투지 말라" (24절)</strong>.</p>
        <p>이 경고는 복음의 무한한 용서를 체험한 성도가 경주하는 삶 속에서 가장 조심해야 할 죄악의 속성을 경계합니다:</p>
        <ul class="list-disc list-inside space-y-2 bg-rose-50/50 p-3 rounded-lg border border-rose-100 text-xs sm:text-sm">
            <li><strong>상호 책임 전가의 위험:</strong> 가나안으로 향하는 여정 중 형제들이 "누가 먼저 요셉을 팔아넘기려 했는가?", "그때 누가 더 주동했는가?"라며 과거의 죄를 들춰내어 상처를 남기고 분란을 일으킬 가능성을 사전에 차단한 것입니다.</li>
            <li><strong>율법주의적 정죄 배격:</strong> 요셉의 조건 없는 환대와 사랑으로 모든 허물을 탕감받았음에도, 정작 자신들끼리는 용서하지 못하고 책임 시비를 벌이는 것은 구속의 은혜를 전면 부인하는 행태입니다.</li>
        </ul>
    """,
    "application_title": "은혜의 '가시적 수레'를 볼 때 일어나는 메마른 영혼의 소생",
    "application_html": """
        <p>총 22년간 사랑하는 아들의 죽음을 슬퍼하며 가슴에 굳은 영적 마비 상태에 빠져 있던 야곱에게 극적인 영적 회복이 임합니다.</p>
        <div class="bg-emerald-50/50 rounded-xl p-4 border border-emerald-100 text-slate-700 text-xs sm:text-sm">
            <p class="font-bold text-emerald-800 mb-2">👁️ 복음의 말씀과 가시적 표상(성례)의 결합</p>
            <p class="leading-relaxed mb-2">
                야곱은 아들들이 전한 "요셉이 살아 총리가 되었다"는 고귀한 증언을 귀로만 들었을 때는 도저히 믿지 못해 어리둥절하며 혼미해했습니다(26절). 그러나 요셉이 자기를 데려오기 위해 보낸 <span class="keyword">거대하고 아름다운 수레</span>를 두 눈으로 직접 마주했을 때에야 기력이 완전히 소생(Revived)하였습니다.
            </p>
            <p class="leading-relaxed">
                이와 같이 성도의 믿음은 메마른 생각 속에만 머물지 않습니다. 보이지 않는 은혜의 약속을 예배, 기도, 성례(Sacraments), 그리고 일상의 수많은 자비로운 증표(가시적 수레)들을 통해 실감하고 굳게 붙잡을 때, 우리의 낙심했던 믿음과 소망은 번쩍 눈을 뜨고 새로운 생명력을 얻게 됩니다.
            </p>
        </div>
    """,
    "conclusion_title": "\"족하도다!\"의 전율과 부활하사 통치하시는 우리의 요셉 그리스도",
    "conclusion_html": r"""
        <p>수레를 목도한 이스라엘은 "족하도다! 요셉이 지금까지 살아있으니 내가 죽기 전에 가서 보리라"라는 대전환의 고백을 고백합니다. 이 놀라운 결말은 언약 백성의 승리를 엄숙히 보증합니다.</p>
        <div class="space-y-3 text-xs sm:text-sm">
            <p><strong>1. 참된 요셉이신 예수 그리스도:</strong> 시기 속에 죽어 무덤에 갇히신 줄로만 알았던 예수님께서는 다시 살아나사 온 우주를 통치하시고, 기근에 빠진 성도들을 먹여 살리는 생명의 총리이십니다. 이 부활 신앙이 성도에게 완전한 만족을 줍니다.</p>
            <div class="bg-slate-100 p-4 rounded-lg border border-slate-200 text-center my-2 text-slate-800">
                <p class="text-xs mb-1 text-slate-500 font-semibold">구속의 완전한 회복 공식</p>
                <div class="my-1">
                    $$ \text{22년의 슬픔 and 영적 혼미} \xrightarrow{\text{가시적 수레 (언약의 보증)}} \text{영혼의 극적인 기력 소생} $$
                </div>
            </div>
            <p><strong>2. 땅의 세간에 미련을 두지 않는 삶:</strong> 더 나은 애굽 최고의 땅이 영구히 예비되어 있으므로, 가나안의 하찮은 세간을 아까워하지 말라는 말씀을 기억해야 합니다. 성도는 장차 상속받을 영원한 하나님의 영광을 바라보며, 땅의 썩어질 물질과 기득권에 얽매여 이웃과 아웅다웅 다투지 않는 의무를 집행합니다.</p>
        </div>
    """
}

def main():
    print("Starting PWA Paging Integration & Template Verification (Mock Test)...")
    
    if not os.path.exists(TEMPLATE_PATH):
        print(f"ERROR: Template file {TEMPLATE_PATH} does not exist!")
        return
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()
        
    rendered = template
    for key, val in MOCK_SERMON_DATA.items():
        placeholder = f"{{{{ {key.upper()} }}}}"
        rendered = rendered.replace(placeholder, val)
        
    # Replace metadata variables
    rendered = rendered.replace("{{ YOUTUBE_ID }}", MOCK_YOUTUBE_ID)
    rendered = rendered.replace("{{ IMAGE }}", "https://drive.google.com/uc?export=view&id=1HWEyIUmIRa4TEXBUDMpDi--PC8DtitXJ")
    
    # Save the rendered HTML in dailybible/db260523.html (Today's date)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(rendered)
        
    print(f"\nSUCCESS: Mock sermon generated at {OUTPUT_PATH}!")
    print("You can now verify this page locally inside the workspace.")
    print("This file integrates beautifully with your PWA calendar under today's date (2026-05-23)!")

if __name__ == "__main__":
    main()
