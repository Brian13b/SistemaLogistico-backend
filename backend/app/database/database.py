from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL_BACKEND = os.getenv("DATABASE_URL_BACKEND")

engine = create_engine(DATABASE_URL_BACKEND)

localSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()
