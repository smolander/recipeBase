# coding=UTF-8

from flask import url_for
from flask_testing import TestCase

import recipeBase
from recipeBase.models import User, Ingredient, Recipe,\
    IngredientsRecipeAssociation


class test_helpers(TestCase):
  def make_and_login(self):
    logged_in_user = User(email = 'tester@test.com', password = '345pwd')
    self.db.session.add(logged_in_user)
    self.login(email = logged_in_user.email, password = '345pwd')

  
  def login(self, email, password):
    return self.client.post(url_for('auth.login'), data=dict(
        email = email, 
        password = password
      ), follow_redirects=True)

  def logout(self):
    return self.client.get(url_for('auth.logout'), follow_redirects=True)

  def make_ingredients(self):
    for cur_ingredient in self.generate_ingredients_list():
      self.db.session.add(cur_ingredient)

  def generate_ingredients_list(self):
    ingredient_list = []
    names_units = {u"Mjöl":u"dl", u"Ägg":u"stycken", u"Mjölk":u"dl"}
    for (name, unit) in list(names_units.items()):
      cur_ingredient = Ingredient(name=name, unit=unit)
      ingredient_list.append(cur_ingredient)
    return ingredient_list

  def get_recipies(self):
    pancake = Recipe(name=u"Pannkaka",
                    instructions = u"Rör ihop och stek",
                    cooking_time= 45,
                    difficulty = 3,
                    initial_portions = 4
                    )

    waffle = Recipe(name=u"Våffla",
                    instructions = u"Rör ihop och häll i våffeljärn",
                    cooking_time= 45,
                    difficulty = 3,
                    initial_portions = 4
                    )
    
    amount_dict_pancake = {u"Mjöl": 2,
                    u"Ägg": 3,
                    u"Mjölk": 4}
    
    amount_dict_waffle = {"Mjöl": 3,
                        "Ägg": 2,
                        "Mjölk": 4}

    ingredients = self.generate_ingredients_list()

    for ingredient in ingredients:
      pancake.add_ingredient(name=ingredient.name, quantity=amount_dict_pancake[ingredient.name])
      waffle.add_ingredient(name=ingredient.name, quantity=amount_dict_waffle[ingredient.name])

    return {"Pannkaka": pancake, "Våffla": waffle}


  def make_recipies(self):
    
    recipe_dict = self.get_recipies()
   
    for recipe in recipe_dict.values():
      self.db.session.add(recipe)

    return recipe_dict

  def assert_page_response(self, pagename, templatename, arg_dict={}):
    self.make_and_login()
  
    response = self.client.get(url_for(pagename, **arg_dict))
    self.assert_200(response)
    self.assert_template_used(templatename)

  def assert_page_login_required(self, pagename, arg_dict={}):
    response = self.client.get(url_for(pagename, **arg_dict))
    self.assert_status(response, 302)
  
  def create_app(self):
    return recipeBase.create_app('test')

  def setUp(self):
    self.db = recipeBase.db
    self.db.create_all()
    self.client = self.app.test_client()

  def tearDown(self):
    recipeBase.db.session.remove()
    recipeBase.db.drop_all()
