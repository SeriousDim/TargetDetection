from app.models.dto.hit import Hit
from app.models.dto.target import Target
from app.models.geometry.point import GeometricalPoint
from app.services.image_processing import boxes_to_hits, boxes_to_targets


def test_boxes_to_targets():
    boxes = {0.0: [[1, 1, 2, 2]]}
    targets = boxes_to_targets(boxes)
    assert len(targets) == 1
    assert isinstance(targets[0], Target)
    assert targets[0].center == GeometricalPoint(x=1, y=1)


def test_boxes_to_hits():
    boxes = {0: [[1, 1, 2, 2]]}
    hits = boxes_to_hits(boxes)
    assert len(hits) == 1
    assert isinstance(hits[0], Hit)
    assert hits[0].center == GeometricalPoint(x=1, y=1)
