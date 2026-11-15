import os

from flask import Flask, request
from app.config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_babel import Babel

app = Flask(__name__, static_folder='assets')
app.config.from_object(DevelopmentConfig)
app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.abspath(
    os.path.join(app.root_path, '..', 'translations')
)

db = SQLAlchemy(app)

#Cache
cache = Cache()
cache.init_app(app)

from app.api.task import TaskApi, TaskPagination
from app.api.brands_arg import BrandArgApi
from app.api.tags_args import TagArgApi

migrate = Migrate(app, db) #Con esto ya no haria falta crear la tabla con create all
# Esta línea inicializa Flask-Migrate, vinculando la aplicación `app` 
# con la base de datos `db`, lo que permite gestionar cambios en el 
# esquema de la base de datos a través de migraciones automáticas.

#LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

#jwt
jwt = JWTManager()
jwt.init_app(app)


#Babel
def get_locale():
    return request.accept_languages.best_match(['es', 'en'])

babel = Babel(app, locale_selector=get_locale)


#RestApi
api = Api(app)
api.add_resource(TaskApi, '/api/task', '/api/task/<int:id>')
api.add_resource(TaskPagination, '/api/task/<int:page>/<int:per_page>')
api.add_resource(BrandArgApi, '/api/brand', '/api/brand/<int:id>')
api.add_resource(TagArgApi, '/api/tag', '/api/tag/<int:id>')



from app.auth.controllers import authRoute
from app.tasks.controllers import taskRoute
app.register_blueprint(taskRoute)
app.register_blueprint(authRoute)

#with app.app_context():
#    db.create_all()

@app.route('/')
def hello_world():
    return {'hello':'world'}
