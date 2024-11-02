from datetime import time, datetime
from pydantic import BaseModel
from typing import Any


class CityBase(BaseModel):
    name: str


class CreateCity(CityBase):
    pass


class City(CityBase):
    id: int

    # BEdzie wydlubywac pola z obiektow.
    class Config:
        from_attributes = True


class WeatherDataBase(BaseModel):

    @classmethod
    def from_external_data_response(cls, city_name: str, data: dict[str, Any]) -> 'WeatherDataBase':
        return cls(
            city_name=city_name,
            description=data['weather'][0]['description'],
            temperature=data['main']['feels_like'],
            sunrise=data['sys']['sunrise'],
            sunset=data['sys']['sunset']
        )

    def convert_sunrise_and_sunset(self):
        self.sunrise = datetime.fromtimestamp(self.sunrise).time()
        self.sunset = datetime.fromtimestamp(self.sunset).time()


class WeatherCreate(WeatherDataBase):
    city_name: str
    description: str
    temperature: float
    sunrise: int
    sunset: int


class WeatherData(WeatherDataBase):
    id: int
    city_id: int
    description: str
    temperature: float
    sunrise: time
    sunset: time

    class Config:
        from_attributes = True
