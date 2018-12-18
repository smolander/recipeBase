from sqlalchemy import desc

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from recipeBase import db

class IngredientsRecipeAssociation(db.Model):
  __tablename__ = "ingredient_recipe_association"
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
  ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
  quantity = db.Column(db.Integer)
  recipe = db.relationship("Recipe", back_populates="ingredients")
  ingredient = db.relationship("Ingredient", back_populates="recipies")

  def __repr__(self):
    return str('{} ({} {})'.format(self.ingredient.name, self.quantity, self.ingredient.unit))
  

class Recipe(db.Model):
  __tablename__ = "recipe"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False, index=True)
  instructions = db.Column(db.String)
  cooking_time = db.Column(db.Integer)
  difficulty = db.Column(db.Integer)
  initial_portions = db.Column(db.Integer)
  ingredients = db.relationship('IngredientsRecipeAssociation', back_populates="recipe")

  def __repr__(self):
    return str(self.name)

  def add_ingredient(self, name, quantity):
    ingredient = Ingredient.query.filter_by(name=name).first()

    if ingredient==None:
      return None
    amount = IngredientsRecipeAssociation(quantity=quantity, ingredient=ingredient, recipe=self)
    return amount

  def add_ingredients(self, ingredients_string):
    association_list = []
    ingredient_list = ingredients_string.split(',')
    for ingredient_string in ingredient_list:
      (ingredient_qty, ingredient_name) = ingredient_string.lstrip().split(' ')
      association_list.append(self.add_ingredient(ingredient_name, ingredient_qty))
    
    return association_list



class Ingredient(db.Model):
  __tablename__ = "ingredient"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False, index=True)
  unit = db.Column(db.String)
  recipies = db.relationship('IngredientsRecipeAssociation', back_populates="ingredient")

  def __repr__(self):
    return str('{} ({})'.format(self.name, self.unit))   


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String)

  @property
  def password(self):
    raise AttributeError('password: write-only field')

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  @staticmethod
  def get_by_email(email):
    return User.query.filter_by(email = email).first()

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<User %r>' % self.email