from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import redis.asyncio as redis
from redis.asyncio import Redis
import json
from fastapi import Depends
from app.schema import WeatherCreate
from app.config import DATABASE_URL, REDIS_URL

async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


redis_pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)


async def get_redis():
    redis_client = Redis(connection_pool=redis_pool)
    try:
        yield redis_client
    finally:
        await redis_client.close()


async def is_stored_in_redis(key: str, redis_: Redis = Depends(get_redis)) -> bool:
    return await redis_.get(key)


async def save_to_redis(key: str, data, redis_: Redis = Depends(get_redis)):
    weather_data_json = json.dumps(data.dict())
    await redis_.set(key, weather_data_json, ex=120)


async def get_cached_weather(key: str, redis_: Redis = Depends(get_redis)):
    cached_data = await redis_.get(key)
    cached_data_dict = json.loads(cached_data)
    cached_weather_entity = WeatherCreate(**cached_data_dict)
    cached_weather_entity.convert_sunrise_and_sunset()
    return cached_weather_entity
