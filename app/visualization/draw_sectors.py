from PIL import ImageDraw

from app.config.sector_config import SectorConfig
from app.models.geometry.geometry import Geometry
from app.models.sectors.angle_sector import AngleSector
from app.models.sectors.circle_sector import CircleSector


def draw_circle_sector(image, box: Geometry, sector: CircleSector):
    draw = ImageDraw.Draw(image)

    x_shift = sector.center.x * box.width
    width_radius = box.width * sector.radius
    y_shift = sector.center.y * box.height
    height_radius = box.height * sector.radius
    x1 = box.center.x + x_shift - width_radius
    y1 = box.center.y + y_shift - height_radius
    x2 = box.center.x + x_shift + width_radius
    y2 = box.center.y + y_shift + height_radius
    draw.ellipse(
        [x1, y1, x2, y2], outline=(255, 0, 0), width=SectorConfig.line_width
    )


def draw_angle_sector(image, box: Geometry, sector: AngleSector):
    draw = ImageDraw.Draw(image)

    x_shift = sector.center.x * box.width
    y_shift = sector.center.y * box.height
    x0 = box.center.x + x_shift
    y0 = box.center.y + y_shift
    x1 = box.center.x + x_shift + sector.rays[0].x * box.width
    y1 = box.center.y + y_shift + sector.rays[0].y * box.height
    x2 = box.center.x + x_shift + sector.rays[1].x * box.width
    y2 = box.center.y + y_shift + sector.rays[1].y * box.height
    draw.line(
        [x0, y0, x1, y1], fill=(255, 0, 0), width=SectorConfig.line_width
    )
    draw.line(
        [x0, y0, x2, y2], fill=(255, 0, 0), width=SectorConfig.line_width
    )
