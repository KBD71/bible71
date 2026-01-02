import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def upload_to_gemini(path, mime_type="application/pdf"):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
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

def generate_html_from_pdf():
    pdf_path = "catechism_book.pdf"
    template_path = "catechism/dc0905.html"
    output_path = "catechism/dc0106.html"
    target_date = "1월 6일"
    target_date_key = "0106"

    # Read Template
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Upload PDF
    pdf_file = upload_to_gemini(pdf_path, mime_type="application/pdf")
    wait_for_files_active([pdf_file])

    # Model Configuration
    generation_config = {
        "temperature": 0.1, # Low temperature for faithful extraction
        "top_p": 0.95,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    prompt = f"""
    당신은 숙련된 웹 퍼블리셔입니다.
    제공된 PDF 파일에서 **{target_date}**에 해당하는 내용을 찾아, 아래 제공된 HTML 템플릿 코드에 맞춰 새로운 HTML 코드를 작성해 주세요.

    [HTML 템플릿 코드]
    ```html
    {template_content}
    ```

    [작업 지침]
    1. **내용 추출 및 교체**:
        - PDF에서 **{target_date}**의 내용을 찾으십시오.
        - **날짜 변경**: 헤더의 날짜나 관련 텍스트를 '{target_date}'에 맞게 수정하십시오. (템플릿에 날짜 텍스트가 명시되어 있지 않다면 제목/부제목을 적절히 조정)
        - **제목(h1)**: 주제(예: 성경의 필요성)만 남기고, '신앙고백서 X장 X항' 같은 텍스트는 삭제하십시오.
        - **부제목(p)**: 제목 아래의 p 태그나 적절한 위치에 '신앙고백서 번호'(예: 제1장 1항)를 기입하십시오.
        - **본문 (신앙고백)**: `<section class="infographic-card card-border-blue">` 내부의 텍스트와 각주를 PDF의 신앙고백 내용으로 교체하십시오.
        - **관련 말씀**: `<section class="infographic-card card-border-yellow">` 내부의 성경 구절 리스트를 PDF의 '관련 말씀'으로 교체하십시오.
        - **교리 해설**: `<section class="infographic-card card-border-green">` (또는 유사한 해설 섹션) 내부를 PDF의 해설 내용으로 교체하십시오. PDF의 구조(소제목 등)를 반영하여 `<h3>`, `<ul>`, `<li>` 등을 적절히 사용하십시오.

    2. **스타일 및 구조 변경**:
        - **AI 요약 숨김**: AI 요약 듣기 버튼이 포함된 영역(예: `header` 내의 `button` 또는 감싸고 있는 `div`)에 `hidden` 클래스를 추가하여 화면에 보이지 않게 하십시오. (예: `<div class="mt-8 flex justify-center hidden">`)
        - **JavaScript 수정**: 코드 하단의 `const DATE_KEY = 'MMDD';` 부분을 `const DATE_KEY = '{target_date_key}';`로 반드시 수정하십시오.
        - `title` 태그도 내용에 맞게 수정하십시오.

    3. **제약 사항**:
        - Tailwind CSS 클래스와 전체적인 HTML 구조는 원본 템플릿을 유지해야 합니다.
        - 오직 완성된 HTML 코드만 출력하십시오 (마크다운 포맷팅 제외).
    """

    print("Generating HTML...", flush=True)
    try:
        response = model.generate_content([pdf_file, prompt])
        html_content = response.text
        # Cleanup markdown if present
        if "```html" in html_content:
            html_content = html_content.replace("```html", "").replace("```", "")
        html_content = html_content.strip()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"Successfully generated {output_path}", flush=True)
    except Exception as e:
        print(f"Error generating content: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_html_from_pdf()
