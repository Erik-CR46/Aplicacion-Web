from flask import Flask
from app.config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
from app.api.task import TaskApi

migrate = Migrate(app, db) #Con esto ya no haria falta crear la tabla con create all
# Esta línea inicializa Flask-Migrate, vinculando la aplicación `app` 
# con la base de datos `db`, lo que permite gestionar cambios en el 
# esquema de la base de datos a través de migraciones automáticas.

#LOGIN
login_manager = LoginManager()
login_manager.init_app(app)

#RestApi
api = Api(app)
api.add_resource(TaskApi, '/api/task', '/api/task/<int:id>')

from app.auth.controllers import authRoute
from app.tasks.controllers import taskRoute
app.register_blueprint(taskRoute)
app.register_blueprint(authRoute)

#with app.app_context():
#    db.create_all()

