import os, glob, re

path = 'mccheyne/mc*.html'
files = glob.glob(path)

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Text buttons
    text_matches = re.findall(r'<button class=\"btn btn-primary view-text-btn\" data-path=\"([^\"]+)\" data-title=\"([^\"]+)\">', content)
    for data_path, data_title in text_matches:
        if '-' in data_title and ',' not in data_path:
            m = re.search(r'(\d+)-(\d+)', data_title)
            if m:
                start_ch = int(m.group(1))
                end_ch = int(m.group(2))
                # Example data_path: https://kbd71.github.io/bible71/bible_html/OT/OT_19_PSA_11.html
                # Generate new paths
                parts = data_path.split('_')
                if len(parts) >= 3 and parts[-1].endswith('.html'):
                    prefix = '_'.join(parts[:-1])
                    new_paths = []
                    for ch in range(start_ch, end_ch + 1):
                        new_paths.append(f"{prefix}_{ch}.html")
                    new_data_path = ','.join(new_paths)
                    content = content.replace(f'data-path="{data_path}"', f'data-path="{new_data_path}"')

    # Audio buttons
    audio_matches = re.findall(r'<button class=\"btn btn-secondary listen-audio-btn\" data-key=\"([^\"]+)\" data-title=\"([^\"]+)\">', content)
    for data_key, data_title in audio_matches:
        parts = data_key.split('_')
        if '-' in data_title and len(parts) == 2:
            m = re.search(r'(\d+)-(\d+)', data_title)
            if m:
                start_ch = int(m.group(1))
                end_ch = int(m.group(2))
                
                # Check if data_key implies single chapter
                book_code = parts[0]
                ch_key = int(parts[1])
                
                if ch_key == start_ch:
                    new_key_parts = [book_code]
                    for ch in range(start_ch, end_ch + 1):
                        new_key_parts.append(str(ch))
                    new_data_key = '_'.join(new_key_parts)
                    content = content.replace(f'data-key="{data_key}"', f'data-key="{new_data_key}"')

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print('Patching complete!')
