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
        assert data['token'] != ""


def test_login_email():
    # With email
    for u in user_data_test:
        u_d = {
            "email": u['email'],
            "password": u['password']
        }
        response = client.post("users/login", json=u_d)
        assert response.status_code == 200
        data = response.json()
        assert data['token'] != ""
        assert data['email'] == u['email']


def test_login_username():
    # With username
    for u in user_data_test:
        u_d = {
            "username": u['username'],
            "password": u['password']
        }
        response = client.post("users/login", json=u_d)
        assert response.status_code == 200
        data = response.json()
        assert data['token'] != ""
        assert data['username'] == u['username']


def test_repeated_users():
    for u in user_data_test:
        response = client.post("users/", json=u)
        assert response.status_code == 422
        users_collection.delete_one({"username": u['username']})
