"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Character, Planet
from sqlalchemy import select
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    all_users = User.query.all()
    print(all_users)
    results = list(map(lambda user: user.serialize(),all_users))
    print(list(results))
    response_body = {

        "users": results
    }  
    return jsonify(response_body), 200
 

@app.route('/character', methods=['GET'])
def handle_character():
    all_characters = Character.query.all()
    print(all_characters)
    results = list(map(lambda character: character.serialize(),all_characters))
    print(list(results))
    
    response_body = {

        "characters": results
    }  

    return jsonify(response_body), 200


@app.route('/character', methods=['POST'])
def add_character():

    body = request.get_json()

    if body['Name']== '':
        return jsonify({"msg": "nombre no puede quedar vacio"}),400
    
    character = Character(**body)
    db.session.add(character)
    db.session.commit()
    response_body = {

        "character" : character.serialize()
    }  

    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def handle_planet():
    all_planets = Planet.query.all()
    print(all_planets)
    results = list(map(lambda planet: planet.serialize(),all_planets))
    print(list(results))
    response_body = {

        "planets": results
    }  

    return jsonify(response_body), 200

@app.route('/planet', methods=['POST'])
def add_planet():

    body = request.get_json()

    if body['Name']== '':
        return jsonify({"msg": "nombre no puede quedar vacio"}),400
    
    planet = Planet(**body)
    db.session.add(planet)
    db.session.commit()
    response_body = {

        "planet" : planet.serialize()
    }  

    return jsonify(response_body), 200    

@app.route('/character/<int:character_id>', methods=['DELETE'])
def remove_character(character_id):
    character = db.session.execute(select(Character).where(Character.id == character_id)).scalar_one_or_none()

    db.session.delete(character)
    db.session.commit()
 
 
    response_body = {
        "msg" : "Eliminado exitosamente "+ character.Name 
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def remove_planet(planet_id):
    planet = db.session.execute(select(Planet).where(Planet.id == planet_id)).scalar_one_or_none()

    db.session.delete(planet)
    db.session.commit()
 
 
    response_body = {
        "msg" : "Eliminado exitosamente "+ planet.name 
    }
    return jsonify(response_body), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
