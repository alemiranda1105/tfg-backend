from starlette.testclient import TestClient
from app.server.app import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
