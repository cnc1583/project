import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Query
from back.cache.cache import RedisCache
from back.components.real_estate_api.repository import RealEstateRepository

router = APIRouter()
repo = RealEstateRepository()
cache = RedisCache()

def filter_by_date(items, start_date, end_date):
    filtered = []

    for item in items:
        for raw in item:
            year = raw.get("dealYear")
            month = raw.get("dealMonth")
            day = raw.get("dealDay")

            date = datetime(year, month, day)

            if start_date <= date <= end_date:
                filtered.append(raw)

    return filtered

@router.get("/apartment-trades")
async def apartment_trades(
    start_ym: str,
    end_ym: str,
    region_code: str = Query("11680"),
    start_day: str = Query("01"),
    end_day: str = Query("31")
):

    start_date = datetime.strptime(f"{start_ym}{start_day}".replace("-", ""), "%Y%m%d")
    end_date = datetime.strptime(f"{end_ym}{end_day}".replace("-", ""), "%Y%m%d")

    # 캐시 키 생성
    key = f"apartment_trades:{region_code}:{start_ym}{start_day}-{end_ym}{end_day}"

    # 캐시 확인
    cached = await cache.get(key)
    if cached:
        return cached

    # 월별 리스트
    ym_list = []
    cur = start_date.replace(day=1)
    while cur <= end_date.replace(day=1):
        ym_list.append(cur.strftime("%Y%m"))
        cur += relativedelta(months=1)

    # 병렬 요청
    request = [repo.get_apartment_trades(region_code, ym) for ym in ym_list]
    results_month = await asyncio.gather(*request)

    # 월별 요청 데이터 병합
    merged = []
    for month_data in results_month:
        if month_data["item"]:
            merged.append(month_data["item"])

    # 날짜 필터링
    filtered = filter_by_date(merged, start_date, end_date)

    # 전용면적 평당 실거래가 변환 및 결과 생성
    result = []
    for f in filtered:
        try:
            price = int(f.get("dealAmount").replace(",", ""))
            area = float(f.get("excluUseAr"))
            price_per_day = price / (area / 3.3058)

            year = str(f.get("dealYear"))
            month = f"{int(f.get("dealMonth")):02d}"
            day = f"{int(f.get("dealDay")):02d}"

            date = f"{year}-{month}-{day}"

            result.append({
                "date": date,
                "price": round(price_per_day, 0)
            })
        except Exception:
            continue


    await cache.set(key, result, expire=3600)
    return result