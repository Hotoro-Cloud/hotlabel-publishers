import aioredis
import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

_redis_pool: Optional[aioredis.Redis] = None

async def get_redis_pool() -> aioredis.Redis:
    """Get or create a Redis connection pool."""
    global _redis_pool
    
    if _redis_pool is None:
        try:
            logger.info(f"Connecting to Redis at {settings.REDIS_URL}")
            _redis_pool = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise
    
    return _redis_pool

async def close_redis_pool():
    """Close the Redis connection pool."""
    global _redis_pool
    
    if _redis_pool is not None:
        await _redis_pool.close()
        _redis_pool = None
        logger.info("Redis connection closed")
