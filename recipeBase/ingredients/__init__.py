from flask import Blueprint

ingredients = Blueprint('ingredients', __name__)

from . import views