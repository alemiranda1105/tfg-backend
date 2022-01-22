from fastapi import FastAPI

from app.server.views import Method_view, User_view

app = FastAPI()
app.include_router(Method_view.router)
app.include_router(User_view.router)


@app.get("/")
async def root():
    return {
        "Bienvenido": "Esta es la API de la plataforma"
    }
