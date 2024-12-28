import pytest
from app.models.geometry.point import GeometricalPoint
from app.models.sectors.circle_sector import CircleSector  # Import CircleSector


@pytest.fixture
def circle():
    yield CircleSector(
        name = 'test1',
        center=GeometricalPoint(x=0.0,
                                y=0.0),
        radius = 1.0
    )

def test_contains_point_inside_circle(circle):
    point = GeometricalPoint(x=0.5, y=0.5)
    assert circle.contains_point(point)

def test_contains_point_on_border(circle):
    point = GeometricalPoint(x=1.0, y=0.0)
    assert circle.contains_point(point)

def test_contains_point_close_to_the_border_inside(circle):
    point = GeometricalPoint(x=0.99, y=0.0)
    assert circle.contains_point(point)

def test_contains_point_close_to_the_border_out(circle):
    point = GeometricalPoint(x=1.005, y=0.0)
    assert not circle.contains_point(point)

def test_contains_point_outside_circle(circle):
    point = GeometricalPoint(x=2.0, y=0.0)
    assert not circle.contains_point(point)

def test_contains_point_outside_circle_1(circle):
    point = GeometricalPoint(x=1.1, y=1.1)
    assert not circle.contains_point(point)

@pytest.mark.parametrize("x, y", [(0.0, 0.0), (0.5, 0.5), (0.707, 0.707), (0.8, 0)])
def test_circle_param(circle, x, y):
    """Тестирует, что точки внутри сектора возвращают True."""
    point = GeometricalPoint(x=x, y=y)
    assert circle.contains_point(point)


@pytest.mark.parametrize("x, y", [(1.1, 0.0), (0.0, 1.1), (2.0, 0.0)])
def test_circle_param_outside(circle, x, y):
     """Тестирует, что точки вне сектора возвращают False."""
     point = GeometricalPoint(x=x, y=y)
     assert not circle.contains_point(point)