import os, glob, re

path = 'mccheyne/mc*.html'
files = glob.glob(path)
count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # regex to find buttons
    matches = re.findall(r'<button class=\"btn btn-primary view-text-btn\" data-path=\"([^\"]+)\" data-title=\"([^\"]+)\">', content)
    for data_path, data_title in matches:
        if '-' in data_title and ',' not in data_path:
            m = re.search(r'(\d+)-(\d+)', data_title)
            if m:
                count += 1
                print(f'{f}: {data_title} -> {data_path}')
print(f'Total text buttons needing fix: {count}')

count2 = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # regex to find audio buttons
    matches = re.findall(r'<button class=\"btn btn-secondary listen-audio-btn\" data-key=\"([^\"]+)\" data-title=\"([^\"]+)\">', content)
    for data_key, data_title in matches:
        if '-' in data_title and '_' not in data_key.split('_', 1)[-1]: # Needs more robust check but this is basic
            m = re.search(r'(\d+)-(\d+)', data_title)
            if m:
                count2 += 1
                print(f'{f}: {data_title} -> {data_key}')
print(f'Total audio buttons needing fix: {count2}')
