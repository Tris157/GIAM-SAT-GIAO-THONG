"""
Generate 20,000 test traffic records for the report
Script to create realistic test data for demonstration purposes
"""
import random
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Import models after fixing path
sys.path.append('.')
from app.models.traffic_record import TrafficRecord
from app.db.database import Base

def generate_test_data(days: int = 167, roads: list = None):
    """
    Generate test traffic data

    Args:
        days: Number of days of historical data to generate
        roads: List of road names
    """
    if roads is None:
        roads = ['Van Quan', 'Van Phu', 'Nguyen Trai', 'Nga Tu So', 'Duong Lang']

    print(f"[*] Generating test data for {days} days, {len(roads)} roads...")
    print(f"[*] Expected records: {days} days x {len(roads)} roads x 24 hours = {days * len(roads) * 24}")

    # Create engine and session
    DATABASE_URL = "sqlite:///./app/traffic_data.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    # Create tables
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        total_records = 0

        for day_offset in range(days):
            current_date = datetime.now() - timedelta(days=day_offset)

            # Generate data for each hour of the day
            for hour in range(24):
                for road in roads:
                    # Simulate realistic traffic patterns
                    base_vehicles = _get_base_traffic(hour)

                    # Add some randomness
                    count_car = max(0, int(base_vehicles * 0.4 + random.randint(-3, 3)))
                    count_motor = max(0, int(base_vehicles * 0.6 + random.randint(-5, 5)))
                    total_vehicles = count_car + count_motor

                    # Speed varies by time of day (slower during rush hours)
                    speed_car = _get_speed(hour, 'car')
                    speed_motor = _get_speed(hour, 'motor')

                    # Calculate average speed weighted by count
                    if total_vehicles > 0:
                        avg_speed = (speed_car * count_car + speed_motor * count_motor) / total_vehicles
                    else:
                        avg_speed = 0

                    # Determine traffic status
                    if total_vehicles > 15:
                        traffic_status = "congested"
                    elif total_vehicles > 8:
                        traffic_status = "busy"
                    else:
                        traffic_status = "clear"

                    # Create record with specific timestamp
                    record_time = current_date.replace(
                        hour=hour,
                        minute=random.randint(0, 59),
                        second=random.randint(0, 59),
                        microsecond=0
                    )

                    record = TrafficRecord(
                        road_name=road,
                        count_car=count_car,
                        count_motor=count_motor,
                        total_vehicles=total_vehicles,
                        speed_car=round(speed_car, 2),
                        speed_motor=round(speed_motor, 2),
                        avg_speed=round(avg_speed, 2),
                        traffic_status=traffic_status,
                        hour_of_day=hour,
                        day_of_week=record_time.weekday(),
                        date=record_time.strftime('%Y-%m-%d'),
                        recorded_at=record_time
                    )

                    db.add(record)
                    total_records += 1

            # Commit after each day
            db.commit()

            # Show progress every 10 days
            if (day_offset + 1) % 10 == 0 or day_offset == 0:
                print(f"[OK] Day {day_offset + 1}/{days} completed (Total: {total_records} records)")

        print(f"\n{'='*60}")
        print(f"[SUCCESS] Generated {total_records:,} test records!")
        print(f"[INFO] Coverage: {days} days x {len(roads)} roads x 24 hours")
        print(f"[INFO] Database: app/traffic_data.db")
        print(f"{'='*60}")

    except Exception as e:
        print(f"[ERROR] Failed to generate data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def _get_base_traffic(hour: int) -> int:
    """
    Get base traffic volume based on hour of day
    Simulates realistic traffic patterns
    """
    # Rush hours: 7-9 AM and 5-7 PM
    if hour in [7, 8]:
        return random.randint(12, 18)  # Morning rush
    elif hour in [17, 18]:
        return random.randint(14, 20)  # Evening rush
    elif 9 <= hour <= 16:
        return random.randint(6, 12)   # Daytime
    elif 19 <= hour <= 22:
        return random.randint(4, 10)   # Evening
    else:
        return random.randint(1, 5)    # Night


def _get_speed(hour: int, vehicle_type: str) -> float:
    """
    Get speed based on hour and vehicle type
    Slower during rush hours
    """
    base_speed_car = 45.0
    base_speed_motor = 35.0

    # Reduce speed during rush hours
    if hour in [7, 8, 17, 18]:
        speed_multiplier = random.uniform(0.5, 0.7)
    elif 9 <= hour <= 16:
        speed_multiplier = random.uniform(0.7, 0.9)
    elif 0 <= hour <= 5:
        speed_multiplier = random.uniform(0.9, 1.1)
    else:
        speed_multiplier = random.uniform(0.8, 1.0)

    if vehicle_type == 'car':
        return base_speed_car * speed_multiplier + random.uniform(-5, 5)
    else:
        return base_speed_motor * speed_multiplier + random.uniform(-3, 3)


def count_records():
    """Count existing records in database"""
    DATABASE_URL = "sqlite:///./app/traffic_data.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        count = db.query(TrafficRecord).count()
        print(f"[INFO] Current records in database: {count:,}")
        return count
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "count":
        count_records()
    else:
        days = int(sys.argv[1]) if len(sys.argv) > 1 else 167
        generate_test_data(days=days)
        count_records()
