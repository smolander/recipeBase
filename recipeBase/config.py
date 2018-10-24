import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = '\xcc\xb6\x97\xb6\xcc\xd6h\x05\x89\xd5\xb6\x89\x15\xba\xa4\x1e\x10\xd2\x00\xc4'
  DEBUG = False
  

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'recipeBase.db')

class TestingConfig(Config):
  TESTING = True
  WTF_CSRF_ENABLED = False
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
  DEBUG = False
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'recipeBase.db')

config_by_name = dict(
  dev = DevelopmentConfig,
  test = TestingConfig,
  prod = ProductionConfig
)