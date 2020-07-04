from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")