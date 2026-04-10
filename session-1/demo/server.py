from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = 8000
BODY = b"Hello from Docker!\n"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(BODY)))
        self.end_headers()
        self.wfile.write(BODY)

    def log_message(self, format, *args):
        print(
            f"{self.client_address[0]} - - "
            f"[{self.log_date_time_string()}] {format % args}"
        )


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Server running on http://{HOST}:{PORT}")
    server.serve_forever()

