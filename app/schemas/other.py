from pydantic import BaseModel
from typing import Union


class Named(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Genre(Named):
    pass


class Country(Named):
    pass


class User(Named):
    pass


class ReviewToCreate(BaseModel):
    rating: int
    description: Union[str, None]
    user_name: str

    class Config:
        orm_mode = True


class ReviewCreated(ReviewToCreate):
    id: int
    movie_id: int
