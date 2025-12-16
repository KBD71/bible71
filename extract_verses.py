import os

def extract_verses():
    file_path = r'c:\Users\matht\bible71\bible_html\bible.txt'
    targets = [
        '여호수아1:1', '수1:1',
        '역대하1:1', '대하1:1',
        '에스라1:1', '스1:1',
        '신명기34:12', '신34:12',
        '역대상29:30', '대상29:30'
    ]
    
    try:
        with open(file_path, 'r', encoding='cp949') as f:
            for line in f:
                for target in targets:
                    if line.startswith(target):
                        print(line.strip())
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    extract_verses()
