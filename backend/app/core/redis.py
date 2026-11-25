from app.core.config import settings
import logging

logger = logging.getLogger("hirepilot.redis")

class RedisClientWrapper:
    """
    Robust Redis abstraction: tries connecting to Redis,
    falls back cleanly to in-memory cache if Redis is not running locally.
    """
    def __init__(self):
        self._memory_cache = {}
        self._redis = None
        self._connected = False
        
    async def connect(self):
        try:
            import redis.asyncio as aioredis
            self._redis = aioredis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=1
            )
            await self._redis.ping()
            self._connected = True
            logger.info("Connected to Redis server successfully.")
        except Exception as e:
            self._connected = False
            logger.info("Redis unavailable, falling back to built-in in-memory cache.")

    async def get(self, key: str):
        if self._connected and self._redis:
            try:
                return await self._redis.get(key)
            except Exception:
                pass
        return self._memory_cache.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        if self._connected and self._redis:
            try:
                await self._redis.set(key, value, ex=expire)
                return True
            except Exception:
                pass
        self._memory_cache[key] = value
        return True

    async def delete(self, key: str):
        if self._connected and self._redis:
            try:
                await self._redis.delete(key)
            except Exception:
                pass
        self._memory_cache.pop(key, None)
        return True

redis_client = RedisClientWrapper()
