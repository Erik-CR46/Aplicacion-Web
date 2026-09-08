from werkzeug.security import generate_password_hash, check_password_hash #Importacion de funciones para encriptar y verificar contraseñas 
from app import db

# Este modelo representa a los usuarios de la aplicacion en la bdd.
# Guardaremos el nombre de usuario y una version hash de su contrasena.
# El controlador de autenticacion usara esta clase para buscar usuarios durante
# el login, y Flask-Login usara sus propiedades para mantener la sesion activa.
class User(db.Model):
    table_name = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwhash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.pwhash = generate_password_hash(password) #Encriptacion de la contraseña usando la funcion generate_password_hash

    def check_password(self, password):
        return check_password_hash(self.pwhash, password) #Verificacion de la contraseña usando la funcion check_password_hash

    @property
    # Indica a Flask-Login que este usuario ha sido autenticado correctamente.
    def is_authenticated(self):
        return True

    @property
    # Indica que la cuenta puede iniciar y mantener una sesion.
    def is_active(self):
        return True

    @property
    # Indica que este objeto no representa a un usuario anonimo.
    def is_anonymous(self):
        return False

    # Devuelve el identificador que Flask-Login guardara en la sesion.
    # El controlador lo usara despues para recuperar el usuario desde la base de datos.
    def get_id(self):
        return str(self.id)
