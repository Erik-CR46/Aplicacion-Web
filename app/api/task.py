import json
from flask import abort, request
from flask_restful import Resource
from app.tasks import operations

class TaskApi(Resource):

    def get(self, id=None):
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

        return task.serialize

    def delete(self, id=None):
        task = operations.getById(id)
        if not task:
              abort(400, {'message': 'id not exist'})

        operations.delete(id)
        
        return json.dumps({'message':'Succes'})

class TaskPagination(Resource):

      def get(self, page:int, per_page:int):
              tasks = operations.pagination(page, per_page)
              res = {}
              for task in tasks:
                     res[task.id] = task.serialize
              return res


