from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, POwer, HeroPower
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():

    return jsonify({
        "message": "SuperHeroes API",
        "endpoints": {
            "GET /heroes": "Get all heroes",
            "GET /heroes/:id": "Get a specific hero",
            "GET /powers": "Get all powers",
            "GET /powers/:id": "Get a specific power",
            "PATCH /powers/:id": "Update a power",
            "POST /hero_powers": "Create a hero-power association"
        }
    })

@app.route('/heroes', methods=['GET'])
def get_heroes():
    


