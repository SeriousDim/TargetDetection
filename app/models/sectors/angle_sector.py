from app.models.geometry.point import GeometricalPoint
from app.models.sectors.sector import Sector


class AngleSector(Sector):
    center: GeometricalPoint = GeometricalPoint(x=0, y=0)
    rays: list[GeometricalPoint]
    __ray_polar_angles: list[float]

    def __init__(self, **data):
        super().__init__(**data)
        self.__ray_polar_angles = [r.get_polar_angle() for r in self.rays]
        if self.__ray_polar_angles[0] > self.__ray_polar_angles[1]:
            self.__ray_polar_angles[0], self.__ray_polar_angles[1] = (
                self.__ray_polar_angles[1],
                self.__ray_polar_angles[0],
            )

    @staticmethod
    def from_rays_list(l: list[list[float]], name: str):
        return AngleSector(
            name=name,
            rays=[
                GeometricalPoint.from_list(l[0]),
                GeometricalPoint.from_list(l[1]),
            ],
        )

    @staticmethod
    def create_list(sectors: list[list[list[float]]], names: list[str]):
        return [
            AngleSector.from_rays_list(sectors[i], names[i])
            for i in range(len(sectors))
        ]

    def contains_point(self, point: GeometricalPoint) -> bool:
        point_angle = point.get_polar_angle()

        return (
            self.__ray_polar_angles[0]
            <= point_angle
            <= self.__ray_polar_angles[1]
        )
