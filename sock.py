import http.server
import socketserver
import json
import webbrowser
import io
import csv

class SimpleCSVHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            # 1. 데이터 수신
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # 2. CSV 파싱
            csv_content = data['csv_text']
            f = io.StringIO(csv_content.strip())
            reader = list(csv.reader(f))
            
            if not reader:
                return

            # 3. 파이썬 콘솔에 표 형태로 출력
            print("\n" + "=[ CSV 데이터 출력 ]".ljust(50, "="))
            # 헤더 출력
            headers = reader[0]
            print(f" | {' | '.join(headers)} |")
            print("-" * 50)
            
            # 본문 데이터 출력
            for row in reader[1:]:
                print(f" | {' | '.join(row)} |")
            print("=" * 50 + "\n")

            # 4. 브라우저에 응답
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "success", "message": "파이썬 콘솔 확인 요망"}
            self.wfile.write(json.dumps(response).encode())

def run_server():
    PORT = 8000
    # 주소 재사용 허용 (서버 재시작 시 에러 방지)
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), SimpleCSVHandler) as httpd:
        print(f"서버 실행 중: http://localhost:{PORT}")
        print("브라우저에서 파일을 선택하면 이 창에 표가 출력됩니다.")
        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
