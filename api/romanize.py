from flask import Flask
from flask import request
from korean_romanizer.romanizer import Romanizer

app = Flask(__name__)

@app.route("/<text>")
def romanize(text):
    r = Romanizer(text)
    romanized = r.romanize()
    return romanized