import crawler
import cluster2
import embedding_batch
from datetime import date, timedelta, datetime, time
import runpy

TARGET_HOUR = 0
TARGET_MINUTE = 1

if __name__ == "__main__":
    
    while True:
        
        if datetime.now().hour == TARGET_HOUR and datetime.now().minute == TARGET_MINUTE:
            
            yesterday=date.today() - timedelta(days=1)
            
            # 1. 크롤링
            print("1. 크롤링 시작")
            crawler.main(yesterday, yesterday)

            # 2. 임베딩 배치 처리
            print("2. 임베딩 배치 처리 시작")
            embedding_batch.main(yesterday, yesterday)

            # 3. 클러스터링
            print("3. 클러스터링 시작")
            cluster2.main(yesterday-timedelta(days=365), yesterday)

            # 4. 토픽화
            print("4. 토픽화 시작")
            import topic 
            # 5. 키워드 추출
            print("5. 키워드 추출 시작")
            import keyword
            print("모든 작업이 완료되었습니다.")
        
        else:
            print(f"현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. 대기 중...")
            time.sleep(600)  # 10분 대기

