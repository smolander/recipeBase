#! /usr/bin/env python
#coding=UTF-8
import os

from recipeBase import create_app, db

from recipeBase.models import User, Ingredient, Recipe
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('RB_ENV') or 'dev')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def injectData():
  db.session.add(User(email = "simon.molander@valtech.se", password="asdf"))
  names_units = {u"Mjöl":u"dl", u"Ägg":u"stycken", u"Mjölk":u"dl"}
  for (name, unit) in names_units.items():
    cur_ingredient = Ingredient(name=name, unit=unit)
    db.session.add(cur_ingredient)
  db.session.commit()
  print('Database initialized')

@manager.command
def dropdb():
  if prompt_bool(
    "This will make you lose all your data. Are you sure?"):
    db.drop_all()
    db.create_all()
    print('Database dropped')
    
if __name__ == '__main__':
  manager.run() 