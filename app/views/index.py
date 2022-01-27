from app import app, mysql
from flask import render_template


@app.route("/")
def index():

    return render_template("index.html")
