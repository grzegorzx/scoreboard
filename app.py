from flask import Flask, render_template, request, session, redirect, url_for
from forms import LoginForm, ScoreForm, SignupForm
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scoreboard.db'
db = SQLAlchemy(app)

users = [
    {"id": 1, "name": "Minyao", "email":"m@h.cn", "password":"mh1337"}
]

records = [
    {"id": 1, "name": "Grzegorz", "score": 9, "game": "Golf Story"},
    {"id": 2, "name": "Grzegorz", "score": 9, "game": "Golf Story"},
    {"id": 3, "name": "Grzegorz", "score": 9, "game": "Golf Story"}
]

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    records = db.relationship('Record', backref='user')

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False, unique=True)
    records = db.relationship('Record', backref='game')

class Record(db.Model):
    record_id = db.Column(db.String, primary_key=True, nullable=False)
    game_title = db.Column(db.String, db.ForeignKey('game.title'), nullable = False)
    user = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)

db.create_all()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data), None)
        if user is None:
            return render_template("login.html", form = form, message = "Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user
            return render_template("login.html", message = "Successfully Logged In!")
    
    return render_template("login.html", form=form)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = {"id": len(users)+1, "name": form.name.data, "email": form.email.data, "password": form.password.data}
        users.append(new_user)
        print(users)
        return render_template("signup.html", message="Succuessfully signed up!")
    return render_template("signup.html", form=form)

@app.route("/add", methods=["POST", "GET"])
def add():
    form = ScoreForm()
    if form.validate_on_submit():
        new_record = {"id": len(records)+1, "name": form.name.data, "score": form.score.data, "game": form.game.data}
        records.append(new_record)
        return render_template("add.html", message="Successfully added a record.")
    return render_template("add.html", form=form)

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