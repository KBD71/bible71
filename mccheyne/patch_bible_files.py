import os
import re
import time
import urllib.request
from bs4 import BeautifulSoup
from pathlib import Path

# Mapping our file codes to ibibles.net codes if needed
# Our codes: GEN, EXO, LEV...
# ibibles: gen, exo, lev... (lowercase)
# Some might differ.
# Check 1SAM -> 1sa?
# Let's define manual map for tricky ones.
CODE_MAP = {
    "1SA": "1sa", "2SA": "2sa", "1KI": "1ki", "2KI": "2ki", "1CH": "1ch", "2CH": "2ch",
    "1CO": "1co", "2CO": "2co", "1TH": "1th", "2TH": "2th", "1TI": "1ti", "2TI": "2ti",
    "1PE": "1pe", "2PE": "2pe", "1JN": "1jn", "2JN": "2jn", "3JN": "3jn",
    "SOS": "sng", # Song of Songs might be 'sng' or 'sos' on ibibles?
    # Common codes typically match lowercase
}

def get_online_verse(book_code, chapter, verse):
    # ibibles format: https://ibibles.net/quote.php?kor-book/chap:verse
    # e.g. https://ibibles.net/quote.php?kor-exo/1:1
    
    code = CODE_MAP.get(book_code, book_code.lower())
    url = f"https://ibibles.net/quote.php?kor-{code}/{chapter}:{verse}"
    
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
            # Format is usually: <small>1:1</small> Text...
            # We strip tags.
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text().strip()
            # Remove "1:1 " prefix if present
            text = re.sub(r'^\d+:\d+\s*', '', text)
            print(f"Fetched {book_code} {chapter}:{verse} -> {text[:20]}...")
            return text
    except Exception as e:
        print(f"Failed to fetch {book_code} {chapter}:{verse}: {e}")
        return None

def patch_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        content_div = soup.find('div', class_='bible-content')
        if not content_div: return False
        
        # Check if Verse 1 exists
        first_verse = content_div.find('span', class_='verse-number')
        if not first_verse: return False
        if first_verse.get_text().strip() == '1':
            return False # Already has Verse 1
            
        # If headers/subtitles exist before verse 2, put verse 1 AFTER them?
        # Usually standard is: <h1>Title</h1> <div content> <p><span 2>...
        # We should insert AT THE BEGINNING of content_div
        # BUT check if there is a subtitle <div class="subtitle"> at the top?
        
        # Extract Book Code from filename
        filename = Path(filepath).name
        # Format: OT_02_EXO_01.html
        parts = filename.split('_')
        book_code = parts[2]
        chapter = int(parts[3].replace('.html', ''))
        
        if chapter != 1: 
            return False # Only patching Chapter 1s for now based on scan
            
        print(f"Patching {filename}...")
        text = get_online_verse(book_code, chapter, 1)
        if not text:
            return False
            
        # Create new paragraph
        new_p = soup.new_tag("p")
        span = soup.new_tag("span", attrs={"class": "verse-number"})
        span.string = "1"
        new_p.append(span)
        new_p.append(f" {text}")
        
        # Insert 
        # Detect where to insert. If first child is subtitle, after it?
        # Or just prepend?
        # Typically Verse 1 is first. Subtitles usually come later or describe the section.
        # But if subtitle is "The Beginning", it comes before.
        # Let's peek at children.
        first_child = next(content_div.children)
        while first_child == '\n':
            first_child = first_child.next_sibling
            
        if first_child and first_child.name == 'div' and 'subtitle' in first_child.get('class', []):
            # Insert after subtitle
            first_child.insert_after(new_p)
        else:
            content_div.insert(0, new_p)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
        return True

    except Exception as e:
        print(f"Error patching {filepath}: {e}")
        return False

def scan_and_patch(directory):
    files = sorted(list(directory.glob("*_01.html"))) # Only scan Chapter 1s
    count = 0
    for f in files:
        if patch_file(f):
            count += 1
            time.sleep(0.5) # Be gentle on API
    return count

BASE_DIR = Path(r"c:\Users\matht\bible71\bible_html")
print("Starting Patch Process...")
patched_ot = scan_and_patch(BASE_DIR / "OT")
patched_nt = scan_and_patch(BASE_DIR / "NT")
print(f"Patched {patched_ot + patched_nt} files.")
