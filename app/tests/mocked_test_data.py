from app.server.auth.auth_handler import sign_jwt

mocked_jwt = sign_jwt("1")['token']

methods_data_test = [
        {
            "user_id": "1",
            "name": "test",
            "info": "This is an example",
            "link": "www.example.com",
            "private": True,
            "anonymous": False,
            "results": {}
        },
        {
            "user_id": "1",
            "name": "test2",
            "info": "This is an example2",
            "link": "www.example.com",
            "private": False,
            "anonymous": False,
            "results": {}
        },
        {
            "user_id": "1",
            "name": "test3",
            "info": "This is an example3",
            "link": "www.example.com",
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
