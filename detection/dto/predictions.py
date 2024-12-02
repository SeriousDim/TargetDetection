from pydantic import BaseModel

from detection.dto.hit import Hit
from detection.dto.image_size import ImageSize
from detection.dto.target import Target


class Predictions(BaseModel):
    targets: list[Target]
    hits: list[Hit]
    image_size: ImageSize
