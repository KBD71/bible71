import os
import google.generativeai as genai
from googleapiclient.discovery import build
from youtube_transcript_api import get_transcript as youtube_get_transcript
from datetime import datetime, timedelta

# --- 설정 (사용자 정의) ---
YOUTUBE_PLAYLIST_ID = "PLfNjKaA2UoyqqPrAPu4skV75DJk_p5O5V"
OUTPUT_DIR = "dailybible"
STATE_FILE = "last_video_id.txt"
# -------------------------

# GitHub Secrets에서 API 키 가져오기
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

if not GEMINI_API_KEY or not YOUTUBE_API_KEY:
    raise ValueError("API 키가 설정되지 않았습니다. GitHub Secrets를 확인하세요.")

# Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest') # 긴 텍스트 처리를 위해 1.5 Pro 사용

def get_last_processed_video_id():
    """마지막으로 처리한 영상 ID를 파일에서 읽어옵니다."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return f.read().strip()
    return None

def set_last_processed_video_id(video_id):
    """처리한 영상 ID를 파일에 저장합니다."""
    with open(STATE_FILE, 'w') as f:
        f.write(video_id)

def get_latest_video_from_playlist(playlist_id):
    """재생목록에서 가장 최근 영상을 가져옵니다."""
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id,
        maxResults=1
    )
    response = request.execute()
    if not response['items']:
        return None
    return response['items'][0]

def get_transcript(video_id):
    """유튜브 영상의 스크립트(자막)를 가져옵니다."""
    try:
        # 라이브러리 함수 호출 방식을 직접적이고 명확하게 변경
        transcript_list = youtube_get_transcript(video_id, languages=['ko'])
        return " ".join([item['text'] for item in transcript_list])
    except Exception as e:
        # 예외 발생 시 더 상세한 오류 메시지를 출력하도록 개선
        import traceback
        print(f"스크립트를 가져올 수 없습니다: {e}")
        traceback.print_exc()
        return None

def generate_html_content(transcript, video_info):
    """Gemini API를 호출하여 HTML 콘텐츠를 생성합니다."""

    # 사용자로부터 받은 프롬프트를 여기에 그대로 삽입합니다.
    # f-string을 사용하여 동적으로 영상 정보를 전달합니다.
    prompt_template = f"""
[기본 임무] 당신은 제공된 유튜브 설교 영상을 분석하여, 개혁신학적으로 깊이 있고 웹 프-레임워크 환경에서도 완벽하게 렌더링되는 인포그래픽 형태의 학습 자료를 생성하는 전문 콘텐츠 제작자입니다. 당신의 임무는 설교의 논리적 핵심뿐만 아니라 감성적 뉘앙스까지 완벽하게 파악하여, 아래의 모든 지침에 따라 상세하고 가독성 높은 단일 HTML 파일을 생성하는 것입니다.

[입력 데이터]
- 설교 영상 제목: {video_info['title']}
- 설교자: (영상 정보에 설교자 정보가 명확하지 않으므로 '설교자 정보 확인 필요' 또는 채널명으로 대체)
- 설교 날짜: {video_info['published_at']}
- 설교 스크립트 전문:
---
{transcript}
---

[지침]
1. 설교 내용 심층 분석 및 구조화

전체 분석 및 기본 정보 확정: 설교 전체를 시청하여, 설교의 공식적인 제목, 설교자, 설교 본문(성경 구절), 설교 날짜를 정확히 파악하여 HTML의 <header> 섹션에 배치할 내용을 확정합니다.
[중요] 설교 본문 전문 확보: 위 단계에서 확정된 설교 본문의 성경 본문 전체를 절(verse) 단위로 빠짐없이 확보합니다. 이 텍스트는 HTML 생성 시 가장 먼저 배치될 핵심 콘텐츠입니다.
핵심 주제 정의: 설교의 가장 핵심적인 주제를 한 문장으로 요약하여 <p class="text-2xl ..."> 태그의 내용으로 삼습니다.
논리적 흐름에 따른 모든 중요 주제 도출: 설교의 서론, 본론, 결론에 해당하는 논리적 흐름을 완벽히 파악하고, 본론에서 다루는 모든 중요 논점, 핵심 주장, 주요 구분점들을 빠짐없이 도출합니다. 각 주제는 하나의 <div class="card"> 섹션이 됩니다.
전문가의 관점으로 내용 상세화 및 재구성:
보고 형식 절대 금지: '설교자는 ~라고 말합니다'와 같은 표현을 절대 사용하지 마십시오. 설교 내용을 완전히 당신의 것으로 소화하여, 해당 주제의 전문가로서 직접 설명하는 방식으로 내용을 재구성해야 합니다.
완전한 상세화: 각 장의 내용을 단순 요약하지 말고, 설교자가 제시한 핵심 개념의 정의, 신학적 중요성, 성경적 근거, 역사적 배경(예: 종교개혁), 그리고 구체적인 적용점 등을 모두 포함하여 매우 상세하고 풍성하게 서술합니다.
주요 예화 및 비유의 역할 분석: 설교에 사용된 핵심 예화나 비유는 단순히 내용을 전달하는 것을 넘어, 그것이 어떤 신학적 논점을 뒷받침하고 청중의 이해와 감성적 연결을 어떻게 돕는지를 명확히 서술합니다.
핵심 성경 구절 인용 및 연결: 설교자가 신학적 주장의 핵심 근거로 제시하는 성경 구절은 반드시 그 본문을 직접 인용합니다. 인용된 구절이 어떻게 해당 주장을 뒷받침하는지 명확하게 설명해야 합니다. 본문은 <blockquote> 태그로, 성경 출처는 그 안의 <cite> 태그로 감싸 시각적으로 구분되도록 제시합니다.
2. 인포그래픽 HTML 구조 및 디자인 (매우 중요)

[최우선 원칙] Tailwind CSS 클래스 직접 적용: <style> 태그에 h1, p 등 태그 전체에 적용되는 스타일을 정의할 경우, Tailwind CSS 프레임워크와 충돌하여 스타일이 적용되지 않을 수 있습니다. 따라서 모든 스타일링은 Tailwind CSS 유틸리티 클래스를 해당 HTML 태그에 직접 class="..." 형태로 적용하는 것을 원칙으로 합니다. 특히 <h1> 제목은 class="text-4xl md:text-5xl font-black ..."와 같이 직접 스타일을 지정하여 명확하게 렌더링되도록 합니다.
[최우선 작업] 설교 본문(개역개정) 전체 삽입:
<header> 태그 바로 뒤, 그리고 분석 내용이 시작되는 <main> 태그 바로 앞에, 설교 본문 전체를 담는 별도의 섹션(예: <div class="scripture-text-section">)을 반드시 생성해야 합니다.
이 섹션에는 "설교 본문" 이라는 제목(<h2>)과 함께, 1단계에서 확보한 성경 본문 전체가 모든 절이 하나도 빠짐없이, 절 번호와 함께 명확하게 표시되어야 합니다.
이는 분석 내용 요약 카드(card)들보다 반드시 먼저 위치해야 하는 절대적인 요구사항입니다.
CSS 스타일링 기술 지침:
반응형 디자인 강화 (모바일 가독성): 카드(.card) 섹션은 화면 폭이 400px 이하인 모바일 환경에서 아이콘과 텍스트가 **세로로 쌓이는 구조(flex-direction: column)**로 변경되어야 합니다. 미디어 쿼리(@media (max-width: 400px))를 사용하여 스타일을 조정하십시오.
웹 접근성 준수 (Color Contrast): 모든 텍스트와 배경색의 조합은 WCAG 2.1 AA 레벨 이상의 명도 대비를 충족해야 합니다. <span class="keyword">의 스타일 지정 시, 가독성을 위해 배경색을 제거하고 텍스트 색상만으로 강조하는 것을 원칙으로 합니다.
동적 아이콘 선택 및 적용: 각 카드 섹션의 내용을 분석한 후, '아이콘 라이브러리'에서 가장 적합한 아이콘을 선택하여 적용합니다.
시각적 강조: 설교의 핵심 신학 용어 및 반복적으로 강조되는 중요 개념은 <span class="keyword"> 태그로 감싸 시각적으로 강조합니다.
3. 오디오 플레이어 기능 구현 (매우 중요)

'설교 듣기' 버튼(id="listen-btn")과 보이지 않는 플레이어(id="hidden-player-container")를 생성합니다.
초기 상태는 "로딩 중..."이며 비활성화 상태여야 합니다.
플레이어가 준비되면(onReady), 버튼을 활성화하고 재생 상태로 아이콘/텍스트를 변경합니다.
버튼 클릭 시 재생/일시정지를 토글하고, 플레이어의 실제 상태 변화(onStateChange)에 따라 버튼의 UI가 정확하게 동기화되어야 합니다.
4. 콘텐츠 생성 원칙 및 자기 검증

절대적 완전성: 설교에서 중요하게 언급된 개념, 인물, 사건, 성경 구절, 적용점 등은 절대 누락해서는 안 됩니다.
목록 처리 특별 지침: 설교자가 명시적으로 تعداد을 언급하며 나열하는 항목 (예: "3가지 이유")이 있다면, 반드시 <ol> 태그를 사용하여 모든 항목을 정확한 개수로 포함시켜야 합니다.
최종 자기 검증: HTML 코드 생성을 완료하기 직전, 아래 항목들을 순서대로 반드시 확인하십시오.
[최우선 검증] 설교 본문 전체 수록 여부: <header>와 <main> 사이에 설교 본문 전체가 절 단위로 빠짐없이 수록되었는지 가장 먼저 확인합니다. 이 항목은 절대 누락될 수 없습니다.
[스타일 적용 검증]: <h1> 등 주요 태그에 Tailwind CSS 클래스가 직접 적용되었는지 확인합니다.
[목록 항목 검증]: '목록 처리 특별 지침'에 해당하는 항목들이 모두 정확한 개수로 포함되었는지 확인합니다.
[핵심 인용 검증]: 설교에서 핵심 근거로 사용된 모든 성경 구절이 본문에 <blockquote>를 사용하여 정확히 인용되었는지 확인합니다.
5. 최종 결과물 형식

다른 부가 설명 없이, 위 모든 지침을 따라 생성된 index.html 파일의 전체 코드를 담은 단일 코드 블록으로만 응답을 마무리합니다.

아이콘 라이브러리 (Icon Library)
카테고리설명색상 클래스SVG 코드원리/본질주제의 핵심 정의, 신학적 원리, 기초 개념bg-purple-600<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" /></svg>목록/규례구체적인 항목, 목록, 지켜야 할 규례 나열bg-blue-600<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6-2.292m0 0A9.043 9.043 0 0 1 12 6.042" /></svg>적용/목적삶에 적용하는 방법, 실천적 교훈, 목적 설명bg-emerald-600<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582" /></svg>경고/배격피해야 할 것, 잘못된 것에 대한 경고, 책임bg-rose-600<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.134-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.067-2.09 1.02-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>역사/배경역사적 사건, 성경적 배경, 인물 소개bg-orange-500<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0 0 12 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75Z" /></svg>결론/책임최종 결론, 요약, 성도의 책임과 자세bg-gray-600<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15.042 21.672L13.684 16.6m0 0l-2.51 2.225.569-9.47 5.227 7.917-3.286-.672ZM12 2.25V4.5m5.834.166l-1.591 1.591M21.75 12h-2.25m-1.666 5.834L16.409 16.5M4.5 12H2.25m1.666-5.834L5.591 7.5M12 21.75v-2.25" /></svg>
"""

    try:
        response = gemini_model.generate_content(prompt_template)
        # Gemini가 생성한 코드 블록(```html ... ```)에서 순수 HTML 코드만 추출
        html_code = response.text.strip()
        if html_code.startswith("```html"):
            html_code = html_code[7:]
        if html_code.endswith("```"):
            html_code = html_code[:-3]
        return html_code.strip()
    except Exception as e:
        print(f"Gemini 콘텐츠 생성 중 오류 발생: {e}")
        return None

def main():
    """메인 실행 함수"""
    last_processed_id = get_last_processed_video_id()
    print(f"마지막으로 처리한 영상 ID: {last_processed_id}")

    latest_video = get_latest_video_from_playlist(YOUTUBE_PLAYLIST_ID)
    if not latest_video:
        print("재생목록에서 영상을 찾을 수 없습니다.")
        return

    latest_video_id = latest_video['contentDetails']['videoId']
    print(f"최신 영상 ID: {latest_video_id}")

    if latest_video_id == last_processed_id:
        print("새로운 영상이 없습니다. 작업을 종료합니다.")
        return

    print(f"새로운 영상({latest_video_id})을 발견했습니다. 처리를 시작합니다.")

    transcript = get_transcript(latest_video_id)
    if not transcript:
        print("스크립트를 가져오지 못해 작업을 중단합니다.")
        return

    # 날짜 처리 로직
    published_iso = latest_video['snippet']['publishedAt']
    published_date = datetime.fromisoformat(published_iso.replace('Z', '+00:00')).date()
    weekday = published_date.weekday() # 월요일=0, 금요일=4, 토요일=5

    # 금요일 또는 토요일 영상이면 다음 날짜로 저장
    if weekday == 4 or weekday == 5:
        published_date += timedelta(days=1)
    
    file_name = f"db{published_date.strftime('%y%m%d')}.html"
    
    video_info = {
        'title': latest_video['snippet']['title'],
        'published_at': published_date.strftime('%Y-%m-%d'),
    }

    html_content = generate_html_content(transcript, video_info)

    if html_content:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        file_path = os.path.join(OUTPUT_DIR, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"성공적으로 '{file_path}' 파일을 생성했습니다.")
        set_last_processed_video_id(latest_video_id)
        print(f"상태 파일 업데이트 완료: {latest_video_id}")
    else:
        print("HTML 콘텐츠 생성에 실패했습니다.")

if __name__ == "__main__":
    main()
