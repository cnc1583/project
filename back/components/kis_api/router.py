from fastapi import APIRouter
from back.core.listed_company import StockMapper
from back.components.kis_api.repository import StockRepository
from back.cache.cache import RedisCache

router = APIRouter()
repo = StockRepository()
cache = RedisCache()
stock_mapper = StockMapper()

@router.get("/stock")
async def get_data(start, end, item_code):
    print(item_code)
    key = cache.generate_key("stock", start, end, item_code)

    cached = await cache.get(key)
    if cached:
        return {"data": cached}

    print("Cache miss. Fetching from API...")
    
    data = await repo.get_stocks(start, end, item_code)

    print(data)
    await cache.set(key, data, expire=900)

    return {"data": data}
