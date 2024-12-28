from app.models.geometry.point import GeometricalPoint
from app.models.dto.target import Target
import pytest

@pytest.fixture
def target():
    yield Target(
        id = '1',
        name='test_target',
        center=GeometricalPoint(
            x=0,
            y=0
        ),
        width=10,
        height=10
    )

def test_contains_point_inside(target):
    point = GeometricalPoint(x=2, y=2)
    assert target.contains_point(point)

def test_contains_point_close_to_border_inside(target):
    point = GeometricalPoint(x=0, y=4.9)
    assert target.contains_point(point)

def test_contains_point_close_to_border_out(target):
    point = GeometricalPoint(x=5, y=5.1)
    assert not target.contains_point(point)

def test_contains_point_out(target):
    point = GeometricalPoint(x=15, y=15)
    assert not target.contains_point(point)
