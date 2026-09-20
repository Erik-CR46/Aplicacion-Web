from app.tasks import operations
from flask_jwt_extended import create_access_token
from app.auth.models import User

def test_index(app, client):
    with app.app_context():
        response = client.get('/api/task')
        assert response.status_code == 200

        tasks = operations.getAll()
        for i in range(len(tasks)):
            assert tasks[i].name == response.get_json()[i]['name']

def test_index_detail(app, client):
    with app.app_context():
        lastTask = operations.last_task()
        response = client.get(f'/api/task/{str(lastTask)}')
        assert response.status_code == 200

        task = operations.getById(lastTask)
        assert task.model == response.get_json()['model']
        assert task.id == response.get_json()['id']

def test_create(app, client):

    with app.app_context():
        tokenAuth = create_access_token(identity=str(User.query.filter_by(username='admin').first().id))
        
        header = {
            'Authorization':f'Bearer {tokenAuth}'
        }
        taskCount = len(operations.getAll())
        data_api = {
                "model":"prueba Unitaria Api",
                "brand_id": 8,
            }

        response = client.post('/api/task', data=data_api, headers=header)
        assert response.status_code == 200

        response = client.get('/api/task', headers=header)
        assert data_api['model'] in response.get_data(as_text=True)
        assert len(operations.getAll()) == taskCount + 1

def test_update(app, client):

    with app.app_context():
        tokenAuth = create_access_token(identity=str(User.query.filter_by(username='admin').first().id))
        
        header = {
            'Authorization':f'Bearer {tokenAuth}'
        }

        id_task = operations.last_task()
        data_api = {
                "model":"prueba Unitaria Api Super Nueva",
                "brand_id": id_task,
            }

        response = client.put(f'/api/task/{str(id_task)}', data=data_api, headers=header)
        assert response.status_code == 200

        response = client.get('/api/task', headers=header)
        assert data_api['model'] in response.get_data(as_text=True)


def test_delete(app, client):

    with app.app_context():
        tokenAuth = create_access_token(identity=str(User.query.filter_by(username='admin').first().id))
        
        header = {
            'Authorization':f'Bearer {tokenAuth}'
        }

        id_task = operations.last_task()

        response = client.delete(f'/api/task/{str(id_task)}', headers=header)
        assert response.status_code == 200

        response = client.get('/api/task', headers=header)
        assert str(id_task) not in response.get_data(as_text=True)