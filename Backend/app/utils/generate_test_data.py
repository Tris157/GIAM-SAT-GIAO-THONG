"""
Generate test traffic data for testing reports and analytics
"""
import asyncio
import random
import sys
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import SessionLocal
from app.models.traffic_record import TrafficRecord

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


async def generate_test_data(days: int = 7, roads: list = None):
    """
    Generate test traffic data for the specified number of days

    Args:
        days: Number of days of historical data to generate
        roads: List of road names (default: ['Văn Quán', 'Văn Phú', 'Nguyễn Trãi', 'Ngã Tư Sở', 'Đường Láng'])
    """
    if roads is None:
        roads = ['Van Quan', 'Van Phu', 'Nguyen Trai', 'Nga Tu So', 'Duong Lang']

    print(f"[*] Generating test data for {days} days, {len(roads)} roads...")

    async with SessionLocal() as db:
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
                        second=random.randint(0, 59)
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
            await db.commit()
            print(f"[OK] Day {day_offset + 1}/{days} completed ({len(roads) * 24} records)")

        print(f"\n[OK] Successfully generated {total_records} test records!")
        print(f"[INFO] Coverage: {days} days x {len(roads)} roads x 24 hours = {total_records} records")


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


async def clear_test_data():
    """Clear all test data from database"""
    async with SessionLocal() as db:
        print("[WARNING] Clearing all traffic records...")

        # Delete all records
        from sqlalchemy import delete
        stmt = delete(TrafficRecord)
        result = await db.execute(stmt)
        await db.commit()

        print(f"[OK] Cleared {result.rowcount} records")


if __name__ == "__main__":
    import sys

    async def main():
        if len(sys.argv) > 1 and sys.argv[1] == "clear":
            await clear_test_data()
        else:
            days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
            await generate_test_data(days=days)

    asyncio.run(main())
