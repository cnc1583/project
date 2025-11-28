from pydantic import BaseModel
from typing import Optional

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    article_date: str
    url: str
    cluster_id: Optional[str] = None

    class Config:
        from_attributes = True