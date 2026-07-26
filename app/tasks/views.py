from flask import render_template, request, redirect, url_for
from flask.views import View
from app import app

task_list = [1, 2, 3]

class ListView(View):
    init_every_request = False

    def __init__(self, template):
        self.template = template

    def dispatch_request(self):
        return render_template(self.template, task_list=task_list)

class CreateView(View):
    methods = ['GET', 'POST']
    init_every_request = False

    def __init__(self, template):
        self.template = template

    def dispatch_request(self):
        task = request.form.get('task')
        if task is not None and task != '':
            task_list.append(task)
            return redirect(url_for('tasks.index'))
        return render_template(self.template, task_list=task_list)

class UpdateView(View):
    methods = ['GET', 'POST']
    init_every_request = False

    def __init__(self, template):
        self.template = template

    def dispatch_request(self, id):
        task = request.form.get('task')
        if id is not None:
            if id >= 0 or id <= len(task_list):
                if task is not None and task != '':
                    task_list[id] = task
                    return redirect(url_for('tasks.index'))

        return render_template(self.template)

class DeleteView(View):
    methods = ['GET', 'POST']
    init_every_request = False

    def __init__(self, template):
        self.template = template

    def dispatch_request(self, id):
        del task_list[id]
        return redirect(url_for('tasks.index'))

app.add_url_rule('/tasks/', view_func=ListView.as_view('tasks.index', 'tasks/index.html'))
app.add_url_rule('/tasks/create', view_func=CreateView.as_view('tasks.create', 'tasks/create.html'))
app.add_url_rule('/tasks/update/<int:id>', view_func=UpdateView.as_view('tasks.update', 'tasks/update.html'))
app.add_url_rule('/tasks/delete/<int:id>', view_func=DeleteView.as_view('tasks.delete', 'tasks/delete.html'))