from geometry.geometry import Geometry
from geometry.point import GeometricalPoint


class Target(Geometry):
    id: int
    name: str

    def contains_point(self, point: GeometricalPoint):
        half_width = self.width / 2
        half_height = self.height / 2
        return self.center.x - half_width <= point.x <= self.center.x + half_width and \
            self.center.y - half_height <= point.y <= self.center.y + half_height
