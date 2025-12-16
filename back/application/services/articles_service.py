import json
import numpy as np
from sklearn.preprocessing import normalize
from back.infrastructure.db_repo.articles_repository import ArticlesRepository
from back.infrastructure.db_repo.cluster_repository import ClusterRepository
from back.infrastructure.config.alias_map import get_alias_item_code

class ArticlesService:
    SIMILARITY_THRESHOLD = 0.90

    def __init__(self, articles_repo: ArticlesRepository, cluster_repo: ClusterRepository):
        self.articles_repo = articles_repo
        self.cluster_repo = cluster_repo

    def get_clusters(self, start, end):
        clusters_count_list = self.articles_repo.get_all(start, end)
        if not clusters_count_list:
            return {"stock": []}

        cluster_map = self.cluster_repo.get_all(clusters_count_list)

        clusters_data = []
        for cluster_id, count in clusters_count_list:
            details = cluster_map.get(cluster_id)
            if not details:
                continue
            norm_vec = self._parse_and_normalize_centroid(details.get("centroid"))
            if norm_vec is not None:
                clusters_data.append({
                    'id': cluster_id,
                    'count': count,
                    'vec': norm_vec,
                    'topic': details.get("topic", "None"),
                    'keywords': details.get("keywords", "")
                })

        clusters_data.sort(key=lambda x: x['count'], reverse=True)
        
        merged_results = []
        visited_ids = set()

        for i, main_cluster in enumerate(clusters_data):
            if main_cluster['id'] in visited_ids:
                continue
            
            visited_ids.add(main_cluster['id'])
            
            
            main_keywords_str = main_cluster.get('keywords') or ""
            
            keywords_accumulator = {k.strip() for k in main_keywords_str.split(',') if k.strip()}

            current_group = {
                'main_id': main_cluster['id'],
                'topic': main_cluster['topic'],
                'keywords_set': keywords_accumulator, 
                'total_count': main_cluster['count']
            }

            for j in range(i + 1, len(clusters_data)):
                candidate = clusters_data[j]
                if candidate['id'] in visited_ids:
                    continue
                
                similarity = np.dot(main_cluster['vec'], candidate['vec'].T)[0][0]
                
                if similarity >= self.SIMILARITY_THRESHOLD:
                    visited_ids.add(candidate['id'])
                    current_group['total_count'] += candidate['count']
                    
                    
                    candidate_keywords_str = candidate.get('keywords') or ""
                    candidate_keywords = {k.strip() for k in candidate_keywords_str.split(',') if k.strip()}
                    current_group['keywords_set'].update(candidate_keywords)

            merged_results.append(current_group)

        
        final_list = []
        
        for group in merged_results:
            topic_str = group.get('topic') or ""
            
            accumulated_keywords = list(group.get('keywords_set', set()))
            
            topic_words = topic_str.split()
            
            combined_keyword_list = topic_words + accumulated_keywords
            final_keywords_str = ", ".join(combined_keyword_list)

            item_code, representative_keyword = self._get_stock_code(final_keywords_str)

            elem = {
                "cluster_id": group['main_id'],
                "topic": group['topic'],
                "keywords": final_keywords_str,
                "representative_keyword": representative_keyword,
                "item_code": item_code,
                "count": group['total_count']
            }
            final_list.append(elem)
            
            print(group['topic']," : ",group['total_count']," : ",representative_keyword, item_code)
            print("\n-----------------------------------------\n")
        
        final_list = sorted(final_list, key=lambda k: k["count"], reverse=True)[:10]

        return { "stock": final_list }

    def _parse_and_normalize_centroid(self, blob_or_string):
        vec = None
        try:
            if not blob_or_string: return None
            if isinstance(blob_or_string, str):
                vec = np.array(json.loads(blob_or_string), dtype=np.float32)
            elif isinstance(blob_or_string, bytes):
                vec = np.frombuffer(blob_or_string, dtype=np.float32)
        except Exception as e:
            print(f"Centroid parsing error: {e}")
            return None
        if vec is not None:
            vec = vec.reshape(1, -1)
            vec = normalize(vec, norm='l2')
            return vec
        return None

    def _get_stock_code(self, keywords):
        if not keywords: return None, None
        for kwrd in [k.strip() for k in keywords.split(",")]:
            item_code = get_alias_item_code(kwrd)
            if item_code:
                return item_code, kwrd
        return None, None