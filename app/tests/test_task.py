from app.tasks import operations

def test_create(app, client):

    #Get
    response = client.get('/tasks/create')
    assert response.status_code == 200

    # response contiene la respuesta HTTP que devuelve Flask.
    # get_data() obtiene el HTML de la respuesta en formato bytes.
    # El prefijo b convierte el HTML esperado también en bytes.
    # in comprueba que este campo exista dentro de todo el HTML,
    # sin exigir que sea el contenido completo de la respuesta.
    assert b'<input id="name" name="name" required type="text" value="">' in response.get_data()

    #Lo mismo pero pasando los bytes a texto
    #assert '<input id="name" name="name" required type="text" value="">' in response.get_data(as_text=True)


    #Post
    dataform = { #Primero creamos una variable con la nueva task que queremos crear
        'name':'jose',
        'brand':'54'
    }



    with app.app_context():
        taskCount = len(operations.getAll())
        response = client.post('/tasks/create', data=dataform)
        assert response.status_code == 302

        response = client.get('/tasks/')
        assert dataform.get('name') in response.get_data(as_text=True)
        assert len(operations.getAll()) == taskCount + 1

def test_update(app, client):

    dataform = {
        'name':'Alfredo',
        'brand':'8',
    }

    with app.app_context():
        #Get
        task = operations.getById(1)
        response = client.get(f'/tasks/update/{task.id}')
        assert response.status_code == 200

        response = client.post(f'/tasks/update/{task.id}', data=dataform)
        assert response.status_code == 302

        response = client.get('/tasks/')
        assert dataform.get('name') in response.get_data(as_text=True)


def test_index(app, client, auth):
    # `auth` y `client` son fixtures definidos en conftest.py.
    # El login es necesario porque la ruta /tasks/ está protegida.
    auth.login()

    # Simula una petición GET del navegador a la lista de tareas.
    response = client.get('/tasks/')

    # La vista debe responder correctamente y no redirigir al login.
    assert response.status_code == 200

    with app.app_context():
        # Accedemos directamente a la base de datos para conocer
        # qué tareas deberían aparecer en la respuesta HTML.
        tasks = operations.getAll()

        # La plantilla index.html genera un <li> por cada tarea.
        for task in tasks:
            expected_html = f'<li>{task.model}</li>'
            assert expected_html in response.get_data(as_text=True)


def test_delete(app, client):
    
    dataform = {
        'name':'Alfredo',
        'brand':'8',
    }

    with app.app_context():
        task_count = len(operations.getAll())

        if task_count == 0:
            response = client.post('/tasks/create', data=dataform)
            assert response.status_code == 302
            task_count = len(operations.getAll())

        task_id = operations.last_task()

        response = client.get(f'/tasks/delete/{task_id}')
        assert response.status_code == 302
        assert len(operations.getAll()) == task_count - 1




