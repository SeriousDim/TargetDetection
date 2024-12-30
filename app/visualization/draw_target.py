from PIL import ImageDraw

from app.config.sector_config import SectorConfig
from app.models.dto.target import Target


def draw_target_box(image, target: Target):
    draw = ImageDraw.Draw(image)

    x1 = target.center.x - target.width / 2
    y1 = target.center.y - target.height / 2
    x2 = target.center.x + target.width / 2
    y2 = target.center.y + target.height / 2

    # Отрисовка рамки
    draw.rectangle(
        [x1, y1, x2, y2],
        outline=(0, 255, 255),
        width=SectorConfig.line_width,
    )
    # Отрисовка текста в центре мишени
    draw.text((target.center.x, target.center.y), "Target", fill=(255, 0, 0))
