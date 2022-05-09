import json
from dotenv import load_dotenv
import os

from starlette.testclient import TestClient
from app.server.app import app
from .mocked_test_data import methods_data_test, mocked_jwt

client = TestClient(app)

inserted_methods = []
load_dotenv()
file = os.getenv('TEST_FILE_ZIP')


def test_all_methods_error():
    response = client.get("idsemapi/methods/all")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] is not ""


def test_create_methods():
    for m in methods_data_test:
        response = client.post(
            "idsemapi/methods/",
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt)
            },
            files={
                'file': (file, open(file, 'rb')),
                'data': (None, json.dumps(m)),
            }
        )
        assert response.status_code == 201
        data = response.json()
        inserted_methods.append(data)
        assert data['name'] == str(m['name'])
        assert len(data['results']) == 3


def test_create_methods_errors():
    for m in methods_data_test:
        response = client.post(
            "idsemapi/methods/",
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt)
            },
            files={
                'file': (file, open(file, 'rb')),
                'data': (None, json.dumps(m)),
            }
        )
        assert response.status_code == 500
        # No file
        response = client.post(
            "idsemapi/methods/",
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt)
            },
            files={
                'data': (None, json.dumps(m)),
            }
        )
        assert response.status_code == 422


def test_all_methods():
    response = client.get("idsemapi/methods/all")
    assert response.status_code == 200

    data = response.json()
    assert len(data) < len(inserted_methods)
    for m in data:
        assert not m['private']


def test_get_by_id():
    for m in inserted_methods:
        response = client.get(
            "idsemapi/methods/{}".format(m['id']),
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt)
            }
        )
        data = response.json()
        assert response.status_code == 200
        assert data['id'] == str(m['id'])


def test_get_by_id_errors():
    # wrong formatted id
    response = client.get("idsemapi/methods/badid")
    data = response.json()
    assert response.status_code == 400
    assert data['detail'] is not ""
    # non-existent id
    response = client.get("idsemapi/methods/61f55939068506c05536aecf")
    data = response.json()
    assert response.status_code == 404
    assert data['detail'] is not ""


def test_get_by_user_id():
    response = client.get(
        "idsemapi/methods/user_methods?user_id=1",
        headers={'Authorization': 'Bearer {}'.format(mocked_jwt)}
    )
    data = response.json()
    assert response.status_code == 200
    for m in data:
        assert m['user_id'] == str(1)
    response = client.get(
        "idsemapi/methods/user_methods?user_id=60",
        headers={'Authorization': 'Bearer {}'.format(mocked_jwt)}
    )
    assert response.status_code == 404
    response = client.get(
        "idsemapi/methods/user_methods",
        headers={'Authorization': 'Bearer {}'.format(mocked_jwt)}
    )
    assert response.status_code == 400


def test_update_method_error():
    for m, name in zip(inserted_methods, ['test3', 'test', 'test2']):
        m['name'] = name
        response = client.put(
            "idsemapi/methods/{}".format(m['id']),
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt)
            },
            files={
                'data': (None, json.dumps(m))
            }
        )
        assert response.status_code == 422


def test_update_method():
    i = 0
    for m in inserted_methods:
        updated_name = "actualizado-{}".format(i)
        updated_link = "https://www.test_{}.com".format(updated_name)
        m['name'] = updated_name
        m['link'] = updated_link
        i += 1
        response = client.put(
            "idsemapi/methods/{}".format(m['id']),
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt)
            },
            files={
                'data': (None, json.dumps(m))
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == updated_name
        assert data['link'] == updated_link


def test_update_and_evaluate_method():
    i = 0
    for m in inserted_methods:
        updated_name = "actualizado_evaluado-{}".format(i)
        updated_link = "https://www.test-ev_{}.com".format(updated_name)
        m['name'] = updated_name
        m['link'] = updated_link
        m['source_code'] = updated_link
        i += 1
        response = client.put(
            "idsemapi/methods/{}".format(m['id']),
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt)
            },
            files={
                'file': (file, open(file, 'rb')),
                'data': (None, json.dumps(m)),
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == updated_name
        assert data['link'] == updated_link


def test_remove_method():
    for m in inserted_methods:
        response = client.delete(
            "idsemapi/methods/{}".format(m['id']),
            headers={'Authorization': 'Bearer {}'.format(mocked_jwt)}
        )
        assert response.status_code == 200
        assert response.json()['success']


def test_remove_method_error():
    for m in inserted_methods:
        response = client.delete(
            "idsemapi/methods/{}".format(m['id']),
            headers={'Authorization': 'Bearer {}'.format(mocked_jwt)}
        )
        assert response.status_code == 404
