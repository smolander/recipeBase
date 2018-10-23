#! /usr/bin/env python

from recipeBase import app, db
from recipeBase.models import User
from flask_script import Manager, prompt_bool

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