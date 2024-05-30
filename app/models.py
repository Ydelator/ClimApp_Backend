from pydantic import BaseModel
from typing import List


class Task:
    def __init__(self, id: int, title: str, description: str = None, done: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.done = done


class Day(BaseModel):
    avgtemp_c: float


class ForecastDay(BaseModel):
    date: str
    day: Day


class LocationInfo(BaseModel):
    name: str
    country: str


class Forecast(BaseModel):
    forecastday: List[ForecastDay]


class Prediction(BaseModel):
    date: str
    predicted_avgtemp_c: float


class WeatherResponse(BaseModel):
    prediction: Prediction
