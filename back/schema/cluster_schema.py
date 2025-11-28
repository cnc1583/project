from pydantic import BaseModel
from typing import Optional

class ClusterResponse(BaseModel):
    id: str
    depth: int
    ch_score: float
    size: int
    reason: str
    samples: str
    centroid: str
    is_leaf: int
    topic: str
    keywords: Optional[str] = None

    class Config:
        from_attributes = True