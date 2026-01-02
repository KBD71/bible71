import http.server
import socketserver
import webbrowser
import os
import time

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    os.chdir(DIRECTORY)
    # Check if port is in use, if so try next
    port = PORT
    while True:
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                print(f"서버가 http://localhost:{port}/viewer.html 에서 시작되었습니다.")
                print("웹 브라우저가 자동으로 열립니다...")
                print("서버를 종료하려면 Ctrl+C를 누르세요.")
                
                # Open browser
                webbrowser.open(f"http://localhost:{port}/viewer.html")
                
                httpd.serve_forever()
        except OSError:
            port += 1

if __name__ == "__main__":
    start_server()
