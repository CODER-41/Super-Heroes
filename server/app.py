from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
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
    
    heroes = Hero.query.all()

    heroes_dict = [hero.to_dict(only = ('id', 'name', 'super_name')) for hero in heroes]

    return jsonify(heroes_dict), 200


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):

    hero =Hero.query.get(id)

    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    hero_dict = hero.to_dict(only = (
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

@app.route('/powers', methods = ['GET'])
def get_powers():

    powers = Power.query.all()

    power_dict = [power.to_dict(only=('id', 'name', 'description')) for power in powers]

    return jsonify(power_dict), 200


@app.route('/powers/<int:id>',  methods=['GET'])
def get_power(id):

    power = Power.query.get(id)

    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    power_dict = power.to_dict(only=(
        'id',
        'name',
        'description'
    ))

    return jsonify(power_dict), 200

@app.route('/powers<int:id>', methods=['PATCH'])
def update_power(id):

    power = Power.query.get(id)

    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()

    try:
        if 'description' in data:
            power.description = data['description']
        
        db.session.commit()
        power_dict=power.to_dict(only=('id', 'name', 'description'))
        return jsonify(power_dict), 200
    
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():

    data = request.get_json()

    try:
        hero_power = HeroPower(
            strength=data.get('strength'),
            power_id = data.get('power_id'),
            hero_id = data.get('hero_id')
        )

        db.session.add(hero_power)

        db.session.commit()

        hero_power_dict = hero_power.to_dict(only=(
            'id',
            'strength',
            'hero_id',
            'power_id',
            'hero.id',
            'hero.name',
            'hero.super_name',
            'power.id',
            'power.name',
            'power.description'
        ))

        return jsonify(hero_power_dict), 201
    
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    
    except Exception as e:
        
        db.session.rollback()

        error_message = str(e)
        if 'foreign key' in error_message.lower() or 'FOREIGN KEY' in error_message:
            return jsonify({"errors": ["Hero or Power not found"]}), 400
        
        return jsonify({"errors": ["Failed to create hero_power association"]}), 400
    

@app.errorhandler(404)
def not_found(e):

    return jsonify({"errors": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(e):

    return jsonify ({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)
        

