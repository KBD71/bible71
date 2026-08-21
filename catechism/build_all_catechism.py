#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_all_catechism.py
dailycatechism의 365일치 콘텐츠를 bible71/catechism의 dcMMDD.html 포맷으로 일괄 변환 및 생성합니다.
"""

import os
import re
import json
import html

DAILY_CATECHISM_DIR = '/Users/kbd/Desktop/dailycatechism/content'
TARGET_DIR = '/Users/kbd/Desktop/bible71/catechism'

TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{month_num}월 {day_num}일: {title} | 날마다 읽는 교리</title>
    <!-- Pretendard Font & Tailwind CSS -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, "Helvetica Neue", "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
            background-color: #f8fafc;
        }}
        .keyword {{ box-shadow: inset 0 -0.5em 0 0 rgba(255, 255, 0, 0.3); font-weight: 700; }}
        .card {{ transition: transform 0.2s ease; }}
        .card:hover {{ transform: translateY(-2px); }}
        .keep-all {{ word-break: keep-all; }}
    </style>
</head>
<body class="text-slate-800 antialiased min-h-screen pb-16">

    <div class="max-w-3xl mx-auto px-4 py-8">
        <!-- 상단 헤더 -->
        <header class="bg-slate-900 text-white rounded-2xl p-6 md:p-8 mb-6 shadow-xl relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 opacity-60"></div>
            <div class="relative z-10">
                <div class="flex items-center space-x-2 text-blue-300 text-sm font-semibold tracking-wider uppercase mb-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                    <span>{confession}</span>
                </div>
                <h1 class="text-2xl md:text-3xl font-bold tracking-tight mb-3 keep-all">{title}</h1>
                <div class="text-xs md:text-sm text-slate-300 border-t border-slate-700/80 pt-3 flex flex-wrap items-center gap-x-4 gap-y-1">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-200 border border-blue-400/30">{month_num}월 {day_num}일</span>
                    {chapter_tag}
                    {source_tag}
                </div>
                {key_theme_box}
            </div>
        </header>

        <!-- 오디오 플레이어 섹션 -->
        <section class="bg-white rounded-2xl shadow-md border border-slate-100 p-6 mb-6">
            <h2 class="text-lg font-bold text-slate-800 mb-4 flex items-center justify-between">
                <span class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                    </svg>
                    오늘의 AI요약 듣기
                </span>
                <span class="text-xs font-medium text-slate-400">{month_num}월 {day_num}일 교리 해설</span>
            </h2>
            
            <div id="audio-player-container" class="w-full aspect-video bg-slate-900 rounded-xl flex items-center justify-center relative overflow-hidden hidden shadow-inner">
                <div id="player"></div>
            </div>

            <div id="audio-controls" class="mt-4 text-center">
                <div id="status-message" class="text-sm text-slate-500 mb-2 min-h-[20px]">오디오 정보를 확인하고 있습니다...</div>
                <button id="play-pause-btn" disabled class="w-full sm:w-auto px-6 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-200 disabled:text-slate-400 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-all shadow-sm flex items-center justify-center gap-2 mx-auto" aria-label="교리 오디오 재생/일시정지">
                    <svg id="play-icon" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                    <span id="btn-text">로딩 중...</span>
                </button>
            </div>
        </section>

        <!-- 본문 내용 (교리 문답, 참고 성경구절, 인포그래픽 카드, 적용 질문 등) -->
        {body_content}

        <!-- 푸터 -->
        <footer class="mt-12 text-center text-xs text-slate-400 border-t border-slate-200 pt-6">
            <p>교재는 날마다 양식으로 읽는 웨스트민스터 표준교리(지평서원)를 사용합니다</p>
        </footer>
    </div>

    <!-- JavaScript Logic (오디오 플레이어 및 YouTube IFrame API) -->
    <script>
        const DATE_KEY = "{mmdd}";
        const ADDRESS_FILE_URL = "../address/dcaddr.txt";

        const playBtn = document.getElementById('play-pause-btn');
        const btnText = document.getElementById('btn-text');
        const statusMessage = document.getElementById('status-message');
        const playerContainer = document.getElementById('audio-player-container');
        window.player = null;
        let videoId = null;
        let isPlayerReady = false;

        async function initAudioPlayer() {{
            try {{
                const response = await fetch(ADDRESS_FILE_URL);
                if (!response.ok) throw new Error('주소 파일을 불러올 수 없습니다.');
                
                const text = await response.text();
                const lines = text.split('\\n');
                
                const targetLine = lines.find(line => line.trim().startsWith(DATE_KEY));
                
                if (targetLine) {{
                    const match = targetLine.match(/(?:https?:\\/\\/)?(?:www\\.)?(?:youtube\\.com\\/watch\\?v=|youtu\\.be\\/)([a-zA-Z0-9_-]{{11}})/);
                    if (match && match[1]) {{
                        videoId = match[1];
                        loadYouTubeAPI();
                    }} else {{
                        handleAudioStatus("오디오 주소 형식이 올바르지 않습니다.", false);
                    }}
                }} else {{
                    handleAudioStatus("오늘의 AI요약 음성은 아직 업로드 전입니다.", false);
                }}
            }} catch (error) {{
                console.error("Audio Load Error:", error);
                handleAudioStatus("오디오 정보를 불러오는 중 오류가 발생했습니다.", false);
            }}
        }}

        function handleAudioStatus(msg, isAvailable) {{
            statusMessage.textContent = msg;
            if (!isAvailable) {{
                btnText.textContent = "음성 준비 중";
                playBtn.disabled = true;
                playBtn.classList.add('opacity-60', 'cursor-not-allowed');
            }} else {{
                statusMessage.textContent = "";
                btnText.textContent = "AI요약 듣기";
                playBtn.disabled = false;
            }}
        }}

        function loadYouTubeAPI() {{
            if (!window.YT) {{
                const tag = document.createElement('script');
                tag.src = "https://www.youtube.com/iframe_api";
                const firstScriptTag = document.getElementsByTagName('script')[0];
                firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
            }} else {{
                onYouTubeIframeAPIReady();
            }}
        }}

        window.onYouTubeIframeAPIReady = function() {{
            window.player = new YT.Player('player', {{
                height: '100%',
                width: '100%',
                videoId: videoId,
                playerVars: {{
                    'playsinline': 1,
                    'controls': 1,
                    'modestbranding': 1
                }},
                events: {{
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange,
                    'onError': onPlayerError
                }}
            }});
        }};

        function onPlayerReady(event) {{
            isPlayerReady = true;
            handleAudioStatus("", true);
        }}

        function onPlayerError(event) {{
            handleAudioStatus("오디오를 재생할 수 없습니다. (에러 코드: " + event.data + ")", false);
        }}

        function onPlayerStateChange(event) {{
            if (event.data === YT.PlayerState.PLAYING) {{
                btnText.textContent = "일시정지";
                playerContainer.classList.remove('hidden');
            }} else if (event.data === YT.PlayerState.PAUSED) {{
                btnText.textContent = "계속 듣기";
            }} else if (event.data === YT.PlayerState.ENDED) {{
                btnText.textContent = "다시 듣기";
            }}
        }}

        playBtn.addEventListener('click', () => {{
            if (!isPlayerReady || !window.player) return;

            const state = window.player.getPlayerState();
            if (playerContainer.classList.contains('hidden')) {{
                playerContainer.classList.remove('hidden');
                window.player.playVideo();
            }} else {{
                if (state === YT.PlayerState.PLAYING) {{
                    window.player.pauseVideo();
                }} else {{
                    window.player.playVideo();
                }}
            }}
        }});

        document.addEventListener('DOMContentLoaded', initAudioPlayer);
    </script>
</body>
</html>
"""

def extract_body(html_text):
    # Remove script and style tags
    text = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html_text, flags=re.IGNORECASE)
    text = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', text, flags=re.IGNORECASE)
    
    # Locate container inside body
    container_match = re.search(r'<body[^>]*>\s*<div class=\"max-w-3xl[^\"]*\"[^>]*>(.*?)</div>\s*</body>', text, re.DOTALL | re.IGNORECASE)
    if not container_match:
        container_match = re.search(r'<body[^>]*>\s*<div[^>]*>(.*?)</div>\s*</body>', text, re.DOTALL | re.IGNORECASE)
    if not container_match:
        container_match = re.search(r'<body[^>]*>(.*?)</body>', text, re.DOTALL | re.IGNORECASE)
    
    inner = container_match.group(1) if container_match else text
    
    # Remove header
    inner = re.sub(r'<header[^>]*>.*?</header>', '', inner, count=1, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove footer
    inner = re.sub(r'<footer[^>]*>.*?</footer>', '', inner, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up empty comments and trim
    inner = re.sub(r'<!--\s*(헤더|푸터)\s*-->', '', inner, flags=re.IGNORECASE)
    
    return inner.strip()

def build_all():
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    dates = sorted([d for d in os.listdir(DAILY_CATECHISM_DIR) if os.path.isdir(os.path.join(DAILY_CATECHISM_DIR, d)) and len(d) == 4 and d.isdigit()])
    print(f"Total dates found: {len(dates)}")
    
    count = 0
    for d in dates:
        p = os.path.join(DAILY_CATECHISM_DIR, d)
        meta_p = os.path.join(p, 'meta.json')
        if not os.path.exists(meta_p):
            print(f"Skipping {d}: No meta.json")
            continue
            
        with open(meta_p, 'r', encoding='utf-8') as f:
            meta = json.load(f)
            
        html_files = [f for f in os.listdir(p) if f.endswith('.html') and not f.startswith('infographic-embed')]
        if not html_files:
            print(f"Skipping {d}: No html file")
            continue
            
        with open(os.path.join(p, html_files[0]), 'r', encoding='utf-8') as f:
            raw_html = f.read()
            
        body_content = extract_body(raw_html)
        
        month_num = int(d[:2])
        day_num = int(d[2:])
        title = meta.get('title', '').strip()
        confession = meta.get('confession', '').strip() or '웨스트민스터 표준교리'
        chapter = meta.get('chapter', '').strip()
        source = meta.get('source', '').strip()
        key_theme = meta.get('keyTheme', '').strip()
        
        chapter_tag = f"<span>{chapter}</span>" if chapter else ""
        source_tag = f'<span class="text-slate-400">| {source}</span>' if source else ""
        
        if key_theme:
            key_theme_box = f"""<!-- 핵심 주제 박스 -->
                <div class="mt-5 bg-slate-800/90 border border-slate-700/80 rounded-xl p-4 text-sm md:text-base text-slate-200">
                    <span class="text-blue-400 font-bold block mb-1">핵심 주제</span>
                    <p class="keep-all leading-relaxed">{key_theme}</p>
                </div>"""
        else:
            key_theme_box = ""
            
        page_html = TEMPLATE.format(
            month_num=month_num,
            day_num=day_num,
            title=title,
            confession=confession,
            mmdd=d,
            chapter_tag=chapter_tag,
            source_tag=source_tag,
            key_theme_box=key_theme_box,
            body_content=body_content
        )
        
        target_filename = f"dc{d}.html"
        target_path = os.path.join(TARGET_DIR, target_filename)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
            
        count += 1
        if count % 50 == 0 or count == len(dates):
            print(f"Generated {count}/{len(dates)} files...")

    print(f"\nSuccessfully generated {count} catechism files in {TARGET_DIR}!")

if __name__ == '__main__':
    build_all()
