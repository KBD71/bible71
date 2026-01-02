import http.server
import socketserver
import webbrowser
import os
import mimetypes
import sys

# Ensure correct working directory
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIRECTORY)

# Explicitly add MIME types
mimetypes.init()
mimetypes.add_type('application/epub+zip', '.epub')
mimetypes.add_type('application/xhtml+xml', '.xhtml')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers just in case
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def start_server():
    # Try a range of ports
    port = 8081
    while port < 8100:
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                print(f"Server started at http://localhost:{port}/viewer.html")
                print(f"Serving files from: {DIRECTORY}")
                webbrowser.open(f"http://localhost:{port}/viewer.html")
                httpd.serve_forever()
                break
        except OSError:
            port += 1

if __name__ == "__main__":
    print("Starting EPUB Viewer Server...")
    start_server()
