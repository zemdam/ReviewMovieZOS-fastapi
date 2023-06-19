from sqlalchemy.orm import Session
from app.schemas import other
from app import models


def create_genre(db: Session, genre: other.Genre):
    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def get_genres(db: Session):
    return db.query(models.Genre).all()


def create_country(db: Session, country: other.Country):
    db_country = models.Country(name=country.name)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


def get_countries(db: Session):
    return db.query(models.Country).all()


def create_user(db: Session, user: other.User):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()
