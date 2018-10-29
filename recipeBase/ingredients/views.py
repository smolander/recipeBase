#coding=UTF-8

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from . import ingredients
from .. import db
from ..models import Ingredient


@ingredients.route('/list')
@login_required
def list():
  ingredient_list = Ingredient.query.order_by(Ingredient.name).all()
  return render_template('list.html', item_list=ingredient_list).encode('utf8')

