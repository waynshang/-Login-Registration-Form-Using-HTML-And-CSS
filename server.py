from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from helper import check_user_password
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wayeshang'
#session store in a specific folder in client server
#if not assign session will be clear once browser close
app.permanent_session_lifetime = timedelta(minute=5)

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
  flash('You were successfully logged out')
  return redirect(url_for("login"))

#----------------test
@app.route("/test/<name>")
def test(name):
  return render_template("index2.html")
@app.route("/test1")
def test1():
  return redirect(url_for("test",name="wayne"))

@app.route("/user")
def user():
  session["user"] = "wayne"
  if "user" in session:
    user = session["user"]
    return redirect(url_for("test",name=user))
if __name__ == "__main__":
  app.run(debug=True)

