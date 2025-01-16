from app.models.dto.hit import Hit
from app.models.geometry.geometry import Geometry


def calculate_iou(hit1: Geometry, hit2: Geometry) -> float:
    x1 = max(hit1.center.x - hit1.width / 2, hit2.center.x - hit2.width / 2)
    y1 = max(hit1.center.y - hit1.height / 2, hit2.center.y - hit2.height / 2)
    x2 = min(hit1.center.x + hit1.width / 2, hit2.center.x + hit2.width / 2)
    y2 = min(hit1.center.y + hit1.height / 2, hit2.center.y + hit2.height / 2)

    if x1 >= x2 or y1 >= y2:
        return 0.0

    intersection_area = (x2 - x1) * (y2 - y1)
    area1 = hit1.width * hit1.height
    area2 = hit2.width * hit2.height

    return intersection_area / (area1 + area2 - intersection_area)


previous_hits = {}


def filter_new_hits(hits: list[Hit], target_name: str) -> list[Hit]:
    global previous_hits

    if target_name not in previous_hits:
        previous_hits[target_name] = hits
        return hits

    old_hits = previous_hits[target_name]
    new_hits = []
    for hit in hits:
        if all(calculate_iou(hit, old_hit) <= 0.5 for old_hit in old_hits):
            new_hits.append(hit)

    previous_hits[target_name] = old_hits + new_hits
    return new_hits


def clear_previous_hits():
    global previous_hits
    previous_hits = {}
