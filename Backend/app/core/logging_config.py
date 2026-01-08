# ============================================================================
# FILE: logging_config.py - CẤU HÌNH LOGGING CHO HỆ THỐNG
# ============================================================================
"""
Module cấu hình logging cho Smart Traffic Monitoring System.

Tính năng:
- RotatingFileHandler: Tự động rotate khi file quá lớn
- ColoredFormatter: Hiển thị màu trong console
- Separate log files: app.log (general), error.log (errors only)
- JSON format option cho production
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path


# ============================================================================
# CONSTANTS
# ============================================================================

# Thư mục logs
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Kích thước file log max (10MB)
MAX_LOG_SIZE = 10 * 1024 * 1024

# Số file backup giữ lại
BACKUP_COUNT = 5

# Format chi tiết
DETAILED_FORMAT = "[%(asctime)s] [%(levelname)-8s] [%(name)s:%(lineno)d] - %(message)s"
SIMPLE_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================================
# COLORED FORMATTER CHO CONSOLE
# ============================================================================

class ColoredFormatter(logging.Formatter):
    """
    Formatter với màu sắc cho console output.
    
    Màu sắc:
    - DEBUG: Xám
    - INFO: Xanh lá
    - WARNING: Vàng
    - ERROR: Đỏ
    - CRITICAL: Đỏ đậm
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[90m',      # Gray
        'INFO': '\033[92m',       # Green
        'WARNING': '\033[93m',    # Yellow
        'ERROR': '\033[91m',      # Red
        'CRITICAL': '\033[91;1m', # Bold Red
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Thêm màu cho level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        
        return super().format(record)


# ============================================================================
# JSON FORMATTER CHO PRODUCTION
# ============================================================================

class JSONFormatter(logging.Formatter):
    """
    Formatter xuất log dạng JSON cho production.
    Dễ dàng parse bởi các tool như ELK Stack, Grafana Loki.
    """
    
    def format(self, record):
        import json
        
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Thêm exception info nếu có
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Thêm extra fields nếu có
        if hasattr(record, 'extra_data'):
            log_data["extra"] = record.extra_data
            
        return json.dumps(log_data, ensure_ascii=False)


# ============================================================================
# SETUP LOGGING FUNCTION
# ============================================================================

def setup_logging(
    level: str = "INFO",
    log_to_file: bool = True,
    log_to_console: bool = True,
    json_format: bool = False,
    app_name: str = "smart_traffic"
) -> logging.Logger:
    """
    Cấu hình logging cho ứng dụng.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Có ghi log ra file không
        log_to_console: Có hiển thị log trên console không
        json_format: Sử dụng JSON format (cho production)
        app_name: Tên ứng dụng để tạo logger
        
    Returns:
        Logger instance đã cấu hình
        
    Example:
        >>> logger = setup_logging(level="DEBUG", log_to_file=True)
        >>> logger.info("Server started")
        >>> logger.error("Connection failed", exc_info=True)
    """
    
    # Lấy root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Chọn formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(DETAILED_FORMAT, DATE_FORMAT)
    
    # ========================================
    # CONSOLE HANDLER
    # ========================================
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        if json_format:
            console_handler.setFormatter(formatter)
        else:
            # Sử dụng ColoredFormatter cho console
            colored_formatter = ColoredFormatter(DETAILED_FORMAT, DATE_FORMAT)
            console_handler.setFormatter(colored_formatter)
        
        root_logger.addHandler(console_handler)
    
    # ========================================
    # FILE HANDLERS
    # ========================================
    if log_to_file:
        # Main log file (all levels)
        main_log_path = LOG_DIR / f"{app_name}.log"
        main_handler = RotatingFileHandler(
            main_log_path,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        main_handler.setLevel(logging.DEBUG)
        main_handler.setFormatter(formatter)
        root_logger.addHandler(main_handler)
        
        # Error log file (ERROR and above)
        error_log_path = LOG_DIR / f"{app_name}_error.log"
        error_handler = RotatingFileHandler(
            error_log_path,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root_logger.addHandler(error_handler)
        
        # Access log file (requests only)
        access_log_path = LOG_DIR / f"{app_name}_access.log"
        access_handler = RotatingFileHandler(
            access_log_path,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        access_handler.setLevel(logging.INFO)
        access_handler.setFormatter(formatter)
        access_logger = logging.getLogger("access")
        access_logger.addHandler(access_handler)
        access_logger.setLevel(logging.INFO)
    
    # Tạo app logger
    app_logger = logging.getLogger(app_name)
    
    # Log startup message
    app_logger.info(f"=" * 60)
    app_logger.info(f"🚀 Logging initialized for {app_name}")
    app_logger.info(f"   Level: {level}")
    app_logger.info(f"   Log to file: {log_to_file}")
    app_logger.info(f"   Log directory: {LOG_DIR}")
    app_logger.info(f"=" * 60)
    
    return app_logger


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_logger(name: str) -> logging.Logger:
    """
    Lấy logger instance cho module cụ thể.
    
    Args:
        name: Tên module (thường dùng __name__)
        
    Returns:
        Logger instance
        
    Example:
        >>> from app.core.logging_config import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    return logging.getLogger(name)


def log_request(method: str, path: str, status_code: int, duration_ms: float):
    """
    Log HTTP request vào access log.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        path: Request path
        status_code: Response status code
        duration_ms: Duration in milliseconds
    """
    access_logger = logging.getLogger("access")
    
    # Màu theo status code
    if status_code < 400:
        status_emoji = "✅"
    elif status_code < 500:
        status_emoji = "⚠️"
    else:
        status_emoji = "❌"
    
    access_logger.info(
        f"{status_emoji} {method} {path} → {status_code} ({duration_ms:.2f}ms)"
    )


def log_exception(logger: logging.Logger, exception: Exception, context: str = ""):
    """
    Log exception với full traceback.
    
    Args:
        logger: Logger instance
        exception: Exception object
        context: Context thêm về lỗi
    """
    if context:
        logger.error(f"Exception in {context}: {str(exception)}", exc_info=True)
    else:
        logger.error(f"Exception: {str(exception)}", exc_info=True)


# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

# Auto-setup khi import module (optional)
# Uncomment nếu muốn tự động setup
# _default_logger = setup_logging()

if __name__ == "__main__":
    # Test logging
    logger = setup_logging(level="DEBUG", log_to_file=True, json_format=False)
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Test access log
    log_request("GET", "/api/traffic", 200, 45.3)
    log_request("POST", "/api/chat", 201, 123.5)
    log_request("GET", "/api/error", 500, 10.2)
    
    # Test exception logging
    try:
        raise ValueError("Test exception")
    except Exception as e:
        log_exception(logger, e, "test module")
    
    print(f"\n✅ Logs written to: {LOG_DIR}")
