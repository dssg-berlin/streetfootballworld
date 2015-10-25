from flask import Flask, render_template, redirect, request
from forms import KeywordForm
import json

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = KeywordForm()
    keyword = request.form.get('keyword', '')
    posts = json.load(open("../topics.json"))

    posts = posts[0]['posts']
    return render_template('index.html', form=form, keyword=keyword, posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
