from pydantic import BaseModel

from geometry.point import GeometricalPoint


class Geometry(BaseModel):
    center: GeometricalPoint
    width: float
    height: float
