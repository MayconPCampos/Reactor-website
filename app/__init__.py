from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

mysql = MySQL(app)

from app.views import index, news, user