from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
        searchterm = StringField()
        submit = SubmitField("SEARCH")
        
        