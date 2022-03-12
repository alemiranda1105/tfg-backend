from starlette.testclient import TestClient

from app.server.app import app
from app.server.auth.auth_handler import sign_jwt
from app.server.database import users_collection
from mocked_test_data import user_data_test, mocked_jwt

client = TestClient(app)

inserted_users = []


def test_signup():
    for u in user_data_test:
        response = client.post("users/", json=u)
        assert response.status_code == 201
        data = response.json()
        inserted_users.append(data['id'])
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


def test_profile_page():
    user = user_data_test[0]
    login_data = {
        "username": user['username'],
        "password": user['password']
    }

    # User login
    response = client.post("users/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data['token'] != ""

    # token is saved for request the profile
    token = data['token']
    assert data['username'] == user['username']

    # profile request
    response = client.get(
        "users/profile?user_id={}".format(data['id']),
        headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    profile_data = response.json()
    assert profile_data['username'] == user['username']
    assert profile_data['email'] == user['email']


def test_profile_page_error():
    response = client.get(
        "users/profile?user_id={error}",
        headers={
            'Authorization': 'Bearer {}'.format(mocked_jwt)
        }
    )
    assert response.status_code == 403


def test_login_error():
    data = {
        "username": "error",
        "password": "123456"
    }
    response = client.post("users/login", json=data)
    assert response.status_code == 404


def test_get_user_by_id():
    for u in inserted_users:
        response = client.get("users/{}".format(u))
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == u
        assert data['username'] != ''


def test_update_user():
    user = user_data_test[0]
    login_data = {
        "username": user['username'],
        "password": user['password']
    }

    # User login
    response = client.post("users/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data['token'] != ""

    # token is saved for request the profile
    token = data['token']
    assert data['username'] == user['username']

    # Update
    new_data = {
        "username": "test_u",
        "email": "updated@example.com",
        "password": user['password']
    }
    response = client.put("users/{}".format(data['id']),
                          json=new_data,
                          headers={
                              'Authorization': 'Bearer {}'.format(token)
                          })
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == new_data['username']
    assert data['email'] == new_data['email']


def test_update_user_auth_error():
    user = user_data_test[0]
    # Update
    new_data = {
        "username": "test_u",
        "email": "updated@example.com",
        "password": user['password']
    }
    response = client.put("users/{}".format(inserted_users[0]),
                          json=new_data,
                          headers={
                              'Authorization': 'Bearer {}'.format(mocked_jwt)
                          })
    assert response.status_code == 403


def test_update_user_error():
    user = user_data_test[1]
    login_data = {
        "username": user['username'],
        "password": user['password']
    }

    # User login
    response = client.post("users/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data['token'] != ""

    # token is saved for request the profile
    token = data['token']
    assert data['username'] == user['username']

    # Update
    new_data = {
        "username": "test3",
        "email": user['email'],
        "password": user['password']
    }
    response = client.put("users/{}".format(data['id']),
                          json=new_data,
                          headers={
                              'Authorization': 'Bearer {}'.format(token)
                          })
    assert response.status_code == 500


def test_repeated_users():
    user_data_test.remove(user_data_test[0])
    for u in user_data_test:
        response = client.post("users/", json=u)
        assert response.status_code == 422


def test_remove_user_auth_error():
    for u in inserted_users:
        response = client.delete("users/{}".format(u))
        assert response.status_code == 403


def test_remove_user():
    for u in inserted_users:
        token = sign_jwt(u)['token']
        response = client.delete("users/{}".format(u), headers={
                              'Authorization': 'Bearer {}'.format(token)
                          })
        assert response.status_code == 200


def test_remove_user_error():
    for u in inserted_users:
        token = sign_jwt(u)['token']
        response = client.delete("users/{}".format(u), headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert response.status_code == 500
