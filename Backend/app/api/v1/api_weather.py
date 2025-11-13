"""
Weather API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.services.weather_service import weather_service

router = APIRouter()


@router.get("/weather/current")
async def get_current_weather(
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    """
    Get current weather data

    - **lat**: Latitude (default: Hanoi)
    - **lon**: Longitude (default: Hanoi)
    """
    weather_data = await weather_service.get_current_weather(lat, lon)

    # Add traffic impact analysis
    traffic_impact = weather_service.get_traffic_impact(weather_data)

    return {
        "weather": weather_data,
        "traffic_impact": traffic_impact
    }


@router.get("/weather/forecast")
async def get_weather_forecast(
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    days: int = Query(5, ge=1, le=5, description="Number of days to forecast")
):
    """
    Get weather forecast

    - **lat**: Latitude (default: Hanoi)
    - **lon**: Longitude (default: Hanoi)
    - **days**: Number of days (1-5)
    """
    forecast_data = await weather_service.get_forecast(lat, lon, days)
    return forecast_data
