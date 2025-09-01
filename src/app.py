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
from models import db, User,Character, Planet,FavoriteCharacter,FavoritePlanet
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
    results = list(map(lambda user: user.serialize(),all_users))
    response_body = {

        "users": results
    }  
    return jsonify(response_body), 200
 

@app.route('/people', methods=['GET'])
def handle_character():
    all_characters = Character.query.all()
    results = list(map(lambda character: character.serialize(),all_characters))
    
    response_body = {

        "characters": results
    }  

    return jsonify(response_body), 200


@app.route('/people', methods=['POST'])
def add_character():

    body = request.get_json()

    if body['name']== '':
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
    results = list(map(lambda planet: planet.serialize(),all_planets))
    response_body = {

        "planets": results
    }  

    return jsonify(response_body), 200

@app.route('/planet', methods=['POST'])
def add_planet():

    body = request.get_json()

    if body['name']== '':
        return jsonify({"msg": "nombre no puede quedar vacio"}),400
    
    planet = Planet(**body)
    db.session.add(planet)
    db.session.commit()
    response_body = {

        "planet" : planet.serialize()
    }  

    return jsonify(response_body), 200    

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    body = request.get_json()
    user_id = body.get("user_id", None)

    if not user_id:
        return jsonify({"msg": "user_id es requerido"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    character = Character.query.get(people_id)
    if not character:
        return jsonify({"msg": "Character no encontrado"}), 404


    favorite = FavoriteCharacter(user_id=user_id, character_id=people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "msg": "Personaje agregado a favoritos",
        "favorite": {
            "id": favorite.id,
            "user_id": favorite.user_id,
            "character_id": favorite.character_id
        }
    }), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    body = request.get_json()
    user_id = body.get("user_id", None)

    if not user_id:
        return jsonify({"msg": "Es necesario el user_id"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planeta no encontrado"}), 404

    favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "msg": "Planeta agregado a favoritos",
        "favorite": {
            "id": favorite.id,
            "user_id": favorite.user_id,
            "planet_id": favorite.planet_id
        }
    }), 201


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    body = request.get_json()
    user_id = body.get("user_id", None)

    if not user_id:
        return jsonify({"msg": "es necesario el user_id"}), 400

    favorite = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=people_id).first()

    if not favorite:
        return jsonify({"msg": "no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Personaje eliminado de favoritos"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    body = request.get_json()
    user_id = body.get("user_id", None)

    if not user_id:
        return jsonify({"msg": "es necesario el user_id"}), 400

    favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if not favorite:
        return jsonify({"msg": "no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta eliminado de favoritos"}), 200


#todos los favoritos listados
@app.route('/users/favorites', methods=['GET'])
def get_all_favorites():
    users = User.query
    results = []

    for user in users:
        favorite_characters = FavoriteCharacter.query.filter_by(user_id=user.id)
        favorite_planets = FavoritePlanet.query.filter_by(user_id=user.id)

        results.append({
            "user_id": user.id,
            "user_name": user.name,
            "favorites": {
                "characters": [
                    {
                        "favorite_id": favorite.id,
                        "character": favorite.character.serialize()
                    } for favorite in favorite_characters
                ],
                "planets": [
                    {
                        "favorite_id": favorite.id,
                        "planet": favorite.planet.serialize()
                    } for favorite in favorite_planets
                ]
            }
        })

    return jsonify(results), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
