from PIL import ImageDraw

from detection.dto.target import Target
from detection.target_sectors.config import SectorConfig


def draw_target_box(image, target: Target):
    draw = ImageDraw.Draw(image)

    x1 = target.center.x - target.width / 2
    y1 = target.center.y - target.height / 2
    x2 = target.center.x + target.width / 2
    y2 = target.center.y + target.height / 2
    draw.rectangle([x1, y1, x2, y2], outline=(0, 255, 255), width=SectorConfig.line_width)
