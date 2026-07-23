from flask import Flask
from app.config import DevelopmentConfig
from app.tasks.controllers import taskRoute

app = Flask(__name__)
app.register_blueprint(taskRoute)

app.config.from_object(DevelopmentConfig)
