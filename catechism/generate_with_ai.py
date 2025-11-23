#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Daily Catechism Files with AI-summarized content
Using the style format from dc1110.html (Nov 10) as reference
"""

import pypdfium2 as pdfium
import re
import os
import anthropic

# Date to Page mapping
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

# Anthropic API 클라이언트 초기화
client = anthropic.Anthropic()

def extract_text_by_pages(pdf, start_page, end_page):
    text = ""
    for i in range(start_page - 1, min(end_page - 1, len(pdf))):
        text += pdf[i].get_textpage().get_text_range() + "\n"
    return text

def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if re.search(r'^\s*\d+\s*$', line): continue
        if re.search(r'^1[12]월\.\s+\d+[AB]?장\.', line): continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def parse_raw_content(text):
    """Extract title and raw catechism/exposition/questions from PDF text"""
    # Normalize section markers
    text = re.sub(r'신\s*앙\s*고\s*백\s*서', '신앙고백서', text)
    text = re.sub(r'대\s*요\s*리\s*문\s*답', '대요리문답', text)
    text = re.sub(r'소\s*요\s*리\s*문\s*답', '소요리문답', text)
    text = re.sub(r'교\s*리\s*해\s*설', '교리해설', text)
    text = re.sub(r'적\s*용\s*질\s*문', '적용질문', text)
    
    # Extract title
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
    
    # Extract sections
    catechism = ""
    catechism_title = "신앙고백서"
    exposition = ""
    questions = ""
    
    cat_pattern = r'(신앙고백서|대요리문답|소요리문답)\s*(\d+(?:\.\d+)?)?([\s\S]*?)(?=말씀요절|교리해설|$)'
    cat_match = re.search(cat_pattern, text)
    if cat_match:
        doc_type = cat_match.group(1)
        doc_num = cat_match.group(2) if cat_match.group(2) else ""
        catechism_title = f"{doc_type} {doc_num}".strip()
        catechism = cat_match.group(3).strip()
        catechism = re.sub(r'^\s*\d+\)\s*', '', catechism)
        catechism = re.sub(r'\s+', ' ', catechism)
    
    exp_pattern = r'교리해설\s*[\'"]?\s*([\s\S]*?)(?=적용질문|$)'
    exp_match = re.search(exp_pattern, text)
    if exp_match:
        exposition = exp_match.group(1).strip()
    
    q_pattern = r'적용질문\s*[\'"]?\s*([\s\S]*?)$'
    q_match = re.search(q_pattern, text)
    if q_match:
        questions = q_match.group(1).strip()
    
    return title, catechism_title, catechism, exposition, questions

def summarize_with_ai(catechism, exposition, catechism_title):
    """Use Claude API to summarize and restructure the content with OCR correction and theological review"""
    
    prompt = f"""당신은 개혁주의 신학 전문가입니다. 아래 웨스트민스터 신앙고백서/문답 교리 내용을 분석하여 처리해주세요.

**원본 신앙고백서/문답:**
{catechism}

**원본 교리 해설:**
{exposition}

**요구사항:**

1. **OCR 오류 수정**: 
   - 텍스트에 OCR 오류가 있을 수 있습니다 (예: "올" → "을", "홀란" → "흘리는" 등)
   - 문맥을 고려하여 오타와 오류를 수정하세요
   - 개혁신학 용어의 정확성을 확인하세요

2. **개혁신학적 검토**:
   - 내용이 웨스트민스터 신앙고백서/대소요리문답의 정통 개혁신학과 일치하는지 확인
   - 언약신학, 선택론, 성화론 등의 교리가 정확한지 점검
   - 필요시 신학적으로 더 명확하게 표현

3. **핵심 주제 중심 재구성**:
   - 교리 해설을 2-4개의 핵심 주제로 재구성
   - 각 주제는 `<h3>` 태그로 제목 작성 (예: `<h3>1. 성례의 본질</h3>`)
   - 원문을 있는 그대로 옮기지 말고, 핵심을 명확히 정리하여 재서술

4. **강조 표시**:
   - 핵심 신학 용어나 중요 표현은 `<strong class="text-blue-600"></strong>`로 강조
   - 성경 인용구는 따옴표와 함께 강조

5. **가독성**:
   - 각 문단은 `<p>` 태그로 감싸기
   - 불필요한 마커(', " 등)나 OCR 잔여물 제거
   - 자연스러운 한국어 문장으로 다듬기

**출력 형식** (HTML 코드만, 다른 설명 없이):
<h3>1. [첫 번째 핵심 주제]</h3>
<p>[상세한 설명... <strong class="text-blue-600">핵심 용어</strong> 등]</p>

<h3>2. [두 번째 핵심 주제]</h3>
<p>[상세한 설명...]</p>

[필요시 3-4번째 주제도 동일 형식]"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content[0].text.strip()
    except Exception as e:
        print(f"  ⚠ AI 요약 실패: {e}")
        # Fallback: basic formatting with OCR fix attempts
        cleaned = exposition.replace("올 ", "을 ").replace("홀란", "흘리는")
        return f"<p>{cleaned[:1000]}...</p>"

def generate_html_file(date_str, title, cat_title, catechism, summarized_exposition, questions):
    """Generate HTML file with the new styled format"""
    month = int(date_str[:2])
    day = int(date_str[2:])
    
    # Format questions
    questions_lines = [q.strip() for q in questions.split('\n') if q.strip()]
    questions_html = ""
    for i, q in enumerate(questions_lines[:6], 1):  # Max 6 questions
        q = re.sub(r'^\d+\.\s*', '', q)
        questions_html += f'<li><span class="question">{q}</span></li>\n'
    
    if not questions_html:
        questions_html = '<li><span class="question">적용 질문이 제공되지 않았습니다.</span></li>'
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>날마다 읽는 교리 - {month}월 {day}일</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" as="style" crossorigin="anonymous" />
    <style>
        body {{
            font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            word-break: keep-all;
            background-color: #f3f4f6;
        }}
        .card {{
            background-color: white;
            border-radius: 0.75rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
            overflow: hidden;
        }}
        .card-header {{
            background-color: #4a5568;
            color: white;
            padding: 1rem 1.5rem;
            font-size: 1.25rem;
            font-weight: 700;
            border-bottom: 1px solid #e5e7eb;
        }}
        .card-body {{
            padding: 1.5rem;
            line-height: 1.75;
        }}
        .card-body h3 {{
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: #1f2937;
        }}
        .card-body p {{
            margin-bottom: 1rem;
            color: #374151;
        }}
        .card-body ul {{
            list-style-type: disc;
            margin-left: 1.5rem;
            margin-bottom: 1rem;
            color: #374151;
        }}
        .card-body li {{
            margin-bottom: 0.5rem;
        }}
        .card-body .question {{
            font-weight: 600;
            color: #111827;
        }}
        .card-body .answer {{
            color: #374151;
        }}
        .audio-player-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
            background-color: #f9fafb;
            border-top: 1px solid #e5e7eb;
        }}
        .audio-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 500;
            border-radius: 0.5rem;
            transition: all 0.2s ease-in-out;
            border: 1px solid transparent;
        }}
        .audio-button:disabled {{
            background-color: #e5e7eb;
            color: #9ca3af;
            cursor: not-allowed;
        }}
        .audio-button.play {{
            background-color: #2563eb;
            color: white;
        }}
        .audio-button.play:hover {{
            background-color: #1d4ed8;
        }}
        .audio-button.pause {{
            background-color: #f87171;
            color: white;
        }}
        .audio-button.pause:hover {{
            background-color: #ef4444;
        }}
        .audio-error {{
            color: #dc2626;
            font-weight: 500;
            text-align: center;
        }}
        #player-container {{
            width: 1px;
            height: 1px;
            opacity: 0;
            position: absolute;
            top: -100px;
            left: -100px;
        }}
        footer {{
            text-align: center;
            padding: 2rem 1rem;
            font-size: 0.875rem;
            color: #6b7280;
        }}
    </style>
</head>
<body class="bg-gray-100">

    <div class="container mx-auto max-w-3xl px-4 py-8 sm:py-12">

        <header class="mb-8 text-center">
            <h1 class="text-4xl font-bold text-gray-800">{month}월 {day}일</h1>
            <p class="text-xl text-gray-600 mt-2">{title}</p>
        </header>

        <main>
            <div class="card">
                <div class="card-header">
                    {cat_title}
                </div>
                <div class="card-body">
                    <p class="answer">{catechism}</p>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    AI요약 듣기
                </div>
                <div class="audio-player-container" id="audio-player-ui">
                    <div id="player-container"></div>
                    <button id="audio-button" class="audio-button play" aria-label="교리 오디오 재생" disabled>
                        <svg id="play-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6 mr-2">
                            <path fill-rule="evenodd" d="M4.5 5.653c0-1.427 1.529-2.33 2.779-1.643l11.54 6.347c1.295.712 1.295 2.573 0 3.286L7.28 19.99c-1.25.687-2.779-.217-2.779-1.643V5.653Z" clip-rule="evenodd" />
                        </svg>
                        <svg id="pause-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6 mr-2" style="display: none;">
                            <path fill-rule="evenodd" d="M6.75 5.25a.75.75 0 0 1 .75-.75H9a.75.75 0 0 1 .75.75v13.5a.75.75 0 0 1-.75.75H7.5a.75.75 0 0 1-.75-.75V5.25Zm7.5 0a.75.75 0 0 1 .75-.75h1.5a.75.75 0 0 1 .75.75v13.5a.75.75 0 0 1-.75.75H15a.75.75 0 0 1-.75-.75V5.25Z" clip-rule="evenodd" />
                        </svg>
                        <span id="button-text">로딩 중...</span>
                    </button>
                    <div id="audio-error" class="audio-error mt-4" style="display: none;"></div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    교리 해설
                </div>
                <div class="card-body">
                    {summarized_exposition}
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    적용 질문
                </div>
                <div class="card-body">
                    <ul>
                        {questions_html}
                    </ul>
                </div>
            </div>
        </main>

        <footer>
            <p>교재는 날마다 양식으로 읽는 웨스트민스터 표준교리(영음사)를 사용합니다</p>
        </footer>

    </div>

    <script>
        let player;
        let videoId = null;
        let isPlayerReady = false;
        let isPlaying = false;
        const audioButton = document.getElementById('audio-button');
        const buttonText = document.getElementById('button-text');
        const playIcon = document.getElementById('play-icon');
        const pauseIcon = document.getElementById('pause-icon');
        const errorContainer = document.getElementById('audio-error');

        function loadYouTubeAPI() {{
            const tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            const firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        }}

        function onYouTubeIframeAPIReady() {{
            fetchAudioAddress();
        }}

        async function fetchAudioAddress() {{
            try {{
                const response = await fetch('../address/dcaddr.txt');
                if (!response.ok) {{
                    throw new Error('오디오 목록 파일을 불러오는 데 실패했습니다.');
                }}
                const text = await response.text();
                const lines = text.split('\\n');
                const today = '{date_str}';
                const todayLine = lines.find(line => line.startsWith(today));

                if (todayLine) {{
                    const regex = /(?:v=|youtu\\.be\\/)([a-zA-Z0-9_-]{{11}})/;
                    const match = todayLine.match(regex);
                    if (match && match[1]) {{
                        videoId = match[1];
                        initializePlayer();
                    }} else {{
                        throw new Error('오늘 날짜의 오디오 주소 형식이 올바르지 않습니다.');
                    }}
                }} else {{
                    showError('오늘의 AI요약 음성은 아직 업로드 전입니다.');
                }}
            }} catch (error) {{
                console.error('Error fetching audio address:', error);
                showError(error.message || '오디오를 불러오는 중 오류가 발생했습니다.');
            }}
        }}

        function initializePlayer() {{
            player = new YT.Player('player-container', {{
                height: '1',
                width: '1',
                videoId: videoId,
                playerVars: {{
                    'playsinline': 1,
                    'controls': 0,
                  'showinfo': 0,
                    'rel': 0
                }},
                events: {{
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }}
            }});
        }}

        function onPlayerReady(event) {{
            isPlayerReady = true;
            audioButton.disabled = false;
            buttonText.textContent = 'AI요약 듣기';
            audioButton.setAttribute('aria-label', '교리 오디오 재생');
            audioButton.addEventListener('click', togglePlayPause);
        }}

        function onPlayerStateChange(event) {{
            if (event.data === YT.PlayerState.PLAYING) {{
                isPlaying = true;
                updateButtonUI(true);
            }} else if (event.data === YT.PlayerState.PAUSED || event.data === YT.PlayerState.ENDED) {{
                isPlaying = false;
                updateButtonUI(false);
                if (event.data === YT.PlayerState.ENDED) {{
                    player.seekTo(0);
                }}
            }}
        }}

        function togglePlayPause() {{
            if (!isPlayerReady) return;
            if (isPlaying) {{
                player.pauseVideo();
            }} else {{
                player.playVideo();
            }}
        }}

        function updateButtonUI(playing) {{
            if (playing) {{
                audioButton.classList.remove('play');
                audioButton.classList.add('pause');
                playIcon.style.display = 'none';
                pauseIcon.style.display = 'inline';
                buttonText.textContent = '일시정지';
                audioButton.setAttribute('aria-label', '교리 오디오 일시정지');
            }} else {{
                audioButton.classList.remove('pause');
                audioButton.classList.add('play');
                playIcon.style.display = 'inline';
                pauseIcon.style.display = 'none';
                buttonText.textContent = 'AI요약 듣기';
                audioButton.setAttribute('aria-label', '교리 오디오 재생');
            }}
        }}

        function showError(message) {{
            const button = document.getElementById('audio-button');
            if (button) {{
                button.style.display = 'none';
            }}
            errorContainer.textContent = message;
            errorContainer.style.display = 'block';
        }}

        loadYouTubeAPI();
    </script>

</body>
</html>"""
    
    return html

def main():
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("경고: ANTHROPIC_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("AI 요약 없이 기본 포맷팅만 적용합니다.")
        use_ai = False
    else:
        use_ai = True
        print("AI 요약 기능 활성화됨")
    
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
        title, cat_title, catechism, exposition, questions = parse_raw_content(cleaned_text)
        
        if not title:
            title = "교리 묵상"
        
        # AI summarization
        if use_ai and exposition:
            try:
                summarized_exposition = summarize_with_ai(catechism, exposition, cat_title)
            except Exception as e:
                print(f"  AI 요약 실패 ({date_str}): {e}")
                summarized_exposition = f"<p>{exposition[:800]}...</p>"
        else:
            summarized_exposition = f"<p>{exposition[:800]}...</p>"
        
        html = generate_html_file(date_str, title, cat_title, catechism, summarized_exposition, questions)
        
        filename = f"dc{date_str}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✓ Generated {filename}")
    
    print(f"\n✅ Successfully generated {len(dates)} catechism files with AI summaries!")

if __name__ == "__main__":
    main()
