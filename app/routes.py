from flask import Flask, render_template, redirect, request
from forms import KeywordForm


app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def index():
  form = KeywordForm()
  keyword = request.form.get('keyword', '')
  return render_template('index.html', form=form, keyword=keyword)

if __name__ == '__main__':
  app.run(debug=True)