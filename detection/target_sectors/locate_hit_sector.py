from detection.dto.hit import Hit
from detection.dto.hit_sector import HitSector
from detection.dto.target import Target
from detection.target_sectors.config import SectorConfig
from geometry.point import GeometricalPoint
from sectors.sector import Sector
from collections import Counter


def locate_point_sector(point: GeometricalPoint, target: Target) -> Sector | None:
    if not target.contains_point(point):
        return None

    p = GeometricalPoint(
        x=(point.x - target.center.x) / target.width,
        y=(point.y - target.center.y) / target.height
    )

    if SectorConfig.center_sector.contains_point(p):
        return SectorConfig.center_sector
    for sector in SectorConfig.angle_sectors:
        if sector.contains_point(p):
            return sector
    return None


def locate_hit_sector(hit: Hit, target: Target) -> HitSector:
    points = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5), (0,0)]
    sectors = []
    for p in points:
        result = locate_point_sector(GeometricalPoint(
            x=hit.center.x + hit.width * p[0],
            y=hit.center.y + hit.height * p[1]
        ), target)
        if result is None:
            sectors.append('10')
        else:
            sectors.append(result.name)
    if '1' in sectors:
        total_sector = '1'
    else:
        c = Counter(sectors)
        total_sector = c.most_common(1)[0][0]
    return HitSector(
        hit_id=hit.id,
        sector=total_sector
    )
