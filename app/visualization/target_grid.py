from app.config.sector_config import SectorConfig
from app.models.dto.target import Target
from app.visualization.draw_sectors import (
    draw_angle_sector,
    draw_circle_sector,
)
from app.visualization.draw_target import draw_target_box


def draw_target_grid(image, target: Target):
    draw_target_box(image, target)

    draw_circle_sector(image, target, SectorConfig.center_sector)
    for angle_sector in SectorConfig.angle_sectors:
        draw_angle_sector(image, target, angle_sector)
