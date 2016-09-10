from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired

class SearchForm(Form):
    url = TextField('URL', validators=[DataRequired()])
