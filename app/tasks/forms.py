from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class Task(FlaskForm):
    name=StringField('Name', validators=[InputRequired()])