# src/seed.py
from app import app
from models import db, User, People, Planet, FavoritePeople, FavoritePlanet

def run_seed():
    with app.app_context():
        # Crea tablas si no existen (si usas migraciones ya estarán)
        db.create_all()

        # ---- Users ----
        if not User.query.first():
            db.session.add_all([
                User(email="luke@rebels.io", username="luke", is_active=True),
                User(email="leia@rebels.io", username="leia", is_active=True),
            ])

        # ---- People ----
        if People.query.count() == 0:
            db.session.add_all([
                People(name="Luke Skywalker", gender="male", height=172, hair_color="blond"),
                People(name="Darth Vader",  gender="male", height=202, hair_color="none"),
                People(name="Leia Organa",  gender="female", height=150, hair_color="brown"),
            ])

        # ---- Planets ----
        if Planet.query.count() == 0:
            db.session.add_all([
                Planet(name="Tatooine", climate="arid",      population=200000,      terrain="desert"),
                Planet(name="Alderaan", climate="temperate", population=2000000000,  terrain="grasslands"),
                Planet(name="Hoth",     climate="frozen",    population=0,           terrain="tundra"),
            ])

        db.session.commit()
        print("✅ Seed: users, people y planets listos.")

        # (Opcional) favoritos de prueba para user 1
        luke = User.query.filter_by(username="luke").first()
        tatooine = Planet.query.filter_by(name="Tatooine").first()
        vader = People.query.filter_by(name="Darth Vader").first()
        if luke and tatooine and not FavoritePlanet.query.filter_by(user_id=luke.id, planet_id=tatooine.id).first():
            db.session.add(FavoritePlanet(user_id=luke.id, planet_id=tatooine.id))
        if luke and vader and not FavoritePeople.query.filter_by(user_id=luke.id, people_id=vader.id).first():
            db.session.add(FavoritePeople(user_id=luke.id, people_id=vader.id))
        db.session.commit()
        print("⭐ Favoritos de prueba (user luke) creados.")

if __name__ == "__main__":
    run_seed()
