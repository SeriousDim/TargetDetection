from pathlib import Path

from PIL import Image

from detection.dto.hit import Hit
from detection.target_sectors.draw.draw_hits import draw_hits
from detection.target_sectors.draw.target_grid import draw_target_grid
from detection.target_sectors.locate_hit_sector import locate_hit_sector
from detection.yolo.models.target_detection_model import TargetDetectionModel
from geometry.point import GeometricalPoint
from views.adapters.target import model_boxes_to_targets, model_boxes_to_hits, get_boxes_with_labels

model = TargetDetectionModel()

test_images_path = Path("./test_images")
test_images = list(test_images_path.iterdir())

for image_path in test_images:
    image = Image.open(image_path, mode='r')
    image = image.resize((1280, 1280))

    results = model.detect(image)
    boxes = model.get_boxes()
    targets = get_boxes_with_labels(boxes[0], 0)

    if len(targets) == 0:
        continue

    target = targets[0]
    hits = [
        Hit(id=1, center=GeometricalPoint(x=150, y=150), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=345, y=110), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=400, y=200), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=390, y=450), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=300, y=550), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=150, y=480), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=200, y=270), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=370, y=130), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=280, y=420), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=300, y=300), width=40, height=40),
        Hit(id=1, center=GeometricalPoint(x=330, y=310), width=40, height=40),
    ]

    for i in range(len(hits)):
        h = hits[i]
        h.center.x *= 2
        h.center.y *= 2
        hits[i] = h

    draw_target_grid(image, target)

    hit_sectors = []
    for h in hits:
        hit_sectors.append(locate_hit_sector(h, target))

    draw_hits(image, hit_sectors, hits)

    image.save(f"./grids/{image_path.stem}.png")
