from pydantic import BaseModel
from typing import Optional, List

class ArticleResponse(BaseModel):
    cluster_id: str
    topic: str
    keywords: str
    representative_keyword: str | None
    item_code: Optional[str] = None
    count: int

    class Config:
        from_attributes = True

class ArticleBySubject(BaseModel):
    stock: List[ArticleResponse]
    

