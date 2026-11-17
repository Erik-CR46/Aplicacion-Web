import os
from sqlalchemy.orm import session
from app.auth import models
from app import app, db, config, cache


def getById(id: int, show404=False):
    if show404:
        user = db.get_or_404(models.User, id)
    else:
        user = db.session.get(models.User, id)
    return user



def update(id: int, first_name: str, last_name: str, email: str):
    userdb = getById(id=id, show404=True)
    userdb.first_name = first_name
    userdb.last_name = last_name
    userdb.email = email
    db.session.add(userdb)
    db.session.commit()
    db.session.refresh(userdb)
    return userdb

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



def getByIdDocument(id: int, show404=False):
    if show404:
        task = db.get_or_404(models.Document, id)
    else:
        task = db.session.get(models.Document, id)
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

#tags

def addTag(id:int, tag_id:int):
    task = getById(id=id)
    tag = models.Tag.query.get_or_404(tag_id)
    task.tags.append(tag)


    db.session.add(task)
    db.session.commit()
    db.session.refresh(task)

    return task

def removeTag(id:int, tag_id:int):
    task = getById(id=id)
    tag = models.Tag.query.get_or_404(tag_id)
    task.tags.remove(tag)

    db.session.add(task)
    db.session.commit()
    db.session.refresh(task)

    return task


def last_task():
    task = models.Task.query.order_by(models.Task.id.desc()).first()
    return task.id