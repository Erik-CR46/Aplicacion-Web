import json
from flask import abort
from flask_restful import Resource, reqparse
from app.tasks.models import  Brand
from app import db

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help='Name cannot be blank!')

class BrandArgApi(Resource):

       def get(self, id=None):
              if not id:
                     res = {}
                     for brand in Brand.query.all():
                            res[brand.id] = brand.serialize
                     return res
              else:
                     brand = Brand.query.get(id)
                     if not brand:
                            abort(404)
              
                     return brand.serialize

       def post(self, id=None):
              args = parser.parse_args()

              if len(args['name']) < 3:
                     abort(403, {'message':'Name not valid'})
              brand = Brand()
              brand.name = args['name']
              db.session.add(brand)
              db.session.commit()
              db.session.refresh(brand)

              return brand.serialize 
       

       def put(self, id=None):
              brand = Brand.query.get(id)
              if not brand:
                     abort(404, {'message':'Brand not exist'})
              args = parser.parse_args()

              if len(args['name']) < 3:
                     abort(403, {'message':'Name not valid'})

              brand.name = args['name']
              db.session.add(brand)
              db.session.commit()
              db.session.refresh(brand)

              return brand.serialize


       def delete(self, id=None):
              brand = Brand.query.get(id)
              if not brand:
                     abort(400, {'message': 'id not exist'})

              db.session.delete(brand)
              db.session.commit()
                            
              return json.dumps({'message':'Succes'})

