import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Cloud,
  CloudRain,
  CloudSnow,
  Sun,
  Wind,
  Droplets,
  Eye,
  Gauge,
  AlertTriangle,
  CloudFog,
  Zap,
  RefreshCw,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { apiCache } from "@/utils/apiCache";

interface WeatherData {
  location: string;
  temperature: number;
  feels_like: number;
  humidity: number;
  pressure: number;
  description: string;
  icon: string;
  wind_speed: number;
  clouds: number;
  visibility: number;
  timestamp: string;
  weather_code: number;
  rain_1h?: number;
  demo?: boolean;
}

interface TrafficImpact {
  level: "low" | "medium" | "high" | "extreme";
  color: string;
  message: string;
  recommendations: string[];
}

interface WeatherResponse {
  weather: WeatherData;
  traffic_impact: TrafficImpact;
}

interface ForecastDay {
  date: string;
  day_name: string;
  temp_min: number;
  temp_max: number;
  temp_avg: number;
  description: string;
  icon: string;
  humidity: number;
  rain_probability: number;
}

interface ForecastResponse {
  location: string;
  days: ForecastDay[];
  timestamp: string;
  demo?: boolean;
}

const WeatherWidget = () => {
  const [currentWeather, setCurrentWeather] = useState<WeatherData | null>(null);
  const [trafficImpact, setTrafficImpact] = useState<TrafficImpact | null>(null);
  const [forecast, setForecast] = useState<ForecastDay[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [isRefreshing, setIsRefreshing] = useState(false);

  const fetchWeather = async () => {
    setIsRefreshing(true);
    try {
      // Fetch current weather with caching (10 minutes cache)
      const weatherData = await apiCache.get<WeatherResponse>(
        'weather-current',
        async () => {
          const response = await fetch("http://localhost:8000/api/v1/weather/current");
          if (!response.ok) throw new Error('Weather fetch failed');
          return response.json();
        },
        10 * 60 * 1000 // 10 minutes cache
      );

      setCurrentWeather(weatherData.weather);
      setTrafficImpact(weatherData.traffic_impact);

      // Fetch forecast with caching (30 minutes cache)
      const forecastData = await apiCache.get<ForecastResponse>(
        'weather-forecast',
        async () => {
          const response = await fetch("http://localhost:8000/api/v1/weather/forecast?days=5");
          if (!response.ok) throw new Error('Forecast fetch failed');
          return response.json();
        },
        30 * 60 * 1000 // 30 minutes cache (forecast doesn't change often)
      );

      setForecast(forecastData.days);
      setLastUpdate(new Date());
    } catch (error) {
      console.error("Error fetching weather:", error);
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      if (isMounted) {
        await fetchWeather();
      }
    };

    fetchData();

    // Auto-refresh every 10 minutes
    const interval = setInterval(() => {
      if (isMounted) {
        fetchWeather();
      }
    }, 10 * 60 * 1000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const getWeatherIcon = (code: number, iconCode: string) => {
    // Thunderstorm
    if (code >= 200 && code < 300) return <Zap className="h-8 w-8 text-yellow-400" />;
    // Drizzle / Rain
    if (code >= 300 && code < 600) return <CloudRain className="h-8 w-8 text-blue-400" />;
    // Snow
    if (code >= 600 && code < 700) return <CloudSnow className="h-8 w-8 text-cyan-200" />;
    // Fog / Mist
    if (code >= 700 && code < 800) return <CloudFog className="h-8 w-8 text-gray-400" />;
    // Clear
    if (code === 800) return <Sun className="h-8 w-8 text-yellow-500" />;
    // Clouds
    return <Cloud className="h-8 w-8 text-gray-400" />;
  };

  const getImpactColor = (level: string) => {
    switch (level) {
      case "low":
        return "border-green-500 bg-green-500/10";
      case "medium":
        return "border-yellow-500 bg-yellow-500/10";
      case "high":
        return "border-orange-500 bg-orange-500/10";
      case "extreme":
        return "border-red-500 bg-red-500/10";
      default:
        return "border-gray-500 bg-gray-500/10";
    }
  };

  if (loading) {
    return (
      <Card className="glass border border-white/10 shadow-2xl">
        <CardContent className="flex items-center justify-center h-64">
          <RefreshCw className="h-8 w-8 animate-spin text-blue-400" />
        </CardContent>
      </Card>
    );
  }

  if (!currentWeather) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="space-y-4"
    >
      {/* Current Weather Card */}
      <Card className="glass border border-white/10 shadow-2xl overflow-hidden">
        <CardHeader className="border-b border-white/10">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-2 text-lg">
              <motion.div
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              >
                <Cloud className="h-5 w-5 text-blue-400" />
              </motion.div>
              <span className="gradient-text">Thời Tiết Hiện Tại</span>
            </CardTitle>
            <motion.button
              whileHover={{ scale: 1.1, rotate: 180 }}
              whileTap={{ scale: 0.9 }}
              onClick={fetchWeather}
              className="p-2 glass rounded-lg hover:bg-white/10 transition-all"
              disabled={isRefreshing}
            >
              <RefreshCw className={`h-4 w-4 text-blue-400 ${isRefreshing ? 'animate-spin' : ''}`} />
            </motion.button>
          </div>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid grid-cols-2 gap-6">
            {/* Temperature & Location */}
            <div className="col-span-2 flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <motion.div
                  animate={{ scale: [1, 1.1, 1] }}
                  transition={{ duration: 3, repeat: Infinity }}
                >
                  {getWeatherIcon(currentWeather.weather_code, currentWeather.icon)}
                </motion.div>
                <div>
                  <h2 className="text-5xl font-bold text-white">
                    {currentWeather.temperature}°C
                  </h2>
                  <p className="text-gray-400 mt-1 capitalize">
                    {currentWeather.description}
                  </p>
                  <p className="text-sm text-gray-500 flex items-center space-x-1 mt-1">
                    <span>Cảm giác:</span>
                    <span className="text-blue-400">{currentWeather.feels_like}°C</span>
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-semibold text-white">{currentWeather.location}</p>
                <p className="text-xs text-gray-500 mt-1">
                  Cập nhật: {new Date(lastUpdate).toLocaleTimeString("vi-VN")}
                </p>
                {currentWeather.demo && (
                  <Badge variant="secondary" className="mt-2 text-xs">
                    Demo Mode
                  </Badge>
                )}
              </div>
            </div>

            {/* Weather Details */}
            <div className="col-span-2 grid grid-cols-2 md:grid-cols-4 gap-3">
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="glass rounded-lg p-3 border border-white/10"
              >
                <div className="flex items-center space-x-2 text-gray-400 mb-1">
                  <Wind className="h-4 w-4" />
                  <span className="text-xs">Gió</span>
                </div>
                <p className="text-lg font-semibold text-white">
                  {currentWeather.wind_speed} km/h
                </p>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.05 }}
                className="glass rounded-lg p-3 border border-white/10"
              >
                <div className="flex items-center space-x-2 text-gray-400 mb-1">
                  <Droplets className="h-4 w-4" />
                  <span className="text-xs">Độ ẩm</span>
                </div>
                <p className="text-lg font-semibold text-white">
                  {currentWeather.humidity}%
                </p>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.05 }}
                className="glass rounded-lg p-3 border border-white/10"
              >
                <div className="flex items-center space-x-2 text-gray-400 mb-1">
                  <Eye className="h-4 w-4" />
                  <span className="text-xs">Tầm nhìn</span>
                </div>
                <p className="text-lg font-semibold text-white">
                  {currentWeather.visibility} km
                </p>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.05 }}
                className="glass rounded-lg p-3 border border-white/10"
              >
                <div className="flex items-center space-x-2 text-gray-400 mb-1">
                  <Gauge className="h-4 w-4" />
                  <span className="text-xs">Áp suất</span>
                </div>
                <p className="text-lg font-semibold text-white">
                  {currentWeather.pressure} hPa
                </p>
              </motion.div>
            </div>

            {currentWeather.rain_1h !== undefined && currentWeather.rain_1h > 0 && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="col-span-2 glass rounded-lg p-3 border border-blue-400/50"
              >
                <div className="flex items-center space-x-2">
                  <CloudRain className="h-5 w-5 text-blue-400" />
                  <span className="text-white font-medium">
                    Lượng mưa: {currentWeather.rain_1h} mm/h
                  </span>
                </div>
              </motion.div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Traffic Impact Alert */}
      {trafficImpact && trafficImpact.level !== "low" && (
        <AnimatePresence>
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <Alert className={`${getImpactColor(trafficImpact.level)} border-2`}>
              <AlertTriangle className="h-5 w-5" />
              <AlertTitle className="text-lg font-bold">
                Cảnh báo ảnh hưởng giao thông
              </AlertTitle>
              <AlertDescription className="space-y-2">
                <p className="font-medium">{trafficImpact.message}</p>
                {trafficImpact.recommendations.length > 0 && (
                  <ul className="list-disc list-inside space-y-1 text-sm">
                    {trafficImpact.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                )}
              </AlertDescription>
            </Alert>
          </motion.div>
        </AnimatePresence>
      )}

      {/* 5-Day Forecast */}
      {forecast.length > 0 && (
        <Card className="glass border border-white/10 shadow-2xl">
          <CardHeader className="border-b border-white/10">
            <CardTitle className="flex items-center space-x-2 text-lg">
              <Cloud className="h-5 w-5 text-purple-400" />
              <span className="gradient-text">Dự Báo 5 Ngày</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="grid grid-cols-5 gap-3">
              {forecast.map((day, index) => (
                <motion.div
                  key={day.date}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.05, y: -5 }}
                  className="glass rounded-lg p-3 border border-white/10 text-center hover:border-purple-400/50 transition-all"
                >
                  <p className="text-xs text-gray-400 mb-2">
                    {index === 0 ? "Hôm nay" : new Date(day.date).toLocaleDateString("vi-VN", { weekday: "short" })}
                  </p>
                  <div className="flex justify-center mb-2">
                    {getWeatherIcon(800, day.icon)}
                  </div>
                  <p className="text-sm font-bold text-white mb-1">
                    {day.temp_max}°
                  </p>
                  <p className="text-xs text-gray-400">
                    {day.temp_min}°
                  </p>
                  {day.rain_probability > 20 && (
                    <div className="flex items-center justify-center space-x-1 mt-2 text-blue-400">
                      <CloudRain className="h-3 w-3" />
                      <span className="text-xs">{day.rain_probability}%</span>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </motion.div>
  );
};

export default WeatherWidget;
