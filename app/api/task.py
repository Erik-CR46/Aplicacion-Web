import json
from flask import abort
from flask_restful import Resource
from app.tasks import operations

class TaskApi(Resource):

    def get(self, id=None):

        if not id:
                tasks = operations.getAll()
                res = {}
                for task in tasks:
                        res[task.id] = {
                                'name': task.model,
                                'brand': task.brand.name if task.brand else None,
                        }
        else:
                task = operations.getById(id)
                if not task:
                       abort(404)

                #El json.dumps sirve para transformar un objeto de python en diccionario, en este caso no es necesario
                res = json.dumps({ 
                        'name' : task.model,
                        'category' : task.brand.name,
                }) 
              
        return res

    def post(self, id=None):
            return 'This is a POST response'

    def put(self, id=None):
            return 'This is a PUT response'

    def delete(self, id=None):
            return 'This is a DELETE response'
              