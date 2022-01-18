from app.server.database import methods_collection, methods_helper


async def find_all():
    methods = []
    for m in methods_collection.find():
        methods.append(methods_helper(m))
    return methods
