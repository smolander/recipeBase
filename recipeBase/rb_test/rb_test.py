from flask import url_for
from flask_testing import TestCase

import recipeBase
from recipeBase.models import User

class RbTestCase(TestCase):

  def create_app(self):
    return recipeBase.create_app('test')

  def setUp(self):
    self.db = recipeBase.db
    self.db.create_all()
    self.client = self.app.test_client()

    logged_in_user = User(email = 'tester@test.com', password = '345pwd')

    self.db.session.add(logged_in_user)

    self.client.post(url_for('auth.login'), data=dict(email = logged_in_user.email, password = '345pwd'))

    print("setup done!")

  def tearDown(self):
    recipeBase.db.session.remove()
    recipeBase.db.drop_all()

  def test_if_logged_in(self):
    response = self.client.get(url_for('main.logged_in'))

    assert response.status_code == 200