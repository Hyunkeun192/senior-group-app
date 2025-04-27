from fastapi import APIRouter, HTTPException
import requests
import os
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
AIRPOLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"

@router.get("/full")
def get_full_weather(city: str):
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="Weather API key is not set.")

    # 1. 현재 날씨 정보 가져오기
    try:
        weather_res = requests.get(WEATHER_URL, params={
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "kr"
        })
        weather_res.raise_for_status()
        weather_data = weather_res.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch current weather: {str(e)}")

    lat = weather_data["coord"]["lat"]
    lon = weather_data["coord"]["lon"]
    current_weather = {
        "weather": weather_data["weather"][0]["description"],
        "temperature": weather_data["main"]["temp"]
    }

    # 2. 3시간 단위 예보 가져오기
    try:
        forecast_res = requests.get(FORECAST_URL, params={
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "kr"
        })
        forecast_res.raise_for_status()
        forecast_data = forecast_res.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch forecast data: {str(e)}")

    now = datetime.utcnow() + timedelta(hours=9)  # 한국 시간 기준

    # 3. 6개 시간별 예보 추출 (3시간 간격)
    hourly_forecast = []
    for item in forecast_data.get("list", [])[:6]:  # 6개 => 18시간 커버
        dt = datetime.utcfromtimestamp(item["dt"]) + timedelta(hours=9)
        hourly_forecast.append({
            "time": f"{dt.hour}시",
            "temp": round(item["main"]["temp"]),
            "weather": item["weather"][0]["description"]
        })

    # 4. 일별 요약 예보 가공 (오늘, 내일, 모레)
    daily_forecast = []
    temp_by_day = {}

    for item in forecast_data.get("list", []):
        dt = datetime.utcfromtimestamp(item["dt"]) + timedelta(hours=9)
        day_key = dt.strftime('%Y-%m-%d')
        if day_key not in temp_by_day:
            temp_by_day[day_key] = {
                "temps": [],
                "weathers": []
            }
        temp_by_day[day_key]["temps"].append(item["main"]["temp"])
        temp_by_day[day_key]["weathers"].append(item["weather"][0]["description"])

    for idx, (day, info) in enumerate(temp_by_day.items()):
        if idx >= 7:
            break  # 7일까지만
        daily_forecast.append({
            "day": "오늘" if idx == 0 else (datetime.strptime(day, '%Y-%m-%d') + timedelta(hours=9)).strftime('%a'),
            "temp_min": round(min(info["temps"])),
            "temp_max": round(max(info["temps"])),
            "weather": max(set(info["weathers"]), key=info["weathers"].count)  # 가장 많이 나온 날씨로 대표
        })

    # 5. 미세먼지 정보 가져오기
    try:
        air_res = requests.get(AIRPOLLUTION_URL, params={
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY
        })
        air_res.raise_for_status()
        air_data = air_res.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch air pollution data: {str(e)}")

    air_info = air_data["list"][0]["components"]
    air_quality = {
        "pm10": int(air_info["pm10"]),
        "pm2_5": int(air_info["pm2_5"])
    }

    return {
        "city": city,
        "current": current_weather,
        "hourly": hourly_forecast,
        "daily": daily_forecast,
        "air": air_quality
    }
