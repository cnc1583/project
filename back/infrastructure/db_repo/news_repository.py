from sqlalchemy.orm import Session
from sqlalchemy import desc
from back.domain.model.news_db_models import Articles

class NewsRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_news_by_cluster(self, cluster_id, limit: int = 50):
        print(cluster_id)
        return self.session.query(Articles).filter(Articles.cluster_id == cluster_id).order_by(desc(Articles.article_date)).limit(limit).all()