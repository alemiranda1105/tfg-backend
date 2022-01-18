from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
        "Bienvenido": "Esta es la API de la plataforma"
    }
