from pydantic import BaseModel
from datetime import date
from typing import Union


class MovieToCreate(BaseModel):
    title: str
    genre_name: str
    release_date: date
    description: str
    country_name: str

    class Config:
        orm_mode = True


class MovieCreated(MovieToCreate):
    id: int
    rating: float
    number_of_ratings: int
