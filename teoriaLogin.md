# Teoria del login con Flask y Flask-Login

## 1. Objetivo

La idea es anadir autenticacion de usuarios a la aplicacion Flask. Para conseguirlo hemos separado el trabajo en varias piezas:

1. Un modelo `User` para representar usuarios en la base de datos.
2. Funciones para guardar contrasenas de forma segura y comprobarlas.
3. Un `LoginManager` para que Flask-Login controle las sesiones.
4. Un controlador de autenticacion agrupado en un `Blueprint`.
5. Un cargador de usuarios para recuperar el usuario guardado en la sesion.
6. Una variable `g.user` para tener disponible el usuario actual durante cada peticion.

La aplicacion se conecta juntando todas estas piezas desde `app/__init__.py`.

## 2. Dependencias

En `app/auth/models.py` usamos Werkzeug:

```python
from werkzeug.security import generate_password_hash, check_password_hash
```

Estas funciones sirven para no guardar la contrasena original:

- `generate_password_hash(password)` crea un hash a partir de la contrasena.
- `check_password_hash(hash, password)` comprueba una contrasena contra el hash guardado.

Tambien usamos Flask-Login en el controlador:

```python
from flask_login import current_user
```

`current_user` representa al usuario que Flask-Login ha identificado en la peticion actual.

## 3. El modelo User

En `app/auth/models.py` creamos la clase:

```python
class User(db.Model):
```

Al heredar de `db.Model`, `User` se convierte en un modelo de SQLAlchemy y representa una tabla de la base de datos.

Sus campos son:

```python
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(80), unique=True, nullable=False)
pwhash = db.Column(db.String(128), nullable=False)
```

- `id`: identificador unico del usuario.
- `username`: nombre del usuario. No puede repetirse.
- `pwhash`: hash de la contrasena. No guardamos la contrasena original.

## 4. Crear un usuario y proteger su contrasena

El constructor recibe el nombre y la contrasena:

```python
def __init__(self, username, password):
    self.username = username
    self.pwhash = generate_password_hash(password)
```

Cuando se crea un objeto `User`, la contrasena se transforma inmediatamente en un hash. Por ejemplo, si la contrasena es `secreto`, en la base de datos no deberia guardarse literalmente `secreto`, sino un valor generado por Werkzeug.

Para verificarla creamos:

```python
def check_password(self, password):
    return check_password_hash(self.pwhash, password)
```

Durante el login se recibe una contrasena escrita por el usuario y se compara con `self.pwhash`. El resultado es `True` si coincide y `False` si no coincide.

## 5. Metodos que necesita Flask-Login

Flask-Login necesita que el modelo de usuario exponga ciertos metodos y propiedades.

### `is_authenticated`

```python
@property
def is_authenticated(self):
    return True
```

Indica si el usuario ha sido autenticado. Para un objeto `User` valido devolvemos `True`.

### `is_active`

```python
@property
def is_active(self):
    return True
```

Indica que la cuenta esta activa y puede iniciar o mantener una sesion. En el futuro se podria conectar a un campo de base de datos para desactivar cuentas.

### `is_anonymous`

```python
@property
def is_anonymous(self):
    return False
```

Indica que el objeto representa a un usuario real y no a un usuario anonimo.

### `get_id`

```python
def get_id(self):
    return str(self.id)
```

Devuelve el identificador del usuario como texto. Flask-Login guarda este identificador en la sesion y lo utilizara en las siguientes peticiones.

## 6. Crear el LoginManager

En `app/__init__.py` importamos la clase:

```python
from flask_login import LoginManager
```

El objetivo es crear y conectar el gestor de sesiones con la aplicacion:

```python
login_manager = LoginManager()
login_manager.init_app(app)
```

`login_manager` es el objeto que coordina Flask-Login. Se encarga de saber si existe una sesion, cargar al usuario y ofrecer el objeto `current_user`.

En el estado actual del proyecto estas dos lineas aparecen comentadas:

```python
#login_manager = LoginManager()
#login_manager.init_app(app)
```

Por eso, antes de ejecutar el login, hay que activarlas. El controlador importa `login_manager` desde `app`, asi que debe existir antes de importar `app.auth.controllers`.

## 7. Crear el Blueprint de autenticacion

En `app/auth/controllers.py` creamos un grupo de rutas para autenticacion:

```python
authRoute = Blueprint('auth', __name__)
```

Esto prepara un blueprint llamado `auth`. Un blueprint permite mantener separado el codigo de autenticacion del codigo de tareas.

Todavia no crea por si solo una pagina de login. Para crear una ruta habria que escribir, por ejemplo:

```python
@authRoute.route('/login')
def login():
    return 'Pagina de login'
```

## 8. Cargar el usuario desde la sesion

Flask-Login necesita saber como transformar el identificador guardado en la sesion en un objeto `User`.

Para eso usamos:

```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

El funcionamiento es:

1. El usuario inicia sesion.
2. Flask-Login guarda su `id` en la sesion.
3. En una peticion posterior, Flask-Login obtiene ese `id`.
4. Ejecuta `load_user(user_id)`.
5. La funcion busca el usuario en la tabla mediante `User.query.get(...)`.
6. El resultado queda disponible como `current_user`.

## 9. Copiar el usuario actual a `g.user`

Tambien registramos una funcion antes de cada peticion del blueprint:

```python
@authRoute.before_request
def get_current_user():
    g.user = current_user
```

El decorador `@authRoute.before_request` indica que la funcion debe ejecutarse antes de las rutas pertenecientes a `authRoute`.

Dentro de la funcion copiamos `current_user` a `g.user`:

- `current_user` lo proporciona Flask-Login.
- `g` es un objeto temporal de Flask para guardar datos durante una peticion.
- `g.user` permite acceder al usuario actual desde otras partes de la aplicacion durante esa peticion.

La forma correcta necesita el simbolo `@`. Escribir solamente `authRoute.before_request` no registra la funcion.

## 10. Registrar los blueprints en la aplicacion

En `app/__init__.py` importamos los controladores:

```python
from app.auth.controllers import authRoute
from app.tasks.controllers import taskRoute
```

Despues registramos los blueprints:

```python
app.register_blueprint(taskRoute)
app.register_blueprint(authRoute)
```

Esto le dice a Flask que active las rutas que cada blueprint tenga definidas.

La separacion queda asi:

```text
app/__init__.py
    crea la aplicacion y conecta las extensiones
            |
            +-- auth/controllers.py
            |       crea authRoute y carga usuarios
            |
            +-- auth/models.py
            |       define User y sus datos
            |
            +-- tasks/controllers.py
                    contiene las rutas de tareas
```

## 11. Flujo completo previsto

Cuando el sistema de login este terminado, el flujo sera:

```text
Usuario escribe username y password
        |
        v
La ruta /login busca el User por username
        |
        v
check_password(password) comprueba el hash
        |
        v
Flask-Login inicia la sesion del usuario
        |
        v
Se guarda el id del usuario en la sesion
        |
        v
En cada peticion load_user recupera el objeto User
        |
        v
current_user y g.user representan al usuario actual
```

## 12. Puntos pendientes

Esta es la parte construida hasta ahora. Para completar el login aun faltaria:

- Activar `LoginManager` en `app/__init__.py`.
- Crear una ruta y un formulario para iniciar sesion.
- Buscar el usuario por `username`.
- Usar `check_password` para comprobar la contrasena.
- Llamar a `login_user(user)` cuando las credenciales sean correctas.
- Crear una ruta de logout usando `logout_user()`.
- Proteger las rutas privadas con `@login_required`.
- Crear las migraciones necesarias para la tabla de usuarios.

Tambien conviene revisar el nombre de la tabla del modelo. SQLAlchemy usa normalmente:

```python
__tablename__ = 'users'
```

El codigo actual utiliza `table_name`, que no es la convencion reconocida por SQLAlchemy para fijar el nombre de la tabla.
