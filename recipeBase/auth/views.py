from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user

from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, SignupForm


@auth.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.get_by_email(form.email.data)
    if user is not None and user.check_password(form.password.data):
      login_user(user, form.remember_me.data)
      flash("Logged in as {}!".format(user.email))
      return redirect(request.args.get('next') or url_for('main.index'))
    else:
      flash("Incorrect login!")
  return render_template("login.html", form=form)

@auth.route('/logout')
def logout():
  logout_user()
  return redirect(url_for("main.index"))

@auth.route('/signup', methods=["GET", "POST"])
def signup():
  form = SignupForm()
  if form.validate_on_submit():
    
    user = User(email=form.email.data,
                password=form.password.data)
    db.session.add(user)
    db.session.commit() 
    flash('Signed up as {}'.format(user.email))
    login_user(user)
    return redirect(url_for('main.index')) 
  return render_template("signup.html", form=form)
