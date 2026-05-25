import yt_dlp
print(yt_dlp.version.__version__)
ydl_opts = {'format': 'm4a/bestaudio/best', 'simulate': True}
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info('https://www.youtube.com/watch?v=BaW_jenozKc', download=False)
except Exception as e:
    print('ERROR:', e)
