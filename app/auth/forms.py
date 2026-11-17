from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, Optional
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

class ChangeInformation(FlaskForm):
    name = StringField(_('Nombre'), [InputRequired(message=_('This field is required.'))])
    lastname = StringField(_('Segundo nombre'), [InputRequired(message=_('This field is required.'))])
    email = EmailField(_('Email'), [InputRequired(message=_('This field is required.'))])

class ChangeAddress(FlaskForm):
    address = TextAreaField(_('Dirección'), [InputRequired(message=_('This field is required.'))])

class ChangePasswordForm(FlaskForm):
    username = StringField(_('Usuario'))
    password = PasswordField(_('Contraseña'), [
        Optional(),
        EqualTo('confirm_password', message=_('Las contraseñas no coinciden.')),
    ])
    confirm_password = PasswordField(_('Confirmar Contraseña'), [
        Optional(),
        EqualTo('password', message=_('Las contraseñas no coinciden.')),
    ])