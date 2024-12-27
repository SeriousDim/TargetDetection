from pydantic import BaseModel

from app.models.geometry.point import GeometricalPoint


class Geometry(BaseModel):
    center: GeometricalPoint
    width: float
    height: float


