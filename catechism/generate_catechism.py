import pypdfium2 as pdfium
import re
import os

# Date to Page mapping (PDF page numbers, 1-based)
DATE_PAGE_MAP = {
    "1116": 140, "1117": 146, "1118": 153, "1119": 159, "1120": 164,
    "1121": 169, "1122": 176, "1123": 184, "1124": 192, "1125": 199,
    "1126": 204, "1127": 211, "1128": 216, "1129": 224, "1130": 230,
    "1201": 236, "1202": 242, "1203": 249, "1204": 256, "1205": 265,
    "1206": 271, "1207": 280, "1208": 288, "1209": 294, "1210": 302,
    "1211": 312, "1212": 319, "1213": 327, "1214": 335, "1215": 342,
    "1216": 348, "1217": 355, "1218": 362, "1219": 370, "1220": 378,
    "1221": 384, "1222": 390, "1223": 396, "1224": 402, "1225": 408,
    "1226": 417, "1227": 424, "1228": 430, "1229": 439, "1230": 448,
    "1231": 456
}

PDF_PATH = "/Users/kbd/Desktop/날마다6.pdf"
OUTPUT_DIR = "/Volumes/minimac/bible71/catechism"

def extract_text_by_pages(pdf, start_page, end_page):
    text = ""
    for i in range(start_page - 1, min(end_page - 1, len(pdf))):
        text += pdf[i].get_textpage().get_text_range() + "\n"
    return text

def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Skip page numbers
        if re.search(r'^\s*\d+\s*$', line): continue
        # Skip headers like "11월. 27B장. 말씀과성례 141"
        if re.search(r'^1[12]월\.\s+\d+[AB]?장\.', line): continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def parse_content(text):
    # Normalize whitespace in section markers
    text = re.sub(r'신\s*앙\s*고\s*백\s*서', '신앙고백서', text)
    text = re.sub(r'대\s*요\s*리\s*문\s*답', '대요리문답', text)
    text = re.sub(r'소\s*요\s*리\s*문\s*답', '소요리문답', text)
    text = re.sub(r'교\s*리\s*해\s*설', '교리해설', text)
    text = re.sub(r'적\s*용\s*질\s*문', '적용질문', text)
    text = re.sub(r'말\s*씀\s*요\s*절', '말씀요절', text)
    
    # Extract Title (look for pattern like "f.0,. 제목" or just "제목")
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    title = ""
    for i, line in enumerate(lines[:10]):  # Check first 10 lines
        # Skip date patterns, page markers
        if re.match(r'^1[12]월', line) or re.match(r'---', line):
            continue
        # Look for title pattern (often has OCR artifacts like "f.0,.")
        if len(line) < 50 and (i < 5 or not title):
            # Clean OCR artifacts
            clean_title = re.sub(r'^[f\.0,\s]+', '', line)
            clean_title = re.sub(r'[,\.]+\s*$', '', clean_title)
            if clean_title and len(clean_title) > 2:
                title = clean_title
                break
    
    # Default title if not found
    if not title or len(title) < 3:
        title = "교리 묵상"
    
    # Split sections
    catechism = ""
    catechism_title = "신앙고백서"
    exposition = ""
    questions = ""
    
    # 1. Extract Catechism section
    cat_pattern = r'(신앙고백서|대요리문답|소요리문답)\s*(\d+(?:\.\d+)?)?([\s\S]*?)(?=말씀요절|교리해설|$)'
    cat_match = re.search(cat_pattern, text, re.DOTALL)
    if cat_match:
        doc_type = cat_match.group(1)
        doc_num = cat_match.group(2) if cat_match.group(2) else ""
        catechism_title = f"{doc_type} {doc_num}".strip()
        catechism = cat_match.group(3).strip()
        # Clean up catechism text
        catechism = re.sub(r'^\s*\d+\)\s*', '', catechism)  # Remove footnote markers
        catechism = re.sub(r'\s+', ' ', catechism)  # Normalize whitespace
    
    # 2. Extract Exposition
    exp_pattern = r'교리해설\s*[\'"]?\s*([\s\S]*?)(?=적용질문|$)'
    exp_match = re.search(exp_pattern, text, re.DOTALL)
    if exp_match:
        exposition = exp_match.group(1).strip()
    
    # 3. Extract Questions
    q_pattern = r'적용질문\s*[\'"]?\s*([\s\S]*?)$'
    q_match = re.search(q_pattern, text, re.DOTALL)
    if q_match:
        questions = q_match.group(1).strip()
    
    return title, catechism_title, catechism, exposition, questions

def format_exposition(text):
    """Format exposition with proper paragraphs and lists"""
    # Split by double newline or numbered sections
    text = text.replace('\r', '')
    
    # First, identify numbered sections like (1), (2), (3) or "첫째", "둘째"
    # Split into sections
    sections = []
    
    # Pattern for numbered sections: (1) or 첫째, or 1., etc
    section_pattern = r'(\(\d+\)|[첫둘셋넷]째,?|\d+\.)'
    
    parts = re.split(f'({section_pattern})', text)
    
    formatted = ""
    current_text = ""
    
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
            
        # Check if this is a section marker
        if re.match(section_pattern, part):
            # Save previous accumulated text
            if current_text:
                # Format as paragraph
                current_text = current_text.strip()
                # Highlight quoted text
                current_text = re.sub(r'"([^"]+)"', r'<strong class="text-blue-600">\1</strong>', current_text)
                current_text = re.sub(r"'([^']+)'", r'<strong class="text-blue-600">\1</strong>', current_text)
                formatted += f'<p class="mb-4 text-gray-700 leading-relaxed">{current_text}</p>\n'
                current_text = ""
            
            # Start new section with marker
            current_text = f"<strong>{part}</strong> "
        else:
            current_text += part + " "
    
    # Add final accumulated text
    if current_text:
        current_text = current_text.strip()
        current_text = re.sub(r'"([^"]+)"', r'<strong class="text-blue-600">\1</strong>', current_text)
        current_text = re.sub(r"'([^']+)'", r'<strong class="text-blue-600">\1</strong>', current_text)
        formatted += f'<p class="mb-4 text-gray-700 leading-relaxed">{current_text}</p>\n'
    
    # If no formatting was applied (no sections found), just split by paragraphs
    if not formatted:
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        for p in paragraphs:
            p = re.sub(r'"([^"]+)"', r'<strong class="text-blue-600">\1</strong>', p)
            p = re.sub(r"'([^']+)'", r'<strong class="text-blue-600">\1</strong>', p)
            formatted += f'<p class="mb-4 text-gray-700 leading-relaxed">{p}</p>\n'
    
    return formatted

def format_questions(text):
    """Format questions as ordered list"""
    # Clean up the text
    text = text.replace('\r', '').strip()
    
    # Try to split by question numbers
    questions = []
    
    # Pattern: "1. ", "2. " etc at start of line
    parts = re.split(r'\n\s*\d+\.\s*', text)
    
    if len(parts) > 1:
        # First part might be empty or intro text
        for part in parts[1:]:  # Skip first empty part
            q = part.strip()
            if q:
                questions.append(q)
    else:
        # Try splitting by newlines and filter
        lines = text.split('\n')
        current_q = ""
        for line in lines:
            line = line.strip()
            if not line:
                if current_q:
                    questions.append(current_q)
                    current_q = ""
            else:
                # Remove leading numbers
                line = re.sub(r'^\d+\.\s*', '', line)
                if current_q:
                    current_q += " " + line
                else:
                    current_q = line
        if current_q:
            questions.append(current_q)
    
    # Format as HTML list
    if questions:
        formatted = '<ol class="list-decimal list-inside space-y-3 text-gray-700 leading-relaxed">\n'
        for q in questions:
            formatted += f'<li class="mb-2">{q}</li>\n'
        formatted += '</ol>'
    else:
        # Fallback: just wrap in paragraph
        formatted = f'<p class="text-gray-700 leading-relaxed">{text}</p>'
    
    return formatted

def generate_html(date_str, title, cat_title, cat_content, exposition, questions):
    month = int(date_str[:2])
    day = int(date_str[2:])
    formatted_date = f"{month}월 {day}일"
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{formatted_date} 교리 묵상</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
    <style>
        body {{ font-family: 'Pretendard', sans-serif; }}
    </style>
</head>
<body class="bg-gray-100 min-h-screen py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto space-y-8">
        <!-- Header -->
        <header class="text-center space-y-2">
            <h1 class="text-3xl font-bold text-gray-900">{formatted_date}</h1>
            <h2 class="text-xl font-semibold text-gray-700">{title}</h2>
        </header>

        <!-- Audio Player -->
        <div class="bg-white rounded-2xl shadow-lg p-6 space-y-4">
            <h3 class="text-lg font-bold text-gray-900">AI요약 듣기</h3>
            <div id="player-container" class="w-full">
                <div id="youtube-player"></div>
            </div>
            <div id="player-status" class="hidden text-center text-gray-500 py-4"></div>
            <button id="play-btn" disabled class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-xl transition-colors flex items-center justify-center gap-2" aria-label="교리 오디오 재생/일시정지">
                <span id="btn-text">로딩 중...</span>
            </button>
        </div>

        <!-- Catechism Section -->
        <div class="bg-white rounded-2xl shadow-lg p-6 space-y-4">
            <h3 class="text-lg font-bold text-indigo-900 border-b-2 border-indigo-100 pb-2">{cat_title}</h3>
            <div class="prose prose-indigo max-w-none text-gray-800 bg-indigo-50 p-4 rounded-lg">
                <p class="leading-relaxed">{cat_content}</p>
            </div>
        </div>

        <!-- Exposition Section -->
        <div class="bg-white rounded-2xl shadow-lg p-6 space-y-4">
            <h3 class="text-lg font-bold text-gray-900 border-b-2 border-gray-100 pb-2">교리 해설</h3>
            <div class="prose prose-blue max-w-none">
                {exposition}
            </div>
        </div>

        <!-- Application Questions -->
        <div class="bg-white rounded-2xl shadow-lg p-6 space-y-4">
            <h3 class="text-lg font-bold text-gray-900 border-b-2 border-gray-100 pb-2">적용 질문</h3>
            <div class="prose prose-green max-w-none bg-green-50 p-4 rounded-lg">
                {questions}
            </div>
        </div>

        <!-- Footer -->
        <footer class="text-center text-gray-500 text-sm py-4">
            <p>교재는 날마다 양식으로 읽는 웨스트민스터 표준교리(영음사)를 사용합니다</p>
        </footer>
    </div>

    <script>
        // Audio Player Logic
        const dateStr = "{date_str}";
        let player;
        let isReady = false;
        let videoId = null;

        async function initAudio() {{
            try {{
                const response = await fetch('../address/dcaddr.txt');
                if (!response.ok) throw new Error('Address file not found');
                const text = await response.text();
                
                // Parse file for today's video ID
                const lines = text.split('\\n');
                const todayLine = lines.find(line => line.startsWith(dateStr));
                
                if (!todayLine) {{
                    showError("오늘의 AI요약 음성은 아직 업로드 전입니다.");
                    return;
                }}

                // Extract Video ID (regex for youtube URLs)
                const urlMatch = todayLine.match(/(?:v=|\\/)([a-zA-Z0-9_-]{{11}})/);
                if (urlMatch && urlMatch[1]) {{
                    videoId = urlMatch[1];
                    loadYoutubeAPI();
                }} else {{
                    showError("오디오 주소를 찾을 수 없습니다.");
                }}
            }} catch (e) {{
                showError("오디오 정보를 불러오는 중 오류가 발생했습니다.");
                console.error(e);
            }}
        }}

        function showError(msg) {{
            const status = document.getElementById('player-status');
            const btn = document.getElementById('play-btn');
            status.textContent = msg;
            status.classList.remove('hidden');
            btn.classList.add('hidden');
        }}

        function loadYoutubeAPI() {{
            const tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            const firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        }}

        function onYouTubeIframeAPIReady() {{
            player = new YT.Player('youtube-player', {{
                height: '0',
                width: '0',
                videoId: videoId,
                playerVars: {{
                    'playsinline': 1,
                    'controls': 0
                }},
                events: {{
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }}
            }});
        }}

        function onPlayerReady(event) {{
            isReady = true;
            const btn = document.getElementById('play-btn');
            btn.disabled = false;
            document.getElementById('btn-text').textContent = '재생';
        }}

        function onPlayerStateChange(event) {{
            const btnText = document.getElementById('btn-text');
            if (event.data === YT.PlayerState.PLAYING) {{
                btnText.textContent = '일시정지';
            }} else {{
                btnText.textContent = '재생';
            }}
        }}

        document.getElementById('play-btn').addEventListener('click', () => {{
            if (!isReady) return;
            const state = player.getPlayerState();
            if (state === YT.PlayerState.PLAYING) {{
                player.pauseVideo();
            }} else {{
                player.playVideo();
            }}
        }});

        // Start initialization
        initAudio();
    </script>
</body>
</html>"""
    return html

def main():
    pdf = pdfium.PdfDocument(PDF_PATH)
    dates = sorted(DATE_PAGE_MAP.keys())
    
    for i, date_str in enumerate(dates):
        start_page = DATE_PAGE_MAP[date_str]
        # Determine end page
        if i < len(dates) - 1:
            end_page = DATE_PAGE_MAP[dates[i+1]]
        else:
            end_page = min(start_page + 5, len(pdf))
            
        print(f"Processing {date_str} (Pages {start_page}-{end_page})...")
        
        raw_text = extract_text_by_pages(pdf, start_page, end_page)
        cleaned_text = clean_text(raw_text)
        title, cat_title, cat_content, exposition, questions = parse_content(cleaned_text)
        
        # Fallback for title
        if not title or len(title) < 3:
            title = "교리 묵상"
        
        # Format content
        formatted_exp = format_exposition(exposition)
        formatted_q = format_questions(questions)
        
        html = generate_html(date_str, title, cat_title, cat_content, formatted_exp, formatted_q)
        
        filename = f"dc{date_str}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    
    print(f"\n✅ Successfully generated {len(dates)} catechism files!")
    print(f"Files: dc1116.html ~ dc1231.html")

if __name__ == "__main__":
    main()
