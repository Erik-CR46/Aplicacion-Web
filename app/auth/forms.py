from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo
from flask_babel import lazy_gettext as _

class RegisterForm(FlaskForm):
    username = StringField(_('Username'), [InputRequired(message=_('This field is required.'))])
    password = PasswordField(_('Password'), [
        InputRequired(message=_('This field is required.')),
        EqualTo('confirm_password', message=_('Passwords must match.')),
    ])
    confirm_password = PasswordField(_('Confirm Password'), [
        InputRequired(message=_('This field is required.')),
        EqualTo('password', message=_('Passwords must match.')),
    ])

class LoginForm(FlaskForm):
    username = StringField(_('Username'), [InputRequired(message=_('This field is required.'))])
    password = PasswordField(_('Password'), [InputRequired(message=_('This field is required.'))])