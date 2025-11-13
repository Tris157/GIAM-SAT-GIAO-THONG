"""
Weather Service - Fetch weather data from OpenWeatherMap API
"""
import os
import aiohttp
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching weather data"""

    def __init__(self):
        # OpenWeatherMap API (Free tier)
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "demo")  # Users can set their own key
        self.base_url = "https://api.openweathermap.org/data/2.5"

        # Default location: Hanoi, Vietnam
        self.default_lat = os.getenv("WEATHER_LAT", "21.0285")
        self.default_lon = os.getenv("WEATHER_LON", "105.8542")

        self._cache = {}
        self._cache_timeout = timedelta(minutes=10)  # Cache for 10 minutes

    async def get_current_weather(self, lat: Optional[float] = None, lon: Optional[float] = None) -> Dict:
        """
        Get current weather data

        Args:
            lat: Latitude (default: Hanoi)
            lon: Longitude (default: Hanoi)

        Returns:
            Dict with weather information
        """
        lat = lat or float(self.default_lat)
        lon = lon or float(self.default_lon)

        cache_key = f"current_{lat}_{lon}"

        # Check cache
        if cache_key in self._cache:
            cached_data, cached_time = self._cache[cache_key]
            if datetime.now() - cached_time < self._cache_timeout:
                return cached_data

        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",  # Celsius
                "lang": "vi"  # Vietnamese
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Parse and format the data
                        weather_data = {
                            "location": data.get("name", "Hà Nội"),
                            "temperature": round(data["main"]["temp"], 1),
                            "feels_like": round(data["main"]["feels_like"], 1),
                            "humidity": data["main"]["humidity"],
                            "pressure": data["main"]["pressure"],
                            "description": data["weather"][0]["description"],
                            "icon": data["weather"][0]["icon"],
                            "wind_speed": round(data["wind"]["speed"] * 3.6, 1),  # m/s to km/h
                            "clouds": data["clouds"]["all"],
                            "visibility": data.get("visibility", 10000) / 1000,  # meters to km
                            "timestamp": datetime.now().isoformat(),
                            "weather_code": data["weather"][0]["id"]
                        }

                        # Add rain info if available
                        if "rain" in data:
                            weather_data["rain_1h"] = data["rain"].get("1h", 0)

                        # Cache the result
                        self._cache[cache_key] = (weather_data, datetime.now())

                        return weather_data

                    elif response.status == 401:
                        # API key invalid - return demo data
                        logger.warning("Invalid OpenWeather API key, using demo data")
                        return self._get_demo_weather()

                    else:
                        logger.error(f"Weather API error: {response.status}")
                        return self._get_demo_weather()

        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            return self._get_demo_weather()

    async def get_forecast(self, lat: Optional[float] = None, lon: Optional[float] = None, days: int = 5) -> Dict:
        """
        Get weather forecast for next N days

        Args:
            lat: Latitude (default: Hanoi)
            lon: Longitude (default: Hanoi)
            days: Number of days to forecast (max 5 for free tier)

        Returns:
            Dict with forecast data
        """
        lat = lat or float(self.default_lat)
        lon = lon or float(self.default_lon)

        cache_key = f"forecast_{lat}_{lon}_{days}"

        # Check cache
        if cache_key in self._cache:
            cached_data, cached_time = self._cache[cache_key]
            if datetime.now() - cached_time < self._cache_timeout:
                return cached_data

        try:
            url = f"{self.base_url}/forecast"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "lang": "vi",
                "cnt": min(days * 8, 40)  # 8 forecasts per day (3-hour intervals)
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Group by day
                        daily_forecasts = []
                        current_day = None
                        day_data = []

                        for item in data["list"]:
                            dt = datetime.fromtimestamp(item["dt"])
                            day = dt.date()

                            if current_day != day:
                                if day_data:
                                    daily_forecasts.append(self._aggregate_day_forecast(day_data))
                                current_day = day
                                day_data = []

                            day_data.append(item)

                        # Add last day
                        if day_data:
                            daily_forecasts.append(self._aggregate_day_forecast(day_data))

                        forecast_data = {
                            "location": data["city"]["name"],
                            "days": daily_forecasts[:days],
                            "timestamp": datetime.now().isoformat()
                        }

                        # Cache the result
                        self._cache[cache_key] = (forecast_data, datetime.now())

                        return forecast_data

                    else:
                        logger.error(f"Forecast API error: {response.status}")
                        return self._get_demo_forecast(days)

        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            return self._get_demo_forecast(days)

    def _aggregate_day_forecast(self, day_data: list) -> Dict:
        """Aggregate 3-hour forecasts into daily summary"""
        temps = [item["main"]["temp"] for item in day_data]

        # Most common weather condition
        weather_counts = {}
        for item in day_data:
            weather_id = item["weather"][0]["id"]
            weather_counts[weather_id] = weather_counts.get(weather_id, 0) + 1

        main_weather_id = max(weather_counts, key=weather_counts.get)
        main_weather = next(item["weather"][0] for item in day_data if item["weather"][0]["id"] == main_weather_id)

        return {
            "date": datetime.fromtimestamp(day_data[0]["dt"]).strftime("%Y-%m-%d"),
            "day_name": datetime.fromtimestamp(day_data[0]["dt"]).strftime("%A"),
            "temp_min": round(min(temps), 1),
            "temp_max": round(max(temps), 1),
            "temp_avg": round(sum(temps) / len(temps), 1),
            "description": main_weather["description"],
            "icon": main_weather["icon"],
            "humidity": round(sum(item["main"]["humidity"] for item in day_data) / len(day_data)),
            "rain_probability": round(sum(item.get("pop", 0) for item in day_data) / len(day_data) * 100)
        }

    def _get_demo_weather(self) -> Dict:
        """Return demo weather data when API is unavailable"""
        return {
            "location": "Hà Nội",
            "temperature": 28.5,
            "feels_like": 30.2,
            "humidity": 65,
            "pressure": 1013,
            "description": "trời quang, có mây",
            "icon": "02d",
            "wind_speed": 12.5,
            "clouds": 25,
            "visibility": 10.0,
            "timestamp": datetime.now().isoformat(),
            "weather_code": 801,
            "demo": True
        }

    def _get_demo_forecast(self, days: int = 5) -> Dict:
        """Return demo forecast data"""
        daily_forecasts = []
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            daily_forecasts.append({
                "date": date.strftime("%Y-%m-%d"),
                "day_name": date.strftime("%A"),
                "temp_min": 24.0 + i * 0.5,
                "temp_max": 32.0 + i * 0.3,
                "temp_avg": 28.0 + i * 0.4,
                "description": "có mây rải rác" if i % 2 == 0 else "trời quang",
                "icon": "02d" if i % 2 == 0 else "01d",
                "humidity": 60 + i * 2,
                "rain_probability": 10 + i * 5
            })

        return {
            "location": "Hà Nội",
            "days": daily_forecasts,
            "timestamp": datetime.now().isoformat(),
            "demo": True
        }

    def get_traffic_impact(self, weather_data: Dict) -> Dict:
        """
        Analyze weather impact on traffic

        Args:
            weather_data: Current weather data

        Returns:
            Dict with traffic impact analysis
        """
        weather_code = weather_data.get("weather_code", 800)
        temp = weather_data.get("temperature", 25)
        wind_speed = weather_data.get("wind_speed", 0)
        visibility = weather_data.get("visibility", 10)

        impact = {
            "level": "low",  # low, medium, high, extreme
            "color": "green",
            "message": "Thời tiết tốt, giao thông bình thường",
            "recommendations": []
        }

        # Rain conditions (code 2xx, 3xx, 5xx)
        if 200 <= weather_code < 700:
            if weather_code < 600:  # Rain/Drizzle
                impact["level"] = "high"
                impact["color"] = "red"
                impact["message"] = "Mưa - Nguy cơ tắc đường cao"
                impact["recommendations"] = [
                    "Giảm tốc độ 20-30%",
                    "Tăng khoảng cách an toàn",
                    "Bật đèn xe",
                    "Cẩn thận khi lái xe"
                ]
            else:  # Snow
                impact["level"] = "extreme"
                impact["color"] = "red"
                impact["message"] = "Tuyết - Rất nguy hiểm"
                impact["recommendations"] = [
                    "Hạn chế di chuyển",
                    "Sử dụng phương tiện công cộng",
                    "Kiểm tra lốp xe"
                ]

        # Fog/Mist (code 7xx)
        elif 700 <= weather_code < 800:
            if visibility < 1:  # Heavy fog
                impact["level"] = "extreme"
                impact["color"] = "red"
                impact["message"] = "Sương mù dày đặc - Rất nguy hiểm"
            elif visibility < 5:
                impact["level"] = "high"
                impact["color"] = "orange"
                impact["message"] = "Sương mù - Giảm tầm nhìn"
            impact["recommendations"] = [
                "Bật đèn sương mù",
                "Giảm tốc độ",
                "Không chuyển làn đột ngột"
            ]

        # Strong wind
        if wind_speed > 40:
            impact["level"] = "high"
            impact["color"] = "orange"
            impact["message"] = "Gió mạnh - Cẩn thận khi lái xe"
            impact["recommendations"].append("Cẩn thận với xe tải, xe bus")

        # Extreme temperature
        if temp > 38:
            impact["recommendations"].append("Nhiệt độ cao - Kiểm tra lốp và động cơ")
        elif temp < 5:
            impact["recommendations"].append("Nhiệt độ thấp - Cẩn thận đường trơn")

        return impact

# Global instance
weather_service = WeatherService()
