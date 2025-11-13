from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class TrafficRecordBase(BaseModel):
    road_name: str
    count_car: int = 0
    count_motor: int = 0
    total_vehicles: int = 0
    speed_car: float = 0.0
    speed_motor: float = 0.0
    avg_speed: float = 0.0
    traffic_status: str = "clear"


class TrafficRecordCreate(TrafficRecordBase):
    pass


class TrafficRecordResponse(TrafficRecordBase):
    id: int
    recorded_at: datetime
    hour_of_day: int
    day_of_week: int
    date: str

    class Config:
        from_attributes = True


class ReportFilter(BaseModel):
    road_names: Optional[List[str]] = None
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None    # YYYY-MM-DD
    period: str = "day"  # day, week, month, year


class TrafficStatistics(BaseModel):
    road_name: str
    total_records: int
    avg_vehicles: float
    max_vehicles: int
    min_vehicles: int
    avg_speed: float
    peak_hour: Optional[int] = None
    off_peak_hour: Optional[int] = None
    congestion_rate: float = 0.0  # Percentage of time congested


class HourlyStatistics(BaseModel):
    hour: int
    avg_vehicles: float
    avg_speed: float
    traffic_status: str


class DailyTrend(BaseModel):
    date: str
    avg_vehicles: float
    max_vehicles: int
    avg_speed: float
    peak_hour: int


class RoadComparison(BaseModel):
    road_name: str
    avg_vehicles: float
    avg_speed: float
    congestion_rate: float
    total_records: int


class ReportResponse(BaseModel):
    period: str
    start_date: str
    end_date: str
    statistics: List[TrafficStatistics]
    hourly_trends: Optional[List[HourlyStatistics]] = None
    daily_trends: Optional[List[DailyTrend]] = None
    road_comparisons: Optional[List[RoadComparison]] = None
