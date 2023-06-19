from app.database import Base
from sqlalchemy import Column, Date, ForeignKey, Enum, Integer, String, Float
from sqlalchemy.orm import relationship, validates


class Genre(Base):
    __tablename__ = "genres"

    name = Column(String(20), primary_key=True)

    movies = relationship("Movie", back_populates="genre")


class Country(Base):
    __tablename__ = "countries"

    name = Column(String(20), primary_key=True)

    movies = relationship("Movie", back_populates="country")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    genre_name = Column(String(20), ForeignKey("genres.name"), nullable=False)
    release_date = Column(Date, nullable=False)
    description = Column(String(100), nullable=False)
    country_name = Column(String(20), ForeignKey("countries.name"), nullable=False)
    rating = Column(Float, nullable=False)
    number_of_ratings = Column(Integer, nullable=False)

    genre = relationship("Genre", back_populates="movies")
    country = relationship("Country", back_populates="movies")
    reviews = relationship("Review", back_populates="movie")


class User(Base):
    __tablename__ = "users"

    name = Column(String(20), primary_key=True)

    reviews = relationship("Review", back_populates="user")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    description = Column(String(100))
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    user_name = Column(String(20), ForeignKey("users.name"))

    movie = relationship("Movie", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    @validates("rating")
    def validate_rating(self, key, value):
        if not 1 <= value <= 11:
            raise ValueError(f"Rating must be in range [0,10] but is: {value}")
        return value
