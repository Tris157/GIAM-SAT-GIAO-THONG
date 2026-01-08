// ============================================================================
// FILE: config.ts - CẤU HÌNH API ENDPOINTS CHO FRONTEND
// ============================================================================
// File này chứa:
// - Base URLs cho HTTP và WebSocket APIs
// - Environment variables configuration (Vite)
// - Centralized endpoints definitions
//
// LỢI ÍCH:
// - Dễ dàng thay đổi API URL (chỉ sửa 1 chỗ)
// - Support nhiều environments (dev, staging, production)
// - Type-safe endpoints với TypeScript

// ============================================================================
// PHẦN 1: HELPER FUNCTIONS
// ============================================================================

// Dòng 6: Hàm loại bỏ trailing slash
const trimTrailingSlash = (url: string) => url.replace(/\/$/, "");
// url.replace(/\/$/, ""): Regex remove trailing slash
// - /\/$/:  Pattern match "/" ở cuối string
// - "": Replace bằng empty string
//
// VÍ DỤ:
// trimTrailingSlash("http://localhost:8000/")  → "http://localhost:8000"
// trimTrailingSlash("http://localhost:8000")   → "http://localhost:8000" (no change)
//
// TẠI SAO CẦN?
// - Tránh double slashes: http://localhost:8000//api/v1/violations
// - Consistent URL format trong toàn bộ app


// ============================================================================
// PHẦN 2: API BASE URLS
// ============================================================================

// Dòng 8-10: HTTP API Base URL
export const API_HTTP_BASE: string = trimTrailingSlash(
  (import.meta as any).env?.VITE_API_HTTP_BASE ?? "http://localhost:8000/"
);
// API_HTTP_BASE: Base URL cho REST API endpoints
//
// GIẢI THÍCH:
// - (import.meta as any).env: Vite environment variables
//   import.meta.env: Object chứa tất cả VITE_* env vars
//   .env file: VITE_API_HTTP_BASE=http://160.19.205.198:8000
//
// - ??: Nullish coalescing operator
//   Nếu left side null/undefined → dùng right side
//
// - Default: "http://localhost:8000/"
//   Dùng khi không có VITE_API_HTTP_BASE env var
//
// CÁCH DÙNG:
//
// Development (.env.development):
// VITE_API_HTTP_BASE=http://localhost:8000
// → API_HTTP_BASE = "http://localhost:8000"
//
// Production (.env.production):
// VITE_API_HTTP_BASE=http://160.19.205.198:8000
// → API_HTTP_BASE = "http://160.19.205.198:8000"
//
// VITE ENV VARS:
// - Phải bắt đầu với VITE_ prefix
// - Được expose ra client code
// - Defined trong .env, .env.development, .env.production
// - Access qua import.meta.env.VITE_*

// Dòng 12-14: WebSocket API Base URL
export const API_WS_BASE: string = trimTrailingSlash(
  (import.meta as any).env?.VITE_API_WS_BASE ?? "ws://localhost:8000/"
);
// API_WS_BASE: Base URL cho WebSocket connections
//
// GIẢI THÍCH:
// - Similar to API_HTTP_BASE nhưng protocol là ws:// thay vì http://
// - WebSocket dùng cho real-time communication:
//   + Live video frames stream
//   + Real-time detection data
//   + Chat with AI
//
// PROTOCOLS:
// - ws://: WebSocket (insecure, như http://)
// - wss://: WebSocket Secure (secure, như https://)
//
// CÁCH DÙNG:
//
// Development:
// VITE_API_WS_BASE=ws://localhost:8000
//
// Production (HTTPS site):
// VITE_API_WS_BASE=wss://api.example.com
//
// LƯU Ý:
// - Nếu frontend là HTTPS → WebSocket phải dùng WSS
// - Mixed content (HTTPS → WS) sẽ bị browser block


// ============================================================================
// PHẦN 3: ENDPOINTS OBJECT
// ============================================================================

// Dòng 16-24: Centralized endpoints
export const endpoints = {
  // Base URL cho API (dùng trong violationService.ts)
  base: API_HTTP_BASE,
  // Endpoints.base = "http://localhost:8000"
  // Dùng trong: violationService.ts để construct full URLs
  // VD: `${endpoints.base}/api/v1/violations/list`

  // Dòng 18: REST API - Lấy danh sách roads
  roadNames: `${API_HTTP_BASE}/roads_name`,
  // Full URL: "http://localhost:8000/roads_name"
  // GET /roads_name: Trả về list tên đường/camera available
  //
  // RESPONSE EXAMPLE:
  // ["camera_live", "camera_highway", "camera_intersection_1"]

  // Dòng 19-20: WebSocket - Frames stream
  framesWs: (roadName: string) => {
    // Nếu là camera_live (RTSP), dùng endpoint RTSP
    if (roadName === "camera_live") {
      return `${API_WS_BASE}/ws/rtsp/${encodeURIComponent(roadName)}`;
    }
    // Các video test khác dùng endpoint frames thông thường
    return `${API_WS_BASE}/ws/frames/${encodeURIComponent(roadName)}`;
  },
  // framesWs: Function trả về WebSocket URL
  //
  // PARAMETERS:
  // - roadName: Tên camera/road (ví dụ: "camera_live")
  //
  // RETURN:
  // Full WebSocket URL: "ws://localhost:8000/ws/frames/camera_live"
  //
  // encodeURIComponent():
  // - Encode special characters trong URL
  // - VD: "camera live" → "camera%20live"
  // - Tránh lỗi nếu roadName có space/special chars
  //
  // CÁCH DÙNG:
  // const wsUrl = endpoints.framesWs("camera_live");
  // const ws = new WebSocket(wsUrl);
  // ws.onmessage = (event) => {
  //   // Nhận frames từ backend
  //   const frameData = event.data;
  // }
  //
  // DATA FORMAT:
  // Backend gửi: Base64 encoded JPEG frames
  // Frontend nhận: Display trong <img> tag

  // Dòng 21-22: WebSocket - Info stream
  infoWs: (roadName: string) =>
    `${API_WS_BASE}/ws/info/${encodeURIComponent(roadName)}`,
  // infoWs: Function trả về WebSocket URL cho detection info
  //
  // PARAMETERS:
  // - roadName: Tên camera (ví dụ: "camera_live")
  //
  // RETURN:
  // "ws://localhost:8000/ws/info/camera_live"
  //
  // DATA FORMAT:
  // Backend gửi JSON với detection data:
  // {
  //   "total_vehicles": 15,
  //   "count_car": 10,
  //   "count_motor": 5,
  //   "detections": [
  //     {"class": "car", "confidence": 0.95, "bbox": [...]},
  //     ...
  //   ]
  // }
  //
  // CÁCH DÙNG:
  // const wsUrl = endpoints.infoWs("camera_live");
  // const ws = new WebSocket(wsUrl);
  // ws.onmessage = (event) => {
  //   const data = JSON.parse(event.data);
  //   console.log(`Detected ${data.total_vehicles} vehicles`);
  // }

  // Dòng 23: WebSocket - Chat với AI
  chatWs: `${API_WS_BASE}/ws/chat`,
  // chatWs: WebSocket URL cho chatbot
  //
  // Full URL: "ws://localhost:8000/ws/chat"
  //
  // FLOW:
  // 1. Frontend connect: new WebSocket(endpoints.chatWs)
  // 2. Frontend gửi: ws.send(JSON.stringify({message: "Hôm nay có bao nhiêu vi phạm?"}))
  // 3. Backend xử lý với AI (GPT/Claude)
  // 4. Backend gửi: {response: "Hôm nay có 15 vi phạm..."}
  // 5. Frontend display response
  //
  // MESSAGE FORMAT:
  // Send:
  // {
  //   "message": "User question here",
  //   "session_id": "unique-session-id"
  // }
  //
  // Receive:
  // {
  //   "response": "AI answer here",
  //   "data": {...}  // Optional structured data
  // }
};


// ============================================================================
// TỔNG KẾT: SỬ DỤNG CONFIG
// ============================================================================
/*
===== 1. IMPORT VÀ SỬ DỤNG =====

Trong violationService.ts:

import { endpoints } from '@/config';

export const getViolations = async () => {
  const url = `${endpoints.base}/api/v1/violations/list`;
  const response = await fetch(url);
  return response.json();
};

Trong VideoStream component:

import { endpoints } from '@/config';

const ws = new WebSocket(endpoints.framesWs("camera_live"));
ws.onmessage = (event) => {
  // Handle frame
};

===== 2. ENVIRONMENT VARIABLES =====

.env (default):
VITE_API_HTTP_BASE=http://localhost:8000
VITE_API_WS_BASE=ws://localhost:8000

.env.development:
VITE_API_HTTP_BASE=http://localhost:8000
VITE_API_WS_BASE=ws://localhost:8000

.env.production:
VITE_API_HTTP_BASE=http://160.19.205.198:8000
VITE_API_WS_BASE=ws://160.19.205.198:8000

BUILD COMMANDS:
- npm run dev → Dùng .env.development
- npm run build → Dùng .env.production

PROCESS:
1. Vite đọc .env file tương ứng
2. Replace import.meta.env.VITE_* với giá trị
3. Bundle vào compiled code
4. Frontend có correct URLs

===== 3. WEBSOCKET VS HTTP =====

HTTP (REST API):
- Request/Response pattern
- Client gửi request → Server trả response
- Dùng cho: CRUD operations, queries
- Protocol: http:// hoặc https://

WebSocket:
- Bi-directional real-time communication
- Persistent connection
- Server có thể push data bất cứ lúc nào
- Dùng cho: Live streams, chat, real-time updates
- Protocol: ws:// hoặc wss://

TRONG PROJECT:
- HTTP: /api/v1/violations/*, /api/v1/reports/*
- WebSocket: /ws/frames/*, /ws/info/*, /ws/chat

===== 4. URL CONSTRUCTION PATTERNS =====

PATTERN 1: Static URL
roadNames: `${API_HTTP_BASE}/roads_name`
→ Fixed endpoint

PATTERN 2: Dynamic URL với function
framesWs: (roadName: string) => `${API_WS_BASE}/ws/frames/${roadName}`
→ Generate URL based on parameters

PATTERN 3: Template với encodeURIComponent
framesWs: (roadName) => `${API_WS_BASE}/ws/frames/${encodeURIComponent(roadName)}`
→ Safe encoding cho special characters

===== 5. BEST PRACTICES =====

1. CENTRALIZE URLS:
   ✓ Tất cả URLs trong config.ts
   ✗ Hardcode URLs scattered trong components

2. USE ENV VARIABLES:
   ✓ VITE_API_HTTP_BASE in .env
   ✗ Hardcode http://localhost:8000

3. ENCODE PARAMETERS:
   ✓ encodeURIComponent(roadName)
   ✗ Direct string interpolation

4. TRIM SLASHES:
   ✓ trimTrailingSlash(url)
   ✗ Có thể có double slashes

5. TYPE SAFETY:
   ✓ endpoints object với types
   ✗ Magic strings everywhere

===== 6. DEBUGGING =====

Check current configuration:
console.log("API_HTTP_BASE:", API_HTTP_BASE);
console.log("API_WS_BASE:", API_WS_BASE);
console.log("Endpoints:", endpoints);

Output:
API_HTTP_BASE: http://localhost:8000
API_WS_BASE: ws://localhost:8000
Endpoints: {
  base: "http://localhost:8000",
  roadNames: "http://localhost:8000/roads_name",
  framesWs: [Function],
  infoWs: [Function],
  chatWs: "ws://localhost:8000/ws/chat"
}

Test endpoints:
console.log(endpoints.framesWs("camera_live"));
→ ws://localhost:8000/ws/frames/camera_live

===== 7. PRODUCTION DEPLOYMENT =====

Khi deploy production:

1. Tạo .env.production:
   VITE_API_HTTP_BASE=https://api.traffic-monitor.com
   VITE_API_WS_BASE=wss://api.traffic-monitor.com

2. Build:
   npm run build

3. Deploy dist/ folder

4. Vite replace env vars trong compiled JS:
   API_HTTP_BASE = "https://api.traffic-monitor.com"
   API_WS_BASE = "wss://api.traffic-monitor.com"

LƯU Ý:
- WSS required nếu frontend là HTTPS
- CORS must be configured trên backend
- WebSocket proxy nếu dùng nginx

===== 8. COMMON ISSUES =====

ISSUE 1: WebSocket connection failed
Cause: Mixed content (HTTPS → WS)
Solution: Dùng WSS thay vì WS

ISSUE 2: CORS error
Cause: Backend không allow frontend domain
Solution: Add CORS middleware trong FastAPI

ISSUE 3: Double slashes in URL
Cause: Không trim trailing slashes
Solution: Dùng trimTrailingSlash()

ISSUE 4: Env vars không work
Cause: Không có VITE_ prefix
Solution: Rename thành VITE_API_HTTP_BASE

===== 9. FUTURE ENHANCEMENTS =====

Có thể thêm:

1. API versioning:
   API_VERSION: "/api/v2"

2. Timeout config:
   API_TIMEOUT: 30000  // 30 seconds

3. Retry config:
   API_RETRY_COUNT: 3

4. Feature flags:
   FEATURES: {
     violations: true,
     chat: false
   }

END OF DOCUMENTATION
*/
