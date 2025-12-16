from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from back.application.services.articles_service import ArticlesService
from back.infrastructure.db_repo.articles_repository import ArticlesRepository
from back.infrastructure.db_repo.cluster_repository import ClusterRepository
from back.schema.article_schema import ArticleBySubject
from back.application.di.articles_db_deps import get_news_db
from back.application.di.cluster_db_deps import get_cluster_db
'''
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
'''
router = APIRouter()

@router.get("/articles", response_model=ArticleBySubject)
async def get_articles(
        start,
        end,
        article_db: Session = Depends(get_news_db),
        cluster_db: Session = Depends(get_cluster_db)
):
    article_repo = ArticlesRepository(article_db)
    cluster_repo = ClusterRepository(cluster_db)

    service = ArticlesService(article_repo, cluster_repo)
    result = service.get_clusters(start, end)
    
    print(start, end)
    
    return result

'''
@router.get("/test-news-db")
def test_news_db(db: Session = Depends(get_news_db)):
    try:
        tables = [t[0] for t in db.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()]
        first_row = db.query(Articles).first()
        first_article = jsonable_encoder(ArticleResponse.from_orm(first_row)) if first_row else None
        return {
            "tables": tables,
            "first_article": first_article
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/test-cluster-db")
def test_cluster_db(db: Session = Depends(get_cluster_db)):
    try:
        tables = [t[0] for t in db.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()]
        first_row = db.query(Cluster).first()
        first_article = jsonable_encoder(ClusterResponse.from_orm(first_row)) if first_row else None
        return {
            "tables": tables,
            "first_article": first_article
        }
    except Exception as e:
        return {"error": str(e)}
'''