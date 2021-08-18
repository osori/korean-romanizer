from flask import Flask, request
from korean_romanizer.romanizer import Romanizer

app = Flask(__name__)

@app.route("/romanize/<text>")
def romanize(text):
    r = Romanizer(text)
    romanized = r.romanize()
    return romanized