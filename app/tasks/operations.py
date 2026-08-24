import os
from sqlalchemy.orm import session
from app.tasks import models
from app import app, db, config


def getById(id:int, show404=False):
    if show404:
        task = models.Task.query.get_or_404(id)
    else:    
        task = db.session.query(models.Task).get(id)
    return task

def getAll():
    tasks = db.session.query(models.Task).all()
    return tasks

def create(name:str, brand_id:int=None):
    taskdb = models.Task(model=name, brand_id=brand_id)
    db.session.add(taskdb)
    db.session.commit()
    db.session.refresh(taskdb)
    return taskdb

def update(id:int, name:str, brand_id:int=None, document_id:int=None):
    taskdb = getById(id=id, show404=True)

    taskdb.model = name
    taskdb.brand_id = brand_id

    if document_id is not None:
        taskdb.document_id = document_id

    db.session.add(taskdb)

    db.session.commit()
    db.session.refresh(taskdb)
    return taskdb

def delete(id:int):
    taskdb = getById(id=id, show404=True)
    db.session.delete(taskdb)
    db.session.commit()

def pagination(page:int=1, per_page:int=10):
    return models.Task.query.paginate(page=page, per_page=per_page)


def createDocument(filename:str, extension:str, file=None):
    taskdb = models.Document(filename=filename, extension=extension)
    db.session.add(taskdb)
    db.session.commit()
    db.session.refresh(taskdb)

    if file is not None:
        file.save(os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'], filename))

    return taskdb



def getByIdDocument(id:int, show404=False):
    if show404:
        task = models.Document.query.get_or_404(id)
    else:    
        task = db.session.query(models.Document).get(id)
    return task

def deleteDocument(id:int):
    taskdb = getById(id=id, show404=False)
    document_id = id

    if taskdb is not None and taskdb.document_id is not None:
        document_id = taskdb.document_id

    document = getByIdDocument(id=document_id, show404=False)

    if document is not None:
        file_path = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'], document.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(document)

    if taskdb is not None:
        taskdb.document_id = None
        db.session.add(taskdb)

    db.session.commit()
