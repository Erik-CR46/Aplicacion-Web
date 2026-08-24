from app import db
from sqlalchemy.orm import relationship


class Task(db.Model):
    __tablename__ = 'coches'
    id=db.Column(db.Integer, primary_key=True)
    model=db.Column(db.String(255))

    document_id=db.Column(db.Integer, db.ForeignKey('files.id'))
    document = relationship("Document", lazy="joined")

    brand_id=db.Column(db.Integer, db.ForeignKey('brands.id'))
    brand = relationship("Brand", lazy="joined")

class Document(db.Model):
    __tablename__ = 'files'
    id=db.Column(db.Integer, primary_key=True)
    filename=db.Column(db.String(255))
    extension=db.Column(db.String(10))
    task = relationship("Task", back_populates="document", foreign_keys="Task.document_id", uselist=False)

class Brand(db.Model):
    __tablename__ = 'brands'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))