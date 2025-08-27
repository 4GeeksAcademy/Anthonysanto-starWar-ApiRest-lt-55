from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active":self.is_active
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    #user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    Name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    skin_color: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[str] = mapped_column(String(10))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.Name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "height": self.height


            # do not serialize the password, its a security breach
        }

 				
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    #user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    diameter: Mapped[str] = mapped_column(nullable=False)
    rotation_period: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(String(10))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "population": self.population


            # do not serialize the password, its a security breach
        }
