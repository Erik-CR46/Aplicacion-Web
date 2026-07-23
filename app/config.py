class Config(object):
    pass

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

