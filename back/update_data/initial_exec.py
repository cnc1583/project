import crawler
import cluster2
import embedding_batch

from datetime import date, timedelta, datetime, time
import sqlite3


if __name__ == "__main__":
            
        yesterday=date.today() - timedelta(days=1)
        start_date = (yesterday - timedelta(days=365))
      

        conn = sqlite3.connect("../infrastructure/db/news.db")
        cur = conn.cursor()

        try:
            cur.execute("SELECT MAX(article_date) FROM articles")
            latest_date = cur.fetchone()[0]
            
            if not latest_date:
                start_date = start_date
            else:
                if latest_date==yesterday.strftime("%Y-%m-%d"):
                    print("최신 데이터가 이미 존재합니다. 작업을 종료합니다.")
                    exit()
                
                if latest_date < start_date.strftime("%Y-%m-%d"):
                    start_date = start_date
                else:
                    start_date = datetime.strptime(latest_date, "%Y-%m-%d").date() + timedelta(days=1)

            
        except Exception as e:
            print(f"데이터베이스에서 최신 날짜를 가져오는 중 오류가 발생했습니다: {e}")
            
            
        conn.close()
        
        

        
  
        # 1. 크롤링
        print("1. 크롤링 시작")
        crawler.main(start_date, yesterday)

        # 2. 임베딩 배치 처리
        print("2. 임베딩 배치 처리 시작")
        embedding_batch.main(start_date, yesterday)
        
        # 3. 클러스터링
        print("3. 클러스터링 시작")
        cluster2.main((yesterday-timedelta(days=365)).strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"))

        # 4. 토픽화
        print("4. 토픽화 시작")
        import topic
        # 5. 키워드 추출
        print("5. 키워드 추출 시작")
        import keyword

        print("모든 작업이 완료되었습니다.")
        
       

