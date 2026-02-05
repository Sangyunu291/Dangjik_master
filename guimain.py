import http.server
import socketserver
import json
import webbrowser
import io
import csv

from date import *

class SimpleCSVHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload_time':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            date_data = json.loads(post_data.decode('utf-8'))

            start_date = date_data.get('startDate')
            end_date = date_data.get('endDate')

            date_list = get_custom_date_list(start_date, end_date)
            
            for date in date_list:
                print(date)

            # 응답 보내기
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "success"}
            self.wfile.write(json.dumps(response).encode())





def run_server():
    PORT = 8000
    # 주소 재사용 허용 (서버 재시작 시 에러 방지)
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), SimpleCSVHandler) as httpd:
        print(f"서버 실행 중: http://localhost:{PORT}")
        print("브라우저에서 파일을 선택하면 이 창에 표가 출력됩니다.")
        webbrowser.open(f"http://localhost:{PORT}/index.html")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()