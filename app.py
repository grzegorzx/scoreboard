from flask import Flask, render_template, request, session, redirect, url_for
from forms import LoginForm, ScoreForm, SignupForm
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scoreboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ENV']='development'
db = SQLAlchemy(app)

users = [
    {"id": 1, "name": "Minyao", "email":"m@h.cn", "password":"mh1337"}
]

# records = [
#     {"id": 1, "name": "Grzegorz", "score": 9, "game": "Golf Story"},
#     {"id": 2, "name": "Grzegorz", "score": 9, "game": "Golf Story"},
#     {"id": 3, "name": "Grzegorz", "score": 9, "game": "Golf Story"}
# ]

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
    winner = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)

db.create_all()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data), None)
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
    form = ScoreForm()
    if form.validate_on_submit():
        new_record = {"id": len(records)+1, "name": form.name.data, "score": form.score.data, "game": form.game.data}
        records.append(new_record)
        # new_record = Record(id = (User.query.count())+1, name = form.name.data, score = form.score.data, game = form.game.data)
        # db.session.add(new_record)
        # try:
        #     db.session.commit()
        # except Exception as e:
        #     print(e)
        #     db.session.rollback()
        #     return render_template("add.html", form=form, message="Something went wrong.")
        # finally:
        #     db.session.close()
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