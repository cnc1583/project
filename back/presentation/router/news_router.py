from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from back.application.services.news_service import NewsService
from back.application.di.articles_db_deps import get_news_db
from back.infrastructure.db_repo.news_repository import NewsRepository

router = APIRouter()

@router.get("/{cluster_id}", tags=["News"])
def get_news(cluster_id, db: Session = Depends(get_news_db)):
    repo = NewsRepository(db)
    service = NewsService(repo)
    data = service.get_news_by_topic(cluster_id)
    return {"data" : data}