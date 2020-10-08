from flask import Flask, render_template, request, session, redirect, url_for
from forms import LoginForm, SignupForm, GameForm
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import InputRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABSE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ENV']='development'
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, primary_key=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    records = db.relationship('Record', backref='user')

class Game(db.Model):
    game_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    records = db.relationship('Record', backref='game')

class Record(db.Model):
    record_id = db.Column(db.Integer, primary_key=True, nullable=False)
    game_title = db.Column(db.String, db.ForeignKey('game.title'), nullable = False)
    winner = db.Column(db.String, db.ForeignKey('user.name'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

db.create_all()

def games_query():
    return db.session.query(Game)

def users_query():
    return db.session.query(User)

class ScoreForm(FlaskForm):
    name = QuerySelectField('Name', query_factory=users_query, get_label='name', validators=[InputRequired()])
    score = IntegerField('Score', validators=[InputRequired()])
    game = QuerySelectField('Game', query_factory=games_query, get_label='title', validators=[InputRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    score_results = [u.__dict__ for u in Record.query]
    print(score_results)
    return render_template('home.html', score_results=score_results)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user is None:
            return render_template("login.html", form = form, message = "Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user.user_id
            return render_template("login.html", message = "Successfully Logged In!")
    return render_template("login.html", form=form)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(user_id = (User.query.count())+1, name = form.name.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form=form, message="This email is already registered. Please log in instead.")
        finally:
            db.session.close()
        return render_template("signup.html", message="Succuessfully signed up!")
    return render_template("signup.html", form=form)

@app.route("/add", methods=["POST", "GET"])
def add():
    if 'user' not in session:
        return render_template("home.html", message="You are not logged in.")
    else:
        form = ScoreForm()
        if form.validate_on_submit():
            new_record = Record(record_id = (Record.query.count())+1, game_title = form.game.data.title, winner = form.name.data.name, score = int(form.score.data))
            db.session.add(new_record)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return render_template("add.html", form=form, message="Something went wrong.")
            finally:
                db.session.close()
            return render_template("add.html", message="Successfully added a record.")
        return render_template("add.html", form=form)

@app.route("/game", methods=["POST", "GET"])
def game():
    if 'user' not in session:
        return render_template("home.html", message="You are not logged in.")
    else:
        form = GameForm()
        if form.validate_on_submit():
            new_game = Game(game_id=(Game.query.count())+1, title = form.game.data)
            db.session.add(new_game)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return render_template("game.html", form=form, message="Something went wrong.")
            finally:
                db.session.close()
            return render_template("game.html", message="Successfully added a game.")
        return render_template('game.html', form=form)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home'
    , _scheme='http'
    , _external=True
    ))

@app.route("/about")
def about():
    return render_template('about.html') 

if __name__ == "__main__":
    app.run(debug=True)