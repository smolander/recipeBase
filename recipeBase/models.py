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
  

class Recipe(db.Model):
  __tablename__ = "recipe"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False, index=True)
  instructions = db.Column(db.String)
  cooking_time = db.Column(db.Integer)
  difficulty = db.Column(db.Integer)
  initial_portions = db.Column(db.Integer)
  ingredients = db.relationship('IngredientsRecipeAssociation', back_populates="recipe")

  def addIngredient(self, name, quantity):
    
    if not ingredient = Ingredient.query.filter_by(name=name).first():
      return None
    amount = IngredientsRecipeAssociation(quantity=quantity, ingredient=ingredient, recipe=self)



class Ingredient(db.Model):
  __tablename__ = "ingredient"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False, index=True)
  unit = db.Column(db.String)
  recipies = db.relationship('IngredientsRecipeAssociation', back_populates="ingredient")

  def __unicode__(self):
    return '{} ({})'.format(self.name, self.unit)

  def __repr__(self):
    return self.__unicode__().encode('utf-8')
    


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