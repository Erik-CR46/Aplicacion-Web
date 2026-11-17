from flask_login import current_user, login_user, logout_user, login_required
from flask_jwt_extended import create_access_token
from flask import flash, g, Blueprint, redirect, render_template, url_for, request, jsonify, session
from flask_babel import gettext
from app import login_manager, db
from app.auth.models import User
from app.auth.forms import LoginForm, RegisterForm, ChangeInformation, ChangeAddress, ChangePasswordForm
from app.auth.helpers import authenticate
from app.auth import operations

authRoute = Blueprint('auth', __name__)


# Flask-Login llama automáticamente a esta función cuando necesita
# reconstruir el usuario guardado en la sesión del navegador.
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Se ejecuta antes de cualquier ruta de este blueprint.
# `g.user` permite acceder al usuario actual durante la petición.
@authRoute.before_request
def get_current_user():
    g.user = current_user

# GET: muestra el formulario de registro.
# POST: valida el formulario y crea un usuario en la base de datos.
@authRoute.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(gettext('You are already logged in.'), 'info')
        return redirect(url_for('tasks.index'))
    
    form = RegisterForm()
    login_form = LoginForm()
    if form.validate_on_submit():
        # Estos datos vienen de RegisterForm, que recibe el formulario HTML.
        username = form.username.data
        password = form.password.data

        # Evita registrar dos usuarios con el mismo nombre.
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(gettext('Username already exists. Please choose a different one.'), 'danger')
            return render_template(
                'user/index.html',
                form=login_form,
                register_form=form,
                active_form='register',
            )

        # User es el modelo SQLAlchemy que representa la tabla de usuarios.
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash(gettext('Registration successful! You can now log in.'), 'success')
        return redirect(url_for('auth.login'))
    else:
        if form.errors:
            flash(gettext('Form validation failed. Please check your input.'), 'danger')
    return render_template(
        'user/index.html',
        form=login_form,
        register_form=form,
        active_form='register',
    )

@authRoute.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash(gettext('You are already logged in.'), 'info')
        return redirect(url_for('tasks.index'))
    
    form = LoginForm()
    register_form = RegisterForm()
    if form.validate_on_submit():
        # Los datos validados proceden del formulario de login.
        username = form.username.data
        password = form.password.data

        # Busca el usuario y comprueba la contraseña almacenada.
        existing_user = User.query.filter_by(username=username).first()
        
        if not(existing_user and existing_user.check_password(password)):
            flash(gettext('Invalid username or password.'), 'danger')
            return render_template(
                'user/index.html',
                form=form,
                register_form=register_form,
                active_form='login',
            )

        # Función de Flask-Login: guarda el usuario en la sesión.
        login_user(existing_user)
        session['user'] = existing_user.serialize
        flash(gettext('You have succesfully logged in.'), 'succes')
        return redirect(url_for('tasks.index'))


    if form.errors:
        flash(gettext('Form validation failed. Please check your input.'), 'danger')
    return render_template(
        'user/index.html',
        form=form,
        register_form=register_form,
        active_form='login',
    )

@authRoute.route('/logout')
@login_required
def logout():
    # Función de Flask-Login: elimina el usuario de la sesión.
    logout_user()
    return redirect(url_for('auth.login'))


#JWT
@authRoute.route('/user/api', methods=['POST'])
def api():
    # Esta ruta es una API independiente del login HTML.
    # Espera JSON y devuelve un token JWT si las credenciales son correctas.
    if not request.is_json:
        return jsonify({'msj': 'Missing JSN in request'}), 400
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({'msj': 'Username not exist'}), 400

    if not password:
        return jsonify({'msj': 'Password not exist'}), 400

    # `authenticate` es una función propia que busca y valida el usuario.
    user = authenticate(username, password)

    if not user:
        return jsonify({'msj': 'Username or password not correct'}), 400

    # Función de Flask-JWT-Extended: genera el token para futuras peticiones.
    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200

@authRoute.route('/user/profile')
def profile():
    return render_template('user/profile.html')

@authRoute.route('/user/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ChangeInformation()

    formAddress = ChangeAddress()

    formPassword = ChangePasswordForm()

    if request.method == 'GET':
        form.name.data = current_user.first_name
        form.lastname.data = current_user.last_name
        form.email.data = current_user.email
        formPassword.username.data = current_user.username
        if current_user.address is None:
            formAddress.address.data = ''
        else:
            formAddress.address.data = current_user.address.address

    if form.validate_on_submit() and formPassword.validate_on_submit() and formAddress.validate_on_submit():
        email = form.email.data.strip()
        existing_user = User.query.filter(
            User.email == email,
            User.id != current_user.id,
        ).first()
        if existing_user:
            form.email.errors.append(gettext('Este email ya está en uso.'))
        else:
            operations.update(
                id=current_user.id,
                first_name=form.name.data.strip(),
                last_name=form.lastname.data.strip(),
                email=email,
                address=formAddress.address.data.strip(),
                username=formPassword.username.data.strip(),
                password=formPassword.password.data.strip() if formPassword.password.data else None
            )
            flash(gettext('Profile updated successfully.'), 'success')
            return redirect(url_for('auth.profile'))

    return render_template('user/profile_edit.html', changeInformation=form, changeAddress=formAddress, changePassword=formPassword)