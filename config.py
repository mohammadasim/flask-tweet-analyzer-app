import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{username}:{password}@localhost/{database}'.\
    format(username=os.environ.get('PSQL_USER'), password=os.environ.get('PSQL_USER_PASSWORD'),
           database=os.environ.get('PSQL_DB_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS= False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True