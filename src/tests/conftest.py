import pytest
from fastapi.testclient import TestClient
from main import app

#Fixture
@pytest.fixture
def client():
    return TestClient(app=app)

