import redis  # pyright: ignore[reportMissingImports]
from .config import settings


redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def set_with_ttl(key: str, value: str, ttl_seconds: int) -> None:
    redis_client.set(name=key, value=value, ex=ttl_seconds)


def get_and_delete(key: str):
    pipe = redis_client.pipeline()
    pipe.get(key)
    pipe.delete(key)
    result = pipe.execute()
    return result[0]
