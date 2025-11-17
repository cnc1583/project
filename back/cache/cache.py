import json
import redis.asyncio as aioredis
from back.core.redis_config import RedisSettings

redis_settings = RedisSettings()

class RedisCache:
    def __init__(self):
        self.client = aioredis.Redis(
            host=redis_settings.REDIS_HOST,
            port=redis_settings.REDIS_PORT,
            db=redis_settings.REDIS_DB,
            decode_responses=True
        )

    # noinspection  PyMethodMayBeStatic
    def generate_key(self, namespace, *args):
        return f"{namespace}-" + "-".join(str(p) for p in args)

    async def set(self, key, value, expire: int = 600):
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
            await self.client.set(key, value, ex=expire)

    async def get(self, key):
        try:
            value = await self.client.get(key)

        except Exception as e:
            print("redis GET error:", e)
            return None

        if value is None:
            return None

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

cache = RedisCache()