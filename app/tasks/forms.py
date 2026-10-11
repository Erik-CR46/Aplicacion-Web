from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, HiddenField, IntegerField
from wtforms.validators import InputRequired

class Task(FlaskForm):
    model = StringField('Modelo', validators=[InputRequired()])
    km = IntegerField('Kilómetros')
    cv = IntegerField('CV')
    price = IntegerField('Precio')
    place = StringField('Ubicación')
    gasoline = SelectField('Combustible', choices=[], coerce=int)
    file = FileField('File')
    brand = SelectField('Brand', choices=[], coerce=int)

class TaskTagAdd(FlaskForm):
    tag = SelectField('Tag', choices=[])

class TaskTagRemove(FlaskForm):
    tag = HiddenField('Tag')