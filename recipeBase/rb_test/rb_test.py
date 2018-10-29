#Encoding: UTF-8

from flask import url_for
from flask_testing import TestCase

import recipeBase
from recipeBase.models import User
from recipeBase.rb_test.test_helpers import test_helpers


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
    self.make_and_login()
  
    response = self.client.get(url_for('ingredients.list'))
    self.assert_200(response)
    self.assert_template_used('list.html')

  def test_listing_ingredients_without_logging_in(self):
    response = self.client.get(url_for('ingredients.list'))
    self.assert_status(response, 302)

  def test_litsing_ingredients_with_existing_list(self):
    self.make_and_login()
    self.make_ingredients()

    response = self.client.get(url_for('ingredients.list'))
    self.assertIn("Ägg", response.data)

  def test_listing_ingredients_without_list(self):
    self.make_and_login()

    response = self.client.get(url_for('ingredients.list'))
    self.assertIn("Ingredienslistan är tyvärr tom för tillfället", response.data)

  def test_listing_recipies_response(self):
    self.make_and_login()

    response = self.client.get(url_for('recipies.list'))
    self.assert_200(response)
    self.assert_template_used('list.html')

  def test_listing_recipies_without_login(self):
    response = self.client.get(url_for('recipies.list'))
    self.assert_status(response, 302)

  def test_listing_recipies_with_existing_list(self):
    self.make_and_login()
    self.make_recipies()

    response = self.client.get(url_for('recipies.list'))
    print(response.data)
    self.assertIn("Pannkaka", response.data)
