from flask import render_template, flash, redirect, url_for, request
from recipeBase import app, db, login_manager
from flask_login import login_required, login_user, logout_user, current_user

from forms import LoginForm, SignupForm
from models import User

@login_manager.user_loader
def load_user(userid):
  return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')


@app.route('/logged_in')
@login_required
def logged_in():
  return "Logged in!"

@app.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.get_by_email(form.email.data)
    if user is not None and user.check_password(form.password.data):
      login_user(user, form.remember_me.data)
      flash("Logged in as {}!".format(user.email))
      return redirect(request.args.get('next') or url_for('index'))
    else:
      flash("Incorrect login!")
  return render_template("login.html", form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for("index"))

@app.route('/signup', methods=["GET", "POST"])
def signup():
  form = SignupForm()
  print("this")
  print(form.email.data)
  if form.validate_on_submit():
    
    user = User(email=form.email.data,
                password=form.password.data)
    db.session.add(user)
    db.session.commit() 
    flash('Signed up as {}'.format(user.email))
    login_user(user)
    return redirect(url_for('index')) 
  return render_template("signup.html", form=form)
