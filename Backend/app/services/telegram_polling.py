"""
Telegram Bot Polling Service
Chủ động lấy tin nhắn từ Telegram thay vì dùng webhook
"""

import os
import asyncio
import logging
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class TelegramPolling:
    """
    Service polling tin nhắn từ Telegram Bot

    Sử dụng getUpdates API để lấy tin nhắn mới
    Không cần webhook hay public URL
    """

    def __init__(self):
        """Khởi tạo polling service"""
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.api_base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.offset = 0  # Offset để tracking tin nhắn đã xử lý
        self.is_running = False


    async def start_polling(self, db_session_factory):
        """
        Bắt đầu polling tin nhắn từ Telegram

        Args:
            db_session_factory: Factory để tạo database session
        """
        from app.services.telegram_bot_handler import get_bot_handler

        self.is_running = True
        bot_handler = get_bot_handler()

        logger.info("🤖 Telegram Bot polling started...")

        while self.is_running:
            try:
                # Get updates từ Telegram - use thread executor to avoid blocking event loop
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.get(
                        f"{self.api_base_url}/getUpdates",
                        params={
                            'offset': self.offset,
                            'timeout': 30  # Long polling 30s
                        },
                        timeout=35
                    )
                )

                if response.status_code == 200:
                    data = response.json()

                    if data.get('ok'):
                        updates = data.get('result', [])

                        for update in updates:
                            # Update offset
                            self.offset = update.get('update_id', 0) + 1

                            # Xử lý message
                            if 'message' in update:
                                # Tạo db session cho mỗi message
                                async with db_session_factory() as db:
                                    await bot_handler.handle_message(update, db)

                else:
                    logger.error(f"❌ Telegram API error: {response.status_code}")
                    await asyncio.sleep(5)

            except requests.exceptions.Timeout:
                # Timeout là bình thường với long polling
                continue

            except Exception as e:
                logger.error(f"❌ Lỗi polling: {e}")
                await asyncio.sleep(5)

        logger.info("🛑 Telegram Bot polling stopped")


    def stop_polling(self):
        """Dừng polling"""
        self.is_running = False


# Global polling instance
_polling_service = None

def get_polling_service() -> TelegramPolling:
    """Get singleton instance"""
    global _polling_service
    if _polling_service is None:
        _polling_service = TelegramPolling()
    return _polling_service
