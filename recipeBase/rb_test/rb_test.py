#Encoding: UTF-8

from flask import url_for
from flask_testing import TestCase

import recipeBase
from recipeBase.models import User, Recipe
from recipeBase.rb_test.test_helpers import test_helpers

from ..recipies import search_recipe_by_name
import unittest


class RbTestCase(test_helpers):
  def test_not_being_logged_in(self):
    response = self.client.get(url_for('main.logged_in'))
    self.assert_status(response, 302)

  def test_logging_in(self):
    self.make_and_login()
    response = self.client.get(url_for('main.logged_in'))
    self.assert_200(response)
    self.assert_template_used('logged_in.html')
    

  def test_logging_out(self):
    self.make_and_login()
    self.logout()
    response = self.client.get(url_for('main.logged_in'))
    self.assert_status(response, 302)

  def test_listing_ingredients_response(self):
    self.assert_page_response(pagename = 'ingredients.list', templatename = 'list.html')

  def test_listing_ingredients_without_logging_in(self):
    self.assert_page_login_required('ingredients.list')

  def test_litsing_ingredients_with_existing_list(self):
    self.make_and_login()
    self.make_ingredients()

    response = self.client.get(url_for('ingredients.list'))
    checkname = "Ägg"
    self.assertIn(checkname, response.data.decode('utf-8'))

  def test_listing_ingredients_without_list(self):
    self.make_and_login()

    response = self.client.get(url_for('ingredients.list'))
    self.assertIn("Ingredienslistan är tyvärr tom för tillfället", response.data.decode('utf-8'))

  def test_listing_recipies_response(self):
    self.assert_page_response('recipies.list', 'list.html')
    
  def test_listing_recipies_without_login(self):
    self.assert_page_login_required('recipies.list')

  def test_listing_recipies_with_existing_list(self):
    self.make_and_login()
    self.make_recipies()

    response = self.client.get(url_for('recipies.list'))
    print(response.data)
    self.assertIn("Pannkaka", response.data.decode('utf-8'))

  def test_adding_function_in_recipe_model(self):
    self.make_ingredients()
    pancake = Recipe(name=u"Pannkaka",
                    instructions = u"Rör ihop och stek",
                    cooking_time= 45,
                    difficulty = 3,
                    initial_portions = 4
                    )
    
    association_list = []
    association_list.append(pancake.add_ingredient("Ägg", 3))
    association_list.append(pancake.add_ingredient("Mjöl", 2))
    for association in association_list:
      self.assertIn(association, pancake.ingredients)


  def test_multi_adding_function_in_recipe_model(self):
    self.make_ingredients()
    pancake = Recipe(name=u"Pannkaka",
                    instructions = u"Rör ihop och stek",
                    cooking_time= 45,
                    difficulty = 3,
                    initial_portions = 4
                    )

    associations = pancake.add_ingredients("3 Ägg, 2 Mjöl, 4 Mjölk")
    for association in associations:
      self.assertIn(association, pancake.ingredients)
    
    #self.assertFalse(True)

  def test_recipe_display_page_response(self):
    self.assert_page_response('recipies.show', 'recipe_show.html', {"recipe_id": 1})

  def test_recipe_display_page_without_being_logged_in(self):
    self.assert_page_login_required('recipies.show', {"recipe_id": 1})

  def test_recipe_display_page_with_existing_recipe(self):
    self.make_and_login()
    self.make_recipies()

    recipe_id = Recipe.query.first().id
    print(recipe_id)

    response = self.client.get(url_for('recipies.show', recipe_id=recipe_id))

    self.assertIn("Pannkaka", response.data.decode('utf-8'))

    
  def test_recipe_display_page_without_existing_recipe(self):
    self.make_and_login()

    response = self.client.get(url_for('recipies.show', recipe_id=3))

    self.assertIn("Felaktigt recept-id", response.data.decode('utf-8'))

  def test_recipe_search_page_response(self):
    self.assert_page_response('recipies.search', 'recipe_search.html')

  def test_recipe_search_page_without_being_logged_in(self):
    self.assert_page_login_required('recipies.search')

  def test_recipe_search_page_generate_name_field(self):
    self.make_and_login()

    response = self.client.get(url_for('recipies.search'))
    
    self.assertIn("Receptnamn", response.data.decode('utf-8'))

  def test_recipe_search_posting_without_logging_in(self):
    self.make_recipies()

    response = self.client.post(url_for('recipies.search'), data = {'name': 'Pannkaka'})
    self.assert_status(response, 302)

  def test_recipe_search_function(self):
    recipies = self.make_recipies()

    id_from_function = search_recipe_by_name("Pannkaka").id
    id_from_dict = recipies["Pannkaka"].id
    self.assertEquals(id_from_dict, id_from_function)

  def test_recipe_search_with_existing_recipe(self):
    self.make_and_login()
    recipies = self.make_recipies()
    
    response = self.client.post(url_for('recipies.search'), data = {'name': 'Pannkaka'})
    self.assertRedirects(response, url_for('recipies.show', recipe_id=recipies["Pannkaka"].id))

  def test_recipe_search_without_existing_recipe(self):
    self.make_and_login()
    recipies = self.make_recipies()

    response = self.client.post(url_for('recipies.search'), data = {'name': 'Potatisgratäng'})
    self.assert_200
    self.assert_message_flashed("Hittade inte något recept på Potatisgratäng")

  def test_recipe_editor_for_new_recipe_response(self):
    self.assert_page_response('recipies.new', 'recipe_edit.html')

  def test_recipe_editor_for_new_recipe_without_logging_in(self):
    self.assert_page_login_required('recipies.new')

  def test_recipe_editor_for_new_adds_new_recipe(self):
    self.make_and_login()

    recipe = self.get_recipies()["Pannkaka"]

    formdict = recipe.__dict__
    formdict["ingredients"] = "3 Ägg, 2 Mjöl, 4 Mjölk"

    response = self.client.post(url_for('recipies.new'), data=formdict)
    name_list = [recipe.name for recipe in Recipe.query.all()]

    self.assertIn(recipe.name, name_list)

  def test_recipe_editor_for_new_recipe_posting_response(self):
    self.make_and_login()

    recipe = self.get_recipies()["Pannkaka"]

    formdict = recipe.__dict__
    formdict["ingredients"] = "3 Ägg, 2 Mjöl, 4 Mjölk"
    
    response = self.client.post(url_for('recipies.new'), data=formdict)

    db_recipe = Recipe.query.filter(Recipe.name == recipe.name).first()
    
    self.assertRedirects(response, url_for('recipies.show', recipe_id=db_recipe.id))
    