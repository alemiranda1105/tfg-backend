from app.server.auth.auth_handler import sign_jwt

mocked_jwt = sign_jwt("1", "user")['token']
mocked_jwt_admin = sign_jwt("1", "admin")['token']

methods_data_test = [
    {
        "user_id": "1",
        "name": "test",
        "info": "This is an example",
        "link": "https://www.example.com",
        "private": True,
        "anonymous": False,
        "results": {}
    },
    {
        "user_id": "1",
        "name": "test2",
        "info": "This is an example2",
        "link": "https://www.example.com",
        "source_code": "https://www.example.com",
        "private": False,
        "anonymous": False,
        "results": {}
    },
    {
        "user_id": "1",
        "name": "test3",
        "info": "This is an example3",
        "link": "https://www.example.com",
        "private": False,
        "anonymous": False,
        "results": {}
    }
]

user_data_test = [
    {
        "username": "test1",
        "email": "test1@test.com",
        "password": "123456"
    },
    {
        "username": "test2",
        "email": "test2@test.com",
        "password": "123456"
    },
    {
        "username": "test3",
        "email": "test3@test.com",
        "password": "123456"
    }
]

content_data_test = [
    {
        "title": "About",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed at fermentum magna, ac ultrices eros. "
                "Ut lacinia nisl eu urna ornare scelerisque. Aenean scelerisque mi vitae ipsum molestie, at lobortis "
                "purus iaculis. Nam ultrices rutrum metus, vulputate commodo lorem posuere at. Pellentesque et ligula "
                "egestas, rhoncus mi at, tempus sapien. Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                "Nullam lorem diam, eleifend a mauris id, sodales volutpat velit. Etiam sit amet dapibus risus, "
                "id tincidunt enim. Aliquam sit amet enim maximus, tincidunt mauris in, congue turpis. Donec arcu "
                "augue, feugiat sit amet nulla non, lobortis auctor sem. Integer non justo dignissim, tristique nulla "
                "at, lacinia lectus. Curabitur dictum convallis justo sed elementum. Vivamus nec pellentesque dolor, "
                "et convallis leo. "
    },
    {
        "title": "Description",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed at fermentum magna, ac ultrices eros. "
                "Ut lacinia nisl eu urna ornare scelerisque. Aenean scelerisque mi vitae ipsum molestie, at lobortis "
                "purus iaculis. Nam ultrices rutrum metus, vulputate commodo lorem posuere at. Pellentesque et ligula "
                "egestas, rhoncus mi at, tempus sapien. Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                "Nullam lorem diam, eleifend a mauris id, sodales volutpat velit. Etiam sit amet dapibus risus, "
                "id tincidunt enim. Aliquam sit amet enim maximus, tincidunt mauris in, congue turpis. Donec arcu "
                "augue, feugiat sit amet nulla non, lobortis auctor sem. Integer non justo dignissim, tristique nulla "
                "at, lacinia lectus. Curabitur dictum convallis justo sed elementum. Vivamus nec pellentesque dolor, "
                "et convallis leo. "
    }
]
