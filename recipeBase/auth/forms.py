from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, url, Email, EqualTo, Length
from werkzeug.routing import ValidationError
from ..models import User

class LoginForm(Form):
  email = StringField('Email:', validators=[DataRequired(), Email()])
  password = PasswordField('Password: ', validators=[DataRequired()])
  remember_me = BooleanField('Keep me logged in: ')
  submit = SubmitField('Log In')

class SignupForm(Form):
  email = StringField('Email', validators=[DataRequired(), Length(1,120), Email()])
  password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
  password2 = PasswordField('Confirm password', validators=[DataRequired()])
  submit = SubmitField('Sign up')

  def validate_email(self, email_field):
    if User.get_by_email(email = email_field.data):
      raise ValidationError('There is already a user with this email address')