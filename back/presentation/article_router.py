from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.domain.model.news_db_models import Articles
from back.domain.model.cluster_db_models import Cluster
from back.schema.article_schema import ArticleResponse
from back.schema.cluster_schema import ClusterResponse
from news_db_deps import get_news_db
from cluster_db_deps import get_cluster_db
'''
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
'''
router = APIRouter()

@router.get("/articles", response_model=list[ArticleResponse])
async def get_articles(db: Session = Depends(get_news_db)):
    return db.query(Articles).all()

@router.get("/clusters", response_model=list[ClusterResponse])
async def get_clusters(db: Session = Depends(get_cluster_db)):
    return db.query(Cluster).all()

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