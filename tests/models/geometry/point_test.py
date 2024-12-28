from app.models.geometry.point import GeometricalPoint
from pydantic import BaseModel
import pytest
import math

def test_from_list_correct_list():
    point = GeometricalPoint.from_list([1.0, 2.0])
    assert point.x == 1.0
    assert point.y == 2.0


def test_from_list_too_long_list():
    point = GeometricalPoint.from_list([1.0, 2.0, 3.0])
    # assert  point == [1.0, 2.0]
    assert point.x == 1.0
    assert point.y == 2.0


def test_from_list_empty_list():
    with pytest.raises(IndexError) as e_info:
        GeometricalPoint.from_list([])


def test_get_quarter_first():
    point = GeometricalPoint(x=10.0, y=0.0)
    assert point.get_quarter() == 1


def test_get_quarter_first_1():
    point = GeometricalPoint(x=10.0, y=0.0)
    assert point.get_quarter() == 1


def test_get_quarter_first_2():
    point = GeometricalPoint(x=10.0, y=0.001)
    assert point.get_quarter() == 1


def test_get_quarter_first_3():
    point = GeometricalPoint(x=5.0, y=7.0)
    assert point.get_quarter() == 1


def test_get_quarter_first_4():
    point = GeometricalPoint(x=0.001, y=10)
    assert point.get_quarter() == 1


def test_get_quarter_first_5():
    point = GeometricalPoint(x=0, y=10)
    assert point.get_quarter() == 1


def test_get_quarter_second_1():
    point = GeometricalPoint(x=-0.001, y=10)
    assert point.get_quarter() == 2


def test_get_quarter_second_2():
    point = GeometricalPoint(x=-5.0, y=7.0)
    assert point.get_quarter() == 2


def test_get_quarter_second_3():
    point = GeometricalPoint(x=-10.0, y=0.001)
    assert point.get_quarter() == 2


def test_get_quarter_second_4():
    point = GeometricalPoint(x=-10.0, y=0.0)
    assert point.get_quarter() == 2


def test_get_quarter_third_1():
    point = GeometricalPoint(x=-10.0, y=-0.001)
    assert point.get_quarter() == 3


def test_get_quarter_third_2():
    point = GeometricalPoint(x=-5.0, y=-7.0)
    assert point.get_quarter() == 3


def test_get_quarter_third_3():
    point = GeometricalPoint(x=-0.001, y=-10.0)
    assert point.get_quarter() == 3


def test_get_quarter_fourth_1():
    point = GeometricalPoint(x=0.0, y=-10.0)
    assert point.get_quarter() == 4


def test_get_quarter_fourth_2():
    point = GeometricalPoint(x=0.001, y=-10.0)
    assert point.get_quarter() == 4


def test_get_quarter_fourth_3():
    point = GeometricalPoint(x=5.0, y=-7.0)
    assert point.get_quarter() == 4


def test_get_quarter_fourth_4():
    point = GeometricalPoint(x=10.0, y=-0.001)
    assert point.get_quarter() == 4