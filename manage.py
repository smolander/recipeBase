#! /usr/bin/env python
import os

from recipeBase import create_app, db

from recipeBase.models import User
from flask_script import Manager, prompt_bool

app = create_app(os.getenv('RB_ENV') or 'dev')
manager = Manager(app)

@manager.command
def initdb():
  db.create_all()
  db.session.add(User(email = "simon.molander@valtech.se", password="asdf"))
  db.session.commit()
  print('Database initialized')

@manager.command
def dropdb():
  if prompt_bool(
    "This will make you lose all your data. Are you sure?"):
    db.drop_all()
    print('Database dropped')
    
if __name__ == '__main__':
  manager.run() 