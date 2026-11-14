"""Esta es una api de prueba para desplegar en fastapi cloud"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

"""
En zsh:

curl https://app-prueba-10ef7b9a.fastapicloud.dev

curl "https://app-prueba-10ef7b9a.fastapicloud.dev/items/3"
"""