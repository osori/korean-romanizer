from http.server import BaseHTTPRequestHandler
from korean_romanizer.romanizer import Romanizer

class handler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()

    r = Romanizer("안녕하세요")
    romanized = r.romanize()
    self.wfile.write(romanized.encode())
    return