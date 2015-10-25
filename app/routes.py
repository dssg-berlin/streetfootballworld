from flask import Flask, render_template, redirect, request
from forms import KeywordForm
import json

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def index():
    posts = json.load(open("./static/resources/topics.json"))
    posts = posts[0]['posts']
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
