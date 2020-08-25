from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from helper import check_user_password
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wayeshang'
#session store in a specific folder in client server
#if not assign session will be clear once browser close
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Qiok5432!@localhost/users"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class users(db.Model):
  _id = db.Column('id', db.Integer, primary_key = True)
  name = db.Column( db.String(100)) #use variable name as column name if not defined
  email = db.Column(db.String(100))
  def __init__(self, name, email):
    self.name = name
    self.email= email

@app.route("/")
def home():
  if "user_id" in session:
    print(session)
    print(session['user_id'])
    return render_template("index.html", name = session['user_id'])
  else:
    return redirect("/login")
  return render_template("login.html")

@app.route("/login", methods =["GET", "POST"])
def login():
  if request.method == "POST":
    user_id = request.form.get("user_id")
    user_password = request.form.get("user_password")
    is_user_valid = check_user_password(user_id, user_password)

    session.permanent = True
    session["user_id"] = user_id if is_user_valid else session.clear()
    return redirect(url_for("home"))
  else:
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
  print(request.form.to_dict())
  for key, value in request.form.to_dict().items():
    session[key] = value
  # use url_for cause it can find the url via its function when route change can still find right url
  return redirect(url_for("home"))

@app.route("/logout")
def logout():
  session.clear()
  flash('You were successfully logged out','info')
  return redirect(url_for("login"))

#----------------test
@app.route("/test/<name>", methods=['POST', 'GET'])
def test(name):
  email = None
  user_name = None
  if request.method == "POST":
    create_session(request, session)
    print("sessoin")
    print(session)
    find_user = users.query.filter_by(email=session["email"]).first()
    if find_user:
      session["user_name"]  = find_user.name
    else:
      user = users(session['user_name'], session["email"])
      db.session.add(user)#add this user model
      db.session.commit()
    return redirect(url_for('home'))
  else:
    if "email" in session:
      email = session["email"]
    if "user_name" in session:
      user_name = session["user_name"]
    return render_template("index2.html", user_name = user_name,email=email)

@app.route("/test1")
def test1():
  return redirect(url_for("test",name="wayne"))


def create_session(request, session):
  for key, value in request.form.to_dict().items():
    session[key] = value


if __name__ == "__main__":
  db.create_all()
  #create class before app run
  app.run(debug=True)

