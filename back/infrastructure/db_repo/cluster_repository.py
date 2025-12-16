from back.domain.model.cluster_db_models import Cluster
from sqlalchemy.orm import Session

class ClusterRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, cluster_info):
        if not cluster_info:
            return {}

        rows = (
            self.db.query(Cluster.id,  Cluster.centroid, Cluster.topic, Cluster.keywords, Cluster.subject)
            .filter(Cluster.id.in_([c_id for c_id, _ in cluster_info]))
            .all()
        )
        
        cluster_dict = dict(cluster_info)

        cluster_map = {
            cluster_id: {
                "count": cluster_dict.get(cluster_id, 0),
                "centroid": centroid if centroid else "",
                "topic": topic if topic else "None",
                "keywords": keywords if keywords else "",
                "subject": subject if subject else ""
            }

            for cluster_id, centroid, topic, keywords, subject in rows
        }

        return cluster_map