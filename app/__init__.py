from flask import Flask
from app.config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db) #Con esto ya no haria falta crear la tabla con create all
# Esta línea inicializa Flask-Migrate, vinculando la aplicación `app` 
# con la base de datos `db`, lo que permite gestionar cambios en el 
# esquema de la base de datos a través de migraciones automáticas.

from app.tasks.controllers import taskRoute
app.register_blueprint(taskRoute)

#with app.app_context():
#    db.create_all()