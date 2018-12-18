from ..models import Recipe

def search_recipe_by_name(name):
  recipe = Recipe.query.filter(Recipe.name == name).first()
  return recipe