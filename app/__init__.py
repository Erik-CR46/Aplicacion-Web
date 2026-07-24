from flask import Flask, render_template, request
from app.config import DevelopmentConfig
from app.tasks.controllers import taskRoute

app = Flask(__name__)
app.register_blueprint(taskRoute)

app.config.from_object(DevelopmentConfig)


@app.route('/')
def main():
    name = request.args.get('name', 'Desarrollador')
    return render_template('index.html', name=name)