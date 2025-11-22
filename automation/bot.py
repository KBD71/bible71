import os
import datetime
import time
import json
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
YOUTUBE_PLAYLIST_URL = "https://youtube.com/playlist?list=PLfNjKaA2UoyqqPrAPu4skV75DJk_p5O5V&si=_4hLNKWMzGdijvHt"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROMPT_FILE = "automation/prompt.txt"
OUTPUT_DIR = "dailybible"

def setup_gemini():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=GEMINI_API_KEY)

def get_video_target_date(upload_date_str, video_title=""):
    """
    Determines the target date for the HTML file based on upload date and video title.
    
    Rules:
    1. Video title contains '금요기도회' -> Next day (Saturday)
    2. Friday upload (for Saturday morning service) -> +2 days (Sunday)
    3. Saturday video (not 금요기도회) -> Next day (Sunday)
    4. Others -> Same day
    """
    # Parse upload date (YYYYMMDD)
    date_obj = datetime.datetime.strptime(upload_date_str, "%Y%m%d")
    weekday = date_obj.weekday() # Mon=0, ..., Fri=4, Sat=5, Sun=6
    
    # Check if video title contains '금요기도회'
    is_friday_prayer = '금요기도회' in video_title
    
    if is_friday_prayer:
        target_date = date_obj + datetime.timedelta(days=1)
        print(f"Rule applied: 금요기도회 video -> Target next day ({target_date.strftime('%Y%m%d')})")
    elif weekday == 4:  # Friday upload (for Saturday morning)
        # Friday night uploads are for Saturday morning service
        # Saturday videos -> Sunday file
        target_date = date_obj + datetime.timedelta(days=2)
        print(f"Rule applied: Friday upload (Saturday service) -> Target Sunday ({target_date.strftime('%Y%m%d')})")
    elif weekday == 5: # Saturday upload
        target_date = date_obj + datetime.timedelta(days=1)
        print(f"Rule applied: Saturday video -> Target Sunday ({target_date.strftime('%Y%m%d')})")
    else:
        target_date = date_obj
        
    return target_date.strftime("%Y%m%d")

def get_latest_video_and_target_date():
    print("Checking for latest video...")
    
    # Get playlist entries
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-single-json",
        YOUTUBE_PLAYLIST_URL
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error fetching playlist: {result.stderr}")
        return None, None

    data = json.loads(result.stdout)
    entries = data.get('entries', [])

    if not entries:
        print("No videos found in playlist.")
        return None, None

    # Check the latest video
    latest_video = entries[-1]
    video_id = latest_video.get('id')
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Get detailed info including timestamp
    cmd_detail = [
        "yt-dlp",
        "--dump-json",
        video_url
    ]
    result_detail = subprocess.run(cmd_detail, capture_output=True, text=True)
    if result_detail.returncode != 0:
        print(f"Error fetching video details: {result_detail.stderr}")
        return None, None
        
    video_info = json.loads(result_detail.stdout)
    upload_date = video_info.get('upload_date')
    title = video_info.get('title')
    
    print(f"Latest video found: {title} (Uploaded: {upload_date})")
    
    target_date = get_video_target_date(upload_date, title)
    return video_info, target_date

def download_audio(video_url, output_path):
    print(f"Downloading audio from {video_url}...")
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", output_path,
        video_url
    ]
    subprocess.run(cmd, check=True)
    if not os.path.exists(output_path) and os.path.exists(output_path + ".mp3"):
        return output_path + ".mp3"
    return output_path

def generate_html(audio_path, video_id):
    print("Uploading audio to Gemini...")
    myfile = genai.upload_file(audio_path)
    print(f"File uploaded: {myfile.name}")

    # Wait for processing
    while myfile.state.name == "PROCESSING":
        print("Processing audio...")
        time.sleep(5)
        myfile = genai.get_file(myfile.name)

    if myfile.state.name == "FAILED":
        raise ValueError("Audio processing failed.")

    print("Generating content...")
    with open(PROMPT_FILE, "r") as f:
        prompt_text = f.read()

    full_prompt = f"{prompt_text}\n\n[Context Info]\nYouTube Video ID: {video_id}\n"

    model = genai.GenerativeModel("gemini-3-pro-preview")
    result = model.generate_content([myfile, full_prompt])
    
    return result.text

def save_html(content, date_str):
    if "```html" in content:
        content = content.split("```html")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
        
    filename = f"db{date_str[2:]}.html" # dbYYMMDD.html
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, "w") as f:
        f.write(content)
    
    print(f"Saved HTML to {filepath}")
    return filepath

def git_push(filepath):
    print("Pushing to GitHub...")
    subprocess.run(["git", "add", filepath], check=True)
    subprocess.run(["git", "commit", "-m", f"Add {os.path.basename(filepath)}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("Done!")

def check_and_create_placeholder(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist. Creating placeholder.")
        with open(filepath, "w") as f:
            f.write("<html><body><h1>아직 업로드 전입니다.</h1></body></html>")
        git_push(filepath)
        return True # Created placeholder
    return False # File exists

def is_placeholder(filepath):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r") as f:
        content = f.read()
    return "아직 업로드 전입니다." in content

def main():
    try:
        setup_gemini()
        
        # 1. Determine "Today" (Target Date for the file we want to create/update)
        today = datetime.datetime.now().strftime("%Y%m%d")
        weekday = datetime.datetime.now().weekday() # Mon=0, ..., Sat=5, Sun=6
        
        # On Saturday, we create Sunday's file (because Saturday videos -> Sunday date)
        # On other days, we create today's file
        if weekday == 5:  # Saturday
            target_date_obj = datetime.datetime.now() + datetime.timedelta(days=1)
            target_date = target_date_obj.strftime("%Y%m%d")
            print(f"Today is Saturday. Will create/update file for tomorrow (Sunday): {target_date}")
        else:
            target_date = today
            
        filename = f"db{target_date[2:]}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # 2. Check/Create Placeholder
        if check_and_create_placeholder(filepath):
            print(f"Created placeholder for {target_date}. Waiting for video...")
            
        # 3. If file exists but is NOT a placeholder, we are done.
        if not is_placeholder(filepath):
            print(f"File {filename} already exists and is not a placeholder. Skipping.")
            return

        print(f"Checking for video matching target date: {target_date}...")
        
        # 4. Find matching video
        # We need to look at recent videos and see if any of them map to our target_date
        
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--dump-single-json",
            YOUTUBE_PLAYLIST_URL
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error fetching playlist.")
            return

        data = json.loads(result.stdout)
        entries = data.get('entries', [])
        
        # Check first few entries (playlist is in reverse chronological order - newest first)
        target_video = None
        
        # Check first 5 videos
        for entry in entries[:5]: 
            video_id = entry.get('id')
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            cmd_detail = ["yt-dlp", "--dump-json", video_url]
            res_detail = subprocess.run(cmd_detail, capture_output=True, text=True)
            if res_detail.returncode != 0:
                continue
                
            info = json.loads(res_detail.stdout)
            upload_date = info.get('upload_date')
            title = info.get('title')
            
            calculated_target = get_video_target_date(upload_date, title)
            
            print(f"  Checking video: {title[:50]}... (upload: {upload_date}) -> target: {calculated_target}")
            
            if calculated_target == target_date:
                target_video = info
                break
        
        if not target_video:
            print(f"No video found that targets date {target_date}.")
            return

        print(f"Found matching video: {target_video.get('title')}")
        
        # 5. Generate and Overwrite
        video_id = target_video['id']
        video_url = target_video['webpage_url']
        
        audio_filename = "temp_audio"
        audio_path = download_audio(video_url, audio_filename)
        
        try:
            html_content = generate_html(audio_path, video_id)
            saved_path = save_html(html_content, target_date) # Save using target_date
            git_push(saved_path)
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
