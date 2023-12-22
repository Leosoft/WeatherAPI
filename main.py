from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


API_KEY = 'b5f28b897c57b65370482c2509cf06a2'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

#METHOD
def get_wather(city:str):
    params = {'q': city, 'appid': API_KEY, 'units':'metric'}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching weather data")


@app.get("/weather/{city}")
def get_current_weather(city:str):
    weather_data = get_wather(city)
    return {"city": city, "current_temperature": weather_data["main"]["temp"], "description": weather_data["weather"][0]["description"]}


@app.get("/forecast/{city}")
def get_weather_forecast(city: str):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
    response = requests.get(forecast_url, params=params)
    if response.status_code == 200:
        forecast_data = response.json()
        return {"city": city, "forecast": forecast_data["list"]}
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching weather forecast data")