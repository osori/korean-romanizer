from http.server import BaseHTTPRequestHandler
import cgi
import requests
import os

WEBHOOK_URL = os.environ.get('BUG_REPORT_WEBHOOK_URL')

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        src_text = postvars.get("srcText", "")
        tgt_text = postvars.get("tgtText", "")

        data = {
            "content" : src_text + "\n" +  tgt_text,
            "username" : "korean-romanizer"
        }

        result = requests.post(url, json = data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            self.wfile.write(str(err).encode())
        else:
            self.wfile.write(str(result.status_code).encode())
        
        return