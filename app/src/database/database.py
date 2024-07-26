import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_USER = os.getenv("DB_USER", "admin")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD", "mysecretpassword")
DATABASE_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_PORT = os.getenv("DB_PORT", "3306")
DATABASE_NAME = os.getenv("DB_NAME", "consultorio")
DATABASE_URL = f"mysql+mysqlconnector://admin:mysecretpassword@consultorio.clmys2yoibiz.us-east-1.rds.amazonaws.com:3306/consultorio"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
