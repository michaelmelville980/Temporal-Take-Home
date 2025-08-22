import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DEFAULT_DB_URL = "postgresql://temporal:temporal@localhost:5434/mydb"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

Base = declarative_base()
