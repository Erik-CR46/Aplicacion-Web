from werkzeug.security import generate_password_hash, check_password_hash #Importacion de funciones para encriptar y verificar contraseñas 
from app import db
from sqlalchemy.orm import relationship
import enum

# Este modelo representa a los usuarios de la aplicacion en la bdd.
# Guardaremos el nombre de usuario y una version hash de su contrasena.
# El controlador de autenticacion usara esta clase para buscar usuarios durante
# el login, y Flask-Login usara sus propiedades para mantener la sesion activa.
class LangChoices(enum.Enum):
    ES = 'es'
    EN = 'en'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwhash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_cofirmed_at = db.Column(db.DateTime())

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    avatar_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)

    avatar = relationship('Document', lazy='joined')
    social_networks = relationship('SocialNetwork', lazy='joined', secondary='user_social_networks')
    
    lang = db.Column(db.Enum(LangChoices), default=LangChoices.EN)
    
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

    @property
    # Indica que este objeto no representa a un usuario anonimo.
    def serialize(self):
        return {
            'id':self.id,
            'user':self.username
        }

    # Devuelve el identificador que Flask-Login guardara en la sesion.
    # El controlador lo usara despues para recuperar el usuario desde la base de datos.
    def get_id(self):
        return str(self.id)

class SocialNetwork(db.Model):
    __tablename__ = 'social_networks'
    id= db.Column(db.Integer(), primary_key=True)
    name= db.Column(db.String(50), unique=True)

class UserSocialNetwork(db.Model):
    __tablename__ = 'user_social_networks'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    social_network_id = db.Column(db.Integer(), db.ForeignKey('social_networks.id', ondelete='CASCADE'))


class Address(db.Model):
    __tablename__ = 'addresses'
    id= db.Column(db.Integer(), primary_key=True)
    address= db.Column(db.String(250), unique=True)


