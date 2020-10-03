from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import InputRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

# def games_query():
#     return 

# class ScoreForm(FlaskForm):
#     name = StringField('Name', validators=[InputRequired()])
#     score = IntegerField('Score', validators=[InputRequired()])
#     # game = RadioField('Game', validators=[InputRequired()], choices=games)
#     game = QuerySelectField('Game', query_factory=games_query)
#     submit = SubmitField('Submit')

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