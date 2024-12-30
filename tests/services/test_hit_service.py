import pytest

from app.models.dto.hit import Hit
from app.models.geometry.point import GeometricalPoint
from app.services.hit_service import (
    calculate_iou,
    filter_new_hits,
    previous_hits,
)


def test_calculate_iou_partial_overlap():
    hit1 = Hit(center=GeometricalPoint(x=0, y=0), width=3, height=3, id=1)
    hit2 = Hit(center=GeometricalPoint(x=1, y=1), width=3, height=3, id=2)
    result = calculate_iou(hit1, hit2)
    assert pytest.approx(result, 0.01) == 4 / 14


def test_calculate_iou_full_overlap():
    hit1 = Hit(center=GeometricalPoint(x=0, y=0), width=3, height=3, id=1)
    hit2 = Hit(center=GeometricalPoint(x=0, y=0), width=3, height=3, id=2)
    result = calculate_iou(hit1, hit2)
    assert pytest.approx(result, 0.1) == 1


def test_calculate_iou_partial_overlap_large():
    hit1 = Hit(center=GeometricalPoint(x=0, y=0), width=6, height=6, id=1)
    hit2 = Hit(center=GeometricalPoint(x=2, y=2), width=4, height=4, id=2)
    result = calculate_iou(hit1, hit2)
    assert pytest.approx(result, 0.01) == 9 / 43


def test_filter_new_hits():
    global previous_hits
    previous_hits.clear()

    previous_hits_data = [
        Hit(center=GeometricalPoint(x=0, y=0), width=2, height=2, id=1),
    ]
    new_hits_data = [
        Hit(center=GeometricalPoint(x=3, y=3), width=2, height=2, id=2),
    ]

    previous_hits["target"] = previous_hits_data

    result = filter_new_hits(previous_hits_data + new_hits_data, "target")

    assert len(result) == 1
    assert result[0].center == new_hits_data[0].center

    previous_hits.clear()
