from flask import Blueprint, render_template, request, redirect, url_for
from app.tasks import operations
from app.tasks import forms
from werkzeug.utils import secure_filename
from app import app, config
import os

taskRoute = Blueprint('tasks', __name__, url_prefix='/tasks')

@taskRoute.route('/')
def index():

    #operations.create("Task")
    #operations.update(1,"hola")
    #print(operations.getById(2))
    #print(operations.getAll())
    #print(operations.delete(4))
    #print(operations.pagination().items)

    return render_template("tasks/index.html", task_list= operations.getAll())

@taskRoute.route('/create', methods=('GET', 'POST'))
def create():
    form = forms.Task()
    if form.validate_on_submit():
        operations.create(form.name.data)
        return redirect(url_for('tasks.index'))
    return render_template("tasks/create.html", form=form)

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
    operations.delete(id)
    return redirect(url_for('tasks.index'))

@taskRoute.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id:int):
    task = operations.getById(id)
    form = forms.Task()

    if request.method == 'GET':
        form.name.data = task.model

    if form.validate_on_submit():
        operations.update(id, form.name.data)

        if form.file.data and config.allowed_extensions_name(form.file.data.filename):
            taskdb_file = form.file.data
            filename = secure_filename(taskdb_file.filename)
            taskdb_file.save(os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'], filename))


        return redirect(url_for('tasks.index'))

    return render_template("tasks/update.html", form=form, id=id)
