from flask import Flask
from app.config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)

from app.tasks.controllers import taskRoute
app.register_blueprint(taskRoute)

with app.app_context():
    db.create_all()