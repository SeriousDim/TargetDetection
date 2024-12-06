from fastapi import FastAPI

from detection.routes import service_router  # Импортируем маршруты

app = FastAPI()

# Подключаем роутеры
app.include_router(service_router)


# Пробной эндпоинт для проверки
@app.get("/")
async def root():
    return {"message": "Welcome to the Detection API!"}


# # Все изменения в этой директории будут отображены
# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
