import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(r"c:\Users\matht\bible71\bible_html")
OT_DIR = BASE_DIR / "OT"
NT_DIR = BASE_DIR / "NT"

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        content_div = soup.find('div', class_='bible-content')
        
        if not content_div:
            return "No content div"

        # Find first verse number
        first_verse_span = content_div.find('span', class_='verse-number')
        
        if not first_verse_span:
            return "No verse numbers found"
            
        first_num = first_verse_span.get_text().strip()
        
        if first_num != '1':
            # Check what's before it?
            prev_siblings = []
            curr = first_verse_span.parent.previous_sibling
            while curr:
                if curr.name == 'p':
                    prev_siblings.append(curr.get_text().strip())
                curr = curr.previous_sibling
            
            return f"Starts with {first_num}. Preceding text present: {bool(prev_siblings)}"
            
        return None

    except Exception as e:
        return f"Error: {e}"

def scan_dir(directory):
    print(f"Scanning {directory.name}...")
    issues = []
    files = sorted(list(directory.glob("*.html")))
    for f in files:
        res = check_file(f)
        if res:
            issues.append(f"{f.name}: {res}")
    return issues

ot_issues = scan_dir(OT_DIR)
nt_issues = scan_dir(NT_DIR)

print("\n--- OT Issues ---")
for i in ot_issues: print(i)

print("\n--- NT Issues ---")
for i in nt_issues: print(i)
