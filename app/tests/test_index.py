import json

def test_index(app, client): #app y client hacen referencia a confitest
    response=client.get('/') #Miramos la respuesta de esta ruta
    assert response.status_code == 200 #Comprobamos que su status sea 200
    expected ={'hello':'world'} #El texto que deberia esperar
    assert expected == json.loads(response.get_data(as_text=True)) #Comparamos