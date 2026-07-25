from flask import Blueprint, render_template, request

taskRoute = Blueprint('tasks', __name__, url_prefix='/tasks')

task_list = [1,2,3]

@taskRoute.route('/')
def index():
    return render_template("tasks/index.html", task_list= task_list)

@taskRoute.route('/create', methods=('GET', 'POST'))
def create():
    task = request.form.get('task')
    if task is not None:
        task_list.append(task)
    return render_template("tasks/create.html")

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
    return 'Delete ' + str(id) 

@taskRoute.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id:int):
    task = request.form.get('task')
    if id >= 0 or id <= len(task_list):
        task_list[id] = task
    return render_template("tasks/update.html")