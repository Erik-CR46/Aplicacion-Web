from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.tasks import operations, forms, models as task_models
from werkzeug.utils import secure_filename
from app import app, config
from app.auth import models as auth_models
import os


taskRoute = Blueprint('tasks', __name__, url_prefix='/tasks')

@taskRoute.before_request
@login_required
def before():
    pass


@taskRoute.route('/')
#@login_required
def index():

    #operations.create("Task")
    #operations.update(1,"hola")
    #print(operations.getById(2))
    #print(operations.getAll())
    #print(operations.delete(4))
    #print(operations.pagination().items)

    return render_template("dashboard/tasks/index.html", task_list= operations.getAll())

@taskRoute.route('/create', methods=('GET', 'POST'))
def create():
    form = forms.Task()
    form.brand.choices = [(brand.id, brand.name) for brand in task_models.Brand.query.all()]
    if form.validate_on_submit():
        operations.create(form.name.data, form.brand.data)
        return redirect(url_for('tasks.index'))
    return render_template("dashboard/tasks/create.html", form=form)

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
    operations.deleteDocument(id)
    operations.delete(id)
    return redirect(url_for('tasks.index'))

@taskRoute.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id:int):
    task = operations.getById(id, show404=True)
    form = forms.Task()
    form.brand.choices = [(brand.id, brand.name) for brand in task_models.Brand.query.all()]

    #tags
    form_tag = forms.TaskTagAdd()
    form_tag.tag.choices = [(tag.id, tag.name) for tag in task_models.Tag.query.all()]

    formTagRemove = forms.TaskTagRemove()

    document = None

    if task.document_id is not None:
        document = operations.getByIdDocument(task.document_id)

    if request.method == 'GET':
        form.name.data = task.model
        form.brand.data = task.brand_id

    if form.validate_on_submit():
        operations.update(id, form.name.data, form.brand.data)

        if form.file.data and config.allowed_extensions_name(form.file.data.filename):
            taskdb_file = form.file.data
            filename = secure_filename(taskdb_file.filename)
            document = operations.createDocument(filename=filename, extension=filename.split('.')[-1], file=taskdb_file)
            operations.update(id, form.name.data, form.brand.data, document.id)

        flash('Task updated successfully!', 'success')

        return redirect(url_for('tasks.index'))


    return render_template("dashboard/tasks/update.html", form=form, formTag=form_tag, formTagRemove=formTagRemove, id=id, document=document, task=task)

#tag

@taskRoute.route('/<int:id>/tag/add', methods=['POST'])
def add_tag(id:int):
    formTag = forms.TaskTagAdd()
    formTag.tag.choices = [(tag.id, tag.name) for tag in task_models.Tag.query.all()]

    if formTag.validate_on_submit():
        operations.addTag(id, formTag.tag.data)

    #flash('Tag added successfully!', 'success')
    return redirect(url_for('tasks.update', id=id))

@taskRoute.route('/<int:id>/tag/remove', methods=['POST'])
def remove_tag(id:int):
    formTagRemove = forms.TaskTagRemove()

    if formTagRemove.validate_on_submit():
        operations.removeTag(id, formTagRemove.tag.data)

    return redirect(url_for('tasks.update', id=id))
