#!/usr/bin/env python3
"""
성경 챗봇을 위한 간단한 프록시 서버
Claude API CORS 문제를 해결하기 위해 사용
"""

import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.error import HTTPError
import sys

class ProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # API 프록시 요청만 처리
        if self.path == '/api/claude':
            self.handle_claude_api()
        else:
            self.send_error(404, "Not Found")

    def do_GET(self):
        self.send_error(405, "Method Not Allowed")

    def do_OPTIONS(self):
        # CORS preflight 요청 처리
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def handle_claude_api(self):
        try:
            # 요청 본문 읽기
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            # Claude API로 요청 전달
            claude_url = 'https://api.anthropic.com/v1/messages'

            # 요청 헤더 구성
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': request_data.get('api_key', ''),
                'anthropic-version': request_data.get('anthropic_version', '2023-06-01')
            }

            # API 키 제거 (Claude에는 헤더로만 전송)
            claude_request = {
                'model': request_data.get('model'),
                'system': request_data.get('system'),
                'messages': request_data.get('messages'),
                'max_tokens': request_data.get('max_tokens', 1000),
                'temperature': request_data.get('temperature', 0.3)
            }

            # Claude API 호출
            req = urllib.request.Request(
                claude_url,
                data=json.dumps(claude_request).encode('utf-8'),
                headers=headers
            )

            try:
                with urllib.request.urlopen(req) as response:
                    response_data = response.read().decode('utf-8')

                # 성공 응답
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_data.encode('utf-8'))

            except HTTPError as e:
                # API 에러 응답
                error_data = e.read().decode('utf-8') if e.fp else '{}'
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(error_data.encode('utf-8'))

        except Exception as e:
            # 서버 에러
            error_response = json.dumps({
                'error': {
                    'message': f'프록시 서버 오류: {str(e)}',
                    'type': 'proxy_error'
                }
            })

            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(error_response.encode('utf-8'))

    def log_message(self, format, *args):
        # 로그 출력 (간단하게)
        print(f"[{self.address_string()}] {format % args}")

def run_server(port=8001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f"🚀 프록시 서버가 http://localhost:{port} 에서 시작되었습니다.")
    print("📋 사용법:")
    print(f"   - 챗봇: http://localhost:8000 (별도 터미널에서 실행)")
    print(f"   - API 프록시: http://localhost:{port}/api/claude")
    print("🛑 중지하려면 Ctrl+C를 누르세요.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ 프록시 서버를 중지합니다.")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()