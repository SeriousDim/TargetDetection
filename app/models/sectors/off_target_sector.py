from app.models.geometry.point import GeometricalPoint
from app.models.sectors.sector import Sector


class OutOfBoundsSector(Sector):
    def contains_point(self, point: GeometricalPoint) -> bool:
        return True


class BelowTargetSector(Sector):
    def contains_point(self, point: GeometricalPoint) -> bool:
        return True
