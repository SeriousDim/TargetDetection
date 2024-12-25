from collections import Counter

from app.config.sector_config import SectorConfig
from app.models.dto.hit import Hit
from app.models.dto.hit_sector import HitSector
from app.models.dto.target import Target
from app.models.geometry.point import GeometricalPoint


def locate_point_sector(point: GeometricalPoint, target: Target):
    if not target.contains_point(point):
        return None

    normalized_point = GeometricalPoint(
        x=(point.x - target.center.x) / target.width,
        y=(point.y - target.center.y) / target.height,
    )

    if SectorConfig.center_sector.contains_point(normalized_point):
        return SectorConfig.center_sector
    for sector in SectorConfig.angle_sectors:
        # Обрабатываем отдельно сектора на границах
        if sector.name == "3":
            continue
        if sector.contains_point(normalized_point):
            return sector
    return SectorConfig.angle_sectors[1]


def locate_hit_sector(hit: Hit, target: Target) -> HitSector:
    points = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5), (0, 0)]
    sectors = []

    for p in points:
        result = locate_point_sector(
            GeometricalPoint(
                x=hit.center.x + hit.width * p[0],
                y=hit.center.y + hit.height * p[1],
            ),
            target,
        )
        if result is None:
            sectors.append("10")
        else:
            sectors.append(result.name)

    if "1" in sectors:
        total_sector = "1"
    else:
        c = Counter(sectors)
        total_sector = c.most_common(1)[0][0]

    return HitSector(hit_id=hit.id, sector=total_sector)
