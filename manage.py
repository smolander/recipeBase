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
  
  pancake = Recipe(name=u"Pannkaka",
                    instructions = u"Rör ihop och stek",
                    cooking_time= 45,
                    difficulty = 3,
                    initial_portions = 4
                    )

  ingredient_list = [{"name": "Mjöl", "unit": "dl", "quantity": 2},
                    {"name": "Ägg", "unit": "stycken", "quantity": 3},
                    {"name": "Mjölk", "unit": "dl", "quantity": 4}]

  
  for ingredient in ingredient_list:
    cur_ingredient = Ingredient(name=ingredient["name"], unit=ingredient["unit"])
    db.session.add(cur_ingredient)
    pancake.add_ingredient(name=ingredient["name"], quantity=ingredient["quantity"])

  db.session.add(pancake)
  
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