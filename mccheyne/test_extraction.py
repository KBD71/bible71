from generate_epub import extract_bible_content, format_reading
from mccheyne_schedule_correct import SCHEDULE

def test_extraction():
    # Test Dec 31
    date_key = "1231"
    readings = SCHEDULE[date_key]
    print(f"Readings for {date_key}: {readings}")
    
    for reading in readings:
        print(f"\n--- Testing: {reading} ---")
        book, chap, v_range = format_reading(reading)
        print(f"Parsed: Book={book}, Chap={chap}, Range={v_range}")
        
        content = extract_bible_content(book, chap, v_range)
        print(f"Content Length: {len(content)}")
        print(f"Content Start: {content[:100]}")
        
        if "표시할 본문이 없습니다" in content or "파일을 찾을 수 없습니다" in content:
            print("!!! ERROR: Content missing !!!")

if __name__ == "__main__":
    test_extraction()
