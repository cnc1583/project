from sqlalchemy import Column, Integer, Text, REAL
from back.infrastructure.db.cluster_db import ClusterBase

class Cluster(ClusterBase):
    __tablename__ = "clusters"

    id = Column(Text, primary_key=True)
    depth = Column(Integer)
    ch_score = Column(REAL)
    size = Column(Integer)
    reason = Column(Text)
    samples = Column(Text)
    centroid = Column(Text)
    is_leaf = Column(Integer)
    topic = Column(Text)
    keywords = Column(Text)
    subject = Column(Text)