import json
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.tasks.models import  Tag
from app import db

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help='Name cannot be blank!')

tags_fields = {
       'id':fields.Integer,
       'name':fields.String,
}

class TagArgApi(Resource):

       @marshal_with(tags_fields)
       def get(self, id=None):
              if not id:
                     return Tag.query.all()
              else:
                     tag = Tag.query.get(id)
                     if not tag:
                            abort(404)
              
                     return tag
              
       @marshal_with(tags_fields)
       def post(self, id=None):
              args = parser.parse_args()

              if len(args['name']) < 3:
                     abort(403, {'message':'Name not valid'})
              tag = Tag()
              tag.name = args['name']
              db.session.add(tag)
              db.session.commit()
              db.session.refresh(tag)

              return tag
       
       @marshal_with(tags_fields)
       def put(self, id=None):
              tag = Tag.query.get(id)
              if not tag:
                     abort(404, {'message':'Brand not exist'})
              args = parser.parse_args()

              if len(args['name']) < 3:
                     abort(403, {'message':'Name not valid'})

              tag.name = args['name']
              db.session.add(tag)
              db.session.commit()
              db.session.refresh(tag)

              return tag


       def delete(self, id=None):
              tag = Tag.query.get(id)
              if not tag:
                     abort(400, {'message': 'id not exist'})

              db.session.delete(tag)
              db.session.commit()
                            
              return json.dumps({'message':'Succes'})

