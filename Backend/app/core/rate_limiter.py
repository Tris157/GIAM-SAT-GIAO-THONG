# ============================================================================
# FILE: rate_limiter.py - RATE LIMITING CHO API
# ============================================================================
"""
Module Rate Limiting cho Smart Traffic Monitoring System.

Bảo vệ API khỏi:
- DDoS attacks
- Brute force attacks  
- Excessive API usage

Sử dụng slowapi (dựa trên Flask-Limiter).
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# RATE LIMITER CONFIGURATION
# ============================================================================

# Key function để xác định client
# Mặc định dùng IP address
def get_client_identifier(request: Request) -> str:
    """
    Xác định client để áp dụng rate limit.
    
    Priority:
    1. X-Forwarded-For header (nếu qua reverse proxy)
    2. X-Real-IP header
    3. Client IP address
    
    Returns:
        Client identifier string
    """
    # Check forwarded headers (khi dùng nginx/cloudflare)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Lấy IP đầu tiên trong chain
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to client host
    if request.client:
        return request.client.host
    
    return "unknown"


# Tạo Limiter instance
limiter = Limiter(
    key_func=get_client_identifier,
    default_limits=["200/minute", "1000/hour"],  # Default limits
    storage_uri="memory://",  # Có thể đổi sang redis:// cho production
    strategy="fixed-window"  # Hoặc "sliding-window" cho chính xác hơn
)


# ============================================================================
# RATE LIMIT PRESETS
# ============================================================================

class RateLimits:
    """
    Các preset rate limit cho từng loại endpoint.
    
    Format: "số_requests/khoảng_thời_gian"
    Ví dụ: "10/minute", "100/hour", "1000/day"
    """
    
    # Public endpoints - nhẹ nhàng
    PUBLIC = "60/minute"
    
    # Authentication - chặt để chống brute force
    AUTH = "5/minute"
    AUTH_STRICT = "3/minute"
    
    # API endpoints - trung bình
    API_STANDARD = "100/minute"
    API_HEAVY = "30/minute"
    
    # Video streaming - cho phép nhiều hơn vì cần liên tục
    STREAMING = "300/minute"
    
    # Chat/AI - giới hạn vì tốn resources
    AI_CHAT = "20/minute"
    
    # Export/Report - tốn resources, giới hạn chặt
    EXPORT = "10/minute"
    
    # Admin operations
    ADMIN = "50/minute"
    
    # Health check - không giới hạn
    HEALTH = "1000/minute"


# ============================================================================
# CUSTOM RATE LIMIT EXCEEDED HANDLER
# ============================================================================

async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Custom handler khi vượt quá rate limit.
    
    Trả về response thân thiện với đầy đủ thông tin.
    """
    # Log warning
    logger.warning(
        f"Rate limit exceeded: {get_client_identifier(request)} "
        f"on {request.method} {request.url.path}"
    )
    
    # Parse limit info
    limit_value = str(exc.detail) if exc.detail else "unknown"
    
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "message": "Bạn đã gửi quá nhiều requests. Vui lòng thử lại sau.",
            "message_en": "Too many requests. Please try again later.",
            "limit": limit_value,
            "retry_after": "60 seconds",
            "tips": [
                "Giảm tần suất gọi API",
                "Sử dụng caching ở client",
                "Liên hệ admin nếu cần tăng limit"
            ]
        },
        headers={
            "Retry-After": "60",
            "X-RateLimit-Limit": limit_value,
        }
    )


# ============================================================================
# SETUP FUNCTION
# ============================================================================

def setup_rate_limiter(app: FastAPI) -> Limiter:
    """
    Cấu hình rate limiter cho FastAPI app.
    
    Args:
        app: FastAPI application instance
        
    Returns:
        Limiter instance
        
    Example:
        >>> from fastapi import FastAPI
        >>> from app.core.rate_limiter import setup_rate_limiter, limiter, RateLimits
        >>> 
        >>> app = FastAPI()
        >>> setup_rate_limiter(app)
        >>> 
        >>> @app.get("/api/data")
        >>> @limiter.limit(RateLimits.API_STANDARD)
        >>> async def get_data(request: Request):
        >>>     return {"data": "..."}
    """
    # Thêm limiter vào app state
    app.state.limiter = limiter
    
    # Thêm exception handler
    app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
    
    # Thêm middleware
    app.add_middleware(SlowAPIMiddleware)
    
    logger.info("✅ Rate limiter initialized")
    logger.info(f"   Default limits: {limiter._default_limits}")
    
    return limiter


# ============================================================================
# DECORATORS FOR COMMON USE CASES
# ============================================================================

def limit_auth(func):
    """Decorator cho authentication endpoints."""
    return limiter.limit(RateLimits.AUTH)(func)


def limit_api(func):
    """Decorator cho API endpoints thông thường."""
    return limiter.limit(RateLimits.API_STANDARD)(func)


def limit_heavy(func):
    """Decorator cho heavy endpoints."""
    return limiter.limit(RateLimits.API_HEAVY)(func)


def limit_export(func):
    """Decorator cho export endpoints."""
    return limiter.limit(RateLimits.EXPORT)(func)


def limit_ai(func):
    """Decorator cho AI chat endpoints."""
    return limiter.limit(RateLimits.AI_CHAT)(func)


# ============================================================================
# WHITELIST / BLACKLIST
# ============================================================================

# IPs được bypass rate limit (internal services, monitoring)
WHITELIST_IPS = {
    "127.0.0.1",
    "localhost",
    # Thêm IPs của internal services
}

# IPs bị block hoàn toàn
BLACKLIST_IPS = set()


def is_whitelisted(request: Request) -> bool:
    """Kiểm tra IP có trong whitelist không."""
    client_ip = get_client_identifier(request)
    return client_ip in WHITELIST_IPS


def is_blacklisted(request: Request) -> bool:
    """Kiểm tra IP có trong blacklist không."""
    client_ip = get_client_identifier(request)
    return client_ip in BLACKLIST_IPS


def add_to_blacklist(ip: str):
    """Thêm IP vào blacklist."""
    BLACKLIST_IPS.add(ip)
    logger.warning(f"IP {ip} added to blacklist")


def remove_from_blacklist(ip: str):
    """Xóa IP khỏi blacklist."""
    BLACKLIST_IPS.discard(ip)
    logger.info(f"IP {ip} removed from blacklist")
