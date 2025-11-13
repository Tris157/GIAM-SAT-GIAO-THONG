"""
Script tạo dữ liệu vi phạm test để demo UI
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.traffic_violation import TrafficViolation
from app.db.base import Base


async def create_test_violations(num_violations: int = 20):
    """Tạo dữ liệu vi phạm test"""

    # Tạo async engine
    engine = create_async_engine(
        "sqlite+aiosqlite:///./traffic_data.db",
        echo=False
    )

    # Tạo async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # Tạo tables nếu chưa có
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print(f"[+] Dang tao {num_violations} vi pham test...")

    async with async_session() as session:
        async with session.begin():
            # Tạo vi phạm với thời gian ngẫu nhiên trong 7 ngày qua
            now = datetime.now()

            violation_types = ['red_light', 'speeding', 'wrong_lane']
            vehicle_types = ['car', 'motor', 'motorcycle']
            camera_names = ['camera_live', 'camera_north', 'camera_south', 'camera_east']
            light_statuses = ['red', 'yellow', 'green']

            for i in range(num_violations):
                # Random datetime trong 7 ngày qua
                days_ago = random.randint(0, 7)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)

                violated_time = now - timedelta(
                    days=days_ago,
                    hours=hours_ago,
                    minutes=minutes_ago
                )

                # Random processed status (70% chưa xử lý)
                is_processed = random.random() > 0.7

                violation = TrafficViolation(
                    camera_name=random.choice(camera_names),
                    violation_type=random.choice(violation_types),
                    vehicle_type=random.choice(vehicle_types),
                    image_path=f"./app/static/violation_images/test_violation_{i+1}.jpg",
                    position_x=random.uniform(100, 1800),
                    position_y=random.uniform(100, 900),
                    traffic_light_status=random.choice(light_statuses),
                    violated_at=violated_time,
                    date=violated_time.strftime('%Y-%m-%d'),
                    hour_of_day=violated_time.hour,
                    is_processed=is_processed,
                    note="Vi phạm test" if is_processed else None,
                    confidence=random.uniform(0.75, 0.99)
                )

                session.add(violation)

            await session.commit()

    print(f"[+] Da tao xong {num_violations} vi pham test!")
    print(f"[>] Truy cap: http://localhost:5174/violations de xem")

    await engine.dispose()


if __name__ == "__main__":
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    asyncio.run(create_test_violations(num))
