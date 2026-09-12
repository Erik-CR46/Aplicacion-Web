import requests

#Get sin auth
#res = requests.get('http://127.0.0.1:5000/api/task')
#print(res)
#print(res.json())

#Get con auth
#res = requests.get('http://127.0.0.1:5000/api/task', headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4OTI1MDE1OSwianRpIjoiZTBmNzVhNDktZWUwNS00NTRmLTkzYWMtOTIxNWU5YjU2NTMxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3ODkyNTAxNTksImNzcmYiOiI3MTk5ZjQzOC1iYTE5LTQ2MmUtYjIwMy1kMTZhYmQ1ZDhmMGMiLCJleHAiOjE3ODkzMzY1NTl9.pbUQkVudc1YzqpxAtusTQy2-oIxoWe5iqfCEbvQgKo0'})
#print(res.json())


#POST
#d = {
#    'model':'maza miata',
#    'brand_id':'4'
#}
#res = requests.post('http://127.0.0.1:5000/api/task', headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4OTI1MDE1OSwianRpIjoiZTBmNzVhNDktZWUwNS00NTRmLTkzYWMtOTIxNWU5YjU2NTMxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3ODkyNTAxNTksImNzcmYiOiI3MTk5ZjQzOC1iYTE5LTQ2MmUtYjIwMy1kMTZhYmQ1ZDhmMGMiLCJleHAiOjE3ODkzMzY1NTl9.pbUQkVudc1YzqpxAtusTQy2-oIxoWe5iqfCEbvQgKo0'}, data=d)
#print(res.json())



#PUT
#d = {
#    'model':'maza',
#    'brand_id':'6'
#    }
#res = requests.put('http://127.0.0.1:5000/api/task/3', headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4OTI1MDE1OSwianRpIjoiZTBmNzVhNDktZWUwNS00NTRmLTkzYWMtOTIxNWU5YjU2NTMxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3ODkyNTAxNTksImNzcmYiOiI3MTk5ZjQzOC1iYTE5LTQ2MmUtYjIwMy1kMTZhYmQ1ZDhmMGMiLCJleHAiOjE3ODkzMzY1NTl9.pbUQkVudc1YzqpxAtusTQy2-oIxoWe5iqfCEbvQgKo0'}, data=d)
#print(res.json())


#DELETE
res = requests.delete('http://127.0.0.1:5000/api/task/3', headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4OTI1MDE1OSwianRpIjoiZTBmNzVhNDktZWUwNS00NTRmLTkzYWMtOTIxNWU5YjU2NTMxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3ODkyNTAxNTksImNzcmYiOiI3MTk5ZjQzOC1iYTE5LTQ2MmUtYjIwMy1kMTZhYmQ1ZDhmMGMiLCJleHAiOjE3ODkzMzY1NTl9.pbUQkVudc1YzqpxAtusTQy2-oIxoWe5iqfCEbvQgKo0'})
print(res.json())