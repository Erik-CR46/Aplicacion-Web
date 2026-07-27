import os

class Config(object):
    pass

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:P%40ssw0rd@localhost:3306/concesionario'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

