from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.views import Method_view, User_view, Content_view, Changelog_view

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://idsem.ulpgc.es"
]

app = FastAPI()
prefix = "/idsemapi"

app.include_router(Method_view.router, prefix=prefix)
app.include_router(User_view.router, prefix=prefix)
app.include_router(Content_view.router, prefix=prefix)
app.include_router(Changelog_view.router, prefix=prefix)

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
