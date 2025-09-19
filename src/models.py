from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active
        }


class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(20))
    height = db.Column(db.Integer)
    hair_color = db.Column(db.String(20))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "hair_color": self.hair_color
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(50))
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(50))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain
        }




class FavoritePeople(db.Model):
    __tablename__ = "favorite_people"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey(
        "people.id"), nullable=False)

    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "people_id": self.people_id}


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey(
        "planet.id"), nullable=False)

    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "planet_id": self.planet_id}
