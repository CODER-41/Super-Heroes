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


@app.route('/')
def index ():
    return jsonify({
        "message": "Superheroes API",
        "endpoints": {
            "heroes": "/heroes",           
            "hero_by_id": "/heroes/:id",      
            "powers": "/powers",             
            "power_by_id": "/powers/:id",   
            "hero_powers": "/hero_powers"     
        }
    })



@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()

    heroes_list = [
        hero.to_dict(only=('id', 'name', 'super_name')) for hero in heroes
        for hero in heroes
    ]

    return jsonify(heroes_list), 200


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):

    hero = Hero.query.filter_by(id=id).first()

    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    

    hero_dict = hero.to_dict(only=(
        'id',
        'name',
        'super_name',
        'hero_powers.id',
        'hero_powers.hero_id',
        'hero_powers.power_id',
        'hero_powers.strength',
        'hero_powers.power.id',
        'hero_powers.power.name',
        'hero_powers.power.description'
        

    ))

    return jsonify(hero_dict), 200


@app.route('/powers', methods=['GET'])
def get_powers():

    powers = Power.query.all()

    powers_list = [
        power.to_dict(only=('id', 'name', 'description'))
         for power in powers
    ]

    return jsonify(powers_list), 200


@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):

    power = Power.query.filter_by(id=id).first()

    if not power:
        return jsonify({"error": "Power not found"}), 404
    

    power_dict = power.to_dict(only=('id', 'name', 'description'))

    return jsonify(power_dict), 200


    
