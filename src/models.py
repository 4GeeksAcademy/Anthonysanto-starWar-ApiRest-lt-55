from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favoritescharacters: Mapped[List["FavoriteCharacter"]] = relationship(back_populates="user")
    favoritesplanets: Mapped[List["FavoritePlanet"]] = relationship(back_populates="user")

    def __repr__(self):
        return  self.email  
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active":self.is_active
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    skin_color: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[str] = mapped_column(String(10))

    favorites: Mapped[List["FavoriteCharacter"]] = relationship(back_populates="character")

    def __repr__(self):
        return self.Name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.Name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "height": self.height
 
        }

 #Favorito
class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="favoritescharacters")
    character: Mapped["Character"] = relationship(back_populates="favorites")

    def __repr__(self):
        return f"<FavoriteCharacter user={self.user.email} character={self.character.Name}>"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.email,
            "character": self.character.Name
        }
    
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    diameter: Mapped[str] = mapped_column(nullable=False)
    rotation_period: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(String(10))

    favoritespl: Mapped[List["FavoritePlanet"]] = relationship(back_populates="planet")
    
    def __repr__(self):
        return self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "population": self.population
        }

 
class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="favoritesplanets")
    planet: Mapped["Planet"] = relationship(back_populates="favoritespl")

    def __repr__(self):
        return f"<FavoriteCharacter user={self.user.email} character={self.character.Name}>"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.email,
            "character": self.character.Name
        }