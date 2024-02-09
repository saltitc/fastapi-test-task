import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./sqlite.db"
TEST_DATABASE_URL = "sqlite:///./test_sqlite.db"

if os.getenv("TESTING"):
    engine = create_engine(TEST_DATABASE_URL)
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
