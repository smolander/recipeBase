#coding=UTF-8

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from . import recipies
from .. import db
from ..models import Recipe


@recipies.route('/list')
@login_required
def list():
  recipe_list = Recipe.query.order_by(Recipe.name).all()
  return render_template('list.html', item_list=recipe_list)

