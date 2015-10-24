from flask import Flask, render_template, redirect, request
from forms import KeywordForm


app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def index():
  form = KeywordForm()
  if form.validate_on_submit():
    keyword = request.form['keyword']
    return redirect('/', form=form, keyword=keyword)
  return render_template('index.html', form=form)

if __name__ == '__main__':
  app.run(debug=True)