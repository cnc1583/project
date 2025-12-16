from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

CLUSTER_DB_URL = "sqlite:///./back/infrastructure/db/cluster.db"

engine = create_engine(
    CLUSTER_DB_URL,
    connect_args={"check_same_thread": False},
)

ClusterSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ClusterBase = declarative_base()