from flask import Blueprint

recipies = Blueprint('recipies', __name__)

from . import views