from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, HiddenField
from wtforms.validators import InputRequired

class Task(FlaskForm):
    name=StringField('Name', validators=[InputRequired()])
    file=FileField('File',)
    brand=SelectField('Brand', choices=[], coerce=int)

class TaskTagAdd(FlaskForm):
    tag = SelectField('Tag', choices=[])

class TaskTagRemove(FlaskForm):
    tag = HiddenField('Tag')