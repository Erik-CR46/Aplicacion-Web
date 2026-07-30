import os

# Ruta base del proyecto (donde está run.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config(object):
    """Configuración base compartida por todos los entornos."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    """
    Configuración para desarrollo.

    BASE DE DATOS:
    - Por defecto usa SQLite (no requiere instalar nada).
    - Si prefieres usar MySQL, comenta la línea de SQLite y descomenta la de MySQL.
      Para MySQL necesitas:
        1. Tener MySQL Server instalado y corriendo.
        2. Crear la base de datos: CREATE DATABASE concesionario;
        3. Ajustar usuario/contraseña en la URI.
        4. Instalar el conector: pip install pymysql
    """
    DEBUG = True

    # --- Opción 1: SQLite (por defecto, no requiere instalación externa) ---
    # El archivo app.db se crea en la carpeta instance/ del proyecto
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'app.db')
    )

    # --- Opción 2: MySQL (descomentar si tienes MySQL instalado) ---
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'DATABASE_URL',
    #     'mysql+pymysql://root:P%40ssw0rd@localhost:3306/concesionario'
    # )
    SECRET_KEY='P@ssw0rd'
    #WTF_CSRF_ENABLED = False

