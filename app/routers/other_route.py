from fastapi import APIRouter, Depends
from app.schemas import other
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import other_service

router = APIRouter(prefix="/other", tags=["other"])


@router.post("/genre", response_model=other.Genre)
def create_genre(genre: other.Genre, db: Session = Depends(get_db)):
    return other_service.create_genre(db=db, genre=genre)


@router.get("/genres", response_model=list[other.Genre])
def get_genres(db: Session = Depends(get_db)):
    return other_service.get_genres(db=db)


@router.post("/country", response_model=other.Country)
def create_country(country: other.Country, db: Session = Depends(get_db)):
    return other_service.create_country(db=db, country=country)


@router.get("/countries", response_model=list[other.Country])
def get_countries(db: Session = Depends(get_db)):
    return other_service.get_countries(db=db)


@router.post("/user", response_model=other.User)
def create_user(user: other.User, db: Session = Depends(get_db)):
    return other_service.create_user(db=db, user=user)


@router.get("/users", response_model=list[other.User])
def get_users(db: Session = Depends(get_db)):
    return other_service.get_users(db=db)
