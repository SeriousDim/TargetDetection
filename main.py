import base64
import logging
from io import BytesIO

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

from detection.dto.hit import Hit
from detection.target_sectors.draw.draw_hits import draw_hits
from detection.target_sectors.draw.target_grid import draw_target_grid
from detection.target_sectors.locate_hit_sector import locate_hit_sector
from detection.yolo.models.hit_detection_model import HitDetectionModel
from detection.yolo.models.target_detection_model import TargetDetectionModel
from views.adapters.new_adapters import boxes_to_hits, boxes_to_targets
from models_for_swag import Hit, VisualizationRequest, VisualizationResponse

app = FastAPI()

# Подключение статических файлов и шаблонов Jinja2
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Инициализация моделей
target_model = TargetDetectionModel()
hit_model = HitDetectionModel()

logging.basicConfig(level=logging.DEBUG)

previous_hits = {}

# Маршрут для отображения HTML-страницы
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def calculate_iou(hit1: Hit, hit2: Hit) -> float:
    # Вычисляем координаты пересекающегося прямоугольника
    x1 = max(hit1.center.x - hit1.width / 2, hit2.center.x - hit2.width / 2)
    y1 = max(hit1.center.y - hit1.height / 2, hit2.center.y - hit2.height / 2)
    x2 = min(hit1.center.x + hit1.width / 2, hit2.center.x + hit2.width / 2)
    y2 = min(hit1.center.y + hit1.height / 2, hit2.center.y + hit2.height / 2)

    # Проверяем, есть ли пересечение
    if x1 >= x2 or y1 >= y2:
        return 0.0

    # Площадь пересечения
    intersection_area = (x2 - x1) * (y2 - y1)

    # Площади прямоугольников
    area1 = hit1.width * hit1.height
    area2 = hit2.width * hit2.height

    # Вычисляем IoU
    iou = intersection_area / (area1 + area2 - intersection_area)
    return iou


def filter_new_hits(hits: list[Hit], target_name: str) -> list[Hit]:
    global previous_hits

    # Если нет старых данных для данной мишени, считаем все попадания новыми
    if target_name not in previous_hits:
        previous_hits[target_name] = hits
        return hits

    # Фильтруем попадания с IoU > 0.5
    old_hits = previous_hits[target_name]
    new_hits = []
    for hit in hits:
        is_new = True
        for old_hit in old_hits:
            if calculate_iou(hit, old_hit) > 0.5:
                is_new = False
                break
        if is_new:
            new_hits.append(hit)

    # Обновляем глобальные данные для данной мишени
    previous_hits[target_name] = old_hits + new_hits
    return new_hits


@app.post(
    "/visualization_recommendations",
    response_model=VisualizationResponse,
    summary="Анализ изображения мишени",
    description="Принимает изображение, анализирует попадания и возвращает размеченное изображение с рекомендациями."
)
async def visualization_recommendations(file: UploadFile = File(...)):
    """
    Эндпоинт для анализа изображения.
    - **file**: Загружаемое изображение.
    
    Возвращает:
    - **target_name**: Название мишени.
    - **hits_sectors**: Список секторов, в которые попали.
    - **recommendation**: Рекомендация для улучшения.
    - **image**: Размеченное изображение в формате Base64.
    """
    try:
        # Чтение изображения из файла
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes))

        # Получение результатов детекции для мишени
        target_model.detect([image])
        target_boxes = target_model.get_boxes()
        targets = boxes_to_targets(target_boxes)

        # Проверяем наличие мишеней
        if not targets:
            logging.error("Мишени не найдены на изображении.")
            return {"message": "Мишени не найдены на изображении."}

        # Получение результатов детекции для попаданий
        hit_model.detect([image])
        hit_boxes = hit_model.get_boxes()
        hits = boxes_to_hits(hit_boxes)

        # Фильтруем новые попадания
        target_name = targets[0].name
        new_hits = filter_new_hits(hits, target_name)

        # Рисуем мишени и только новые попадания
        draw_target_grid(image, targets[0])  # Рисуем только первую мишень
        hit_sectors = [locate_hit_sector(hit, targets[0]) for hit in new_hits]
        draw_hits(image, hit_sectors, new_hits)

        # Сохраняем размеченное изображение в байтовый поток
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Преобразуем изображение в строку base64
        base64_encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")
        
        # Определение рекомендации по новым попаданиям
        sorted_sectors = sorted([int(sector.sector) for sector in hit_sectors])
        sectors = ", ".join([f"С{sector}" for sector in sorted_sectors])

        matched_recommendation = get_recommendations_for_sectors(sectors)

        # Возвращаем результат
        return {
            "target_name": target_name,
            "hits_sectors": sorted([int(sector.sector) for sector in hit_sectors]),
            "recommendation": matched_recommendation,
            "image": base64_encoded_image,
        }

    except Exception as e:
        logging.error(f"Ошибка при анализе изображения: {str(e)}")
        return {"message": f"Ошибка при анализе изображения: {str(e)}"}


def get_recommendations_for_sectors(sectors):
    # Тут реализуется логика для получения рекомендаций на основе секторов
    # В примере подгружается Excel-файл с рекомендациями

    # Функция для замены "-" на "C10" в строках, где они есть
    def replace_dashes_with_c10(cell):
        if "-" in cell:
            # Убираем все запятые из строки
            cell = cell.replace(",", "")
            # Разбиваем строку на элементы, игнорируя пустые элементы
            parts = [part.strip() for part in cell.split() if part.strip()]
            # Заменяем "-" на "С10"
            updated_parts = ["С10" if part == "-" else part for part in parts]
            # Соединяем элементы через запятую
            return ", ".join(updated_parts)
        return cell.strip()  # Удаляем пробелы для остальных строк

    # Функция для сортировки содержимого ячейки
    def sort_sectors(cell):
        if not cell:
            return cell  # Пропускаем пустые ячейки
        
        # Разделяем строку по запятой, удаляем пробелы
        sectors = [s.strip() for s in cell.split(",")]
        
        # Сортируем по числовому значению после "С"
        sectors.sort(key=lambda s: int(s[1:]) if s.startswith("С") else float("inf"))
        
        # Соединяем обратно через запятую
        return ", ".join(sectors)

    df = pd.read_excel(
        "./detection/recommendations/resources/recommendations.xlsx"
    )

    df["Пример набора секторов пробоин с 10м"] = df["Пример набора секторов пробоин с 10м"].apply(replace_dashes_with_c10)
    df['Пример набора секторов пробоин с 10м'] = df['Пример набора секторов пробоин с 10м'].apply(sort_sectors)
    matched_row = df[df["Пример набора секторов пробоин с 10м"] == sectors]

    if matched_row.empty:
        return "Рекомендация не найдена для текущего набора секторов."

    recommendation = matched_row.iloc[0]["Рекомендаци"]
    return recommendation


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
