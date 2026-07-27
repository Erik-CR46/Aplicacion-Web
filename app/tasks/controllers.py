from flask import Blueprint, render_template, request, redirect, url_for
from app.tasks import operations

taskRoute = Blueprint('tasks', __name__, url_prefix='/tasks')

task_list = [1,2,3]

@taskRoute.route('/')
def index():

    #operations.create("Task")
    #operations.update(1,"hola")
    #print(operations.getById(2))
    #print(operations.getAll())
    #print(operations.delete(4))
    #print(operations.pagination().items)

    return render_template("tasks/index.html", task_list= task_list)

@taskRoute.route('/create', methods=('GET', 'POST'))
def create():
    task = request.form.get('task')
    if task is not None and task != '':
        task_list.append(task)
        return redirect(url_for('tasks.index'))
    return render_template("tasks/create.html")

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
    del task_list[id]
    return redirect(url_for('tasks.index'))

@taskRoute.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id:int):
    task = request.form.get('task')
    if id is not None:
        if id >= 0 or id <= len(task_list):
            if task is not None and task != '':
                task_list[id] = task
                return redirect(url_for('tasks.index'))

    return render_template("tasks/update.html")