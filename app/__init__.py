from flask import Flask, render_template, request
from app.config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

from app.tasks import views