from fastapi import APIRouter, HTTPException, Depends, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    create_city,
    get_city,
    get_all_cities,
    get_city_by_name,
    create_weather,
    get_weather_for_city_id,
    get_weather_from_db
)
from app.weather import get_weather_for
from app.schema import City, CreateCity, WeatherData, WeatherCreate

from app.database import (
    get_session,
    get_redis,
    is_stored_in_redis,
    save_to_redis,
    get_cached_weather
)
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get('/api/external/weather/cities/{city_name}', response_model=WeatherCreate)
async def get_weather_for_city_route_external(
        city_name: str,
        redis: Redis = Depends(get_redis)

):
    cache_key = f'weather:{city_name.lower()}'

    if await is_stored_in_redis(cache_key, redis):
        return await get_cached_weather(cache_key, redis)

    weather = await get_weather_for(city_name)
    await save_to_redis(cache_key, weather, redis)
    return weather


@router.get('/api/external/weather/cities', response_model=list[WeatherCreate])
async def get_weather_for_cities_route(session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)):
    cities = await get_all_cities(session)
    if not cities:
        raise HTTPException(status_code=404, detail='Cities not found')

    weathers = []
    for city in cities:
        cache_key = f'weather:{city.name.lower()}'
        if await is_stored_in_redis(cache_key, redis):
            data = await get_cached_weather(cache_key, redis)
            if data:
                weathers.append(data)
        if await is_stored_in_redis(cache_key, redis):
            weathers.append(await get_cached_weather(cache_key, redis))
        else:
            try:
                weather_data = await get_weather_for(city.name)
                await save_to_redis(cache_key, weather_data, redis)
                weathers.append(weather_data)

            except HTTPException as e:
                logging.error(f"Failed to fetch weather for {city.name}: {e.detail}")

    return weathers


@router.get('/api/internal/weather/cities/{city_name}', response_model=WeatherData)
async def get_weather_for_city_route_internal(session: AsyncSession = Depends(get_session),
                                              city_name: str | None = None):
    city_entity = await get_city_by_name(session, city_name)
    if not city_entity:
        raise HTTPException(status_code=404, detail='City not found')
    weather_for_city = await get_weather_for_city_id(session, city_entity.id)

    if not weather_for_city:
        raise HTTPException(status_code=404, detail='Weather not found')

    weather_for_city.convert_sunrise_and_sunset()
    return weather_for_city


@router.post('/api/internal/weather', response_model=WeatherData, status_code=status.HTTP_201_CREATED)
async def create_weather_route(session: AsyncSession = Depends(get_session), weather: WeatherCreate | None = None):
    city_name = weather.city_name
    if not await get_city_by_name(session, city_name):
        await create_city(session, CreateCity(name=city_name))

    if await get_weather_from_db(session, city_name):
        raise HTTPException(status_code=409, detail=f'Weather for city:{city_name} already exists')

    weather = await create_weather(session, weather)
    weather.convert_sunrise_and_sunset()
    return weather


@router.post('/api/internal/cities', response_model=City)
async def create_city_route(session: AsyncSession = Depends(get_session), city_create: CreateCity | None = None):
    if await get_city_by_name(session, city_create.name):
        raise HTTPException(status_code=409, detail='City already exists')

    return await create_city(session, city_create)


@router.get('/api/internal/cities/{city_id}', response_model=City)
async def get_city_route(session: AsyncSession = Depends(get_session), city_id: int | None = None):
    city_entity = await get_city(session, city_id)
    if city_entity is None:
        raise HTTPException(status_code=404, detail='City not found')
    return city_entity


@router.get('/api/internal/cities', response_model=list[City])
async def get_city_route(session: AsyncSession = Depends(get_session)):
    city_entities = await get_all_cities(session)
    if city_entities is None:
        raise HTTPException(status_code=404, detail='Cities not found')
    return city_entities


@router.get('/api/weather/{city_name}', response_model=WeatherData)
async def get_weather_for_city(
        session: AsyncSession = Depends(get_session),
        city_name: str | None = None):
    if not await get_city_by_name(session, city_name):
        await create_city(session, CreateCity(name=city_name))

    weather_from_db = await get_weather_from_db(session, city_name)

    if weather_from_db is not None:
        weather_from_db.convert_sunrise_and_sunset()
        return weather_from_db

    weather_from_external_api = await get_weather_for(city_name)

    weather = await create_weather(session, weather_from_external_api)
    weather.convert_sunrise_and_sunset()

    return weather
