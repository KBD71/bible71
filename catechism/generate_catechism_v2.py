import pypdfium2 as pdfium
import re
import os
import random

# Date to Page mapping (PDF page numbers, 1-based)
# Covers Nov 1 to Dec 31
DATE_PAGE_MAP = {
    # November
    "1101": 10, "1102": 16, "1103": 22, "1104": 28, "1105": 34,
    "1106": 40, "1107": 46, "1108": 52, "1109": 58, "1110": 64,
    "1111": 70, "1112": 76, "1113": 82, "1114": 88, "1115": 94,
    "1116": 140, "1117": 146, "1118": 153, "1119": 159, "1120": 164,
    "1121": 169, "1122": 176, "1123": 184, "1124": 192, "1125": 199,
    "1126": 204, "1127": 211, "1128": 216, "1129": 224, "1130": 230,
    # December
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

# SVG Icons for cards
ICONS = [
    # Book/Scripture
    '<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>',
    # Lightbulb/Idea
    '<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>',
    # Shield/Defense
    '<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>',
    # Heart/Love
    '<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>',
    # Key/Unlock
    '<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" /></svg>'
]

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
    
    # Extract Title
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    title = ""
    for i, line in enumerate(lines[:10]):
        if re.match(r'^1[12]월', line) or re.match(r'---', line):
            continue
        if len(line) < 50 and (i < 5 or not title):
            clean_title = re.sub(r'^[f\.0,\s]+', '', line)
            clean_title = re.sub(r'[,\.]+\s*$', '', clean_title)
            if clean_title and len(clean_title) > 2:
                title = clean_title
                break
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
        catechism = re.sub(r'^\s*\d+\)\s*', '', catechism)
        catechism = re.sub(r'\s+', ' ', catechism)
    
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

def split_exposition_into_cards(exposition):
    """Split exposition text into topic cards"""
    cards = []
    
    # Common OCR fixes
    replacements = {
        "피 홀란": "피 흘리는",
        "올 ": "을 ",
        "그립자": "그림자",
        "이룰": "이를",
        "다움": "다음",
        "유익올": "유익을",
        "주어전": "주어진"
    }
    for old, new in replacements.items():
        exposition = exposition.replace(old, new)
    
    # Clean text
    exposition = exposition.replace('\r', '').strip()
    
    # Try to split by numbered lists (1. 2. or (1) (2) or 첫째, 둘째)
    # Improved regex to handle newlines and whitespace better
    split_pattern = r'(?:^|\n)\s*(?:\(?\d+\)|[첫둘셋넷]째,?|\d+\.)\s*'
    
    parts = re.split(split_pattern, exposition)
    
    # If we found splits
    if len(parts) > 1:
        # The first part might be intro text
        if parts[0].strip():
            cards.append({"title": "서론", "content": parts[0].strip()})
        
        for i, part in enumerate(parts[1:], 1):
            if not part.strip(): continue
            
            # Try to extract a title from the first sentence
            # Remove leading quotes/punctuation for title extraction
            clean_part = part.strip().lstrip('"\'“‘')
            sentences = re.split(r'[.!?]\s+', clean_part)
            first_sentence = sentences[0]
            
            # If first sentence is short (likely a title like "구약의 성례들은"), use it
            if len(first_sentence) < 40:
                title = first_sentence.strip().rstrip(':"\'”’')
                content = part[len(first_sentence):].strip().lstrip(':"\'”’')
                # If content is empty, the whole part was the title? Unlikely in this context.
                if not content: content = part
            else:
                title = f"핵심 주제 {i}"
                content = part
            
            # Clean content
            content = re.sub(r'"([^"]+)"', r'<strong class="text-blue-600">\1</strong>', content)
            content = re.sub(r"'([^']+)'", r'<strong class="text-blue-600">\1</strong>', content)
            content = re.sub(r'“([^”]+)”', r'<strong class="text-blue-600">\1</strong>', content)
            
            cards.append({"title": title, "content": content})
    else:
        # If no clear split, split by paragraphs and group them
        paragraphs = [p for p in exposition.split('\n') if p.strip()]
        
        # Merge short lines that might be broken sentences
        merged_paragraphs = []
        current_para = ""
        for p in paragraphs:
            if not current_para:
                current_para = p
            elif len(current_para) < 50 or not current_para.endswith(('.', '!', '?')):
                current_para += " " + p
            else:
                merged_paragraphs.append(current_para)
                current_para = p
        if current_para:
            merged_paragraphs.append(current_para)
            
        paragraphs = merged_paragraphs
        
        if len(paragraphs) <= 2:
            # Just one card
            content = "\n\n".join([f"<p>{p}</p>" for p in paragraphs])
            cards.append({"title": "교리 해설", "content": content})
        else:
            # Split into 2 cards
            mid = len(paragraphs) // 2
            
            content1 = "\n\n".join([f"<p>{p}</p>" for p in paragraphs[:mid]])
            cards.append({"title": "교리 해설 (1)", "content": content1})
            
            content2 = "\n\n".join([f"<p>{p}</p>" for p in paragraphs[mid:]])
            cards.append({"title": "교리 해설 (2)", "content": content2})
            
    return cards

def format_questions(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    formatted = '<ul class="list-decimal pl-5 space-y-3 text-gray-700">\n'
    for line in lines:
        line = re.sub(r'^\d+\.\s*', '', line)
        formatted += f'<li>{line}</li>\n'
    formatted += '</ul>'
    return formatted

def generate_html(date_str, title, cat_title, cat_content, exp_cards, questions):
    month = int(date_str[:2])
    day = int(date_str[2:])
    formatted_date = f"{month}월 {day}일"
    
    # Generate cards HTML
    cards_html = ""
    
    # 1. Catechism Card (Full width)
    cards_html += f"""
            <section class="infographic-card md:col-span-2">
                <div class="card-header">
                    <div class="card-icon">
                        {ICONS[0]}
                    </div>
                    <h2 class="card-title">{cat_title}</h2>
                </div>
                <div class="catechism-body">
                    <p>{cat_content}</p>
                </div>
            </section>
    """
    
    # 2. Exposition Cards
    for i, card in enumerate(exp_cards):
        icon = ICONS[(i + 1) % len(ICONS)]
        # Wrap content in p tags if not already
        content = card['content']
        if not content.startswith('<p>'):
            content = f"<p>{content}</p>"
        content = content.replace('\n\n', '</p><p>')
            
        cards_html += f"""
            <section class="infographic-card">
                <div class="card-header">
                    <div class="card-icon">
                        {icon}
                    </div>
                    <h2 class="card-title">{card['title']}</h2>
                </div>
                <div class="space-y-4 text-gray-600">
                    {content}
                </div>
            </section>
        """
        
    # 3. Questions Card (Full width)
    cards_html += f"""
            <section class="infographic-card md:col-span-2">
                <div class="card-header">
                    <div class="card-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.79 4 4s-1.79 4-4 4c-1.742 0-3.223-.835-3.772-2M12 12h.01M12 12a2 2 0 100 4 2 2 0 000-4z"/></svg>
                    </div>
                    <h2 class="card-title">적용 질문</h2>
                </div>
                {questions}
            </section>
    """

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{formatted_date}: {title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
    <style>
        body {{
            font-family: 'Pretendard', sans-serif;
            background-color: #f0f2f5;
            color: #1a202c;
        }}
        .infographic-card {{
            background-color: white;
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            padding: 2rem;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }}
        .infographic-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        }}
        .card-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        .card-icon {{
            flex-shrink: 0;
            width: 3rem;
            height: 3rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 9999px;
            background-color: #e0e7ff;
            color: #4338ca;
        }}
        .card-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e3a8a;
        }}
        .catechism-body {{
            color: #374151;
            padding-left: 1rem;
            border-left: 3px solid #6366f1;
            line-height: 1.7;
        }}
        .sub-heading {{
            font-weight: 700;
            color: #1e40af;
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
            font-size: 1.2rem;
        }}
        #player {{
            display: none;
        }}
    </style>
</head>
<body class="antialiased">

    <div class="container mx-auto p-4 md:p-8 max-w-3xl">

        <header class="text-center mb-12">
            <h1 class="text-4xl md:text-5xl font-extrabold text-gray-800 mb-2">{title}</h1>
            <p class="text-lg md:text-xl text-gray-500">{formatted_date}</p>
            <div class="mt-6 flex justify-center">
                <button id="audio-toggle" class="flex items-center justify-center px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300">
                    <svg id="play-icon" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <svg id="pause-icon" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span id="button-text">AI 요약</span>
                </button>
            </div>
        </header>

        <main class="grid grid-cols-1 md:grid-cols-2 gap-8">
            {cards_html}
        </main>
        
        <div id="player"></div>

        <footer class="text-center text-sm text-gray-500 mt-12 py-4 border-t">
            교재는 날마다 양식으로 읽는 웨스트민스터 표준교리(영음사)를 사용합니다.
        </footer>

    </div>

    <script>
        // YouTube IFrame Player API 비동기 로드
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        let player;
        let playerState;

        const audioToggleButton = document.getElementById('audio-toggle');
        const buttonText = document.getElementById('button-text');
        const playIcon = document.getElementById('play-icon');
        const pauseIcon = document.getElementById('pause-icon');

        function onYouTubeIframeAPIReady() {{
            // 플레이어는 버튼 클릭 시 생성
        }}

        function onPlayerReady(event) {{
            event.target.playVideo();
        }}

        function onPlayerStateChange(event) {{
            playerState = event.data;
            updateButtonUI(playerState);
        }}

        function updateButtonUI(state) {{
            if (state === YT.PlayerState.PLAYING) {{
                buttonText.textContent = '일시정지';
                playIcon.classList.add('hidden');
                pauseIcon.classList.remove('hidden');
            }} else {{
                buttonText.textContent = 'AI 요약';
                playIcon.classList.remove('hidden');
                pauseIcon.classList.add('hidden');
            }}
        }}
        
        function extractVideoID(url) {{
            const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{{11}})/;
            const match = url.match(regex);
            return match ? match[1] : null;
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            if (audioToggleButton) {{
                audioToggleButton.addEventListener('click', () => {{
                    if (player && (playerState === YT.PlayerState.PLAYING || playerState === YT.PlayerState.BUFFERING)) {{
                        player.pauseVideo();
                    }} 
                    else if (player && playerState === YT.PlayerState.PAUSED) {{
                        player.playVideo();
                    }} 
                    else {{
                        const audioFilePath = '../address/dcaddr.txt';

                        fetch(audioFilePath)
                            .then(response => {{
                                if (!response.ok) throw new Error('404');
                                return response.text();
                            }})
                            .then(fileContent => {{
                                if (!fileContent || fileContent.trim() === '') {{
                                    alert('유효한 오디오 주소가 파일에 없습니다.');
                                    return;
                                }}

                                const lines = fileContent.split('\\n');
                                const targetDate = '{date_str}';
                                let url = '';

                                for (const line of lines) {{
                                    if (line.trim().startsWith(targetDate + ' ')) {{
                                        url = line.trim().substring(5);
                                        break;
                                    }}
                                }}

                                if (!url) {{
                                    alert('해당 날짜의 오디오 주소를 찾을 수 없습니다.');
                                    return;
                                }}

                                const videoId = extractVideoID(url.trim());

                                if (!videoId) {{
                                    alert('유효한 YouTube URL이 아닙니다.');
                                    return;
                                }}

                                if (player) {{
                                    player.loadVideoById(videoId);
                                }} else {{
                                    player = new YT.Player('player', {{
                                        height: '0',
                                        width: '0',
                                        videoId: videoId,
                                        playerVars: {{
                                            'playsinline': 1
                                        }},
                                        events: {{
                                            'onReady': onPlayerReady,
                                            'onStateChange': onPlayerStateChange
                                        }}
                                    }});
                                }}
                            }})
                            .catch(error => {{
                                if (error.message === '404') {{
                                    alert('아직 업로드 전입니다.');
                                }} else {{
                                    console.error('오디오 파일 로드 중 오류 발생:', error);
                                }}
                            }});
                    }}
                }});
            }}
        }});
    </script>

</body>
</html>"""
    return html

def main():
    pdf = pdfium.PdfDocument(PDF_PATH)
    dates = sorted(DATE_PAGE_MAP.keys())
    
    for i, date_str in enumerate(dates):
        start_page = DATE_PAGE_MAP[date_str]
        if i < len(dates) - 1:
            end_page = DATE_PAGE_MAP[dates[i+1]]
        else:
            end_page = min(start_page + 5, len(pdf))
            
        print(f"Processing {date_str} (Pages {start_page}-{end_page})...")
        
        raw_text = extract_text_by_pages(pdf, start_page, end_page)
        cleaned_text = clean_text(raw_text)
        title, cat_title, catechism, exposition, questions = parse_content(cleaned_text)
        
        # Split exposition into cards
        exp_cards = split_exposition_into_cards(exposition)
        
        # Format questions
        formatted_questions = format_questions(questions)
        
        html = generate_html(date_str, title, cat_title, catechism, exp_cards, formatted_questions)
        
        filename = f"dc{date_str}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
    print(f"✅ Successfully generated {len(dates)} catechism files with card layout!")

if __name__ == "__main__":
    main()
