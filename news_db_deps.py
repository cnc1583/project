from back.infrastructure.news_db import NewsSessionLocal

def get_news_db():
    db = NewsSessionLocal()
    try:
        yield db
    finally:
        db.close()