from app import db
from sqlalchemy import table
from sqlalchemy.orm import relationship


#Tables

task_tags = db.Table('task_tags',db.Column('task_id', db.Integer, db.ForeignKey('coches.id'), primary_key=True),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True))

#Models
class Task(db.Model):
    __tablename__ = 'coches'
    id=db.Column(db.Integer, primary_key=True)
    model=db.Column(db.String(255))

    document_id=db.Column(db.Integer, db.ForeignKey('files.id'))
    document = relationship("Document", lazy="joined")

    brand_id=db.Column(db.Integer, db.ForeignKey('brands.id'))
    brand = relationship("Brand", lazy="joined")

    tags = relationship("Tag", secondary=task_tags)

    @property
    def serialize(self):
        return {
            'id':self.id,
            'model':self.model,
            'brand':self.brand.name,
            'tags': [tag.name for tag in self.tags],
        }

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

    @property
    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
        }

class Tag(db.Model):
    __tablename__ = 'tags'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))

    #tasks = relationship("Task", secondary=task_tags)