from flask_wtf import Form
from wtforms import StringField

class KeywordForm(Form):
    keyword = StringField('keyword')
