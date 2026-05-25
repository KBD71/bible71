import os
import re
import sys

# Ensure UTF-8 printing
sys.stdout.reconfigure(encoding='utf-8')

mccheyne_dir = "mccheyne"
files = [f for f in os.listdir(mccheyne_dir) if f.startswith("mc08") and f.endswith(".html")]

errors = 0

for file_name in sorted(files):
    file_path = os.path.join(mccheyne_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. No style="display:none;" inline style on tab-content
    if re.search(r'class="[^"]*tab-content[^"]*"[^>]*style="[^"]*display:\s*none', content, re.IGNORECASE):
        print(f"Error in {file_name}: Found display:none inline style on tab-content")
        errors += 1
        
    # 2. data-path validation (must not contain markdown links or bracket characters)
    data_paths = re.findall(r'data-path="([^"]+)"', content)
    for dp in data_paths:
        # Note: can be a comma-separated list of URLs due to multi-chapter range patching
        for sub_dp in dp.split(','):
            if not sub_dp.startswith("https://kbd71.github.io/bible71/bible_html/"):
                print(f"Error in {file_name}: data-path does not start with correct URL: {sub_dp}")
                errors += 1
            if "markdown" in sub_dp or "[" in sub_dp or "]" in sub_dp:
                print(f"Error in {file_name}: data-path contains markdown or bracket chars: {sub_dp}")
                errors += 1
            
    # 3. data-key validation (no padding)
    data_keys = re.findall(r'data-key="([^"]+)"', content)
    for dk in data_keys:
        # Note: can be underscores due to multi-chapter range patching (e.g. JER_30_31)
        parts = dk.split("_")
        if len(parts) >= 2:
            # Check the chapters themselves (any segment that is completely digits, except the first part if it's book name like 1SA)
            for part in parts[1:]:
                if part.isdigit() and part.startswith("0") and len(part) > 1:
                    print(f"Error in {file_name}: data-key contains zero-padded chapter: {dk}")
                    errors += 1

    # 4. playOriginalAudio validation (no Korean, correct language codes)
    # Parse only calls inside onclick attributes to avoid JS function definition (function playOriginalAudio(text, langCode))
    poas = re.findall(r"onclick=\"playOriginalAudio\(([^)]+)\)\"", content)
    for poa in poas:
        if re.search(r"[가-힣]", poa):
            safe_poa = poa.encode('ascii', errors='ignore').decode('ascii')
            print(f"Error in {file_name}: playOriginalAudio contains Korean characters: {safe_poa}")
            errors += 1
        # Extract parameters: e.g. 'δεῦτε...', 'el-GR'
        params = [p.strip().strip("'").strip('"') for p in poa.split(',')]
        if len(params) >= 2:
            lang_code = params[1]
            if lang_code not in ['he-IL', 'el-GR']:
                print(f"Error in {file_name}: playOriginalAudio has invalid language code: {lang_code} in {poa}")
                errors += 1
            
    # 5. AI citation markers
    if "[cite" in content:
        print(f"Error in {file_name}: Found [cite] markers")
        errors += 1

if errors == 0:
    print("All August files are 100% compliant with the premium rules!")
else:
    print(f"Total errors found in August files: {errors}")
