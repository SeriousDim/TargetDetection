import json
import logging  # ! Логги
import random  # ! Искусственные данные
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image

from detection.dto.hit import Hit  # ! Искусственные данные
from detection.dto.hit_sector import HitSector
from detection.dto.target import Target
from detection.target_sectors.draw.draw_hits import draw_hits
from detection.target_sectors.draw.target_grid import draw_target_grid
from detection.target_sectors.locate_hit_sector import locate_hit_sector
from detection.yolo.model import DetectionModel
from geometry.point import GeometricalPoint  # ! Искусственные данные
from views.adapters.target import (
    model_boxes_to_targets,
)  # model_boxes_to_hits,

# * Инициализация моделей
target_model = DetectionModel()
# hit_model = HitDetectionModel()

service_router = APIRouter(tags=["detection"])

# Загружаем Excel файл в память при запуске сервера
RECOMMENDATIONS_PATH = (
    "./detection/recommendations/resources/recommendations.xlsx"
)
try:
    recommendations_df = pd.read_excel(RECOMMENDATIONS_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Excel файл по пути {RECOMMENDATIONS_PATH} не найден.")

logging.basicConfig(level=logging.DEBUG)  # ! Логги


def generate_fake_hits(targets, num_hits=4):
    """
    Генератор попаданий.
    """
    hits = []
    for _ in range(num_hits):
        target = targets[0]
        x_offset = random.uniform(
            -target.width / 4, target.width / 4
        )  # ! Смещение попадания
        y_offset = random.uniform(-target.height / 4, target.height / 4)

        hit = Hit(
            id=random.randint(1000, 9999),  # ! Случайный ID для попадания
            center=GeometricalPoint(
                x=target.center.x + x_offset, y=target.center.y + y_offset
            ),
            width=target.width / 10,
            height=target.height / 10,
        )
        hits.append(hit)
    return hits


@service_router.post("/predict")
async def predict(file: UploadFile = File(...)):
    # * Читаем, загружаем и получаем размеры изображения
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes))
    image_size = {"width": image.width, "height": image.height}

    # * Отправляем изображения в модели
    target_model.detect([image])
    # hit_model.detect([image])

    # * Получаем коробки для мишеней и попаданий
    target_boxes = target_model.get_boxes()
    # hit_boxes = hit_model.get_boxes()

    # * Преобразуем коробки объекты Target и Hit
    logging.debug(f"Списки классов для мишеней: {target_boxes[0]}")  # ! Логги
    targets = model_boxes_to_targets(target_boxes[0])
    # logging.debug(f"Списки классов для попаданий: {hit_boxes[0]}")  # ! Логги
    # hits = model_boxes_to_hits(hit_boxes[0])

    hits = generate_fake_hits(targets)  # ! Искусственные данные

    response_content = {
        "targets": [target.dict() for target in targets],
        "hits": [hit.dict() for hit in hits],
        "image_size": image_size,
    }

    return JSONResponse(content=response_content)


@service_router.post("/sectors")
async def get_sectors(detection_results: dict):
    # * Извлекаем результаты детекции
    hits = detection_results.get("hits", [])
    targets = detection_results.get("targets", [])

    logging.debug(
        f"Результаты обнаружения - Попадания: {hits}, Мишени: {targets}"
    )  # ! Логги

    # * Проверяем, что есть и мишени, и попадания
    if not hits or not targets:
        return JSONResponse(
            content={"message": "Нет мишеней или попаданий"}, status_code=400
        )

    target = Target(**targets[0])
    hit_sectors = []

    # * Определяем сектора для каждого попадания
    for hit_data in hits:
        hit = Hit(**hit_data)
        sector = locate_hit_sector(hit, target)
        logging.debug(f"Hit ID: {hit.id}, Sector: {sector.sector}")  # ! Логги
        hit_sectors.append({"hit_id": hit.id, "sector": sector.sector})

    return JSONResponse(content=hit_sectors)


@service_router.post("/sector_visualization")
async def sector_visualization(
    file: UploadFile = File(...), detection_results: str = Form(...)
):
    # * Читаем и загружаем изображение
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes))

    # * Парсим строку JSON в словарь
    try:
        detection_results = json.loads(detection_results)
    except json.JSONDecodeError:
        return JSONResponse(
            content={"message": "Инвалид"},
            status_code=400,
        )

    # * Извлекаем результаты детекции
    hits_data = detection_results.get("hits", [])
    targets_data = detection_results.get("targets", [])

    # ! Логгирование данных
    logging.debug(
        "Результаты детекции для визуализации: "
        f"Попадания: {hits_data}, Мишени: {targets_data}"
    )

    # * Проверяем, что есть и мишени, и попадания
    if not hits_data or not targets_data:
        return JSONResponse(
            content={"message": "Нет мишеней или попаданий"}, status_code=400
        )

    # * Преобразование данных в объекты
    target = Target(**targets_data[0])

    # Преобразование попаданий из словарей в объекты Hit
    hits = [
        hit_data if isinstance(hit_data, Hit) else Hit(**hit_data)
        for hit_data in hits_data
    ]

    # * Рисуем сетку мишени
    draw_target_grid(image, target)

    # * Определяем сектора для каждого попадания
    hit_sectors = []
    for hit in hits:
        sector = locate_hit_sector(hit, target)
        hit_sectors.append(HitSector(hit_id=hit.id, sector=sector.sector))

    # * Рисуем попадания с указанием сектора
    draw_hits(image, hit_sectors, hits)

    # * Сохраняем изображение в байтовый поток
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")


@service_router.post("/recommendations")
async def get_recommendations(detection_results: dict = Body(...)):
    """
    Эндпоинт для получения рекомендации на основе набора секторов попаданий.
    Принимает массив из 4 чисел: [1, 2, 3, 4].
    Возвращает соответствующую рекомендацию из таблицы.
    """
    # * Извлекаем массив секторов из JSON
    sectors = detection_results.get("sectors")

    # * Проверяем, что массив содержит ровно 4 элемента
    if len(sectors) != 4:
        raise HTTPException(
            status_code=400,
            detail="Необходимо передать массив из ровно 4 секторов.",
        )

    # Преобразуем массив в строку
    sectors_str = ", ".join([f"С{sector}" for sector in sectors])

    # * Поиск строки с совпадающим набором секторов
    matched_row = recommendations_df[
        recommendations_df["Пример набора секторов пробоин с 10м"]
        == sectors_str
    ]

    if matched_row.empty:
        raise HTTPException(
            status_code=404,
            detail="Рекомендация для данного набора секторов не найдена.",
        )

    recommendation = matched_row.iloc[0]["Рекомендаци"]
    return {"recommendation": recommendation}
