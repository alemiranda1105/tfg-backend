from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.server.views import Method_view, User_view

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000"
]

app = FastAPI()
app.include_router(Method_view.router)
app.include_router(User_view.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {
        "Bienvenido": "Esta es la API de la plataforma"
    }
