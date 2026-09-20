import pytest
from app import app as flask_app #Importamos la app de Flask para poder usarla en los tests
from app.config import TestingConfig

# El nombre conftest.py es especial: pytest lo busca automáticamente.
# Por eso sus fixtures pueden usarse en los tests sin importarlos.
# Estos fixtures están disponibles para los tests de esta carpeta y sus subcarpetas.


@pytest.fixture # Indicamos que es una función con entorno preparado para los tests.
def app(): #Creamos un fixture llamado app
    yield flask_app #Devolvemos la instancia de la aplicacion para que los tests la puedan usar
    
@pytest.fixture
def client(app): #Creamos otro fixture llamado client que depende de app
    app.config.from_object(TestingConfig)
    yield app.test_client() #Devolvemos un cliente de prueba para hacer peticiones HTTP a la app sin levantar el servidor

#yield es una forma de crear un “fixture” que se prepara antes del test y se limpia después.

#LOGIN
class AuthActions(object):
    def __init__(self, client):
        self.client = client

    def login(self, username='admin', password='admin'):
        return self.client.post('/login', data={'username':username, 'password':password})

    def logout(self):
        return self.client.get('/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client) 