import json
from app import config
from flask import abort, request
from flask_restful import Resource
from app.tasks import operations
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

class TaskApi(Resource):
       @jwt_required()
       def get(self, id=None):

              #user_id = get_jwt_identity()
              #print(user_id) Para obtener el id del usuario al que pertenezca ese token
              
              if not id:
                     tasks = operations.getAll()
                     res = {}
                     for task in tasks:
                            res[task.id] = task.serialize
              else:
                     task = operations.getById(id)
                     res = task.serialize
                     if not task:
                            abort(404)
                     
#El json.dumps sirve para transformar un objeto de python en diccionario, en este caso no es necesario
#res = json.dumps({ 
#        'name' : task.model,
#        'category' : task.brand.name,
#}) 
              return res

       def post(self, id=None):
              if not request.form:
                     abort(403, {'message':'Not parameters'})

              if not 'model' in request.form:
                     abort(403, {'message':'Model not valid'})

              if not 'brand_id' in request.form:
                     abort(403, {'message':'Brand not valid'})

              try:
                     int(request.form['brand_id'])
              except:
                     abort(403, {'message':'Brand not valid'})

              task= operations.create(request.form['model'], request.form['brand_id'])

              return task.serialize

       def put(self, id=None):
              if not operations.getById(id):
                     abort(400, {'message': 'id not exist'})
              if not request.form:
                     abort(403, {'message':'Not parameters'})

              if not 'model' in request.form:
                     abort(403, {'message':'Model not valid'})

              if not 'brand_id' in request.form:
                     abort(403, {'message':'Brand not valid'})

              try:
                     int(request.form['brand_id'])
              except:
                     abort(403, {'message':'Brand not valid'})

              task= operations.update(id, request.form['model'], request.form['brand_id'])

              f = request.files.get('file')
              if  f and config.allowed_extensions_name(f.filename):
                     filename = secure_filename(f.filename)
                     document = operations.createDocument(filename=filename, extension=filename.split('.')[-1], file=f)
                     operations.update(id, task.model, task.brand_id, document.id)

              

              return task.serialize

       def delete(self, id=None):
              task = operations.getById(id)
              if not task:
                     abort(400, {'message': 'id not exist'})

              operations.delete(id)
              
              return json.dumps({'message':'Succes'})

class TaskPagination(Resource):
           
       @jwt_required()
       def get(self, page:int, per_page:int):
              tasks = operations.pagination(page, per_page)
              res = {}
              for task in tasks:
                     res[task.id] = task.serialize
              return res


