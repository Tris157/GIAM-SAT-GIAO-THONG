"""
Traffic Data Scheduler - Periodically save traffic data to database
"""
import asyncio
import logging
from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import SessionLocal
from app.services.traffic_recording_service import traffic_recording_service

logger = logging.getLogger(__name__)


class TrafficDataScheduler:
    """Background scheduler to auto-save traffic data"""

    def __init__(self, analyzer, interval_seconds: int = 10):
        """
        Initialize scheduler

        Args:
            analyzer: The AnalyzeOnRoadForMultiprocessing instance
            interval_seconds: How often to save data (default: 10 seconds)
        """
        self.analyzer = analyzer
        self.interval = interval_seconds
        self.is_running = False
        self.task = None

    async def start(self):
        """Start the background task"""
        if self.is_running:
            logger.warning("Scheduler already running")
            return

        self.is_running = True
        self.task = asyncio.create_task(self._run_scheduler())
        logger.info(f"Traffic data scheduler started (interval: {self.interval}s)")

    async def stop(self):
        """Stop the background task"""
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Traffic data scheduler stopped")

    async def _run_scheduler(self):
        """Main scheduler loop"""
        while self.is_running:
            try:
                await self._save_all_roads_data()
                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(self.interval)

    async def _save_all_roads_data(self):
        """Save data for all roads"""
        if not self.analyzer or not self.analyzer.names:
            return

        async with SessionLocal() as db:
            try:
                for road_name in self.analyzer.names:
                    try:
                        # Get traffic info for this road
                        traffic_data = await asyncio.to_thread(
                            self.analyzer.get_info_road,
                            road_name
                        )

                        if traffic_data and isinstance(traffic_data, dict):
                            # Save to database
                            await traffic_recording_service.save_traffic_data(
                                db=db,
                                road_name=road_name,
                                traffic_data=traffic_data
                            )

                            logger.debug(
                                f"Saved data for {road_name}: "
                                f"Cars={traffic_data.get('count_car', 0)}, "
                                f"Motors={traffic_data.get('count_motor', 0)}"
                            )

                    except Exception as e:
                        logger.error(f"Error saving data for {road_name}: {e}")
                        continue

            except Exception as e:
                logger.error(f"Error in _save_all_roads_data: {e}")


# Global scheduler instance (will be initialized in main.py)
traffic_scheduler = None


def get_scheduler():
    """Get the global scheduler instance"""
    return traffic_scheduler


def init_scheduler(analyzer, interval_seconds: int = 10):
    """
    Initialize the global scheduler

    Args:
        analyzer: The analyzer instance
        interval_seconds: Save interval in seconds
    """
    global traffic_scheduler
    traffic_scheduler = TrafficDataScheduler(analyzer, interval_seconds)
    return traffic_scheduler
