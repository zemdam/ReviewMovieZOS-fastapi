from sqlalchemy.orm import Session
from app.schemas import movie, other
from app.models import Movie, Country, Genre, Review
from typing import Union


def create_movie(db: Session, movie: movie.MovieToCreate):
    db_movie = Movie(**movie.dict(), rating=0, number_of_ratings=0)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def get_movies_query(db: Session, country: Union[str, None], genre: Union[str, None]):
    if country == None and genre == None:
        movies = db.query(Movie)
        return movies
    if country and genre:
        movies = db.query(Movie).filter(
            Movie.country_name == country, Movie.genre_name == genre
        )
        return movies
    if country:
        movies = db.query(Movie).filter(Movie.country_name == country)
        return movies
    if genre:
        movies = db.query(Movie).filter(Movie.genre_name == genre)
        return movies


def get_movies(db: Session, country: Union[str, None], genre: Union[str, None]):
    return get_movies_query(db, country, genre).all()


def get_movie(db: Session, movie_id: int):
    db_movie = db.get(Movie, movie_id)
    return db_movie


def add_review(review: other.ReviewToCreate, movie_id: int, db: Session):
    db_review = Review(**review.dict(), movie_id=movie_id)
    db_movie = db.get(Movie, movie_id)
    db_movie.rating = (
        db_movie.rating * db_movie.number_of_ratings + db_review.rating
    ) / (db_movie.number_of_ratings + 1)
    db_movie.number_of_ratings += 1
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews(movie_id: int, db: Session):
    db_movie = db.get(Movie, movie_id)
    return db_movie.reviews


def get_top_movies(
    db: Session,
    country: Union[str, None],
    genre: Union[str, None],
    limit: Union[int, str],
):
    if limit is None:
        return get_movies_query(db, country, genre).order_by(Movie.rating.desc()).all()
    else:
        return (
            get_movies_query(db, country, genre)
            .order_by(Movie.rating.desc())
            .limit(limit)
            .all()
        )
