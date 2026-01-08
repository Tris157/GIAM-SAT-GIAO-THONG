import asyncio
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.traffic_violation import TrafficViolation
from app.core.config import settings

async def create_test_violations():
    """Tạo test violations để demo chức năng"""

    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
    )

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Tạo 15 vi phạm test với thời gian khác nhau
        test_violations = []
        now = datetime.now()

        cameras = ["camera_live", "CAO TOC-LT-DG", "QL14-CM-DB", "QL1K-DL-PH"]
        violation_types = ["red_light", "speeding", "wrong_lane"]

        for i in range(15):
            hours_ago = i * 2  # Mỗi vi phạm cách nhau 2 giờ
            violated_time = now - timedelta(hours=hours_ago)

            violation = TrafficViolation(
                camera_name=cameras[i % len(cameras)],
                violation_type=violation_types[i % len(violation_types)],
                vehicle_type="car" if i % 3 == 0 else "motor",
                image_path=f"./app/static/violation_images/test_violation_{i}.jpg",
                position_x=150.0 + (i * 10.5),
                position_y=420.0 + (i * 5.2),
                traffic_light_status="red" if violation_types[i % len(violation_types)] == "red_light" else "green",
                violated_at=violated_time,
                date=violated_time.strftime("%Y-%m-%d"),
                hour_of_day=violated_time.hour,
                is_processed=(i % 3 == 0),  # 1/3 số vi phạm đã xử lý
                note=f"Test violation #{i+1} - Biển số: 59A-{12345 + i}" if i % 3 == 0 else None,
                confidence=0.85 + (i * 0.01)
            )
            test_violations.append(violation)

        # Add all violations
        session.add_all(test_violations)
        await session.commit()

        print(f"SUCCESS: Created {len(test_violations)} test violations!")
        print(f"   - {sum(1 for v in test_violations if v.is_processed)} processed")
        print(f"   - {sum(1 for v in test_violations if not v.is_processed)} unprocessed")
        print(f"   - {sum(1 for v in test_violations if v.violated_at.date() == now.date())} today")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_test_violations())
