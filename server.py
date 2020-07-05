from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
app = Flask(__name__)

app.config['SECRET_KEY'] = 'wayeshang'


@app.route("/")
def home():
  if "user_id" in session:
    print(session)
    print(session['user_id'])
    return render_template("index.html", name = session['user_id'])
  else:
    return redirect("/login")
  return render_template("login.html")

@app.route("/login")
def login():
  return render_template("login.html")
@app.route("/register", methods=["POST"])
def register():
  print(request.form.to_dict())
  for key, value in request.form.to_dict().items():
    session[key] = value
  # session["user_name"] = request.form.get("user_name")
  # session["user_email"] = request.form.get("user_email")
  # session["user_password"] = request.form.get("user_password")
  return redirect("/")
   