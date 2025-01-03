import math

from pydantic import BaseModel


class GeometricalPoint(BaseModel):
    x: float
    y: float

    @staticmethod
    def from_list(l: list[float]):
        return GeometricalPoint(x=l[0], y=l[1])

    def get_quarter(self):
        if self.x >= 0:
            if self.y >= 0:
                return 1
            else:
                return 4
        else:
            if self.y >= 0:
                return 2
            else:
                return 3

    def get_polar_angle(self):
        # quarter = self.get_quarter()
        atan = math.atan2(self.y, self.x)
        return atan
