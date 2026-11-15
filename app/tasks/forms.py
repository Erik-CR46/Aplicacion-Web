from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, HiddenField, IntegerField
from wtforms.validators import InputRequired
from flask_babel import lazy_gettext as _

class Task(FlaskForm):
    model = StringField(_('Modelo'), validators=[InputRequired(message=_('This field is required.'))])
    km = IntegerField(_('Kilómetros'))
    cv = IntegerField(_('CV'))
    price = IntegerField(_('Precio'))
    place = StringField(_('Ubicación'))
    gasoline = SelectField(_('Combustible'), choices=[], coerce=int)
    file = FileField(_('Archivo'))
    brand = SelectField(_('Marca'), choices=[], coerce=int)

class TaskTagAdd(FlaskForm):
    tag = SelectField(_('Etiqueta'), choices=[])

class TaskTagRemove(FlaskForm):
    tag = HiddenField(_('Etiqueta'))