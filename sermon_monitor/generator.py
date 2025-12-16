import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def upload_to_gemini(path, mime_type="audio/mp3"):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can be
    used as prompt arguments.
    """
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

def generate_sermon_html(audio_file_path, video_id):
    """
    Generates an HTML summary for a sermon audio file using Gemini.
    """
    
    # 1. Upload the audio file
    print(f"Uploading {audio_file_path} to Gemini...")
    files = [upload_to_gemini(audio_file_path)]
    
    # 2. Wait for processing
    wait_for_files_active(files)
    
    # 3. Create the model
    # Using Gemini 1.5 Pro as it handles audio natively and has large context
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    # 4. Construct the prompt
    # Users prompt as defined in the request
    prompt_text = f"""
당신은 '설교 요약 및 인포그래픽 생성 전문가'입니다. 당신의 임무는 제공된 유튜브 설교 영상을 개혁신학적 관점에서 깊이 있게 분석하여, 설교자의 어조와 강조점까지 포착하고 웹 환경에서 완벽하게 렌더링되는 학습 자료용 단일 HTML 코드를 생성하는 것입니다.

아래의 [단계별 작업 지침]을 엄격히 준수하십시오.

[단계별 작업 지침]

1단계: 기본 정보 및 헤더 구성

영상 전체를 분석하여 설교의 공식 제목, 설교자, 설교 본문(성경 구절), 설교 날짜를 정확히 파악하여 HTML <header> 섹션을 구성합니다.

설교 제목은 가장 크게, 그 아래에 설교 본문, 설교자, 설교 날짜를 하나의 라인에 통합하여 간결하게 표시합니다.

'핵심 주제'를 한 문장으로 정의하여 헤더 하단에 눈에 띄는 박스 형태로 배치합니다.

2단계: 성경 본문 배치 (오디오 플레이어 없음)

헤더 바로 아래에 <div class="scripture-text-section">을 배치하여 설교 본문 전체를 수록합니다.

각 절은 <p> 태그로 구분합니다.

절 번호는 <strong> 태그로 감싸 시각적으로 구분하여 가독성을 높입니다.

주의: 화면에 오디오 플레이어를 절대 만들지 마십시오. 성경 본문만 깔끔하게 배치합니다.

3단계: 내용 검수 및 교정 (정확성 확보)

원본 충실성: 자동 생성 텍스트를 기반으로 하되, 설교의 흐름과 감성적 호소(뉘앙스)를 반영합니다.

용어 교정: 음성 인식 오류(예: '연락' → '열납', '참호' → '사모')를 문맥과 신학적 용어에 맞게 교정합니다.

사실 교정: 명백한 사실 오류(수치, 역사적 사실 등)가 있다면 문맥에 맞게 수정합니다.

4단계: 핵심 내용 구조화 및 시각화 (깊이 있는 요약)

설교의 논리적 흐름(서론-본론-결론)에 따라 내용을 분할하고, 각 단위를 <div class="card">로 작성합니다.

상세 서술: 단순 요약이 아닌, 설교자의 예시, 비유, 해석, 적용점을 충실히 서술합니다. 복잡한 내용은 <ul> 태그를 사용합니다.

어조: "~입니다, ~습니다"의 정중하고 현장감 있는 경어체를 일관되게 사용합니다. (제3자 관찰자 시점 금지)

성경 인용: 근거 구절은 <blockquote>와 <cite> 태그를 사용합니다.

강조: 핵심 키워드나 문장은 <span class="keyword">로 감싸 시각적으로 강조합니다.

5단계: 스타일링 (Tailwind CSS)

모든 스타일은 Tailwind CSS 유틸리티 클래스를 사용합니다.

레이아웃: 모바일 가독성을 위해 단일 열(1-column) 레이아웃(max-w-3xl mx-auto)을 유지합니다.

가독성: 줄 간격(leading-relaxed), 충분한 여백(p-6, gap-6)을 적용합니다.

6단계: 외부 연동 코드 및 데이터 삽입 (필수 & 중요)

HTML 코드의 맨 마지막, </body> 태그 바로 윗줄에 아래 코드를 순서대로 삽입하십시오.

오디오 플레이어를 만들지 말고, 아래의 hidden input 태그를 사용하십시오.

URL 정제(중요): value 속성에는 원본 링크를 그대로 넣지 말고, 반드시 불필요한 파라미터(?si=, &feature= 등)를 모두 제거하고 오직 영상 ID만 남긴 https://youtu.be/VIDEO_ID 형식으로 가공하여 넣으십시오.
이 영상의 ID는 다음과 같습니다: {video_id}

스크립트 파일을 연결하십시오.

[작성 예시]

<input type="hidden" id="youtube-link" value="https://youtu.be/{video_id}">

<script src="script.js"></script>

[아이콘 및 카드 디자인 가이드]

각 카드의 주제에 맞춰 아래 표의 '테두리/텍스트 색상'을 적용하고, 주제에 부합하는 SVG 아이콘 코드(<svg>...</svg>)를 직접 생성하여 삽입하십시오. (빈 태그 금지)

카테고리설명테두리/텍스트 색상 클래스기본 스타일카드 공통bg-white rounded-lg shadow-lg p-6 border-t-4원리/본질신학적 원리, 핵심 정의border-purple-600 text-purple-800목록/규례구체적 항목, 실천 지침border-blue-600 text-blue-800적용/목적삶의 적용, 목적border-emerald-600 text-emerald-800경고/배격죄에 대한 경고, 주의사항border-rose-600 text-rose-800역사/배경배경 지식, 인물, 역사border-orange-500 text-orange-800결론/책임최종 요약, 성도의 책임border-gray-600 text-gray-800

[절대 금지 사항]

'설교자는 말했습니다' 식의 관찰자 시점 서술 금지.
성경본문 생략 금지
본문 내 타임스탬프 표기 금지.
<!DOCTYPE html>로 시작하는 소스 코드 외의 채팅 멘트나 부가 설명은 일절 금지합니다.

[최종 결과물 형식]
오직 <!DOCTYPE html>로 시작해서 </html>로 끝나는 단일 코드 블록만 출력하십시오.
"""

    print("Sending prompt to Gemini...")
    response = model.generate_content([files[0], prompt_text])
    
    # Extract text
    html_content = response.text
    
    # Simple cleanup if markdown code blocks are included
    if "```html" in html_content:
        html_content = html_content.replace("```html", "").replace("```", "")
    
    # Remove any extra leading/trailing whitespace
    html_content = html_content.strip()
    
    return html_content

if __name__ == "__main__":
    # Test block
    print("This module is intended to be imported.")
