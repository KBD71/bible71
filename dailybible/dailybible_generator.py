#!/usr/bin/env python3
"""
Daily Bible Sermon Auto-Summarizer & Page Generator
Automates fetching sermon videos, transcribing them, summarizing using Gemini API,
and generating styled HTML files compatible with the PWA calendar.
"""

import os
import re
import sys
import json
import argparse
import requests
from datetime import datetime
from google.generativeai import GenerativeModel
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Constants
DEFAULT_PLAYLIST_ID = "PLfNjKaA2UoyrAm9vu3nty1kgDPpzG5-p0"
TEMPLATE_PATH = "dailybible/dailybible_template.html"
OUTPUT_DIR = "dailybible"

def parse_args():
    parser = argparse.ArgumentParser(description="Automate Daily Bible page generation.")
    parser.add_argument("--url", help="Direct YouTube video URL or 11-char ID.")
    parser.add_argument("--date", help="Sermon date in YYMMDD format. If omitted, extracted from title or defaults to today.")
    parser.add_argument("--auto", action="store_true", help="Auto-scrape Pilgrim Church playlist and generate missing pages.")
    parser.add_argument("--limit", type=int, default=5, help="Number of playlist items to check in auto mode.")
    return parser.parse_args()

def get_youtube_id(url_or_id):
    """Extracts the 11-character video ID from a YouTube URL or returns the ID directly."""
    if len(url_or_id) == 11:
        return url_or_id
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url_or_id)
    return match.group(1) if match else None

def extract_date_from_title(title, default_date=None):
    """Extracts date in YYMMDD format from sermon title. E.g. '2026.05.22' or '26.05.22' or '260522' or '5월 22일'."""
    # Attempt YYYY.MM.DD or YY.MM.DD or YYMMDD
    patterns = [
        r'(\d{4}|\d{2})[.-](\d{1,2})[.-](\d{1,2})',  # 2026.05.22 or 26.05.22
        r'(\d{2})(\d{2})(\d{2})',                    # 260522
        r'(\d{1,2})월\s*(\d{1,2})일',                 # 5월 22일 (uses current year's YY)
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                yy_str = groups[0][-2:] # Support both 4-digit and 2-digit years
                yy, mm, dd = int(yy_str), int(groups[1]), int(groups[2])
                return f"{yy:02d}{mm:02d}{dd:02d}"
            elif len(groups) == 2:
                # MM월 DD일 -> prefix with current year YY (e.g. 26)
                current_year_yy = datetime.now().strftime("%y")
                mm, dd = int(groups[0]), int(groups[1])
                return f"{current_year_yy}{mm:02d}{dd:02d}"
                
    if default_date:
        return default_date
    return datetime.now().strftime("%y%m%d")

def get_playlist_videos(playlist_id, api_key, limit=5):
    """Fetches the latest videos from the YouTube playlist using the API."""
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        'part': 'snippet,contentDetails',
        'playlistId': playlist_id,
        'key': api_key,
        'maxResults': limit
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching YouTube playlist: {e}")
        return None

def fetch_transcript(video_id):
    """Fetches the Korean transcript of the YouTube video."""
    try:
        print(f"Fetching transcript for video ID: {video_id}...")
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['ko'])
        full_text = " ".join([item['text'] for item in transcript_list])
        return full_text
    except Exception as e:
        print(f"Failed to fetch standard transcript: {e}")
        # Try fetching auto-generated transcript as fallback
        try:
            print("Attempting to fetch generated transcripts...")
            transcript_list = YouTubeTranscriptApi().list(video_id)
            transcript = transcript_list.find_generated_transcript(['ko'])
            full_text = " ".join([item['text'] for item in transcript.fetch()])
            return full_text
        except Exception as ex:
            print(f"Failed to fetch any transcript for video {video_id}: {ex}")
            return None

def fetch_sermon_metadata_from_youtube(video_id, api_key):
    """Fetches title and description of a YouTube video."""
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'snippet',
        'id': video_id,
        'key': api_key
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            snippet = data['items'][0]['snippet']
            return snippet.get('title'), snippet.get('description')
    except Exception as e:
        print(f"Error fetching YouTube video metadata: {e}")
    return None, None

def query_gemini_summarization(transcript, title_context, description_context):
    """Sends the transcript to Gemini API to generate the structured Reformed theology summary in JSON."""
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)
        
    genai.configure(api_key=gemini_key)
    
    # Define a clean system instruction for the model
    system_instruction = (
        "당신은 장로교 및 개혁주의(Reformed/Presbyterian) 신학을 전공한 탁월한 개혁주의 신학자이자 목회자입니다. "
        "당신의 사명은 성경 본문과 설교 녹취록(Transcript)을 바탕으로, 역사적 웨스트민스터 표준문서와 언약신학(Covenant Theology), "
        "그리고 주권적 구속사(Redemptive-Historical) 관점에 일치하는 정교하고 은혜로운 설교 요약 문서를 작성하는 것입니다. "
        "존 칼빈과 개혁주의 신학자들의 가르침에 부합하도록 문장 하나하나를 품위 있고 은혜로운 경어체(하십시오체)로 작성하십시오."
    )
    
    prompt = f"""
아래 설교 자료(유튜브 제목, 본문 설명, 그리고 녹취록)를 분석하여 깊이 있는 개혁주의 설교 요약을 생성해 주십시오.

[설교 정보]
유튜브 제목: {title_context}
영상 본문 설명: {description_context}

[녹취록 텍스트]
{transcript}

---
[요구사항 및 출력 스키마]
반드시 다음 스키마를 따르는 순수한 JSON 형식으로만 응답해 주십시오. 마크다운 백틱(```json) 없이 온전한 JSON 문자열만 출력해 주십시오.

스키마의 각 필드 상세 설명:
1. "title": 설교 전체를 관통하는 핵심적인 주제를 은혜롭게 압축한 한글 설교 제목 (예: "하나님의 풍성한 환대와 소생하게 하시는 은혜")
2. "metadata_title": 대괄호 본문 구절과 부제를 결합한 메타데이터 제목 (예: "[창45:16-28] 하나님의 풍성한 환대와 소생하게 하시는 은혜 (주권적 은혜와 복음의 가시적 보증)")
3. "description": 전체 설교 요약의 메타 설명문 (2~3문장, SNS 공유용으로 적합하게)
4. "series": "창세기 강해 시리즈", "출애굽기 강해 시리즈" 처럼 본문에서 파악된 설교 시리즈명
5. "scripture_ref": 본문 구절 (예: "창세기 45장 16-28절")
6. "date_string": 한국어로 표현된 날짜 (예: "2026년 5월 22일 금요일")
7. "core_theme": 이 설교 전체의 핵심적인 영적 진리와 구속사적 의미를 2~3문장으로 요약한 핵심 주제 단락.
8. "scripture_html": 설교 본문 구절의 '개역개정' 본문 구절들 전체를 HTML로 출력하십시오. 각 구절은 다음 형식이어야 합니다:
   "<p><strong>구절번호</strong> 구절 텍스트</p>"
   (예: "<p><strong>16</strong> 요셉의 형들이 왔다는 소문이 바로의 궁에 들리매 바로와 그의 신하들이 기뻐하고</p>")
   반드시 정확한 개역개정 본문 텍스트를 사용하여 구절 전체를 빠짐없이 HTML 단락들로 완성해 주십시오.
9. "principle_title": 1. 원리/본질 섹션의 소제목 (예: "죄의 열매를 선으로 덮으시는 하나님의 주권적 구속사")
10. "principle_html": 하나님의 주권적 구속사와 언약적 신실함, 그리스도와의 연합 원리를 자세히 설명하는 은혜로운 설명 단락(2~3개 <p> 단락)을 HTML로 작성하십시오. 강조하고 싶은 핵심 개념은 반드시 <span class="keyword">핵심개념</span> 태그를 두르고 중요한 단어는 <strong>강조</strong> 처리하십시오.
11. "history_title": 2. 역사/배경 섹션의 소제목 (예: "아낌없이 공급하시는 바로의 왕권적 환대와 수레의 도원")
12. "history_html": 설교 본문의 구약/신약 역사적 배경, 문화적 상징성, 지리적 또는 언어적 맥락에 대해 풍성하게 설명하는 설명문 및 그리드 형식의 HTML 요소를 포함하여 작성하십시오.
13. "warning_title": 3. 경고/배격 섹션의 소제목 (예: "길 위의 손가락질과 율법주의적 정죄의 습성")
14. "warning_html": 신자가 경계해야 할 율법주의(Legalism), 방종주의(Antinomianism), 세속주의 또는 책임 전가 등 영적 낙심이나 사탄의 참소에 관한 엄중한 개혁주의적 경고 단락을 HTML로 작성하십시오.
15. "application_title": 4. 적용/목적 섹션의 소제목 (예: "은혜의 '가시적 수레'를 보고 기력을 소생하기")
16. "application_html": 신자의 삶 속에서 말씀이 어떻게 구체화되고 적용되는지, 눈에 보이지 않는 은혜의 약속을 예배와 성례(Sacraments), 일상의 가시적인 증표들을 통해 묵상하고 힘을 얻는 원리를 설명하는 단락을 HTML로 작성하십시오.
17. "conclusion_title": 5. 결론 섹션 소제목 (예: '"족하도다!"의 신앙과 영원히 살아계신 그리스도 예표')
18. "conclusion_html": 설교 전체를 완벽하게 요약하고 성도의 마땅한 의무와 순종, 부활하사 천지 만물을 먹이시는 참된 요셉이신 예수 그리스도를 대망하는 내용을 담은 결론 단락을 HTML로 작성하십시오.

[중요 디자인 가이드라인]
- HTML 내용 안에는 마크다운 기호를 쓰지 마십시오.
- 핵심 신학 용어(예: 주권적 은혜, 그리스도와의 연합, 구속사적 성취, 언약 등)는 `<span class="keyword">단어</span>` 태그로 감싸주십시오. 이 태그는 노란색 형광펜 효과 스타일을 가집니다.
- 글의 흐름을 좋게 하기 위해 적절히 글머리 기호(`<ul class="list-disc list-inside space-y-2"><li>...</li></ul>`)나 카드/블록인용문(`<blockquote class="border-l-4 border-purple-300 pl-4 py-1 italic text-slate-600">...</blockquote>`)을 삽입하여 고급스럽게 레이아웃 하십시오.
- 수식 표기가 필요할 경우 MathJax 문법(예: $$ 공식 $$)을 삽입하십시오.

출력 JSON 형식 예시:
{{
  "title": "...",
  "metadata_title": "...",
  "description": "...",
  "series": "...",
  "scripture_ref": "...",
  "date_string": "...",
  "core_theme": "...",
  "scripture_html": "<p><strong>16</strong> ...</p><p><strong>17</strong> ...</p>",
  "principle_title": "...",
  "principle_html": "<p>...</p>",
  "history_title": "...",
  "history_html": "<p>...</p>",
  "warning_title": "...",
  "warning_html": "<p>...</p>",
  "application_title": "...",
  "application_html": "<p>...</p>",
  "conclusion_title": "...",
  "conclusion_html": "<p>...</p>"
}}
"""
    
    print("Calling Gemini API to generate Reformed sermon summary...")
    model = GenerativeModel('gemini-3-flash-preview')
    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.2
        }
    )
    
    try:
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(f"Error parsing JSON from Gemini: {e}")
        print(f"Raw Gemini response was:\n{response.text}")
        return None

def generate_html_page(sermon_data, video_id, date_yymmdd):
    """Renders the HTML page using the template and the compiled sermon JSON data."""
    if not os.path.exists(TEMPLATE_PATH):
        print(f"ERROR: Template file not found at {TEMPLATE_PATH}")
        return False
        
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()
        
    # Replace all placeholders in the template
    placeholders = {
        "{{ METADATA_TITLE }}": sermon_data.get("metadata_title", ""),
        "{{ TITLE }}": sermon_data.get("title", ""),
        "{{ DESCRIPTION }}": sermon_data.get("description", ""),
        "{{ IMAGE }}": sermon_data.get("image", "https://drive.google.com/uc?export=view&id=1HWEyIUmIRa4TEXBUDMpDi--PC8DtitXJ"),
        "{{ SERIES }}": sermon_data.get("series", "새벽기도회 강해"),
        "{{ SCRIPTURE_REF }}": sermon_data.get("scripture_ref", ""),
        "{{ DATE_STRING }}": sermon_data.get("date_string", ""),
        "{{ CORE_THEME }}": sermon_data.get("core_theme", ""),
        "{{ SCRIPTURE_HTML }}": sermon_data.get("scripture_html", ""),
        
        "{{ PRINCIPLE_TITLE }}": sermon_data.get("principle_title", "원리/본질"),
        "{{ PRINCIPLE_HTML }}": sermon_data.get("principle_html", ""),
        
        "{{ HISTORY_TITLE }}": sermon_data.get("history_title", "역사/배경"),
        "{{ HISTORY_HTML }}": sermon_data.get("history_html", ""),
        
        "{{ WARNING_TITLE }}": sermon_data.get("warning_title", "경고/배격"),
        "{{ WARNING_HTML }}": sermon_data.get("warning_html", ""),
        
        "{{ APPLICATION_TITLE }}": sermon_data.get("application_title", "적용/목적"),
        "{{ APPLICATION_HTML }}": sermon_data.get("application_html", ""),
        
        "{{ CONCLUSION_TITLE }}": sermon_data.get("conclusion_title", "결론/책임"),
        "{{ CONCLUSION_HTML }}": sermon_data.get("conclusion_html", ""),
        
        "{{ YOUTUBE_ID }}": video_id
    }
    
    rendered = template
    for placeholder, val in placeholders.items():
        rendered = rendered.replace(placeholder, val)
        
    # Ensure dailybible directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output_filename = f"db{date_yymmdd}.html"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
        
    print(f"SUCCESS: Generated {output_path}!")
    return True

def process_single_video(video_id, date_yymmdd, api_key):
    """Processes a single video: fetches title/description, transcript, queries Gemini, and creates the page."""
    print(f"\nProcessing YouTube Video {video_id} for date {date_yymmdd}...")
    
    # 1. Fetch transcript
    transcript = fetch_transcript(video_id)
    if not transcript:
        print(f"Skipping video {video_id} because no transcript could be retrieved.")
        return False
        
    # 2. Fetch video title and description as context for Gemini
    title, description = fetch_sermon_metadata_from_youtube(video_id, api_key)
    if not title:
        title = "새벽기도회 설교"
        description = ""
    print(f"Video Title: {title}")
    
    # Adjust target date based on intelligent rules
    from datetime import timedelta
    adjusted_yymmdd = date_yymmdd
    adjusted_date_str = None
    try:
        dt = datetime.strptime(date_yymmdd, "%y%m%d")
        is_friday_prayer = "금요기도회" in title
        is_saturday_morning_prayer = "새벽기도회" in title and dt.weekday() == 5  # Saturday
        
        if is_friday_prayer or is_saturday_morning_prayer:
            adjusted_dt = dt + timedelta(days=1)
            adjusted_yymmdd = adjusted_dt.strftime("%y%m%d")
            weekdays_ko = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
            adjusted_date_str = f"{adjusted_dt.year}년 {adjusted_dt.month}월 {adjusted_dt.day}일 {weekdays_ko[adjusted_dt.weekday()]}"
            print(f"Intelligent date shift: {date_yymmdd} -> {adjusted_yymmdd} (+1 day, mapped to {weekdays_ko[adjusted_dt.weekday()]})")
    except Exception as e:
        print(f"Warning: Failed to parse/adjust date: {e}")
    
    # 3. Query Gemini for structured Reformed theological summary
    sermon_data = query_gemini_summarization(transcript, title, description)
    if not sermon_data:
        print("Failed to get structured summary from Gemini.")
        return False
        
    # Override date string in data if adjusted
    if adjusted_date_str:
        sermon_data["date_string"] = adjusted_date_str
        
    # 4. Generate the PWA HTML page
    return generate_html_page(sermon_data, video_id, adjusted_yymmdd)

def main():
    args = parse_args()
    api_key = os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        print("WARNING: YOUTUBE_API_KEY environment variable is not set. Scraper and video details might fail.")
    
    if args.auto:
        # Auto mode: Scrape playlist and generate missing pages
        if not api_key:
            print("ERROR: YOUTUBE_API_KEY is required for auto mode.")
            sys.exit(1)
            
        print(f"Starting auto-mode. Checking latest {args.limit} videos in playlist {DEFAULT_PLAYLIST_ID}...")
        playlist_data = get_playlist_videos(DEFAULT_PLAYLIST_ID, api_key, limit=args.limit)
        if not playlist_data or 'items' not in playlist_data:
            print("Could not retrieve playlist videos. Exiting.")
            sys.exit(1)
            
        generated_count = 0
        for item in playlist_data['items']:
            snippet = item['snippet']
            title = snippet['title']
            video_id = None
            if 'resourceId' in snippet and 'videoId' in snippet['resourceId']:
                video_id = snippet['resourceId']['videoId']
            
            if not video_id:
                continue
                
            # Extract base date from title
            base_date_yymmdd = extract_date_from_title(title)
            
            # Adjust target date based on intelligent rules for duplicate checking
            date_yymmdd = base_date_yymmdd
            try:
                dt = datetime.strptime(base_date_yymmdd, "%y%m%d")
                is_friday_prayer = "금요기도회" in title
                is_saturday_morning_prayer = "새벽기도회" in title and dt.weekday() == 5  # Saturday
                
                if is_friday_prayer or is_saturday_morning_prayer:
                    from datetime import timedelta
                    adjusted_dt = dt + timedelta(days=1)
                    date_yymmdd = adjusted_dt.strftime("%y%m%d")
                    print(f"Auto-mode Intelligent date shift: {base_date_yymmdd} -> {date_yymmdd} for title: {title}")
            except Exception as e:
                print(f"Warning: Failed to parse/adjust date in auto-mode: {e}")
                
            output_file = os.path.join(OUTPUT_DIR, f"db{date_yymmdd}.html")
            
            # Check if file already exists
            if os.path.exists(output_file):
                print(f"Page already exists for {date_yymmdd} ({output_file}). Skipping.")
                continue
                
            # Process video and generate page
            success = process_single_video(video_id, base_date_yymmdd, api_key)
            if success:
                generated_count += 1
                
        print(f"\nAuto mode completed. Generated {generated_count} new sermon pages.")
        
    elif args.url:
        # Manual mode: Process single URL or video ID
        video_id = get_youtube_id(args.url)
        if not video_id:
            print(f"ERROR: Invalid YouTube URL or Video ID: {args.url}")
            sys.exit(1)
            
        # Determine date
        if args.date:
            date_yymmdd = args.date
        else:
            # Try to fetch title to extract date
            title, _ = fetch_sermon_metadata_from_youtube(video_id, api_key)
            if title:
                date_yymmdd = extract_date_from_title(title)
            else:
                date_yymmdd = datetime.now().strftime("%y%m%d")
                print(f"Could not retrieve video title. Defaulting to today's date: {date_yymmdd}")
                
        success = process_single_video(video_id, date_yymmdd, api_key)
        if not success:
            sys.exit(1)
            
    else:
        print("ERROR: Must provide either --url [YOUTUBE_URL] or --auto flag.")
        sys.exit(1)

if __name__ == "__main__":
    main()
