import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

    favorites = db.relationship(
        "Favorite", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


class Planet(db.Model):
    __tablename__ = "planet"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80))
    terrain = db.Column(db.String(80))
    population = db.Column(db.String(40))
    diameter = db.Column(db.String(40))

    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

    favorited_by = db.relationship("Favorite", back_populates="planet")

    def __repr__(self):
        return f"<Planet {self.name}>"


class Character(db.Model):
    __tablename__ = "character"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(20))
    birth_year = db.Column(db.String(20))
    height = db.Column(db.String(20))
    mass = db.Column(db.String(20))

    homeworld_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    homeworld = db.relationship("Planet")

    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

    favorited_by = db.relationship("Favorite", back_populates="character")

    def __repr__(self):
        return f"<Character {self.name}>"


class Favorite(db.Model):

    __tablename__ = "favorite"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    planet_id = db.Column(
        db.Integer, db.ForeignKey("planet.id"), nullable=True)
    character_id = db.Column(
        db.Integer, db.ForeignKey("character.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

    user = db.relationship("User", back_populates="favorites")
    planet = db.relationship("Planet", back_populates="favorited_by")
    character = db.relationship("Character", back_populates="favorited_by")

    __table_args__ = (
        # evitar duplicar planetas para el mismo user
        UniqueConstraint("user_id", "planet_id", name="uq_user_planet_fav"),
        # evita duplicar personajes para el mismo user
        UniqueConstraint("user_id", "character_id",
                         name="uq_user_character_fav"),
    )

    def __repr__(self):
        target = f"planet_id={self.planet_id}" if self.planet_id else f"character_id={self.character_id}"
        return f"<Favorite user_id={self.user_id} {target}>"

# genera el uml directo


if __name__ == "__main__":
    from eralchemy2 import render_er
    try:
        render_er(db.Model, "diagram.png")
    except Exception:
        render_er(db.metadata, "diagram.png")
    print("diagram.png generado correctamente")
