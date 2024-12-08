from pydantic import BaseModel
from typing import List


class Center(BaseModel):
    x: float
    y: float


class Hit(BaseModel):
    center: Center
    width: float
    height: float
    id: int


class VisualizationRequest(BaseModel):
    file: bytes  # Это заглушка для описания файла


class VisualizationResponse(BaseModel):
    target_name: str
    hits_sectors: List[int]
    recommendation: str
    image: str
