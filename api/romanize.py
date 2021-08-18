from flask import Flask
from flask import request
from korean_romanizer.romanizer import Romanizer

app = Flask(__name__)

@app.route("/")
def romanize():
    text = request.args.get("text")
    r = Romanizer(text)
    romanized = r.romanize()
    return romanized