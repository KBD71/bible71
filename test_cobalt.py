import requests
url = 'https://api.cobalt.tools/api/json'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
payload = {'url': 'https://www.youtube.com/watch?v=5Nj2IMx9UVw', 'isAudioOnly': True, 'aFormat': 'mp3'}
try:
    r = requests.post(url, headers=headers, json=payload)
    print(r.status_code, r.text)
except Exception as e:
    print('Error:', e)
