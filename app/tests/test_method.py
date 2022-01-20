from starlette.testclient import TestClient
from app.server.app import app
from app.tests.mocked_test_data import methods_data_test

client = TestClient(app)

inserted_methods = []


def test_create_methods():
    for m in methods_data_test:
        response = client.post(
            "methods/",
            json=m
        )
        assert response.status_code == 201
        data = response.json()
        inserted_methods.append(data)
        assert data['name'] == str(m['name'])


def test_all_methods():
    response = client.get("methods/all")
    assert response.status_code == 200
    assert len(response.json()) == len(methods_data_test)


def test_get_by_id():
    for m in inserted_methods:
        response = client.get("methods/{}".format(m['id']))
        data = response.json()
        assert response.status_code == 200
        assert data['id'] == str(m['id'])


def test_get_by_user_id():
    for i in [1, 2, 3]:
        response = client.get("methods/user_methods?user_id={}".format(i))
        data = response.json()
        assert response.status_code == 200
        for m in data:
            assert m['user_id'] == str(i)
    response = client.get("methods/user_methods?user_id=60")
    assert response.status_code == 500
    response = client.get("methods/user_methods")
    assert response.status_code == 400


def test_update_method():
    i = 0
    for m in inserted_methods:
        updated_name = "actualizado-{}".format(i)
        updated_link = "www.test_{}.com".format(updated_name)
        m['name'] = updated_name
        m['link'] = updated_link
        i += 1
        response = client.put(
            "methods/{}".format(m['id']),
            json=m
        )
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == updated_name
        assert data['link'] == updated_link


def test_remove_method():
    i = 0
    for m in inserted_methods:
        response = client.delete("methods/{}".format(m['id']))
        assert response.status_code == 200
        assert response.json()['success']
    response = client.get("methods/all")
    methods = response.json()
    assert methods['Error']
