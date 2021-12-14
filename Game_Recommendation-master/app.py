from flask import Flask, redirect, url_for, render_template
import pandas as pd
from sort_value import df, top10_Rating, top10_forever, top10_positive
import random
from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Game recommendation"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template("home.html",top10_Rating= top10_Rating, top10_forever=top10_forever, top10_positive= top10_positive)
    else:
        return render_template("index.html")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

# @app.route("/")
# def home():
#     return render_template("index.html",top10_Rating= top10_Rating, top10_forever=top10_forever, top10_positive= top10_positive)
#     # return render_template("index.html", df = df)

@app.route("/detail/<game_id>",methods=['GET', 'POST'])
def detail(game_id):
    list1 = random.sample(range(20000), 5)
    list2 = random.sample(range(20000), 5)
    game_detail = df.loc[df["Game_id"]==int(game_id)].squeeze()
    return render_template("detail.html", game_detail=game_detail, df = df, list1=list1, list2=list2)
    

if(__name__ == '__main__'):
    app.secret_key = "Game recommendation"
    db.create_all()
    app.run()