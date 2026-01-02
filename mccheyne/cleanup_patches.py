import os
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(r"c:\Users\matht\bible71\bible_html")

JDG_1_1 = "여호수아가 죽은 후에 이스라엘 자손이 여호와께 여쭈어 이르되 우리 가운데 누가 먼저 올라가서 가나안 족속과 싸우리이까"

def cleanup_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        content_div = soup.find('div', class_='bible-content')
        if not content_div: return
        
        # Find Verse 1
        first_verse = content_div.find('span', class_='verse-number')
        if not first_verse or first_verse.get_text().strip() != '1':
            return 
            
        parent_p = first_verse.parent
        text = parent_p.get_text()
        
        changed = False
        
        # Check for Garbage from ibibles.net
        if "Bible Quote" in text:
            # Remove "Bible Quote" and extra newlines
            # We want to keep the verse number span, and just fix the text node after it.
            # Traverse children
            for child in parent_p.contents:
                if child.name == 'span': continue
                if isinstance(child, str):
                    original = str(child)
                    if "Bible Quote" in original:
                        # Clean it up
                        new_text = original.replace("Bible Quote", "").strip()
                        # Also remove leading "1:1" if distinct from span
                        new_text = new_text.replace("1:1", "", 1).strip()
                        child.replace_with(f" {new_text}")
                        changed = True
        
        # Check for "Bible book not found" (Judges case)
        if "Bible book not found" in text:
            print(f"Fixing broken patch in {filepath.name}")
            # Replace content after span with hardcoded text
            # Assuming Judges 1:1
            if "JDG_01" in filepath.name:
                # Remove all siblings of span
                for sibling in first_verse.next_siblings:
                    sibling.extract() # Remove garbage
                parent_p.append(f" {JDG_1_1}")
                changed = True
        
        if changed:
            print(f"Cleaned {filepath.name}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))

    except Exception as e:
        print(f"Error cleaning {filepath}: {e}")

def run_cleanup():
    print("Starting Cleanup...")
    for d in [BASE_DIR / "OT", BASE_DIR / "NT"]:
        for f in d.glob("*_01.html"):
            cleanup_file(f)

if __name__ == "__main__":
    run_cleanup()
