from PIL import ImageDraw

from detection.dto.hit import Hit
from detection.dto.hit_sector import HitSector

SECTOR_COLORS = {
    '1': (255, 149, 0),
    '2': (190, 111, 0),
    '3': (190, 111, 0),
    '4': (190, 111, 0),
    '5': (190, 111, 0),
    '6': (190, 111, 0),
    '7': (190, 111, 0),
    '8': (190, 111, 0),
    '9': (190, 111, 0),
    '10': (126, 74, 0),
}


def draw_hit(image, sector_name: str, hit: Hit):
    draw = ImageDraw.Draw(image)

    x1 = hit.center.x - hit.width / 2
    y1 = hit.center.y - hit.height / 2
    x2 = hit.center.x + hit.width / 2
    y2 = hit.center.y + hit.height / 2
    draw.rectangle([x1, y1, x2, y2], outline=(0, 255, 255), width=2)
    draw.text((x1 + 1, y1 + 1), sector_name, (0, 255, 255))


def draw_hits(image, sectors: list[HitSector], hits: list[Hit]):
    for i in range(len(sectors)):
        draw_hit(image, sectors[i].sector, hits[i])