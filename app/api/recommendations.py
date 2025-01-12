from base64 import b64encode
from io import BytesIO

from fastapi import APIRouter, File, UploadFile
from PIL import Image

from app.machine_learning.hit_detection_model import HitDetectionModel
from app.machine_learning.target_detection_model import TargetDetectionModel
from app.services.hit_sector_service import locate_hit_sector
from app.services.hit_service import filter_new_hits
from app.services.image_processing import boxes_to_hits, boxes_to_targets
from app.services.recommendation_service import get_recommendations_for_sectors
from app.visualization.draw_hits import draw_hits
from app.visualization.target_grid import draw_target_grid

router = APIRouter()

# Инициализация моделей
target_model = TargetDetectionModel()
hit_model = HitDetectionModel()


@router.post("/recommendations")
async def recommendations(file: UploadFile = File(...)):
    """
    Анализ изображения, возвращение рекомендаций и визуализация результатов.
    """
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes))

    target_model.detect([image])
    target_boxes = target_model.get_boxes()
    targets = boxes_to_targets(target_boxes)

    if not targets:
        return {"message": "Мишени не найдены."}

    hit_model.detect([image])
    hit_boxes = hit_model.get_boxes()
    hits = boxes_to_hits(hit_boxes)

    target = targets[0]
    new_hits = filter_new_hits(hits, target.name)

    draw_target_grid(image, target)
    hit_sectors = [locate_hit_sector(hit, target) for hit in new_hits]
    draw_hits(image, hit_sectors, new_hits)

    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    base64_encoded_image = b64encode(img_byte_arr.getvalue()).decode(
        "utf-8"
    )

    """
    sectors_outside_target = filter(lambda e: e.sector == "0" or "10", hit_sectors)    
    sectors_inside_target = filter(lambda e: e.sector >= "1" and e.sector <= "9", hit_sectors)

    if len(sectors_inside_target) > 4:
        Рекомендаций нет
    else if len(sectors_inside_target) == 4:
        Ищем рекомендацию

    answer = sectors_inside_target

    for i in range(4 - len(answer)):
        answer.append(sectors_outside_target[i])
    
    """
    sectors = ", ".join([f"С{sector.sector}" for sector in hit_sectors])
    recommendation = get_recommendations_for_sectors(sectors)

    return {
        "target_name": target.name,
        "hits_sectors": [sector.sector for sector in hit_sectors],
        "recommendation": recommendation,
        "image": base64_encoded_image,
    }
