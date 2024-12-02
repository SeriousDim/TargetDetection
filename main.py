from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, EmailStr
from pyexpat.errors import messages

from detection.routes import service_router

app = FastAPI()

app.include_router(service_router)

class CreateUser(BaseModel):
    email: EmailStr

@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }

@app.get("/hello/")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}"}

@app.post("/users/")
def create_user(user: CreateUser):
    return {
        "message": "success",
        "email": user.email,
    }

@app.post("/calc/add")
def add(a: int, b: int):
    return  {
        "a": a,
        "b": b,
        "result": a + b,
    }

@app.get("/items/")
def list_items():
    return [
        "Item1",
        "Item2",
        "Item3",
    ]
@app.get("/items/latest")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}

@app.get("/items/{item_id}/")
def get_item_by_id(item_id: int):
    return {
        "item": {
            "id": item_id,
        },
    }
# Все изменения в этой директории будут отображены
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)