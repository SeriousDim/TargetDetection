import os
import pytest
from PIL import Image

from app.machine_learning.target_detection_model import TargetDetectionModel
from app.models.geometry.geometry import Geometry
from app.models.geometry.point import GeometricalPoint
from app.services.hit_service import calculate_iou
from tests.machine_learning.iou import calculate_iou_for_result
from tests.machine_learning.resources.reference_results import results

IOU_THRESHOLD = 0.75


def script(model, image_name):
    image = Image.open(f"{os.path.dirname(os.path.abspath(__file__))}/../resources/{image_name}.jpg")
    model.detect([image])
    box = model.get_boxes()[0.0]
    name, stage = image_name.split('_')
    result = results[name][stage]["target"][0.0]
    assert len(box) == len(result)
    assert calculate_iou_for_result(box[0], result[0]) >= IOU_THRESHOLD


@pytest.fixture
def model():
    yield TargetDetectionModel()


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
