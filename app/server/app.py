from fastapi import FastAPI

from app.server.views import Method_view

app = FastAPI()
app.include_router(method_view.router)


@app.get("/")
async def root():
    return {
        "Bienvenido": "Esta es la API de la plataforma"
    }
