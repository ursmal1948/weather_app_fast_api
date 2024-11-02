from fastapi import HTTPException
import httpx
from app.config import (
    BASE_URL,
    WEATHER_API_KEY,
    GEO_BASE_URL
)
from app.schema import WeatherCreate

import logging

logging.basicConfig(level=logging.INFO)


async def get_coordinates_based_on_city_name(city_name: str) -> tuple[float, float] | None:
    direct_geocoding_url = f'{GEO_BASE_URL}direct?q={city_name}&limit=5&appid={WEATHER_API_KEY}'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(direct_geocoding_url)
            response.raise_for_status()

            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
        except HTTPException as err:
            logging.error(f'Failed to fetch coordinates - {err.detail}')


async def get_city_name_based_on_coordinates(lat: float, lon: float, limit: int = 5):
    reverse_geocoding_url = f'{GEO_BASE_URL}reverse?lat={lat}&lon={lon}&limit={limit}&appid={WEATHER_API_KEY}'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(reverse_geocoding_url)
            if response.status_code == 200:
                data = response.json()
                return data[0]['name']
        except HTTPException as err:
            logging.error(f'Failed to fetch a city -  {err.detail}')


async def get_weather_for(city_name: str):
    coordinates = await get_coordinates_based_on_city_name(city_name)
    if not coordinates:
        raise HTTPException(status_code=404, detail='City not found')

    lat, lon = coordinates

    url = f'{BASE_URL}weather?lat={lat}&lon={lon}&units=metric&appid={WEATHER_API_KEY}'

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            city_name_consistent = await get_city_name_based_on_coordinates(lat, lon)

            weather_data = WeatherCreate.from_external_data_response(city_name_consistent, data)
            return weather_data
        except HTTPException as err:
            logging.error(f'Failed to fetch weather - {err.detail}')
