from sqlalchemy import desc

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from recipeBase import db

class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  instructions = db.Column(db.String)

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