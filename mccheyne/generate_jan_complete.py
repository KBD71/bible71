#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate McCheyne Bible Reading Files for January 7-31
"""

import os

# McCheyne reading plan data for January 7-31
READINGS = {
    7: {"gen": 7, "mat": 7, "ezr": 7, "act": 7, "b3": "에스라", "b4": "사도행전"},
    8: {"gen": 8, "mat": 8, "ezr": 8, "act": 8, "b3": "에스라", "b4": "사도행전"},
    9: {"gen": "9-10", "mat": 9, "ezr": 9, "act": 9, "b3": "에스라", "b4": "사도행전"},
    10: {"gen": 11, "mat": 10, "ezr": 10, "act": 10, "b3": "에스라", "b4": "사도행전"},
    11: {"gen": 12, "mat": 11, "neh": 1, "act": 11, "b3": "느헤미야", "b4": "사도행전"},
    12: {"gen": 13, "mat": 12, "neh": 2, "act": 12, "b3": "느헤미야", "b4": "사도행전"},
    13: {"gen": 14, "mat": 13, "neh": 3, "act": 13, "b3": "느헤미야", "b4": "사도행전"},
    14: {"gen": 15, "mat": 14, "neh": 4, "act": 14, "b3": "느헤미야", "b4": "사도행전"},
    15: {"gen": 16, "mat": 15, "neh": 5, "act": 15, "b3": "느헤미야", "b4": "사도행전"},
    16: {"gen": 17, "mat": 16, "neh": 6, "act": 16, "b3": "느헤미야", "b4": "사도행전"},
    17: {"gen": 18, "mat": 17, "neh": 7, "act": 17, "b3": "느헤미야", "b4": "사도행전"},
    18: {"gen": 19, "mat": 18, "neh": 8, "act": 18, "b3": "느헤미야", "b4": "사도행전"},
    19: {"gen": 20, "mat": 19, "neh": 9, "act": 19, "b3": "느헤미야", "b4": "사도행전"},
    20: {"gen": 21, "mat": 20, "neh": 10, "act": 20, "b3": "느헤미야", "b4": "사도행전"},
    21: {"gen": 22, "mat": 21, "neh": 11, "act": 21, "b3": "느헤미야", "b4": "사도행전"},
    22: {"gen": 23, "mat": 22, "neh": 12, "act": 22, "b3": "느헤미야", "b4": "사도행전"},
    23: {"gen": 24, "mat": 23, "neh": 13, "act": 23, "b3": "느헤미야", "b4": "사도행전"},
    24: {"gen": 25, "mat": 24, "est": 1, "act": 24, "b3": "에스더", "b4": "사도행전"},
    25: {"gen": 26, "mat": 25, "est": 2, "act": 25, "b3": "에스더", "b4": "사도행전"},
    26: {"gen": 27, "mat": 26, "est": 3, "act": 26, "b3": "에스더", "b4": "사도행전"},
    27: {"gen": 28, "mat": 27, "est": 4, "act": 27, "b3": "에스더", "b4": "사도행전"},
    28: {"gen": 29, "mat": 28, "est": 5, "act": 28, "b3": "에스더", "b4": "사도행전"},
    29: {"gen": 30, "mrk": 1, "est": 6, "rom": 1, "b2": "마가복음", "b3": "에스더", "b4": "로마서"},
    30: {"gen": 31, "mrk": 2, "est": 7, "rom": 2, "b2": "마가복음", "b3": "에스더", "b4": "로마서"},
    31: {"gen": 32, "mrk": 3, "est": 8, "rom": 3, "b2": "마가복음", "b3": "에스더", "b4": "로마서"},
}

# Book codes for URL generation
BOOK_CODES = {
    "GEN": "OT/OT_01_GEN",
    "MAT": "NT/NT_40_MAT",
    "MRK": "NT/NT_41_MRK",
    "EZR": "OT/OT_15_EZR",
    "NEH": "OT/OT_16_NEH",
    "EST": "OT/OT_17_EST",
    "ACT": "NT/NT_44_ACT",
    "ROM": "NT/NT_45_ROM"
}

def make_button(book_code, chapter, book_name):
    """Generate button HTML for reading and audio"""
    path = BOOK_CODES[book_code]
    ch_str = str(chapter).replace("-", "_")  # Handle multi-chapter like "9-10"
    ch_num = str(chapter).split("-")[0] if "-" in str(chapter) else str(chapter)
    ch_num_padded = int(ch_num)
    
    return f'''<button class="btn btn-primary view-text-btn" data-path="https://kbd71.github.io/bible71/bible_html/{path}_{ch_num_padded:02d}.html" data-title="{book_name} {chapter}장">본문 보기 ({chapter}장)</button> <button class="btn btn-secondary listen-audio-btn" data-key="{book_code}_{ch_str}" data-title="{book_name} {chapter}장">성경 듣기 ({chapter}장)</button> '''

def generate_html(day, reading):
    """Generate HTML content for a specific day"""
    
    # Determine book names and chapters
    gen_ch = reading["gen"]
    b2_name = reading.get("b2", "마태복음")
    b2_ch = reading.get("mrk", reading.get("mat"))
    b3_name = reading["b3"]
    b3_ch = reading.get("ezr", reading.get("neh", reading.get("est")))
    b4_name = reading["b4"]
    b4_ch = reading.get("rom", reading.get("act"))
    
    # Determine book codes
    b2_code = "MRK" if "마가복음" in b2_name else "MAT"
    if b3_name == "에스라":
        b3_code = "EZR"
    elif b3_name == "느헤미야":
        b3_code = "NEH"
    else:
        b3_code = "EST"
    b4_code = "ROM" if "로마서" in b4_name else "ACT"
    
    # Generate buttons
    gen_btn = make_button("GEN", gen_ch, "창세기")
    b2_btn = make_button(b2_code, b2_ch, b2_name)
    b3_btn = make_button(b3_code, b3_ch, b3_name)
    b4_btn = make_button(b4_code, b4_ch, b4_name)
    
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1월 {day}일 맥체인 성경읽기</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="progress-container"><div class="progress-bar" id="reading-progress"></div></div>
    <div class="container">
        <div class="content-wrapper">
            <header>
                <h4>M'Cheyne Bible Reading Plan</h4>
                <h1>1월 {day}일</h1>
            </header>
            <nav class="tabs">
                <button class="tab-btn active" data-target="content-book1" data-color="book1">창세기 {gen_ch}장</button>
                <button class="tab-btn" data-target="content-book2" data-color="book2">{b2_name} {b2_ch}장</button>
                <button class="tab-btn" data-target="content-book3" data-color="book3">{b3_name} {b3_ch}장</button>
                <button class="tab-btn" data-target="content-book4" data-color="book4">{b4_name} {b4_ch}장</button>
                <button class="tab-btn" data-target="content-integration" data-color="integration">통합 묵상</button>
            </nav>
            <main>
                <div id="content-book1" class="tab-content active">
                    <article class="chapter-card card-book1">
                        <div class="card-content">
                            <h3>창세기 {gen_ch}장</h3>
                            <h4>상세 개요</h4>
                            <p>창세기 {gen_ch}장의 주요 내용을 설명합니다.</p>
                            <h4>심층 신학적 해설</h4>
                            <p>하나님의 언약과 섭리가 이 장에서 어떻게 드러나는지 살펴봅니다.</p>
                            <div class="button-group">{gen_btn}</div>
                        </div>
                    </article>
                </div>
                <div id="content-book2" class="tab-content">
                    <article class="chapter-card card-book2">
                        <div class="card-content">
                            <h3>{b2_name} {b2_ch}장</h3>
                            <h4>상세 개요</h4>
                            <p>{b2_name} {b2_ch}장의 주요 내용을 설명합니다.</p>
                            <h4>심층 신학적 해설</h4>
                            <p>예수 그리스도의 가르침과 사역이 이 장에서 어떻게 나타나는지 살펴봅니다.</p>
                            <div class="button-group">{b2_btn}</div>
                        </div>
                    </article>
                </div>
                <div id="content-book3" class="tab-content">
                    <article class="chapter-card card-book3">
                        <div class="card-content">
                            <h3>{b3_name} {b3_ch}장</h3>
                            <h4>상세 개요</h4>
                            <p>{b3_name} {b3_ch}장의 주요 내용을 설명합니다.</p>
                            <h4>심층 신학적 해설</h4>
                            <p>하나님의 회복과 섭리가 이 장에서 어떻게 드러나는지 살펴봅니다.</p>
                            <div class="button-group">{b3_btn}</div>
                        </div>
                    </article>
                </div>
                <div id="content-book4" class="tab-content">
                    <article class="chapter-card card-book4">
                        <div class="card-content">
                            <h3>{b4_name} {b4_ch}장</h3>
                            <h4>상세 개요</h4>
                            <p>{b4_name} {b4_ch}장의 주요 내용을 설명합니다.</p>
                            <h4>심층 신학적 해설</h4>
                            <p>초대교회의 사역과 복음의 확장이 이 장에서 어떻게 나타나는지 살펴봅니다.</p>
                            <div class="button-group">{b4_btn}</div>
                        </div>
                    </article>
                </div>
                <div id="content-integration" class="tab-content">
                    <article class="integration-card">
                        <div class="card-content">
                            <h3>통합 묵상</h3>
                            <h4>관통하는 주제</h4>
                            <p>오늘의 본문들을 관통하는 하나님의 구속 계획을 살펴봅니다.</p>
                            <h4>핵심 개념 및 상호 참조</h4>
                            <p>각 본문의 핵심 개념과 상호 연결성을 분석합니다.</p>
                            <h4>핵심 단어 연구</h4>
                            <p>오늘 본문의 핵심 히브리어/헬라어 단어를 연구합니다.</p>
                            <h4>구속사적 결론</h4>
                            <p>오늘의 본문들이 구속사에서 어떤 의미를 지니는지 정리합니다.< /p>
                            <h4>신학적 종합과 전망</h4>
                            <p>오늘의 묵상을 통한 신학적 적용과 실천 방향을 제시합니다.</p>
                            <div class="button-group">
                                <a href="#top" class="btn btn-primary">맨 위로 돌아가기</a>
                            </div>
                        </div>
                    </article>
                </div>
            </main>
            <footer>
                <p>&copy; 2025 MacCheyne 5.0. All Rights Reserved.</p>
            </footer>
        </div>
    </div>
    <div class="modal-overlay" id="text-modal">
        <div class="modal-content">
            <div class="modal-header"><h2 id="modal-title"></h2><button class="modal-close-btn" id="modal-close">&times;</button></div>
            <div class="modal-body"><iframe id="modal-iframe" src=""></iframe></div>
        </div>
    </div>
    <div class="floating-nav" id="floating-nav">
        <button class="nav-btn" id="prev-tab" title="이전"><span>◀</span></button>
        <div class="nav-info"><span class="current-tab" id="current-tab-info">1/5</span></div>
        <button class="nav-btn" id="next-tab" title="다음"><span>▶</span></button>
    </div>
    <div class="audio-player" id="audio-player">
        <div class="audio-player-content">
            <div class="audio-player-info" id="player-info">오디오를 선택하세요</div>
            <div class="audio-player-controls">
                <button id="play-pause-btn" title="재생/일시정지">▶</button>
                <button id="close-player-btn" title="닫기"></button>
            </div>
        </div>
    </div>
    <div id="player-container"></div>
    <script src="script.js"></script>
</body>
</html>'''
    
    return html

# Main execution
def main():
    output_dir = "/Volumes/minimac/bible71/mccheyne"
    
    print("Generating McCheyne files for January 7-31...")
    
    for day in range(7, 32):
        reading = READINGS[day]
        html_content = generate_html(day, reading)
        
        filename = f"mc01{day:02d}.html"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Created {filename}")
    
    print(f"\n완료! 총 25개 파일 생성됨 (1월 7일~31일)")

if __name__ == "__main__":
    main()
