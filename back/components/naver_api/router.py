from fastapi import APIRouter
from back.components.naver_api.repository import TrendRepository
from back.cache.cache import RedisCache

router = APIRouter()
repo = TrendRepository()
cache = RedisCache()

@router.get("/trend")
async def get_data(start, end, keyword):
    key = cache.generate_key("trend", start, end, keyword)

    cached = await cache.get(key)
    if cached:
        return {"data": cached}

    data = await repo.get_trends(start, end, keyword)

    await cache.set(key, data, expire=3600)

    return {"data": data}