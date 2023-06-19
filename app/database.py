from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text

# SQLALCHEMY_DATABASE_URL = f"ibm_db_sa://{user}:{password}@/{database};"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# conn_str = f"ibm_db_sa://{db_uid}:{db_pwd}@{db_host}:{db_port}/{db_location};protocol=tcpip;security=ssl;"

# engine = create_engine(conn_str)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
