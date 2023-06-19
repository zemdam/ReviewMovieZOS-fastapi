import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, engine, SessionLocal


@pytest.fixture(scope="session")
def db_engine():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    yield engine


@pytest.fixture(scope="session")
def db_session(db_engine):
    session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    yield session


@pytest.fixture
def db(db_session, db_engine):
    Base.metadata.drop_all(bind=db_engine)
    Base.metadata.create_all(bind=db_engine)

    test_db = db_session()
    yield test_db
    test_db.close()

    Base.metadata.drop_all(bind=db_engine)


# Uncomment to test via db2.
# @pytest.fixture
# def db():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

#     test_db = SessionLocal()
#     yield test_db
#     test_db.close()

#     Base.metadata.drop_all(bind=engine)
