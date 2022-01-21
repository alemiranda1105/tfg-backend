from starlette.testclient import TestClient

from app.server.app import app
from app.server.database import users_collection
from mocked_test_data import user_data_test

client = TestClient(app)


def test_signup():
    for u in user_data_test:
        response = client.post("users/", json=u)
        assert response.status_code == 201
        data = response.json()
        assert data['token']['token'] != ""


def test_repeated_users():
    for u in user_data_test:
        response = client.post("users/", json=u)
        assert response.status_code == 422
        users_collection.delete_one({"username": u['username']})
