from flask import Blueprint

recipies = Blueprint('recipies', __name__)

from . import views
from .helpers import search_recipe_by_name