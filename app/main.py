from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from app.routers import other_route, movie_route

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ReviewMovieZ/OS")

app.include_router(other_route.router)
app.include_router(movie_route.router)
