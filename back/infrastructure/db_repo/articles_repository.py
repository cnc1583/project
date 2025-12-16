from back.domain.model.news_db_models import Articles
from sqlalchemy.orm import Session
from sqlalchemy import func

class ArticlesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, start, end):
        query = (
            self.db.query(
                Articles.cluster_id,
                func.count(Articles.id).label('count'))
            .filter(Articles.article_date.between(start, end))
            .filter(Articles.cluster_id.isnot(None))
            .group_by(Articles.cluster_id)
            # .order_by(...) # 정렬은 결과 개수에 영향 안 줌
        )
        
        # [디버깅] 실제 날아가는 SQL과 파라미터 확인
        print(f"DEBUG SQL: {query}")
        print(f"DEBUG PARAMS: start={start}, end={end}")
        
        return query.all()
            
        