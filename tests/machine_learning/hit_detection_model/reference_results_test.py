import os
import pytest
from PIL import Image

from app.machine_learning.hit_detection_model import HitDetectionModel
from tests.machine_learning.iou import calculate_iou_for_result
from tests.machine_learning.resources.reference_results import results

IOU_THRESHOLD = 0.75


def script(model, image_name):
    image = Image.open(f"{os.path.dirname(os.path.abspath(__file__))}/../resources/{image_name}.jpg")
    model.detect([image])
    boxes = model.get_boxes()[0.0]
    name, stage = image_name.split('_')
    result_list = results[name][stage]["hits"][0.0]
    assert len(boxes) == len(result_list)

    answer = 0
    for res in result_list:
        for box in boxes:
            if calculate_iou_for_result(box, res) >= IOU_THRESHOLD:
                answer += 1
                break

    assert answer == len(result_list)


@pytest.fixture
def model():
    yield HitDetectionModel()


def test_reference_result_3891_1(model):
    script(model, "3897_1")


def test_reference_result_3891_2(model):
    script(model, "3897_2")


def test_reference_result_3891_3(model):
    script(model, "3897_3")


def test_reference_result_3901_1(model):
    script(model, "3901_1")


def test_reference_result_3901_2(model):
    script(model, "3901_2")


def test_reference_result_3901_3(model):
    script(model, "3901_3")

