from pydantic import BaseModel

from geometry.point import GeometricalPoint
from sectors.sector import Sector


class CircleSector(Sector):
    center: GeometricalPoint
    radius: float

    def contains_point(self, point: GeometricalPoint) -> bool:
        return (point.x - self.center.x)**2 + (point.y - self.center.y)**2 <= self.radius**2
