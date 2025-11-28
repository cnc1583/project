from fastapi import APIRouter
from back.core.listed_company import StockMapper
from back.components.kis_api.repository import StockRepository
from back.cache.cache import RedisCache

router = APIRouter()
repo = StockRepository()
cache = RedisCache()
stock_mapper = StockMapper()

@router.get("/stock")
async def get_data(start, end, keyword):
    key = cache.generate_key("stock", start, end, keyword)

    cached = await cache.get(key)
    if cached:
        return {"data": cached}

    item_code = await stock_mapper.get_item_code(keyword)

    data = await repo.get_stocks(start, end, item_code)

    await cache.set(key, data, expire=900)

    return {"data": data}
