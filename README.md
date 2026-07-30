# Aplicación Web - Gestión de Coches (Flask)

Aplicación web desarrollada con Flask que permite gestionar un listado de coches (CRUD: Crear, Leer, Actualizar, Eliminar).

---

## Estructura del Proyecto

```
Aplicacion-Web/
├── app/
│   ├── __init__.py          # Inicialización de Flask, SQLAlchemy y Flask-Migrate
│   ├── config.py            # Configuración de la app (base de datos, debug, etc.)
│   ├── tasks/
│   │   ├── __init__.py      # Marca el directorio como paquete Python
│   │   ├── controllers.py   # Rutas/endpoints de la aplicación (Blueprint)
│   │   ├── models.py        # Modelo de base de datos (tabla 'coches')
│   │   ├── operations.py    # Lógica de negocio (CRUD contra la base de datos)
│   │   └── forms.py         # Formularios con validación (Flask-WTF)
│   ├── templates/
│   │   ├── base.html        # Plantilla base HTML (layout compartido)
│   │   └── tasks/
│   │       ├── index.html   # Vista del listado de coches
│   │       ├── create.html  # Formulario para crear un coche
│   │       └── update.html  # Formulario para editar un coche
│   └── util/
│       ├── __init__.py
│       └── template_filter.py  # Filtros personalizados para Jinja2
├── migrations/              # Migraciones de base de datos (Flask-Migrate/Alembic)
├── run.py                   # Punto de entrada para ejecutar la aplicación
├── requirements.txt         # Dependencias Python del proyecto
└── README.md
```

---

## Qué hace cada archivo

### `run.py`
Punto de entrada de la aplicación. Importa la instancia de Flask y la ejecuta.

### `app/__init__.py`
Inicializa la aplicación Flask y configura:
- **SQLAlchemy**: ORM para interactuar con la base de datos.
- **Flask-Migrate**: Gestión de migraciones (cambios en el esquema de la BD sin perder datos).
- Registra el Blueprint de rutas (`taskRoute`).

### `app/config.py`
Contiene las clases de configuración:
- **DevelopmentConfig**: Usa SQLite por defecto (sin instalación externa). Incluye opción comentada para MySQL.
- **ProductionConfig**: Para despliegue en producción.

### `app/tasks/models.py`
Define el modelo `Task` que mapea a la tabla `coches` en la base de datos:
- `id`: Clave primaria (entero, autoincremental).
- `model`: Nombre/modelo del coche (texto, máx 255 caracteres).

### `app/tasks/controllers.py`
Define las rutas HTTP usando un Blueprint (`/tasks`):
- `GET /tasks/` → Muestra el listado de coches.
- `GET/POST /tasks/create` → Formulario para crear un coche nuevo.
- `GET /tasks/delete/<id>` → Elimina un coche por ID.
- `GET/POST /tasks/update/<id>` → Formulario para editar un coche.

### `app/tasks/operations.py`
Lógica de negocio que interactúa con la base de datos:
- `getById(id)`: Obtiene un coche por su ID.
- `getAll()`: Obtiene todos los coches.
- `create(name)`: Crea un nuevo coche.
- `update(id, name)`: Actualiza el nombre de un coche.
- `delete(id)`: Elimina un coche.
- `pagination(page, per_page)`: Obtiene coches con paginación.

### `app/tasks/forms.py`
Formulario de Flask-WTF con validación:
- Campo `name`: Obligatorio (validador `InputRequired`).

### `migrations/`
Carpeta gestionada por Flask-Migrate. Contiene las migraciones de la base de datos (historial de cambios en el esquema).

---

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Aplicacion-Web
```

### 2. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activar (Windows CMD)
.\venv\Scripts\activate.bat

# Activar (Linux/Mac)
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Inicializar la base de datos

```bash
flask db upgrade
```

Esto crea la base de datos SQLite (`app.db`) y aplica las migraciones (crea las tablas).

### 5. Ejecutar la aplicación

```bash
python run.py
```

La app estará disponible en: **http://localhost:5000/tasks/**

---

## Configuración de Base de Datos

### SQLite (por defecto)

No requiere instalación externa. Se crea un archivo `app.db` automáticamente. Ideal para desarrollo y pruebas.

### MySQL (opcional)

Si prefieres usar MySQL:

1. Instala MySQL Server en tu máquina.
2. Crea la base de datos:
   ```sql
   CREATE DATABASE concesionario;
   ```
3. Instala el conector Python:
   ```bash
   pip install pymysql
   ```
4. Edita `app/config.py`: comenta la línea de SQLite y descomenta la de MySQL (ajustando usuario y contraseña según tu configuración).
5. Ejecuta las migraciones:
   ```bash
   flask db upgrade
   ```

### Usando variable de entorno

También puedes configurar la base de datos sin tocar el código:

```bash
# Windows PowerShell
$env:DATABASE_URL="mysql+pymysql://usuario:contraseña@localhost:3306/concesionario"

# Linux/Mac
export DATABASE_URL="mysql+pymysql://usuario:contraseña@localhost:3306/concesionario"
```

---

## Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| **Flask** | Framework web (micro-framework Python) |
| **Flask-SQLAlchemy** | ORM para base de datos |
| **Flask-Migrate** | Migraciones de esquema de BD |
| **Flask-WTF** | Formularios con validación |
| **SQLite** | Base de datos por defecto (fichero local) |
| **Jinja2** | Motor de plantillas HTML (incluido con Flask) |

---

## Dependencias principales

```
flask
flask-sqlalchemy
flask-migrate
flask-wtf
pymysql          # Solo necesario si usas MySQL
```


python -c "import sqlite3; conn = sqlite3.connect('instance/app.db'); cursor = conn.execute('SELECT * FROM coches'); print(cursor.fetchall())"
