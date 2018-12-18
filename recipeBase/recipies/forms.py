from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, BooleanField, SubmitField, TextAreaField
from wtforms_components import IntegerField
from ..models import Recipe

class SearchForm(Form):
  name = StringField('Receptnamn:')
  submit = SubmitField('Sök')

class EditForm(Form):
  name = StringField('Receptnamn:')
  ingredients = StringField('Ingredienser:')
  cooking_time = IntegerField('Tillagningstid: ')
  difficulty = IntegerField('Svårighetsgrad (1-10):')
  instructions = TextAreaField('Instruktioner:')
  initial_portions = IntegerField('Skalat för:')
  submit = SubmitField('Spara')


