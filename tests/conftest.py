import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base
from db import models

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

