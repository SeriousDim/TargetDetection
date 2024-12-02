from detection.dto.target import Target
from detection.target_sectors.config import SectorConfig
from detection.target_sectors.draw.draw_sectors import draw_circle_sector, draw_angle_sector
from detection.target_sectors.draw.draw_target import draw_target_box


def draw_target_grid(image, target: Target):
    draw_target_box(image, target)

    draw_circle_sector(image, target, SectorConfig.center_sector)
    for angle_sector in SectorConfig.angle_sectors:
        draw_angle_sector(image, target, angle_sector)
