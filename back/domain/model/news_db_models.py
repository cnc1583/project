from sqlalchemy import Column, Integer, Text
from back.infrastructure.db.news_db import NewsBase

class Articles(NewsBase):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(Text)
    content = Column(Text)
    article_date= Column(Text)
    url = Column(Text)
    cluster_id = Column(Text)