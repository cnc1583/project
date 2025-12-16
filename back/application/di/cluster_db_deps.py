from back.infrastructure.db.cluster_db import ClusterSessionLocal

def get_cluster_db():
    db = ClusterSessionLocal()
    try:
        yield db
    finally:
        db.close()