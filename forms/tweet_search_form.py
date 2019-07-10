from wtforms import StringField, SubmitField, Form
from wtforms.validators import DataRequired


class TweetSearchForm(Form):
    search = StringField('search Query', [DataRequired()])
    submit = SubmitField('submit')
