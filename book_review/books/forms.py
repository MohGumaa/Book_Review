from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searchText = StringField(validators=[DataRequired()])
    submit = SubmitField("Search")

class ReviewForm(FlaskForm):
    rating = SelectField("Rating", choices=[('1', 'One star'), ('2', 'Two star'),
        ('3', 'Three star'), ('4', 'Four star'), ('5', 'Five star')])
    comment = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")


