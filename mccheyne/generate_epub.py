# -*- coding: utf-8 -*-
"""
McCheynes Bible Reading Plan EPUB Generator
365일 맥체인 성경읽기 EPUB 생성기

Corrected schedule based on original M'Cheyne plan:
- Family 1: Genesis to Deuteronomy + Joshua to 2 Chronicles  
- Family 2: Matthew to John (twice)
- Secret 1: Ezra to Song of Songs + Isaiah to Malachi
- Secret 2: Acts to Revelation (twice)
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from ebooklib import epub

# Base paths
BASE_DIR = Path(__file__).parent.parent
BIBLE_HTML_DIR = BASE_DIR / "bible_html"
OUTPUT_FILE = Path(__file__).parent / "mccheyne_bible.epub"

# Korean book names mapping
BOOK_NAMES_KO = {
    "GEN": "창세기", "EXO": "출애굽기", "LEV": "레위기", "NUM": "민수기", "DEU": "신명기",
    "JOS": "여호수아", "JDG": "사사기", "RUT": "룻기", "1SA": "사무엘상", "2SA": "사무엘하",
    "1KI": "열왕기상", "2KI": "열왕기하", "1CH": "역대상", "2CH": "역대하",
    "EZR": "에스라", "NEH": "느헤미야", "EST": "에스더", "JOB": "욥기", "PSA": "시편",
    "PRO": "잠언", "ECC": "전도서", "SOS": "아가", "ISA": "이사야", "JER": "예레미야",
    "LAM": "애가", "EZE": "에스겔", "DAN": "다니엘", "HOS": "호세아", "JOE": "요엘",
    "AMO": "아모스", "OBA": "오바댜", "JON": "요나", "MIC": "미가", "NAH": "나훔",
    "HAB": "하박국", "ZEP": "스바냐", "HAG": "학개", "ZEC": "스가랴", "MAL": "말라기",
    "MAT": "마태복음", "MAR": "마가복음", "LUK": "누가복음", "JOH": "요한복음",
    "ACT": "사도행전", "ROM": "로마서", "1CO": "고린도전서", "2CO": "고린도후서",
    "GAL": "갈라디아서", "EPH": "에베소서", "PHI": "빌립보서", "COL": "골로새서",
    "1TH": "데살로니가전서", "2TH": "데살로니가후서", "1TI": "디모데전서", "2TI": "디모데후서",
    "TIT": "디도서", "PHM": "빌레몬서", "HEB": "히브리서", "JAM": "야고보서",
    "1PE": "베드로전서", "2PE": "베드로후서", "1JN": "요한일서", "2JN": "요한이서",
    "3JN": "요한삼서", "JUD": "유다서", "REV": "요한계시록"
}

# Book numbers for file naming
BOOK_NUMS = {
    "GEN": "01", "EXO": "02", "LEV": "03", "NUM": "04", "DEU": "05",
    "JOS": "06", "JDG": "07", "RUT": "08", "1SA": "09", "2SA": "10",
    "1KI": "11", "2KI": "12", "1CH": "13", "2CH": "14", "EZR": "15",
    "NEH": "16", "EST": "17", "JOB": "18", "PSA": "19", "PRO": "20",
    "ECC": "21", "SOS": "22", "ISA": "23", "JER": "24", "LAM": "25",
    "EZE": "26", "DAN": "27", "HOS": "28", "JOE": "29", "AMO": "30",
    "OBA": "31", "JON": "32", "MIC": "33", "NAH": "34", "HAB": "35",
    "ZEP": "36", "HAG": "37", "ZEC": "38", "MAL": "39",
    "MAT": "40", "MAR": "41", "LUK": "42", "JOH": "43", "ACT": "44",
    "ROM": "45", "1CO": "46", "2CO": "47", "GAL": "48", "EPH": "49",
    "PHI": "50", "COL": "51", "1TH": "52", "2TH": "53", "1TI": "54",
    "2TI": "55", "TIT": "56", "PHM": "57", "HEB": "58", "JAM": "59",
    "1PE": "60", "2PE": "61", "1JN": "62", "2JN": "63", "3JN": "64",
    "JUD": "65", "REV": "66"
}

def get_testament(book_code):
    num = int(BOOK_NUMS[book_code])
    return "OT" if num <= 39 else "NT"

def get_html_path(book_code, chapter):
    testament = get_testament(book_code)
    num = BOOK_NUMS[book_code]
    filename = f"{testament}_{num}_{book_code}_{chapter:02d}.html"
    return BIBLE_HTML_DIR / testament / filename

def extract_bible_content(book_code, chapter, verse_range=None):
    """Extract Bible content from HTML file"""
    html_path = get_html_path(book_code, chapter)
    if not html_path.exists():
        return f"<p>[파일을 찾을 수 없습니다: {html_path.name}]</p>"
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_text = f.read()
        
        if not html_text.strip():
            return "<p>[빈 파일입니다]</p>"
        
        soup = BeautifulSoup(html_text, 'html.parser')
        
        content_div = soup.find('div', class_='bible-content')
        if content_div:
            # Clean up content
            for tag in content_div.find_all(True):
                if tag.name in ['script', 'style']:
                    tag.decompose()
            
            # Determine verse limits
            start_v = 1
            end_v = 999
            if verse_range:
                if '-' in verse_range:
                    parts = verse_range.split('-')
                    start_v = int(parts[0])
                    if parts[1] == 'end' or parts[1] == 'ff':
                        end_v = 999
                    elif parts[1].isdigit():
                         end_v = int(parts[1])
                elif verse_range.endswith('ff'):
                     start_v = int(verse_range[:-2])
                     end_v = 999
                else:
                     start_v = int(verse_range)
                     end_v = int(verse_range)

            # Reconstruct content with merged paragraphs
            output_html = ""
            current_paragraph_verses = []
            
            for elem in content_div.children:
                if elem.name == 'p':
                    # Parse verse number
                    v_span = elem.find('span', class_='verse-number')
                    if v_span:
                        v_num_str = v_span.get_text().strip()
                        if v_num_str.isdigit():
                            v_num = int(v_num_str)
                            # Remove span from element to get clean text
                            v_span.decompose()
                            text = elem.get_text().strip()
                            
                            # Filter by range
                            if start_v <= v_num <= end_v:
                                # Apply verse styling
                                current_paragraph_verses.append(f'<sup class="verse-num">{v_num}</sup> {text}')
                    else:
                        # No verse number, append to current if exists
                        text = elem.get_text().strip()
                        if text and current_paragraph_verses:
                            current_paragraph_verses.append(text)
                            
                elif elem.name == 'div' and 'subtitle' in elem.get('class', []):
                    # Flush previous paragraph with line breaks
                    if current_paragraph_verses:
                        output_html += f'<p class="bible-text">{"<br/>".join(current_paragraph_verses)}</p>'
                        current_paragraph_verses = []
                    
                    # Add subtitle matching user preference
                    # Only add subtitle if we are somewhat near/inside the range?
                    # Simplified: Always add subtitle if encountered, but maybe filter?
                    # Let's keep it simple: Add subtitle.
                    output_html += f'<h4 class="bible-subtitle">{elem.get_text().strip()}</h4>'
            
            # Flush final paragraph
            if current_paragraph_verses:
                output_html += f'<p class="bible-text">{"<br/>".join(current_paragraph_verses)}</p>'
            
            return output_html if output_html else "<p>[표시할 본문이 없습니다]</p>"
        
        return "<p>[내용을 추출할 수 없습니다]</p>"
    except Exception as e:
        return f"<p>[파싱 오류: {str(e)}]</p>"

def format_reading(reading):
    """Format reading like 'GEN1' or 'LUK1:1-38' to book code, chapter, verse_range"""
    # Check for verse suffix
    verse_range = None
    if ':' in reading:
        parts = reading.split(':')
        reading = parts[0]
        verse_range = parts[1]
    
    # All book codes in our system (BOOK_CODES mapping) are exactly 3 characters.
    # e.g., GEN, 1SA, 2CH
    # We can effectively slice the first 3 chars as Book Code and the rest as Chapter.
    if len(reading) > 3:
        book_code = reading[:3]
        chapter_str = reading[3:]
        if chapter_str.isdigit():
            return book_code, int(chapter_str), verse_range
    
    return None, None, None

# Import schedule from dedicated file
from mccheyne_schedule_correct import SCHEDULE as MCCHEYNE_PLAN

def get_korean_month(month):
    return f"{month}월"

def get_korean_date(month, day):
    return f"{month}월 {day}일"

def create_day_content(date_key, readings):
    """Create chapter content for a single day"""
    month = int(date_key[:2])
    day = int(date_key[2:])
    date_str = get_korean_date(month, day)
    
    # Build reading list
    reading_items = []
    for i, reading in enumerate(readings):
        book_code, chapter, v_range = format_reading(reading)
        if book_code and book_code in BOOK_NAMES_KO:
            book_name = BOOK_NAMES_KO[book_code]
            suffix = f":{v_range}" if v_range else ""
            reading_items.append(f'<li><a href="#reading{i+1}">{book_name} {chapter}장{suffix}</a></li>')
    
    reading_list = '\n'.join(reading_items)
    
    # Build content sections
    content_sections = []
    for i, reading in enumerate(readings):
        book_code, chapter, v_range = format_reading(reading)
        if book_code and book_code in BOOK_NAMES_KO:
            book_name = BOOK_NAMES_KO[book_code]
            content = extract_bible_content(book_code, chapter, v_range)
            suffix = f":{v_range}" if v_range else ""
            content_sections.append(f'''
<section id="reading{i+1}">
<h3>{book_name} {chapter}장{suffix}</h3>
<div class="bible-content">{content}</div>
</section>''')
    
    sections_html = '\n'.join(content_sections)
    
    return f'''<h1>{date_str}</h1>
<h2>오늘의 읽기 범위</h2>
<ul class="reading-list">
{reading_list}
</ul>
{sections_html}'''

def generate_epub():
    """Generate the complete EPUB file"""
    print("맥체인 성경읽기 EPUB 생성 시작...")
    
    book = epub.EpubBook()
    book.set_identifier('mccheyne-bible-korean-2025')
    book.set_title('맥체인 성경읽기')
    book.set_language('ko')
    book.add_author("Robert Murray M'Cheyne")
    
    # Add CSS
    css_content = '''
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');

body { 
    font-family: 'Noto Serif KR', 'Batang', serif; 
    line-height: 1.7; 
    padding: 0 1em; 
    color: #333333;
    max-width: 900px;
    margin: 0 auto;
}

/* Header Styling */
h1 { 
    font-size: 1.8em; 
    color: #2c3e50; 
    text-align: center;
    margin-top: 1em;
    margin-bottom: 0.5em;
    font-weight: 700;
    letter-spacing: -0.02em;
}

h2 { 
    font-size: 1.1em; 
    color: #7f8c8d; 
    text-align: center;
    margin-top: 0;
    margin-bottom: 2em;
    font-weight: normal;
    border-bottom: 1px solid #eee;
    padding-bottom: 1em;
}

h3 { 
    font-size: 1.4em; 
    color: #000; 
    margin-top: 2.5em; 
    margin-bottom: 0.8em;
    font-weight: 700;
    border-bottom: 2px solid #333;
    padding-bottom: 0.2em;
}

/* Navigation List Styling */
.reading-list { 
    list-style: none; 
    padding: 1.5em; 
    background-color: #f8f9fa; 
    border-radius: 8px;
    margin-bottom: 2em;
    border: 1px solid #e9ecef;
}

.reading-list li { 
    margin: 0.5em 0; 
    text-align: center;
}

.reading-list a { 
    color: #2c3e50; 
    text-decoration: none; 
    font-weight: 600;
    font-size: 1.1em;
    display: block;
    padding: 0.2em;
    transition: color 0.2s;
}

.reading-list a:hover {
    color: #3498db;
}

/* Bible Text Styling */
.bible-content {
    margin-bottom: 3em;
}

.bible-text {
    text-align: justify;
    margin-bottom: 1em;
    word-break: keep-all; /* Korean word breaking */
}

/* Verse Number Styling - refined */
.verse-num { 
    font-size: 0.65em; 
    color: #95a5a6; 
    vertical-align: super; 
    line-height: 0;
    margin-right: 0.3em; 
    font-weight: 400;
    user-select: none; /* Make it easier to copy just text */
}

/* Subtitle Styling - refined */
.bible-subtitle {
    color: #8e44ad; /* Muted purple for distinction without alarm */
    font-size: 1.05em;
    font-weight: 700;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    padding-left: 0.5em;
    border-left: 3px solid #8e44ad;
}

/* Links inside content */
a {
    color: inherit;
    text-decoration: none;
}
'''
    nav_css = epub.EpubItem(uid="style", file_name="style/style.css", media_type="text/css", content=css_content.encode('utf-8'))
    book.add_item(nav_css)
    
    chapters = []
    toc_items = []
    current_month = None
    month_chapters = []
    
    sorted_dates = sorted(MCCHEYNE_PLAN.keys())
    total = len(sorted_dates)
    
    for idx, date_key in enumerate(sorted_dates):
        readings = MCCHEYNE_PLAN[date_key]
        month = int(date_key[:2])
        day = int(date_key[2:])
        
        # Create content
        body_content = create_day_content(date_key, readings)
        
        # Create proper XHTML
        xhtml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ko" lang="ko">
<head>
<meta charset="UTF-8"/>
<title>{get_korean_date(month, day)}</title>
<link rel="stylesheet" type="text/css" href="style/style.css"/>
</head>
<body>
{body_content}
</body>
</html>'''
        
        chapter = epub.EpubHtml(
            title=get_korean_date(month, day),
            file_name=f'day_{date_key}.xhtml',
            lang='ko'
        )
        chapter.set_content(xhtml_content.encode('utf-8'))
        
        book.add_item(chapter)
        chapters.append(chapter)
        
        # Group by month for TOC
        if month != current_month:
            if month_chapters:
                toc_items.append((epub.Section(get_korean_month(current_month)), tuple(month_chapters)))
            current_month = month
            month_chapters = []
        
        month_chapters.append(chapter)
        
        if (idx + 1) % 30 == 0 or idx == total - 1:
            print(f"  진행: {idx + 1}/{total} ({get_korean_date(month, day)})")
    
    # Add last month
    if month_chapters:
        toc_items.append((epub.Section(get_korean_month(current_month)), tuple(month_chapters)))
    
    # Set TOC and spine
    book.toc = tuple(toc_items)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters
    
    # Write EPUB
    epub.write_epub(str(OUTPUT_FILE), book, {})
    print(f"\nEPUB 파일 생성 완료: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_epub()
