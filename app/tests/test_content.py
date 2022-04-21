from starlette.testclient import TestClient
from app.server.app import app
from app.tests.mocked_test_data import content_data_test, mocked_jwt, mocked_jwt_admin

client = TestClient(app)

inserted_content = []


def test_get_all_error():
    response = client.get("content/")
    assert response.status_code == 404


def test_create_content_error():
    content = content_data_test[0]
    response = client.post(
        "content/",
        headers={
            'Authorization': 'Bearer {}'.format(mocked_jwt)
        },
        json=content
    )
    assert response.status_code == 403


def test_create_content():
    for c in content_data_test:
        response = client.post(
            "content/",
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt_admin)
            },
            json=c
        )
        assert response.status_code == 200
        data = response.json()
        inserted_content.append(data['id'])
    assert len(inserted_content) == len(content_data_test)


def test_get_all():
    response = client.get("content/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(content_data_test)


def test_get_by_title():
    response = client.get("content/{}".format(content_data_test[0]['title']))
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == content_data_test[0]['title']


def test_get_by_title_error():
    response = client.get("content/error")
    assert response.status_code == 404


def test_update_content():
    updated = content_data_test[0]
    updated['text'] = "text updated"
    response = client.put(
        "content/{}".format(inserted_content[0]),
        headers={
            'Authorization': 'Bearer {}'.format(mocked_jwt_admin)
        },
        json=updated
    )
    assert response.status_code == 200
    data = response.json()
    assert data['text'] != content_data_test[0]


def test_delete_content_error():
    for c in inserted_content:
        response = client.delete(
            "content/{}".format(c),
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt)
            })
        assert response.status_code == 403


def test_delete_content():
    deleted = 0
    for c in inserted_content:
        response = client.delete(
            "content/{}".format(c),
            headers={
                'Authorization': 'Bearer {}'.format(mocked_jwt_admin)
            })
        assert response.status_code == 200
        deleted += 1
    assert deleted == len(inserted_content)
