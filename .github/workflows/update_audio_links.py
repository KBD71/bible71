#!/usr/bin/env python3
"""
YouTube 플레이리스트에서 새 영상을 확인하고 dcaddr.txt에 추가하는 스크립트
"""

import os
import re
import requests
from datetime import datetime
import sys

def get_playlist_videos(playlist_id, api_key):
    """YouTube API를 사용해 플레이리스트의 영상 목록을 가져옵니다."""
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        'part': 'snippet',
        'playlistId': playlist_id,
        'key': api_key,
        'maxResults': 50,  # 최근 50개 영상
        'order': 'date'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"YouTube API 요청 실패: {e}")
        return None

def extract_date_from_title(title):
    """영상 제목에서 날짜를 추출합니다 (MMDD 형식)."""
    # 다양한 날짜 형식을 시도해봅니다
    patterns = [
        r'(\d{1,2})/(\d{1,2})',  # MM/DD or M/D
        r'(\d{1,2})\.(\d{1,2})',  # MM.DD or M.D
        r'(\d{1,2})-(\d{1,2})',  # MM-DD or M-D
        r'(\d{2})(\d{2})',       # MMDD
        r'(\d{1,2})월\s*(\d{1,2})일',  # M월 D일
    ]

    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))

            # 유효한 날짜인지 확인
            if 1 <= month <= 12 and 1 <= day <= 31:
                return f"{month:02d}{day:02d}"

    return None

def read_existing_links(file_path):
    """기존 dcaddr.txt 파일에서 이미 있는 날짜들을 읽습니다."""
    existing_dates = set()

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ' ' in line:
                        date_part = line.split(' ')[0]
                        if len(date_part) == 4 and date_part.isdigit():
                            existing_dates.add(date_part)
        except Exception as e:
            print(f"기존 파일 읽기 실패: {e}")

    return existing_dates

def append_new_link(file_path, date, video_url):
    """새로운 링크를 dcaddr.txt 파일에 추가합니다."""
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{date} {video_url}\n")
        print(f"새 링크 추가됨: {date} {video_url}")
        return True
    except Exception as e:
        print(f"파일 쓰기 실패: {e}")
        return False

def main():
    # 환경변수에서 YouTube API 키 가져오기
    api_key = os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        print("ERROR: YOUTUBE_API_KEY 환경변수가 설정되지 않았습니다.")
        sys.exit(1)

    # 플레이리스트 ID 추출
    playlist_url = "https://youtube.com/playlist?list=PLfNjKaA2UoyqguyGXZMV1yFgewV3cFXO-&si=av6jRFRZLqI6PUR7"
    playlist_id = "PLfNjKaA2UoyqguyGXZMV1yFgewV3cFXO-"

    # dcaddr.txt 파일 경로
    dcaddr_file = "address/dcaddr.txt"

    # 기존 링크 읽기
    existing_dates = read_existing_links(dcaddr_file)
    print(f"기존에 있는 날짜들: {existing_dates}")

    # YouTube API로 플레이리스트 영상 가져오기
    playlist_data = get_playlist_videos(playlist_id, api_key)
    if not playlist_data:
        print("플레이리스트 데이터를 가져올 수 없습니다.")
        sys.exit(1)

    new_links_added = 0

    # 각 영상에 대해 처리
    for item in playlist_data.get('items', []):
        snippet = item['snippet']
        title = snippet['title']
        video_id = snippet['resourceId']['videoId']
        video_url = f"https://youtu.be/{video_id}"

        # 제목에서 날짜 추출
        date = extract_date_from_title(title)
        if not date:
            print(f"날짜를 추출할 수 없음: {title}")
            continue

        # 이미 존재하는 날짜인지 확인
        if date in existing_dates:
            print(f"이미 존재하는 날짜: {date}")
            continue

        # 새 링크 추가
        if append_new_link(dcaddr_file, date, video_url):
            existing_dates.add(date)
            new_links_added += 1
            print(f"새 영상 추가: {title} -> {date}")

    print(f"총 {new_links_added}개의 새 링크가 추가되었습니다.")

    # GitHub Actions에서 사용할 수 있도록 출력 설정
    if new_links_added > 0:
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write(f"new_links_added={new_links_added}\n")

if __name__ == "__main__":
    main()