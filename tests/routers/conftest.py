import pytest
from app.main import app
from app.database import get_db
from fastapi.testclient import TestClient


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()
