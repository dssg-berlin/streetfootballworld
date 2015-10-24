from flask import Flask, render_template, redirect, request
from forms import KeywordForm

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = KeywordForm()
    keyword = request.form.get('keyword', '')
    posts = []
    for i in range(1, 6):
        posts.append({"relevance": 1. / i,
                      "sentiment": 2.5 - i,
                      "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed luctus erat ac tristique consequat. Nullam justo nibh, iaculis eget magna vehicula, sodales vehicula augue. Quisque quis aliquam diam, non aliquam mauris. Vivamus interdum, mauris vitae tincidunt tempor, sapien odio lobortis leo, at iaculis nisl ligula sed ligula. Sed a mi suscipit dui cursus varius non a elit. Nulla facilisi. Pellentesque mollis ipsum sit amet libero euismod, ut scelerisque arcu lacinia. Nulla viverra sapien lectus."})
    return render_template('index.html', form=form, keyword=keyword, posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
