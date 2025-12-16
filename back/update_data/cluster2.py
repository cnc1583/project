import chromadb
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, pairwise_distances_argmin_min
import sys
import sqlite3
import json
import os
from datetime import datetime, timedelta
import random
from sklearn.preprocessing import normalize


# 1. 글로벌 설정 (상수)

STOP_THRESHOLD_CH = 30.0
MIN_CLUSTER_SIZE = 50
PERSISTENT_PATH = "data/embedding_db"
TARGET_COL_NAME = "news_articles_v1"
CLUSTER_DB_PATH = "../infrastructure/db/cluster.db"
NEWS_DB_PATH = "../infrastructure/db/news.db" 




# 2. 헬퍼 함수 정의

def generate_date_range(start_str, end_str):
    start = datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.strptime(end_str, "%Y-%m-%d")
    date_list = []
    curr = start
    while curr <= end:
        date_list.append(curr.strftime("%Y-%m-%d"))
        curr += timedelta(days=1)
    return date_list

def get_dynamic_k_range(n_curr):
    min_k = 2
    if n_curr >= 50000: max_k = 30
    elif n_curr >= 10000: max_k = 20
    elif n_curr >= 5000: max_k = 15
    elif n_curr >= 1000: max_k = 10
    elif n_curr >= 100: max_k = 5
    else: max_k = 3
    return min_k, max_k

def get_sample_count_by_size(size):
    if size < 100: return 40
    if size < 1000: return 70
    if size < 5000: return 100
    return 150


# 3. DB 및 데이터 관리 함수

def init_cluster_db():
    conn = sqlite3.connect(CLUSTER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS clusters")
    cursor.execute('''
        CREATE TABLE clusters (
            id TEXT PRIMARY KEY,
            depth INTEGER,
            ch_score REAL,
            size INTEGER,
            reason TEXT,
            samples TEXT,
            centroid TEXT, 
            is_leaf INTEGER,
            topic TEXT,
            keywords TEXT,
            subject TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"1. 클러스터 DB 초기화 완료 (Centroid 컬럼 포함)")

def insert_cluster_to_db(conn, info):
    cursor = conn.cursor()
    samples_json = json.dumps(info['samples'], ensure_ascii=False)
    
    centroid_json = "[]"
    if info['centroid'] is not None:
        try:
            centroid_json = json.dumps(info['centroid'].tolist())
        except Exception as e:
            print(f"Error serializing centroid: {e}")
    
    cursor.execute('''
        INSERT INTO clusters (id, depth, ch_score, size, reason, samples, centroid, is_leaf)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        info['id'],
        info['depth'],
        info['ch_score'],
        info['size'],
        info['reason'],
        samples_json,
        centroid_json,
        info['is_leaf']
    ))
    conn.commit()

def load_chroma_data(start_date, end_date):
    print(f"2. 데이터 로드 중...")
    
    # 디렉토리 확인
    os.makedirs("data", exist_ok=True)
    
    client = chromadb.PersistentClient(path=PERSISTENT_PATH)
    try:
        collection = client.get_collection(TARGET_COL_NAME)
    except Exception as e:
        print(f" 컬렉션을 찾을 수 없습니다: {e}")
        sys.exit(1)

    target_dates = generate_date_range(start_date, end_date)
    filter_condition = { "article_date": { "$in": target_dates } }

    data = collection.get(where=filter_condition, include=["embeddings"])
    ids = np.array(data["ids"])
    raw_embeddings = np.array(data["embeddings"])
    
    if len(ids) == 0:
        print(" 데이터가 없습니다 (0개).")
        sys.exit(1)

    # 정규화
    embeddings = normalize(raw_embeddings, axis=1, norm='l2')
    n_samples = len(ids)

    print(f"   -> 데이터 개수: {n_samples}개")
    if n_samples < MIN_CLUSTER_SIZE:
        print(" 데이터 부족")
        sys.exit(1)
        
    return ids, embeddings

def update_news_db_final(leaf_article_mappings):
    print(f"\n4. News DB ({NEWS_DB_PATH}) 업데이트 시작...")
    
    if not os.path.exists(NEWS_DB_PATH):
        print(f" 오류: {NEWS_DB_PATH} 파일이 없습니다.")
        return

    if not leaf_article_mappings:
        print(" 업데이트할 매핑 정보가 없습니다.")
        return

    conn_news = sqlite3.connect(NEWS_DB_PATH)
    cursor = conn_news.cursor()

    try:
        cursor.execute("PRAGMA table_info(articles)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "cluster_id" not in columns:
            print("   -> 'cluster_id' 컬럼 생성 중...")
            cursor.execute("ALTER TABLE articles ADD COLUMN cluster_id TEXT")
        
        print(f"   -> 총 {len(leaf_article_mappings)}건의 기사 매핑 정보를 저장합니다...")
        
        cursor.executemany(
            "UPDATE articles SET cluster_id = ? WHERE id = ?", 
            leaf_article_mappings
        )
        
        conn_news.commit()
        print(" News DB 업데이트 최종 완료.")
        
    except Exception as e:
        print(f" DB 업데이트 실패: {e}")
    finally:
        conn_news.close()


# 4. 재귀 클러스터링 엔진

def recursive_clustering(curr_ids, curr_embs, depth, path_str, inherited_score, conn_cluster, leaf_mappings):
    n_curr = len(curr_ids)
    
    # 1. 중심점(Centroid) 계산
    centroid_vec = np.mean(curr_embs, axis=0)
    
    # 중심점과 가장 가까운 실제 기사(Center Sample) 찾기
    centroid_2d = centroid_vec.reshape(1, -1)
    closest_idx, _ = pairwise_distances_argmin_min(centroid_2d, curr_embs)
    center_id = curr_ids[closest_idx[0]]
    
    # 일반 샘플 추출
    candidates = [x for x in curr_ids if x != center_id]
    target_count = get_sample_count_by_size(n_curr)
    pick_count = min(len(candidates), target_count -1)
    random_samples = random.sample(candidates, pick_count)
    final_samples = [center_id] + random_samples

    # 저장 헬퍼 
    def save_current_node(reason, is_leaf_flag):
        insert_cluster_to_db(conn_cluster, {
            "id": path_str,
            "depth": depth,
            "ch_score": inherited_score,
            "size": n_curr,
            "reason": reason,
            "samples": final_samples,
            "centroid": centroid_vec,
            "is_leaf": is_leaf_flag
        })

        if is_leaf_flag == 1:
            for article_id in curr_ids:
                leaf_mappings.append([path_str, article_id])

    # 사이즈 미달
    if n_curr < MIN_CLUSTER_SIZE:
        save_current_node(f"Size Limit (<{MIN_CLUSTER_SIZE})", 1)
        return

    # K 탐색
    min_k, max_k = get_dynamic_k_range(n_curr)
    real_max_k = min(max_k, int(np.sqrt(n_curr)))
    
    if real_max_k < 2:
        save_current_node("Cannot Split", 1)
        return

    next_best_k = 2
    next_best_model = None
    next_best_score = -1.0

    for k in range(min_k, real_max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=3)
        labels = kmeans.fit_predict(curr_embs)
        if len(np.unique(labels)) < 2: continue
        score = calinski_harabasz_score(curr_embs, labels)
        if score > next_best_score:
            next_best_score = score
            next_best_k = k
            next_best_model = kmeans

    # 모델 실패
    if next_best_model is None:
        save_current_node("Fit Failed", 1)
        return

    # 다음 분할 점수 미달
    if next_best_score < STOP_THRESHOLD_CH:
        save_current_node(f"Next Split Low ({next_best_score:.1f})", 1)
        return

    # 분할 성공 (Branch)
    if depth < 2:
        print(f"{'  ' * depth}↳ [{path_str}] Split:{next_best_k} (New Score:{next_best_score:.1f})")

    save_current_node("Split", 0)
    
    child_labels = next_best_model.labels_
    for i in range(next_best_k):
        mask = (child_labels == i)
        child_ids = curr_ids[mask]
        child_embs = curr_embs[mask]
        if len(child_ids) == 0: continue
        
        next_path = f"{i}" if path_str == "Root" else f"{path_str}-{i}"
        
        # 재귀 호출 시 DB 커넥션과 매핑 리스트 전달
        recursive_clustering(child_ids, child_embs, depth + 1, next_path, float(next_best_score), conn_cluster, leaf_mappings)


# 5. Main Execution

def main(start_date, end_date):
    # 설정 초기화
    sys.setrecursionlimit(5000)
    
    # 1. 클러스터 DB 초기화
    init_cluster_db()
    
    # 2. 데이터 로드
    ids, embeddings = load_chroma_data(start_date, end_date)
    
    # 3. 클러스터링 준비
    conn_cluster = sqlite3.connect(CLUSTER_DB_PATH)
    leaf_article_mappings = [] # 결과를 저장할 리스트
    
    print(f"\n3. 재귀 클러스터링 시작 (점수 상속 모드)...\n")
    
    try:
        recursive_clustering(
            curr_ids=ids,
            curr_embs=embeddings,
            depth=0,
            path_str="Root",
            inherited_score=0.0,
            conn_cluster=conn_cluster,
            leaf_mappings=leaf_article_mappings
        )
        print("\n클러스터링 완료, cluster.db 저장 끝.")
    finally:
        conn_cluster.close()

    # 4. News DB 업데이트
    update_news_db_final(leaf_article_mappings)

if __name__ == "__main__":
    main("2024-11-20", "2025-11-18")