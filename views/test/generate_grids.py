from pathlib import Path

from PIL import Image

from detection.target_sectors.draw.draw_hits import draw_hits
from detection.target_sectors.draw.target_grid import draw_target_grid
from detection.target_sectors.locate_hit_sector import locate_hit_sector
from detection.yolo.model import DetectionModel
from views.adapters.target import model_boxes_to_targets, model_boxes_to_hits, get_boxes_with_labels

model = DetectionModel()

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
    # hits = model_boxes_to_hits(boxes[0])

    draw_target_grid(image, target)

    """
    hit_sectors = []
    for h in hits:
        hit_sectors.append(locate_hit_sector(h, target))

    draw_hits(image, hit_sectors, hits)
    """
    image.save(f"./grids/{image_path.stem}.png")
