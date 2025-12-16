from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

NEWS_DB_URL = "sqlite:///./back/infrastructure/db/news.db"

engine = create_engine(
    NEWS_DB_URL,
    connect_args={"check_same_thread": False},
)

NewsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

NewsBase = declarative_base()