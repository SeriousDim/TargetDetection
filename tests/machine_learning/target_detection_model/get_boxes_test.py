import os
import pytest

from app.machine_learning.hit_detection_model import HitDetectionModel
from app.machine_learning.target_detection_model import TargetDetectionModel


@pytest.fixture
def model():
    yield TargetDetectionModel()


def test_get_boxes_return_format(model):
    model.detect(f"{os.path.dirname(os.path.abspath(__file__))}/../resources/3897_1.jpg")
    boxes = model.get_boxes()
    assert type(boxes) is dict
    assert type(boxes[0.0]) is list
    assert type(boxes[0.0][0]) is list
    assert type(boxes[0.0][0][0]) is float
