import pytest

from app.models.dto.target import Target
from app.models.geometry.point import GeometricalPoint


@pytest.fixture
def target():
    yield Target(
        id="1",
        name="test_target",
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
