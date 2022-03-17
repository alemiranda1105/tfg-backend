import uvicorn
from os import environ

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=environ.get("PORT", 8000), reload=True)
