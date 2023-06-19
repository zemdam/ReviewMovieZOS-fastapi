from fastapi import APIRouter, Depends
from app.schemas import movie, other
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import movie_service
from typing import Union

router = APIRouter(prefix="/movie", tags=["movie"])


@router.post("/", response_model=movie.MovieCreated)
def create_movie(movie: movie.MovieToCreate, db: Session = Depends(get_db)):
    return movie_service.create_movie(db=db, movie=movie)


@router.get("s", response_model=list[movie.MovieCreated])
def get_movies(
    db: Session = Depends(get_db),
    country: Union[str, None] = None,
    genre: Union[str, None] = None,
):
    return movie_service.get_movies(db=db, country=country, genre=genre)


@router.get("/{movie_id}", response_model=movie.MovieCreated)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    return movie_service.get_movie(db=db, movie_id=movie_id)


@router.post("/{movie_id}/review", response_model=other.ReviewCreated)
def add_review(
    review: other.ReviewToCreate, movie_id: int, db: Session = Depends(get_db)
):
    return movie_service.add_review(review=review, movie_id=movie_id, db=db)


@router.get("/{movie_id}/reviews", response_model=list[other.ReviewCreated])
def get_reviews(movie_id: int, db: Session = Depends(get_db)):
    return movie_service.get_reviews(movie_id=movie_id, db=db)


@router.get("s/top")
def get_top_movies(
    db: Session = Depends(get_db),
    country: Union[str, None] = None,
    genre: Union[str, None] = None,
    limit: Union[int, None] = None,
):
    return movie_service.get_top_movies(db, country, genre, limit)
