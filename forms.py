from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import InputRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField('Signup')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class GameForm(FlaskForm):
    game = StringField('Game', validators=[InputRequired()])
    submit = SubmitField('Add a Game')