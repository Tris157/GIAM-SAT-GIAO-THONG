"""
Initialize traffic violations table
Run this to create the violations table in database
"""
from app.db.database import engine, Base
from app.models.traffic_violation import TrafficViolation

def init_violations_table():
    """Create traffic violations table"""
    print("Creating traffic violations table...")
    Base.metadata.create_all(bind=engine, tables=[TrafficViolation.__table__])
    print("✅ Traffic violations table created successfully!")

if __name__ == "__main__":
    init_violations_table()
