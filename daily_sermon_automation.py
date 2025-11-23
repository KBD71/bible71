import os
import sys
import re
import time
import json
import glob
import requests
import google.generativeai as genai
from datetime import datetime, timedelta
import yt_dlp

# Configuration
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
PLAYLIST_ID = "PLfNjKaA2UoyqguyGXZMV1yFgewV3cFXO-"
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
DAILY_BIBLE_DIR = os.path.join(REPO_ROOT, "dailybible")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_kst_now():
    # Returns current time in KST
    return datetime.utcnow() + timedelta(hours=9)

def get_target_files(kst_now):
    """
    Determine which files to check based on the day of the week.
    Returns a list of tuples: (target_file_path, search_date_obj, search_keyword)
    """
    weekday = kst_now.weekday() # 0=Mon, 6=Sun
    targets = []

    # Format: dbYYMMDD.html
    today_str = kst_now.strftime("%y%m%d")
    today_file = os.path.join(DAILY_BIBLE_DIR, f"db{today_str}.html")
    
    # Logic
    if 0 <= weekday <= 3: # Mon(0) - Thu(3)
        # Check today's file for "Dawn Prayer"
        targets.append({
            "file": today_file,
            "search_date": kst_now,
            "keyword": "새벽기도회",
            "upload_date_match": True # Must be uploaded recently
        })
    elif weekday == 4: # Fri(4)
        # No work on Friday
        pass
    elif weekday == 5: # Sat(5)
        # 1. Check Saturday file (for Friday Prayer)
        # Note: The user said "db(토요일).html" gets "금요기도회" (Friday Prayer)
        # Friday was yesterday
        friday_date = kst_now - timedelta(days=1)
        sat_file_str = kst_now.strftime("%y%m%d") # db(Sat).html
        sat_file = os.path.join(DAILY_BIBLE_DIR, f"db{sat_file_str}.html")
        
        targets.append({
            "file": sat_file,
            "search_date": friday_date, # Look for video from Friday
            "keyword": "금요기도회",
            "upload_date_match": False # Might have been uploaded yesterday
        })

        # 2. Check Sunday file (for Saturday Dawn Prayer)
        # Sunday is tomorrow
        sunday_date = kst_now + timedelta(days=1)
        sun_file_str = sunday_date.strftime("%y%m%d") # db(Sun).html
        sun_file = os.path.join(DAILY_BIBLE_DIR, f"db{sun_file_str}.html")

        targets.append({
            "file": sun_file,
            "search_date": kst_now, # Look for video from Today (Saturday)
            "keyword": "새벽기도회",
            "upload_date_match": True
        })
    
    return targets

def check_file_needs_update(file_path):
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "아직 업로드 전입니다" in content:
                return True
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return False

def search_youtube_video(search_date, keyword, upload_date_match=True):
    """
    Search for a video in the playlist matching the date and keyword.
    search_date: datetime object of the expected video date (from title).
    """
    if not YOUTUBE_API_KEY:
        print("Error: YOUTUBE_API_KEY not set.")
        return None

    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        'part': 'snippet,contentDetails',
        'playlistId': PLAYLIST_ID,
        'key': YOUTUBE_API_KEY,
        'maxResults': 20, # Check last 20 videos
        'order': 'date' # This parameter is actually for 'search' endpoint, playlistItems returns in position order usually, but let's try.
        # Actually playlistItems doesn't support 'order'. It returns by position.
        # We assume new videos are at the top (or bottom depending on playlist setting).
        # Usually recently added are at the top (position 0) if sorted by date descending.
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        target_month = search_date.month
        target_day = search_date.day
        
        print(f"Searching for video: Date={target_month}/{target_day}, Keyword={keyword}")

        for item in data.get('items', []):
            snippet = item['snippet']
            title = snippet['title']
            published_at = snippet['publishedAt'] # e.g., 2023-11-23T20:00:00Z
            
            # Check keyword
            if keyword not in title:
                continue
            
            # Check Date in Title
            # Regex for MM.DD, MM/DD, MM-DD, M월 D일
            # Also handle "23.11.23" (YY.MM.DD) - ignore YY if it looks like last year but uploaded recently?
            # User said: "오타 보정: 영상 날짜가 작년으로 잘못 기입되어 있어도 올해로 인식"
            
            # Extract numbers
            # Look for patterns like "11.23", "11/23", "11월 23일"
            date_match = re.search(r'(\d{1,2})[./-](\d{1,2})', title)
            if not date_match:
                date_match = re.search(r'(\d{1,2})월\s*(\d{1,2})일', title)
            
            if date_match:
                m = int(date_match.group(1))
                d = int(date_match.group(2))
                
                if m == target_month and d == target_day:
                    # Found a match!
                    video_id = snippet['resourceId']['videoId']
                    print(f"Found matching video: {title} ({video_id})")
                    return {
                        'id': video_id,
                        'title': title,
                        'published_at': published_at
                    }
            
    except Exception as e:
        print(f"YouTube API Error: {e}")
        
    return None

def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_path = f"temp_audio_{video_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find the file (yt-dlp might add extension)
        files = glob.glob(f"{output_path}*")
        if files:
            return files[0]
    except Exception as e:
        print(f"Download Error: {e}")
    
    return None

def generate_html_content(audio_path, video_info):
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set.")
        return None

    print("Uploading audio to Gemini...")
    myfile = genai.upload_file(audio_path)
    print(f"{myfile=}")

    model = genai.GenerativeModel("gemini-3-pro-preview")
    
    prompt = f"""
    당신은 개혁신학적 관점을 가진 전문 설교 요약가이자 웹 개발자입니다.
    다음 설교 오디오를 분석하여, 아래 요구사항에 맞춰 완벽한 HTML 코드를 작성해주세요.

    **설교 정보:**
    - 제목: {video_info['title']}
    - YouTube Video ID: {video_info['id']}

    **요구사항:**
    1. **신학적 분석:** 개혁신학적 관점에서 설교의 핵심을 깊이 있게 파악하세요.
    2. **디자인:** Tailwind CSS를 사용하여 모바일 친화적이고 세련된 카드 뉴스 형태의 디자인을 적용하세요. (CDN 링크 포함)
    3. **구조:**
       - **헤더:** 설교 제목, 설교자(목사님 이름 추출), 본문 말씀, 날짜.
       - **YouTube 플레이어:** Iframe API를 사용하여 상단에 배치. (ID: {video_info['id']})
       - **핵심 주제:** 한 문장으로 요약.
       - **상세 요약:** 문단별로 나누어 깊이 있는 내용 정리.
       - **적용 및 기도:** 삶에 적용할 점과 기도문.
    4. **출력:** 오직 HTML 코드만 출력하세요. (마크다운 코드 블록 없이 순수 HTML)
    5. **스타일:**
       - 폰트: Google Fonts (Noto Sans KR 등) 사용.
       - 색상: 차분하고 신뢰감을 주는 톤 (Blue, Gray, White 등).
       - 반응형: 모바일에서 완벽하게 보이도록.

    **HTML 템플릿 가이드 (참고용, 자유롭게 개선 가능):**
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>{video_info['title']} - 설교 요약</title>
    </head>
    <body class="bg-gray-100 font-sans antialiased">
        <!-- Content Here -->
    </body>
    </html>
    """

    print("Generating content with Gemini...")
    result = model.generate_content([myfile, prompt])
    
    # Cleanup
    # myfile.delete() # Not strictly necessary for free tier but good practice? API might not support delete on file object directly in some versions.
    
    return result.text

def clean_html_output(text):
    # Remove markdown code blocks if present
    text = re.sub(r'^```html', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```', '', text, flags=re.MULTILINE)
    return text.strip()

def main():
    print("Starting Daily Sermon Automation...")
    
    # Retry logic parameters
    max_retries = 10 # 5 hours / 30 mins = 10 retries
    retry_interval = 1800 # 30 minutes in seconds
    
    # For testing/dev, reduce retry
    if os.environ.get("TEST_MODE"):
        max_retries = 1
        retry_interval = 10

    for attempt in range(max_retries):
        kst_now = get_kst_now()
        print(f"Attempt {attempt+1}/{max_retries} at {kst_now}")
        
        targets = get_target_files(kst_now)
        
        if not targets:
            print("No targets for today.")
            break
            
        all_done = True
        
        for target in targets:
            file_path = target['file']
            search_date = target['search_date']
            keyword = target['keyword']
            
            print(f"Checking target: {os.path.basename(file_path)}")
            
            if check_file_needs_update(file_path):
                print(f"Update needed for {os.path.basename(file_path)}")
                all_done = False # Found at least one pending task
                
                # Search YouTube
                video_info = search_youtube_video(search_date, keyword)
                
                if video_info:
                    print(f"Video found! Processing...")
                    
                    # Download Audio
                    audio_file = download_audio(video_info['id'])
                    
                    if audio_file:
                        # Generate HTML
                        html_content = generate_html_content(audio_file, video_info)
                        
                        if html_content:
                            clean_html = clean_html_output(html_content)
                            
                            # Save to file
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(clean_html)
                            
                            print(f"Successfully updated {file_path}")
                            
                            # Cleanup audio
                            os.remove(audio_file)
                        else:
                            print("Failed to generate HTML content.")
                    else:
                        print("Failed to download audio.")
                else:
                    print("Video not found yet.")
            else:
                print(f"No update needed for {os.path.basename(file_path)} (Already done or not created)")
        
        if all_done:
            print("All tasks completed for today.")
            break
        
        if attempt < max_retries - 1:
            print(f"Waiting {retry_interval} seconds before next check...")
            time.sleep(retry_interval)
        else:
            print("Max retries reached. Exiting.")

if __name__ == "__main__":
    main()
