#coding=UTF-8

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from . import recipies 
from .helpers import search_recipe_by_name
from .. import db
from ..models import Recipe
from .forms import SearchForm, EditForm


@recipies.route('/list')
@login_required
def list():
  recipe_list = Recipe.query.order_by(Recipe.name).all()
  return render_template('list.html', item_list=recipe_list)

@recipies.route('/show/<int:recipe_id>')
@login_required
def show(recipe_id):
  cur_recipe = Recipe.query.get(recipe_id)
  return render_template('recipe_show.html', recipe = cur_recipe)

@recipies.route('/search', methods=["GET", "POST"])
@login_required
def search():
  form = SearchForm()
  if form.validate_on_submit():
    recipe_name = form.name.data
    recipe = search_recipe_by_name(recipe_name)
    if recipe:
      return redirect(url_for('recipies.show', recipe_id=recipe.id))
    else:
      flash("Hittade inte något recept på {}".format(recipe_name))
  return render_template('recipe_search.html', form = form)

@recipies.route('/new', methods=["GET", "POST"])
@login_required
def new():
  form = EditForm()
  if form.validate_on_submit():
    recipe = Recipe()
    recipe.name = form.name.data
    recipe.cooking_time = form.cooking_time.data
    recipe.difficulty = form.difficulty.data
    recipe.initial_portions = form.initial_portions.data
    recipe.instructions = form.initial_portions.data
    recipe.add_ingredients(form.ingredients.data)
    db.session.add(recipe)
    db.session.commit()
    return redirect(url_for('recipies.show', recipe_id=recipe.id))
  return render_template('recipe_edit.html', form=form)