
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.entity import CityEntity, WeatherEntity
from app.schema import CreateCity, WeatherCreate

import logging

logging.basicConfig(level=logging.INFO)


async def create_city(session: AsyncSession, city_create: CreateCity) -> CityEntity:
    city_entity = CityEntity(
        name=city_create.name
    )

    session.add(city_entity)
    await session.commit()
    await session.refresh(city_entity)
    return city_entity


async def get_city(session: AsyncSession, city_id: int) -> CityEntity:
    async with session.begin():
        result = await session.execute(
            select(CityEntity).filter(CityEntity.id == city_id))
        return result.scalars().first()


async def get_city_by_name(session: AsyncSession, city_name: str) -> CityEntity:
    result = await session.execute(
        select(CityEntity).filter(CityEntity.name == city_name))
    return result.scalars().first()


async def get_all_cities(session: AsyncSession) -> list[CityEntity]:
    result = await session.execute(select(CityEntity))
    return result.scalars().all()


async def get_weather_for_city_id(session: AsyncSession, city_id: int) -> WeatherEntity:
    result = await session.execute(
        select(WeatherEntity)
        .filter(WeatherEntity.city_id == city_id)
    )
    return result.scalars().first()


async def create_weather(session: AsyncSession, weather_create: WeatherCreate) -> WeatherEntity:
    city_entity = await get_city_by_name(session, weather_create.city_name)

    weather_entity = WeatherEntity(
        city_id=city_entity.id,
        description=weather_create.description,
        temperature=weather_create.temperature,
        sunrise=weather_create.sunrise,
        sunset=weather_create.sunset
    )

    session.add(weather_entity)

    await session.commit()
    await session.refresh(weather_entity)
    return weather_entity


async def get_weather_from_db(session: AsyncSession, city_name: str) -> WeatherEntity:
    city_entity = await get_city_by_name(session, city_name)
    result = await session.execute(
        select(WeatherEntity)
        .filter(WeatherEntity.city_id == city_entity.id)
    )
    weather_entity = result.scalars().first()
    return weather_entity
