from starlette.testclient import TestClient
from app.server.app import app

client = TestClient(app)


def test_all_methods():
    response = client.get("methods/all")
    assert response.status_code == 200
    assert len(response.json()) >= 1
