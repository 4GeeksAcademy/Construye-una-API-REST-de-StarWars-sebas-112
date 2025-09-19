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
from models import db, User, People, Planet, FavoritePeople, FavoritePlanet
# from models import Person  # (no lo usamos)

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Helpers sencillos


def get_user_id():
    """Obtenemos el 'usuario actual' desde ?user_id=... (no hay auth)."""
    return request.args.get("user_id", type=int)


def not_found(msg="Not found"):
    return jsonify({"msg": msg}), 404

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Endpoints de ejemplo del template


@app.route('/user', methods=['GET'])
def handle_hello():
    return jsonify({"msg": "Hello, this is your GET /user response "}), 200


# PEOPLE


@app.get("/people")
def list_people():
    items = People.query.all()
    return jsonify([p.serialize() for p in items])


@app.get("/people/<int:people_id>")
def get_people(people_id):
    item = People.query.get(people_id)
    if not item:
        return not_found("People not found")
    return jsonify(item.serialize())


# PLANETS


@app.get("/planets")
def list_planets():
    items = Planet.query.all()
    return jsonify([p.serialize() for p in items])


@app.get("/planets/<int:planet_id>")
def get_planet(planet_id):
    item = Planet.query.get(planet_id)
    if not item:
        return not_found("Planet not found")
    return jsonify(item.serialize())

# USERS

@app.get("/users")
def list_users():
    items = User.query.all()
    return jsonify([u.serialize() for u in items])


@app.get("/users/favorites")
def list_user_favorites():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"msg": "Provide ?user_id=<id>"}), 400

    user = User.query.get(user_id)
    if not user:
        return not_found("User not found")

    fav_people_rows = FavoritePeople.query.filter_by(user_id=user_id).all()
    fav_planet_rows = FavoritePlanet.query.filter_by(user_id=user_id).all()

    fav_people = []
    for fp in fav_people_rows:
        p = People.query.get(fp.people_id)
        if p:
            fav_people.append(p.serialize())

    fav_planets = []
    for fl in fav_planet_rows:
        pl = Planet.query.get(fl.planet_id)
        if pl:
            fav_planets.append(pl.serialize())

    return jsonify({
        "user": user.serialize(),
        "favorite_people": fav_people,
        "favorite_planets": fav_planets
    })


# FAVORITES: PLANET


@app.post("/favorite/planet/<int:planet_id>")
def add_fav_planet(planet_id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({"msg": "Provide ?user_id=<id>"}), 400

    if not Planet.query.get(planet_id) or not User.query.get(user_id):
        return not_found("User or Planet not found")

    exists = FavoritePlanet.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if exists:
        return jsonify({"msg": "Already in favorites"}), 200

    fav = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites", "favorite": fav.serialize()}), 201


@app.delete("/favorite/planet/<int:planet_id>")
def remove_fav_planet(planet_id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({"msg": "Provide ?user_id=<id>"}), 400

    fav = FavoritePlanet.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return not_found("Favorite not found")

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Planet removed from favorites"})


# FAVORITES: PEOPLE

@app.post("/favorite/people/<int:people_id>")
def add_fav_people(people_id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({"msg": "Provide ?user_id=<id>"}), 400

    if not People.query.get(people_id) or not User.query.get(user_id):
        return not_found("User or People not found")

    exists = FavoritePeople.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if exists:
        return jsonify({"msg": "Already in favorites"}), 200

    fav = FavoritePeople(user_id=user_id, people_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "People added to favorites", "favorite": fav.serialize()}), 201


@app.delete("/favorite/people/<int:people_id>")
def remove_fav_people(people_id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({"msg": "Provide ?user_id=<id>"}), 400

    fav = FavoritePeople.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if not fav:
        return not_found("Favorite not found")

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "People removed from favorites"})


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
