from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey
from datetime import datetime

Base = declarative_base()


class CityEntity(Base):
    __tablename__ = 'cities'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    weather: Mapped['WeatherEntity'] = relationship(
        'WeatherEntity',
        back_populates='city',
    )


class WeatherEntity(Base):
    __tablename__ = 'weather_records'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'))
    description: Mapped[str] = mapped_column(String(255))
    temperature: Mapped[float] = mapped_column(Float)
    sunrise: Mapped[int] = mapped_column(Integer)
    sunset: Mapped[int] = mapped_column(Integer)

    city: Mapped[CityEntity] = relationship('CityEntity', back_populates='weather')

    def __str__(self) -> str:
        return (f"id: {self.id},  CITY ID: {self.city_id}, DESCIPTION: {self.description} "
                f"temperature: {self.temperature} SUNRISE: {self.sunrise} SUNSET: {self.sunset}")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "description": self.description,
            "temperature": self.temperature,
            "sunrise": self.sunrise,
            "sunset": self.sunset,
        }

    def convert_sunrise_and_sunset(self) -> None:
        self.sunrise = datetime.fromtimestamp(self.sunrise).time()
        self.sunset = datetime.fromtimestamp(self.sunset).time()
