from pydantic import BaseModel

from app.models.dto.hit import Hit
from app.models.dto.image_size import ImageSize
from app.models.dto.target import Target


class Predictions(BaseModel):
    targets: list[Target]
    hits: list[Hit]
    image_size: ImageSize
