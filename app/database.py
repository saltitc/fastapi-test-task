from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./sqlite.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TEST_DATABASE_URL = "sqlite:///./test_sqlite.db"
test_engine = create_engine(TEST_DATABASE_URL)
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
