from bson import ObjectId

from app.server.database import methods_collection

inserted_methods = []
methods_data_test = [
        {
            "user_id": "1",
            "name": "test",
            "info": "This is an example",
            "link": "www.example.com",
            "results": [
                {
                    "name": "m1",
                    "result": 0.9192
                },
                {
                    "name": "m2",
                    "result": 0.5421
                }
            ]
        },
        {
            "user_id": "2",
            "name": "test2",
            "info": "This is an example2",
            "link": "www.example.com",
            "results": [
                {
                    "name": "m1",
                    "result": 0.8123
                },
                {
                    "name": "m2",
                    "result": 0.7263
                }
            ]
        }
    ]


def pytest_configure():
    for m in methods_data_test:
        new_method = methods_collection.insert_one(m)
        inserted_methods.append(new_method.inserted_id)


def pytest_unconfigure(config):
    for m in inserted_methods:
        methods_collection.remove({"_id": ObjectId(m)})
