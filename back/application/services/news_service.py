from back.infrastructure.db_repo.news_repository import NewsRepository
from back.schema.article_schema import ArticleResponse

class NewsService:
    def __init__(self, repo: NewsRepository):
        self.repo = repo

    def get_news_by_topic(self, cluster_id):
        articles = self.repo.get_news_by_cluster(cluster_id)
        
        return [
            {
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "article_date": article.article_date,
                "url": article.url,
                "cluster_id": article.cluster_id
            }
            for article in articles
        ]