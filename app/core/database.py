import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

Base = declarative_base()


def get_database_url():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    if not all([db_user, db_password, db_name, db_host, db_port]):
        raise ValueError("Missing database credentials in .env")

    return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_db_engine():
    database_url = get_database_url()

    return create_engine(database_url)

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("Connected to database")


def get_db_instance():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()