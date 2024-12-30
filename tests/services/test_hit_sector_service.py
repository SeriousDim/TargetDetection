import pytest

from app.models.dto.hit import Hit
from app.models.dto.target import Target
from app.models.geometry.point import GeometricalPoint
from app.services.hit_sector_service import (
    locate_hit_sector,
    locate_point_sector,
)


@pytest.fixture
def target():
    return Target(
        center=GeometricalPoint(x=0.0, y=0.0),
        width=10.0,
        height=10.0,
        id=1,
        name="4",
    )


def test_point_outside_target(target):
    point = GeometricalPoint(x=15, y=15)
    result = locate_point_sector(point, target)
    assert result is None


def test_point_in_center_sector(target):
    point = GeometricalPoint(x=0.0, y=0.0)
    result = locate_point_sector(point, target)
    assert result.name == "1"


def test_point_in_sector_9(target):
    point = GeometricalPoint(x=-1, y=3)
    result = locate_point_sector(point, target)
    assert result.name == "9"


def test_point_in_sector_5(target):
    point = GeometricalPoint(x=-1, y=-3)
    result = locate_point_sector(point, target)
    assert result.name == "5"


def test_hit_fully_in_sector(target):
    hit = Hit(center=GeometricalPoint(x=0, y=0), width=1, height=1, id=1)
    result = locate_hit_sector(hit, target)
    assert result.sector == "1"


def test_hit_split_between_two_sectors(target):
    hit = Hit(center=GeometricalPoint(x=-0.5, y=2.5), width=1, height=1, id=1)
    result = locate_hit_sector(hit, target)
    assert result.sector == "9"


def test_hit_split_between_center_and_sector(target):
    hit = Hit(center=GeometricalPoint(x=0.5, y=0.5), width=1, height=1, id=1)
    result = locate_hit_sector(hit, target)
    assert result.sector == "1"
