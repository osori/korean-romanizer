from http.server import BaseHTTPRequestHandler
from korean_romanizer.romanizer import Romanizer
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        args = parse_qs(self.path[2:])
        text = args.get("text", [""])[0]

        r = Romanizer(text)
        romanized = r.romanize()

        self.wfile.write(romanized.encode())
        return