from app import db

class Task(db.Model):
    __tablename__ = 'coches'
    id=db.Column(db.Integer, primary_key=True)
    model=db.Column(db.String(255))
    

