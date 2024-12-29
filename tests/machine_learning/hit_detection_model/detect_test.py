import pytest

from app.machine_learning.hit_detection_model import HitDetectionModel


@pytest.fixture
def model():
    yield HitDetectionModel()


def test_detect_return_format(model):
    pass

