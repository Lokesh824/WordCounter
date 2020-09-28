import os

class Config(object):
    DEBUG = True
    DEVELOPMENT = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''
    REDISTOGO_URL = ""
    QUEUE_NAME = ''
    DEVELOPMENT = False
    DEBUG = False

class DevelopmentConfig(Config):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    databasepath = os.path.join(project_dir,os.path.join('Database','Queue.db'))
    database_file = "sqlite:///{}".format(databasepath)
    SQLALCHEMY_DATABASE_URI = database_file
    REDISTOGO_URL = "redis://localhost:6379"
    QUEUE_NAME = 'WordCountJobs'
    DEBUG = True
    
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''
    REDISTOGO_URL = ""
    QUEUE_NAME = ''
    TESTING = True
