import yt_dlp
import os
import schedule
import time
import datetime
from generator import generate_sermon_html
from dotenv import load_dotenv

load_dotenv()

PLAYLIST_URL = "https://youtube.com/playlist?list=PLfNjKaA2UoyqqPrAPu4skV75DJk_p5O5V&si=I1gwGSEXmDOWP5Av"
DOWNLOAD_DIR = "downloads"
OUTPUT_DIR = "outputs"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_today_video():
    """
    Checks the playlist for a video uploaded 'today'.
    Note: 'today' determination depends on the video metadata upload_date.
    """
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    print(f"Checking for videos uploaded on {today_str}...")
    
    ydl_opts = {
        'extract_flat': True,  # Don't download yet, just get metadata
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(PLAYLIST_URL, download=False)
        if 'entries' in info:
            # Check the most recent entries (assuming playlist is ordered by date usually, but better to check top few)
            for entry in info['entries'][:5]: # check top 5
                 # yt-dlp flat extraction sometimes lacks upload_date, usually have to get full info for verification if needed
                 # But let's see if title contains date or if we can rely on playlist order.
                 # Actually, for accurate date, we might need to fetch detailed info for the specific video.
                 
                 # Optimization: Just check the very first one fully.
                 pass

    # Re-approach: Get full info for the first few items to check dates
    check_opts = {
        'quiet': True,
        'playlistend': 3, # Only check top 3
        'ignoreerrors': True,
    }
    
    found_video = None
    
    with yt_dlp.YoutubeDL(check_opts) as ydl:
        info = ydl.extract_info(PLAYLIST_URL, download=False)
        if 'entries' in info:
            for entry in info['entries']:
                if entry and entry.get('upload_date') == today_str:
                    print(f"Found video from today: {entry.get('title')} ({entry.get('id')})")
                    found_video = entry
                    break
    
    return found_video

def process_video(video_entry):
    video_id = video_entry['id']
    video_title = video_entry['title']
    upload_date = video_entry['upload_date']
    
    # Format a safe filename
    safe_title = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    output_filename = f"{upload_date}_{safe_title}.html"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    if os.path.exists(output_path):
        print(f"Output for {video_title} already exists. Skipping.")
        return

    print(f"Processing new video: {video_title}")
    
    # Download Audio
    audio_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
    
    if not os.path.exists(audio_path):
        ydl_opts = {
            'format': 'bestaudio/best',
            # ffmpeg is not available, so we skip conversion.
            # Gemini supports m4a, webm, etc.
            'outtmpl': os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s"),
            'quiet': False
        }
        
        print("Downloading audio...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
    
    # Verify file exists
    # we don't know the extension ahead of time now
    found_audio = None
    for f in os.listdir(DOWNLOAD_DIR):
        if f.startswith(video_id):
            found_audio = os.path.join(DOWNLOAD_DIR, f)
            break
            
    if not found_audio:
        print("Error: Audio file fetch failed.")
        return
    else:
        print(f"Audio downloaded to: {found_audio}")

    # Generate HTML
    print("Generating HTML using Gemini...")
    try:
        html_content = generate_sermon_html(found_audio, video_id)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"Successfully generated: {output_path}")
        
    except Exception as e:
        print(f"Error generating HTML: {e}")

def job():
    print(f"Running check job at {datetime.datetime.now()}")
    video = get_today_video()
    if video:
        process_video(video)
    else:
        print("No video found for today yet.")

if __name__ == "__main__":
    print("Starting Sermon Monitor...")
    # Run once immediately
    job()
    
    # Schedule to run every hour
    schedule.every(1).hours.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
