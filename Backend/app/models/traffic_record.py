from sqlalchemy import Column, Integer, Float, String, DateTime, Index
from sqlalchemy.sql import func
from app.db.database import Base


class TrafficRecord(Base):
    """Model to store historical traffic data for analytics and reporting"""
    __tablename__ = "traffic_records"

    id = Column(Integer, primary_key=True, index=True)
    road_name = Column(String, index=True, nullable=False)

    # Vehicle counts
    count_car = Column(Integer, default=0)
    count_motor = Column(Integer, default=0)
    total_vehicles = Column(Integer, default=0)

    # Average speeds (km/h)
    speed_car = Column(Float, default=0.0)
    speed_motor = Column(Float, default=0.0)
    avg_speed = Column(Float, default=0.0)

    # Traffic status
    traffic_status = Column(String, default="clear")  # clear, busy, congested

    # Timestamp
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    hour_of_day = Column(Integer, index=True)  # 0-23
    day_of_week = Column(Integer, index=True)  # 0-6 (Monday-Sunday)
    date = Column(String, index=True)  # YYYY-MM-DD format

    # Create composite indexes for efficient querying
    __table_args__ = (
        Index('idx_road_date', 'road_name', 'date'),
        Index('idx_road_hour', 'road_name', 'hour_of_day'),
        Index('idx_date_hour', 'date', 'hour_of_day'),
    )
