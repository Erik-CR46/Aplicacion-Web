from app import db
from sqlalchemy.orm import relationship


class Task(db.Model):
    __tablename__ = 'coches'
    id=db.Column(db.Integer, primary_key=True)
    model=db.Column(db.String(255))
    document_id=db.Column(db.Integer, db.ForeignKey('files.id'))
    document = relationship("Document", back_populates="task", foreign_keys=[document_id], uselist=False)

class Document(db.Model):
    __tablename__ = 'files'
    id=db.Column(db.Integer, primary_key=True)
    filename=db.Column(db.String(255))
    extension=db.Column(db.String(10))
    task = relationship("Task", back_populates="document", foreign_keys="Task.document_id", uselist=False)