from flask_login import current_user, login_user, logout_user, login_required
from flask_jwt_extended import create_access_token
from flask import flash, g, Blueprint, redirect, render_template, url_for, request, jsonify
from app import login_manager, db
from app.auth.models import User
from app.auth.forms import LoginForm, RegisterForm
from app.auth.helpers import authenticate

authRoute = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@authRoute.before_request
def get_current_user():
    g.user = current_user

@authRoute.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('tasks.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('user/register.html', form=form)

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')

        if form.errors:
            flash('Form validation failed. Please check your input.', 'danger')
    return render_template('user/register.html', form=form)

@authRoute.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('tasks.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        
        if not(existing_user and existing_user.check_password(password)):
            flash('Invalid username or password.', 'danger')
            return render_template('user/login.html', form=form)

        login_user(existing_user)
        flash('You have succesfully logged in.', 'succes')
        return redirect(url_for('tasks.index'))


    if form.errors:
        flash('Form validation failed. Please check your input.', 'danger')
    return render_template('user/login.html', form=form)

@authRoute.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


#JWT
@authRoute.route('/user/api', methods=['POST'])
def api():
    if not request.is_json:
        return jsonify({'msj': 'Missing JSN in request'}), 400
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({'msj': 'Username not exist'}), 400

    if not password:
        return jsonify({'msj': 'Password not exist'}), 400

    user = authenticate(username, password)

    if not user:
        return jsonify({'msj': 'Username or password not correct'}), 400

    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200