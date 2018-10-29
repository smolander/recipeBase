import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

from .config import config_by_name

basedir = os.path.abspath(os.path.dirname(__file__))

#
#app.config['SECRET_KEY'] = '\xcc\xb6\x97\xb6\xcc\xd6h\x05\x89\xd5\xb6\x89\x15\xba\xa4\x1e\x10\xd2\x00\xc4'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'recipeBase.db')
#app.config['DEBUG'] = True
db=SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

toolbar = DebugToolbarExtension()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config_by_name[config_name])
  db.init_app(app)
  login_manager.init_app(app)
  toolbar.init_app(app)

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/auth')

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint, url_prefix='/')

  from .ingredients import ingredients as ingredient_blueprint
  app.register_blueprint(ingredient_blueprint, url_prefix='/ingredients')

  from .recipies import recipies as recipies_blueprint
  app.register_blueprint(recipies_blueprint, url_prefix='/recipies')

  return app

#import models
#import views