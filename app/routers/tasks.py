from datetime import datetime, timedelta

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from app.linear_regression import train_and_predict

from app.models import WeatherResponse, LocationInfo, ForecastDay, Forecast, Day, Prediction

load_dotenv()

router = APIRouter(
    prefix="/get",
    tags=["get"],
)

WEATHER_API_KEY = "0b323c206fb74bee845164351242205"
WEATHER_API_URL = "http://api.weatherapi.com/v1/history.json"


async def fetch_weather(city: str, start_date: str, end_date: str):
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "dt": start_date,
        "end_dt": end_date
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        return response.json()


@router.get("/weather/{city}/{start_date}/{end_date}", response_model=WeatherResponse)
async def get_weather(city: str, start_date: str, end_date: str):
    try:
        dates = []
        avg_temps = []
        weather_data = await fetch_weather(city, start_date, end_date)
        location_info = LocationInfo(
            name=weather_data['location']['name'],
            country=weather_data['location']['country'],
        )
        forecast_day = [
            ForecastDay(
                date=day['date'],
                day=Day(
                    avgtemp_c=day['day']['avgtemp_c'],
                )
            )
            for day in weather_data['forecast']['forecastday']
        ]
        for forecast in forecast_day:
            avg_temps.append(forecast.day.avgtemp_c)
            dates.append(datetime.strptime(forecast.date, "%Y-%m-%d"))

        #llamado a la función de predicción con los parametros correspondientes
        predicted_temp = train_and_predict(dates, avg_temps)

        #calculo de la fecha del día siguiente
        next_day_date = dates[-1] + timedelta(days=1)
        next_day_str = next_day_date.strftime("%Y-%m-%d")

        prediction_info = Prediction(
            date=next_day_str,
            predicted_avgtemp_c=predicted_temp
        )
        forecast_info = Forecast(
            forecastday=forecast_day,
        )
        result = WeatherResponse(
            prediction=prediction_info
        )
        return result
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="Error al obtener datos del clima")
