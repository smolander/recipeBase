from flask import render_template
from flask_login import login_required

from . import main
from .. import login_manager
from ..models import User

@login_manager.user_loader
def load_user(userid):
  return User.query.get(int(userid))


@main.route('/')
@main.route('/index')
def index():
  return render_template('index.html')


@main.route('/logged_in')
@login_required
def logged_in():
  return render_template('logged_in.html')
