from pathlib import Path

from PIL import Image

from detection.target_sectors.draw.draw_hits import draw_hits
from detection.target_sectors.draw.target_grid import draw_target_grid
from detection.target_sectors.locate_hit_sector import locate_hit_sector
from detection.yolo.models.hit_detection_model import HitDetectionModel
from detection.yolo.models.target_detection_model import TargetDetectionModel
from views.adapters.new_adapters import boxes_to_targets, boxes_to_hits

target_model = TargetDetectionModel()
hit_model = HitDetectionModel()

test_images_path = Path("./test_images")
test_images = list(test_images_path.iterdir())

for image_path in test_images:
    image = Image.open(image_path, mode='r')
    image = image.resize((1280, 1280))

    results = target_model.detect(image)
    boxes = target_model.get_boxes()
    targets = boxes_to_targets(boxes)

    results = hit_model.detect(image)
    boxes = hit_model.get_boxes()
    hits = boxes_to_hits(boxes)

    if len(targets) > 0:
        target = targets[0]
        draw_target_grid(image, target)

        hit_sectors = []
        for h in hits:
            hit_sectors.append(locate_hit_sector(h, target))

        draw_hits(image, hit_sectors, hits)

    image.save(f"./grids/{image_path.stem}.png")
