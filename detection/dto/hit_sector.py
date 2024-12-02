from pydantic import BaseModel


class HitSector(BaseModel):
    hit_id: int
    sector: str
