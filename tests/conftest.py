import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app

from app.db.base import Base
from app.models.experiment import Experiment

@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def client(db):
    def overrride_get_db():
        yield db

    app.dependency_overrides[get_db] = overrride_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()