from base64 import b64encode
from io import BytesIO

from fastapi import APIRouter, File, UploadFile
from PIL import Image

from app.machine_learning.hit_detection_model import HitDetectionModel
from app.machine_learning.target_detection_model import TargetDetectionModel
from app.models.dto.hit_sector import HitSector
from app.models.dto.target import Target
from app.models.geometry.point import GeometricalPoint
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
        # return {"message": "Мишени не найдены."}
        target = Target(id=0, name="-", center=GeometricalPoint(x=image.size[0] * 0.5, y=image.size[1] * 0.5), 
                        width=image.size[0], height=image.size[1])
    else:
        target = targets[0]

    hit_model.detect([image])
    hit_boxes = hit_model.get_boxes()
    hits = boxes_to_hits(hit_boxes)

    new_hits = filter_new_hits(hits, target.name)

    draw_target_grid(image, target)
    hit_sectors = [locate_hit_sector(hit, target) for hit in new_hits]
    print("hit_sectors:", hit_sectors, sep="\n")

    # Фильтрация секторов с 1 по 9
    primary_sectors = [
        sector
        for sector in hit_sectors
        if sector.sector in [str(i) for i in range(1, 10)]
    ]
    print("primary_sectors:", primary_sectors, sep="\n")

    # Если секторов с 1 по 9 меньше 4, добавляем сектора 0 или 10
    if len(primary_sectors) < 4:
        zero_sectors = [
            sector for sector in hit_sectors if sector.sector == "0"
        ]
        print("zero_sectors:", zero_sectors, sep="\n")
        ten_sectors = [
            sector for sector in hit_sectors if sector.sector == "10"
        ]
        print("ten_sectors:", ten_sectors, sep="\n")

        additional_sectors = zero_sectors + ten_sectors

        while len(primary_sectors) < 4:
            if additional_sectors:
                primary_sectors.append(additional_sectors.pop(0))
            else:
                primary_sectors.append(HitSector(hit_id=-1, sector="0"))

    print(f"Финальные сектора: {primary_sectors}")

    draw_hits(image, primary_sectors, new_hits)

    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    base64_encoded_image = b64encode(img_byte_arr.getvalue()).decode("utf-8")

    sorted_primary_sectors = sorted(
        primary_sectors, key=lambda x: int(x.sector)
    )
    sectors = ", ".join(
        [f"С{sector.sector}" for sector in sorted_primary_sectors]
    )
    recommendation = get_recommendations_for_sectors(sectors)

    return {
        "target_name": target.name,
        "hits_sectors": [sector.sector for sector in sorted_primary_sectors],
        "recommendation": recommendation,
        "image": base64_encoded_image,
    }
