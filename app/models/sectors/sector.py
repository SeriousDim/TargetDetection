from abc import abstractmethod

from pydantic import BaseModel

from app.models.geometry.point import GeometricalPoint


class Sector(BaseModel):
    name: str

    @abstractmethod
    def contains_point(self, point: GeometricalPoint) -> bool:
        pass
