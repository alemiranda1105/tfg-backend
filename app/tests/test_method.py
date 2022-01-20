from starlette.testclient import TestClient
from app.server.app import app
from app.tests.conftest import inserted_methods

client = TestClient(app)


def test_all_methods():
    response = client.get("methods/all")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_by_id():
    for m in inserted_methods:
        response = client.get("methods/{}".format(m))
        data = response.json()
        assert response.status_code == 200
        assert data['id'] == str(m)
