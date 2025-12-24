from flask import Flask, request, jsonify, make_response

from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = OS.ENVIRON.GET(
    'DATABASE_URI,
    'sqlite:///superheroes.db'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db.init_app(app)

migrate = Migrate(app, db)
