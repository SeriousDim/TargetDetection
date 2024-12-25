from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.index import router as index_router
from app.api.recommendations import router as recommendations_router

app = FastAPI()

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение маршрутов
app.include_router(index_router)
app.include_router(recommendations_router)
