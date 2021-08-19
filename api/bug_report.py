from http.server import BaseHTTPRequestHandler
import requests
import os
import json
import cgi

WEBHOOK_URL = os.environ.get('BUG_REPORT_WEBHOOK_URL')

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        clen = int(self.headers['content-length'])

        postvars = json.loads(self.rfile.read(clen))

        src_text = postvars.get("srcText", "")
        tgt_text = postvars.get("tgtText", "")

        data = {
            "content" : "[BUG REPORT]\n" + src_text + "\n" +  tgt_text,
            "username" : "korean-romanizer"
        }

        result = requests.post(WEBHOOK_URL, json = data)

        return