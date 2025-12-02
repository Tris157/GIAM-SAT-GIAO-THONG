# CLAUDE.md - AI Assistant Development Guide

## Smart Traffic Monitoring System

**Version:** 2.1
**Last Updated:** 2025-12-02
**Maintainer:** Development Team

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Overview](#architecture-overview)
3. [Backend Development Guide](#backend-development-guide)
4. [Frontend Development Guide](#frontend-development-guide)
5. [Key Conventions & Patterns](#key-conventions--patterns)
6. [Development Workflows](#development-workflows)
7. [Common Tasks & Examples](#common-tasks--examples)
8. [Testing & Quality Assurance](#testing--quality-assurance)
9. [Deployment & Production](#deployment--production)
10. [Troubleshooting](#troubleshooting)

---

## Project Overview

### Purpose
A real-time traffic monitoring system using AI (YOLO + OpenVINO) for vehicle detection, speed estimation, red light violation detection, and traffic analytics with an AI-powered chatbot assistant.

### Tech Stack

**Backend:**
- **Framework:** FastAPI 0.104+ (async Python web framework)
- **Database:** SQLite with SQLAlchemy 2.0+ ORM (async support)
- **AI/ML:** YOLOv8 (Ultralytics) + OpenVINO for inference
- **Real-time:** WebSocket for video streaming and live data
- **Authentication:** JWT tokens with passlib for password hashing
- **External APIs:** Google Gemini (chatbot), OpenWeather API, Telegram Bot

**Frontend:**
- **Framework:** React 19.1 + TypeScript 5.8
- **Build Tool:** Vite 7.x
- **UI Library:** shadcn/ui (50+ Radix UI components)
- **Styling:** TailwindCSS 4.1 with custom OKLCH colors
- **Animation:** Framer Motion 12.x
- **Charts:** Recharts 2.x
- **Routing:** React Router DOM 7.x
- **State:** React Context API + Custom Hooks

### Key Features
1. **Multi-camera Traffic Monitoring** - Real-time video streaming with YOLO detection
2. **Speed Estimation** - Average speed calculation for cars and motorcycles
3. **Red Light Violation Detection** - Automatic violation capture and logging
4. **Traffic Analytics** - Peak hour analysis, trend charts, road comparisons
5. **AI Chatbot** - Google Gemini-powered traffic assistant
6. **Weather Integration** - Real-time weather data overlay
7. **Telegram Notifications** - Automated alerts for violations
8. **User Management** - JWT authentication with role-based access (admin/user)

### Project Structure

```
GIAM-SAT-GIAO-THONG/
├── Backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI entry point
│   │   ├── api/v1/                    # API routes (auth, violations, reports, etc.)
│   │   ├── core/                      # Config, security, logging
│   │   ├── db/                        # Database connection
│   │   ├── models/                    # SQLAlchemy models
│   │   ├── schemas/                   # Pydantic schemas
│   │   ├── services/                  # Business logic
│   │   │   ├── road_services/         # YOLO detection & tracking
│   │   │   ├── chat_services/         # AI chatbot logic
│   │   │   ├── red_light_detector.py  # Violation detection
│   │   │   ├── weather_service.py     # Weather API
│   │   │   └── telegram_notifier.py   # Telegram bot
│   │   ├── ai_models/                 # YOLO model files
│   │   ├── video_test/                # Video sources
│   │   ├── utils/                     # Utilities
│   │   └── traffic_monitor.db         # SQLite database
│   ├── requirements_cpu.txt           # CPU dependencies
│   ├── requirements_gpu.txt           # GPU dependencies
│   └── .env                           # Environment variables
│
├── Frontend/
│   ├── src/
│   │   ├── main.tsx                   # React entry point
│   │   ├── App.tsx                    # Root component
│   │   ├── components/
│   │   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── Layout/                # AppLayout, Sidebar
│   │   │   ├── TrafficDashboard.tsx   # Main dashboard
│   │   │   ├── VideoMonitor.tsx       # Video display
│   │   │   ├── ChatInterface.tsx      # AI chatbot UI
│   │   │   ├── ViolationsManagement.tsx
│   │   │   ├── TrafficAnalytics.tsx   # Charts & analytics
│   │   │   └── RTSPLiveStream.tsx     # Live camera
│   │   ├── pages/                     # Login, Register, Dashboard
│   │   ├── contexts/                  # AuthContext
│   │   ├── hooks/                     # useWebSocket, use-mobile
│   │   ├── services/                  # API services
│   │   ├── utils/                     # Utilities
│   │   └── config.ts                  # API endpoints config
│   ├── package.json
│   └── vite.config.ts
│
├── README.md                          # User documentation
├── CLAUDE.md                          # This file (AI assistant guide)
├── BAO_CAO_DU_AN.md                   # Project report (Vietnamese)
├── HUONG_DAN_CAI_DAT.md               # Installation guide (Vietnamese)
└── docker-compose.yml                 # Docker configuration
```

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │Analytics │  │Violations│  │ Chatbot  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        │ WebSocket   │ REST API    │ REST API    │ WebSocket
        │             │             │             │
┌───────┼─────────────┼─────────────┼─────────────┼──────────┐
│       ▼             ▼             ▼             ▼          │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐  │
│  │Frame WS │  │Reports   │  │Violations │  │Chat WS   │  │
│  │Endpoint │  │Endpoint  │  │Endpoint   │  │Endpoint  │  │
│  └────┬────┘  └────┬─────┘  └─────┬─────┘  └────┬─────┘  │
│       │            │               │             │         │
│       │       ┌────┴───────────────┴─────────────┘         │
│       │       │         FastAPI Application                │
│       │       │                                             │
│       ▼       ▼                                             │
│  ┌─────────────────┐        ┌──────────────────┐          │
│  │ Video Analyzer  │◄───────┤ SQLite Database  │          │
│  │ (Multiprocess)  │        │  - TrafficRecord │          │
│  │  - YOLO detect  │        │  - Violation     │          │
│  │  - ByteTrack    │        │  - User          │          │
│  │  - Speed calc   │        └──────────────────┘          │
│  └────┬────────────┘                                       │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────┐        ┌──────────────────┐          │
│  │Red Light Detect │        │ External Services│          │
│  │  - ROI analysis │        │  - Google Gemini │          │
│  │  - Line cross   │        │  - OpenWeather   │          │
│  │  - Auto capture │        │  - Telegram Bot  │          │
│  └─────────────────┘        └──────────────────┘          │
│                     Backend (FastAPI)                      │
└────────────────────────────────────────────────────────────┘
```

### Data Flow

**1. Video Processing Pipeline:**
```
Video Source → Frame Extraction → ROI Crop → YOLO Detection →
ByteTrack Tracking → Speed Calculation → Data Storage →
WebSocket Broadcast → Frontend Display
```

**2. Violation Detection Pipeline:**
```
Frame → Red Light ROI Check → Stop Line Detection →
Vehicle Position Analysis → Violation Logging → Database →
Telegram Notification → Frontend Alert
```

**3. API Request Flow:**
```
Frontend Request → API Endpoint → Pydantic Validation →
Database Query → Response Serialization → JSON Return
```

### Database Schema

**TrafficViolation Table:**
```python
id: Integer (PK)
camera_name: String (indexed)
violation_type: String (indexed) # "red_light", "speeding", etc.
vehicle_type: String             # "car", "motorcycle"
image_path: String
position_x: Integer
position_y: Integer
traffic_light_status: String     # "red", "yellow", "green"
violated_at: DateTime (indexed)
date: Date (indexed)             # Derived from violated_at
hour_of_day: Integer (indexed)  # Derived from violated_at
is_processed: Boolean (indexed)
note: Text
confidence: Float

# Composite indexes:
- (camera_name, date)
- (violation_type, date)
- (is_processed, date)
```

**User Table:**
```python
id: Integer (PK)
username: String (unique)
email: String (unique)
password: String              # bcrypt hashed
full_name: String
role_id: Integer             # 0=admin, 1=user
is_active: Boolean
created_at: DateTime
updated_at: DateTime
```

---

## Backend Development Guide

### Setup & Environment

**1. Virtual Environment:**
```bash
cd Backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**2. Install Dependencies:**
```bash
# CPU (recommended)
pip install -r requirements_cpu.txt

# GPU (NVIDIA CUDA)
pip install -r requirements_gpu.txt
```

**3. Environment Variables (.env):**
```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./app/traffic_monitor.db

# JWT Authentication
JWT_SECRET_KEY=your_super_secret_key_change_this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs (optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
OPENWEATHER_API_KEY=your_openweather_key
GOOGLE_API_KEY=your_google_gemini_key
```

**4. Run Backend:**
```bash
cd Backend/app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Key Backend Files

**main.py** - Application Entry Point
```python
# Key responsibilities:
# 1. FastAPI app initialization
# 2. CORS middleware setup
# 3. Router registration
# 4. Startup events (DB init, analyzer start, scheduler)
# 5. Shutdown handlers (cleanup)

# Startup sequence:
@app.on_event("startup")
async def startup_event():
    create_all_tables()                    # SQLAlchemy sync
    threading.Thread(...).start()          # Analyzer background
    asyncio.create_task(start_scheduler()) # Auto-save scheduler
    threading.Thread(init_telegram_bot)    # Telegram bot
```

**api/v1/api_violations.py** - Violation CRUD
```python
# Endpoints:
GET    /api/v1/violations/list             # List all violations
GET    /api/v1/violations/{id}             # Get single violation
POST   /api/v1/violations/                 # Create violation (manual)
PUT    /api/v1/violations/{id}             # Update violation
DELETE /api/v1/violations/{id}             # Delete violation
PATCH  /api/v1/violations/{id}/process     # Mark as processed
GET    /api/v1/violations/stats/summary    # Statistics

# Common pattern:
@router.get("/violations/list")
async def get_violations(
    camera_name: Optional[str] = None,
    is_processed: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(TrafficViolation)
    if camera_name:
        query = query.filter(TrafficViolation.camera_name == camera_name)
    result = await db.execute(query)
    return result.scalars().all()
```

**services/road_services/AnalyzeOnRoadBase.py** - YOLO Detection
```python
# Core detection logic:
class AnalyzeOnRoadBase:
    def __init__(self, path_video, meter_per_pixel, region, ...):
        self.speed_tool = solutions.SpeedEstimator(
            model=MODELS_PATH,
            tracker='bytetrack.yaml',
            device=DEVICE,
            meter_per_pixel=meter_per_pixel
        )
        self.classNames = ['Car', 'Motorcycle']

    def process_single_frame(self, frame_input):
        # 1. ROI extraction
        ROI_frame = frame_input[self.region[1]:self.region[3],
                                 self.region[0]:self.region[2]]

        # 2. YOLO detection
        self.speed_tool.process(ROI_frame.copy())
        track_data = self.speed_tool.track_data

        # 3. Extract results
        ids = track_data.id.cpu().numpy()
        classes = track_data.cls.cpu().numpy()
        boxes = track_data.xyxy.cpu().numpy()
        speeds = self.speed_tool.spd  # Dict[id: speed_km/h]

        # 4. Update counters and speeds
        for track_id, cls in zip(ids, classes):
            if cls == 0:  # Car
                self.count_car += 1
                self.speed_car.append(speeds[track_id])
            elif cls == 1:  # Motorcycle
                self.count_motor += 1
                self.speed_motor.append(speeds[track_id])

        # 5. Draw overlays
        # 6. Return processed frame
```

**services/red_light_detector.py** - Violation Detection
```python
class RedLightViolationDetector:
    def __init__(self, config: RedLightConfig):
        self.camera_name = config.camera_name
        self.traffic_light_roi = config.traffic_light_roi
        self.stop_line_y = config.stop_line_y
        self.model = YOLO(MODELS_PATH)

    def detect_violations(self, frame, track_data):
        # 1. Check red light status
        light_status = self.detect_light_color(frame)
        if light_status != 'red':
            return []

        # 2. Get vehicle positions
        boxes = track_data.xyxy.cpu().numpy()
        classes = track_data.cls.cpu().numpy()

        violations = []
        for box, cls in zip(boxes, classes):
            x1, y1, x2, y2 = box
            vehicle_y = (y1 + y2) / 2

            # 3. Check if crossed stop line
            if vehicle_y > self.stop_line_y:
                violation = {
                    'camera_name': self.camera_name,
                    'violation_type': 'red_light',
                    'vehicle_type': self.classNames[int(cls)],
                    'position_x': int((x1 + x2) / 2),
                    'position_y': int(vehicle_y),
                    'traffic_light_status': 'red'
                }
                violations.append(violation)

        return violations
```

### Database Operations

**Async Session Pattern:**
```python
from app.db.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def example_query(db: AsyncSession = Depends(get_db)):
    # SELECT
    query = select(TrafficViolation).filter(
        TrafficViolation.camera_name == "camera1"
    ).order_by(TrafficViolation.violated_at.desc())

    result = await db.execute(query)
    violations = result.scalars().all()

    # INSERT
    new_violation = TrafficViolation(
        camera_name="camera1",
        violation_type="red_light",
        # ... other fields
    )
    db.add(new_violation)
    await db.commit()
    await db.refresh(new_violation)

    # UPDATE
    violation.is_processed = True
    await db.commit()

    # DELETE
    await db.delete(violation)
    await db.commit()
```

**Aggregations:**
```python
from sqlalchemy import func

# Count by date
query = select(
    TrafficViolation.date,
    func.count(TrafficViolation.id).label('total')
).group_by(TrafficViolation.date)

# Average, min, max
query = select(
    func.avg(TrafficViolation.confidence),
    func.min(TrafficViolation.violated_at),
    func.max(TrafficViolation.violated_at)
)
```

### API Endpoint Patterns

**Standard CRUD Endpoint:**
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    value: int

class ItemResponse(BaseModel):
    id: int
    name: str
    value: int

    class Config:
        from_attributes = True  # For SQLAlchemy models

@router.get("/items", response_model=List[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_db)):
    """List all items"""
    query = select(Item)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/items", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new item"""
    db_item = Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Get single item"""
    query = select(Item).filter(Item.id == item_id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item
```

**WebSocket Endpoint:**
```python
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

@app.websocket("/ws/data/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()

    try:
        while True:
            # Send data to client
            data = {"message": "Hello", "client_id": client_id}
            await websocket.send_json(data)

            # Or receive from client
            message = await websocket.receive_text()

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        pass
```

### Authentication & Security

**Password Hashing:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

**JWT Tokens:**
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
```

**Protected Endpoints:**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    payload = decode_token(token)
    if not payload:
        raise credentials_exception

    username = payload.get("sub")
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception

    return user

# Admin-only endpoint
async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role_id != 0:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Usage
@router.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    admin: User = Depends(get_current_admin)
):
    # Only admins can delete
    pass
```

---

## Frontend Development Guide

### Setup & Environment

**1. Install Dependencies:**
```bash
cd Frontend

# Install pnpm if not available
npm install -g pnpm

# Install dependencies
pnpm install
```

**2. Environment Variables (.env):**
```env
VITE_API_HTTP_BASE=http://localhost:8000
VITE_API_WS_BASE=ws://localhost:8000
```

**3. Run Development Server:**
```bash
pnpm run dev
# Opens http://localhost:5173
```

**4. Build for Production:**
```bash
pnpm run build
# Output: dist/
```

### Component Structure

**Functional Component Pattern:**
```typescript
// ComponentName.tsx
import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface ComponentProps {
  title: string;
  onAction?: () => void;
}

const ComponentName: React.FC<ComponentProps> = ({ title, onAction }) => {
  // 1. State declarations
  const [data, setData] = useState<DataType[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 2. Effects
  useEffect(() => {
    fetchData();
  }, []);

  // 3. Event handlers
  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/data');
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const handleClick = () => {
    onAction?.();
  };

  // 4. Render
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <Card>
      <h2>{title}</h2>
      <Button onClick={handleClick}>Click Me</Button>
      {data.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </Card>
  );
};

export default ComponentName;
```

### Custom Hooks

**useWebSocket Hook Pattern:**
```typescript
// hooks/useWebSocket.ts
import { useState, useEffect, useRef } from 'react';

interface WebSocketHook<T> {
  data: T | null;
  isConnected: boolean;
  error: string | null;
  send: (message: any) => void;
}

export function useWebSocket<T>(
  url: string | null,
  options = {}
): WebSocketHook<T> {
  const [data, setData] = useState<T | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!url) return;

    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      setError(null);
    };

    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setData(parsed);
      } catch {
        setData(event.data as T);
      }
    };

    ws.onerror = (event) => {
      setError('WebSocket error');
      setIsConnected(false);
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  const send = (message: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  return { data, isConnected, error, send };
}

// Usage:
const { data, isConnected } = useWebSocket<TrafficData>(
  `ws://localhost:8000/ws/info/Văn Phú`
);
```

### API Service Pattern

**Service Layer (services/violationService.ts):**
```typescript
import { endpoints } from '@/config';

export interface Violation {
  id: number;
  camera_name: string;
  violation_type: string;
  vehicle_type: string;
  violated_at: string;
  is_processed: boolean;
  image_path: string;
}

export interface ViolationFilters {
  camera_name?: string;
  is_processed?: boolean;
  start_date?: string;
  end_date?: string;
}

export const getViolations = async (
  filters: ViolationFilters = {}
): Promise<Violation[]> => {
  const params = new URLSearchParams();

  if (filters.camera_name) {
    params.append('camera_name', filters.camera_name);
  }
  if (filters.is_processed !== undefined) {
    params.append('is_processed', filters.is_processed.toString());
  }

  const url = `${endpoints.base}/api/v1/violations/list?${params}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch violations: ${response.statusText}`);
  }

  return response.json();
};

export const markViolationProcessed = async (id: number): Promise<void> => {
  const response = await fetch(
    `${endpoints.base}/api/v1/violations/${id}/process`,
    { method: 'PATCH' }
  );

  if (!response.ok) {
    throw new Error('Failed to mark violation as processed');
  }
};

export const deleteViolation = async (id: number): Promise<void> => {
  const response = await fetch(
    `${endpoints.base}/api/v1/violations/${id}`,
    { method: 'DELETE' }
  );

  if (!response.ok) {
    throw new Error('Failed to delete violation');
  }
};
```

### Context API for Global State

**AuthContext Pattern:**
```typescript
// contexts/AuthContext.tsx
import { createContext, useContext, useState, useEffect } from 'react';

interface User {
  id: number;
  username: string;
  email: string;
  role_id: number;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const token = localStorage.getItem('token');
    if (token) {
      validateToken(token);
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (username: string, password: string) => {
    const response = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    setUser(data.user);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const validateToken = async (token: string) => {
    try {
      const response = await fetch('/api/v1/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        localStorage.removeItem('token');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    user,
    isLoading,
    isAuthenticated: !!user,
    isAdmin: user?.role_id === 0,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### Styling with TailwindCSS

**Common Patterns:**
```typescript
// Glass morphism card
<Card className="glass border border-white/10 backdrop-blur-xl shadow-2xl">
  {/* Content */}
</Card>

// Gradient text
<h1 className="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
  Gradient Text
</h1>

// Animated button with Framer Motion
<motion.div
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  <Button>Click Me</Button>
</motion.div>

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {items.map(item => <ItemCard key={item.id} {...item} />)}
</div>
```

**Custom CSS (App.css):**
```css
/* Glass morphism */
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Animated gradient background */
@keyframes rainbow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.rainbow-gradient {
  background: linear-gradient(270deg, #ff6b6b, #4ecdc4, #45b7d1);
  background-size: 600% 600%;
  animation: rainbow 15s ease infinite;
}
```

### TypeScript Best Practices

**Interface Definitions:**
```typescript
// Always define interfaces for data structures
interface TrafficData {
  count_car: number;
  count_motor: number;
  speed_car: number;
  speed_motor: number;
}

// Use optional properties when appropriate
interface ComponentProps {
  title: string;
  subtitle?: string;
  onAction?: () => void;
}

// Extend interfaces for variations
interface ExtendedTrafficData extends TrafficData {
  timestamp: string;
  road_name: string;
}

// Union types for limited options
type ViolationType = 'red_light' | 'speeding' | 'wrong_lane';
type TrafficStatus = 'smooth' | 'moderate' | 'congested';
```

**Generic Types:**
```typescript
// Generic API response wrapper
interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}

// Generic fetch function
async function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  return response.json();
}

// Usage
const result = await fetchData<Violation[]>('/api/violations');
```

---

## Key Conventions & Patterns

### Naming Conventions

**Backend (Python):**
- **Files:** `snake_case.py` (e.g., `api_violations.py`, `red_light_detector.py`)
- **Classes:** `PascalCase` (e.g., `TrafficViolation`, `RedLightDetector`)
- **Functions/Methods:** `snake_case()` (e.g., `get_violations()`, `process_frame()`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `DATABASE_URL`, `MODELS_PATH`)
- **Private:** `_leading_underscore` (e.g., `_internal_helper()`)
- **Module imports:** Grouped by standard library → third-party → local

**Frontend (TypeScript):**
- **Component files:** `PascalCase.tsx` (e.g., `TrafficDashboard.tsx`)
- **Utility files:** `camelCase.ts` (e.g., `apiCache.ts`)
- **Components:** `PascalCase` (e.g., `VideoMonitor`, `ChatInterface`)
- **Functions/variables:** `camelCase` (e.g., `getViolations`, `userData`)
- **Hooks:** `use` prefix + `PascalCase` (e.g., `useWebSocket`, `useAuth`)
- **Interfaces:** `PascalCase` (e.g., `TrafficData`, `ViolationFilters`)
- **Types:** `PascalCase` (e.g., `ViolationType`)
- **Constants:** `UPPER_SNAKE_CASE` or `camelCase` depending on scope

### Code Organization

**Backend Module Structure:**
```python
# Standard library imports
import os
import sys
from datetime import datetime
from typing import List, Optional

# Third-party imports
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from pydantic import BaseModel
import numpy as np

# Local application imports
from app.db.base import get_db
from app.models.traffic_violation import TrafficViolation
from app.schemas.violation import ViolationResponse
from app.core.security import get_current_user
```

**Frontend Import Structure:**
```typescript
// React imports
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// UI component imports
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

// Icon imports
import { Car, AlertTriangle, CheckCircle } from 'lucide-react';

// Local component imports
import { VideoMonitor } from '@/components/VideoMonitor';

// Context/hook imports
import { useAuth } from '@/contexts/AuthContext';
import { useWebSocket } from '@/hooks/useWebSocket';

// Service/utility imports
import { getViolations } from '@/services/violationService';
import { endpoints } from '@/config';
```

### Error Handling

**Backend:**
```python
# Use HTTPException for API errors
from fastapi import HTTPException

@router.get("/items/{item_id}")
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Item).filter(Item.id == item_id)
        result = await db.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(
                status_code=404,
                detail=f"Item {item_id} not found"
            )

        return item

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        # Log the error
        print(f"Error fetching item: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```

**Frontend:**
```typescript
// Use try-catch with proper state management
const loadData = async () => {
  try {
    setLoading(true);
    setError(null);

    const data = await fetchData();
    setData(data);

  } catch (error) {
    console.error('Failed to load data:', error);
    setError(error instanceof Error ? error.message : 'Unknown error');

    // Optional: Show toast notification
    toast.error('Failed to load data');

  } finally {
    setLoading(false);
  }
};

// Render with error states
if (loading) return <LoadingSpinner />;
if (error) return <ErrorMessage message={error} />;
if (!data) return <EmptyState />;
```

### Async Patterns

**Backend (async/await):**
```python
# Async database operations
async def get_violations(db: AsyncSession):
    query = select(TrafficViolation)
    result = await db.execute(query)
    return result.scalars().all()

# Async external API calls
import httpx

async def fetch_weather():
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_API_URL)
        return response.json()

# Concurrent operations with asyncio.gather
import asyncio

async def get_all_data():
    violations, weather, traffic = await asyncio.gather(
        get_violations(db),
        fetch_weather(),
        get_traffic_stats()
    )
    return {
        'violations': violations,
        'weather': weather,
        'traffic': traffic
    }
```

**Frontend (Promises and async/await):**
```typescript
// Single async operation
const loadViolations = async () => {
  const data = await getViolations();
  setViolations(data);
};

// Parallel operations
const loadAllData = async () => {
  const [violations, cameras, stats] = await Promise.all([
    getViolations(),
    getCameras(),
    getStatistics()
  ]);

  setViolations(violations);
  setCameras(cameras);
  setStats(stats);
};

// Sequential operations (when order matters)
const processViolation = async (id: number) => {
  const violation = await getViolation(id);
  const processed = await markAsProcessed(id);
  await sendNotification(violation);
};
```

### Configuration Management

**Backend (.env access):**
```python
# core/config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./traffic.db")

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET_KEY", "default-secret-change-this")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # External APIs
    TELEGRAM_BOT_TOKEN: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
    GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")

    # Application
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()

# Usage
from app.core.config import settings
print(settings.DATABASE_URL)
```

**Frontend (Vite env variables):**
```typescript
// config.ts
const trimTrailingSlash = (url: string) => url.replace(/\/$/, '');

export const API_HTTP_BASE: string = trimTrailingSlash(
  import.meta.env.VITE_API_HTTP_BASE ?? "http://localhost:8000"
);

export const API_WS_BASE: string = trimTrailingSlash(
  import.meta.env.VITE_API_WS_BASE ?? "ws://localhost:8000"
);

export const endpoints = {
  base: API_HTTP_BASE,

  // Auth
  login: `${API_HTTP_BASE}/api/v1/auth/login`,
  register: `${API_HTTP_BASE}/api/v1/auth/register`,

  // Violations
  violations: `${API_HTTP_BASE}/api/v1/violations/list`,
  violationById: (id: number) => `${API_HTTP_BASE}/api/v1/violations/${id}`,

  // WebSocket
  framesWs: (road: string) =>
    `${API_WS_BASE}/ws/frames/${encodeURIComponent(road)}`,
  infoWs: (road: string) =>
    `${API_WS_BASE}/ws/info/${encodeURIComponent(road)}`,
  chatWs: `${API_WS_BASE}/ws/chat`,
};
```

---

## Development Workflows

### Adding a New API Endpoint

**Step 1: Create Pydantic Schema (Backend/app/schemas/)**
```python
# schemas/my_feature.py
from pydantic import BaseModel
from datetime import datetime

class FeatureCreate(BaseModel):
    name: str
    value: int

class FeatureResponse(BaseModel):
    id: int
    name: str
    value: int
    created_at: datetime

    class Config:
        from_attributes = True
```

**Step 2: Create Database Model (Backend/app/models/)**
```python
# models/my_feature.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

**Step 3: Create API Router (Backend/app/api/v1/)**
```python
# api/v1/api_feature.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.base import get_db
from app.models.my_feature import Feature
from app.schemas.my_feature import FeatureCreate, FeatureResponse

router = APIRouter()

@router.get("/features", response_model=List[FeatureResponse])
async def list_features(db: AsyncSession = Depends(get_db)):
    query = select(Feature)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/features", response_model=FeatureResponse)
async def create_feature(
    feature: FeatureCreate,
    db: AsyncSession = Depends(get_db)
):
    db_feature = Feature(**feature.dict())
    db.add(db_feature)
    await db.commit()
    await db.refresh(db_feature)
    return db_feature
```

**Step 4: Register Router (Backend/app/main.py)**
```python
# main.py
from app.api.v1 import api_feature

app.include_router(
    api_feature.router,
    prefix="/api/v1",
    tags=["features"]
)
```

**Step 5: Create Frontend Service (Frontend/src/services/)**
```typescript
// services/featureService.ts
import { endpoints } from '@/config';

export interface Feature {
  id: number;
  name: string;
  value: number;
  created_at: string;
}

export const getFeatures = async (): Promise<Feature[]> => {
  const response = await fetch(`${endpoints.base}/api/v1/features`);
  if (!response.ok) throw new Error('Failed to fetch features');
  return response.json();
};

export const createFeature = async (
  name: string,
  value: number
): Promise<Feature> => {
  const response = await fetch(`${endpoints.base}/api/v1/features`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, value })
  });

  if (!response.ok) throw new Error('Failed to create feature');
  return response.json();
};
```

**Step 6: Use in Component (Frontend/src/components/)**
```typescript
// components/FeatureList.tsx
import { useState, useEffect } from 'react';
import { getFeatures, Feature } from '@/services/featureService';

const FeatureList: React.FC = () => {
  const [features, setFeatures] = useState<Feature[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFeatures();
  }, []);

  const loadFeatures = async () => {
    try {
      const data = await getFeatures();
      setFeatures(data);
    } catch (error) {
      console.error('Failed to load features:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {features.map(f => (
        <div key={f.id}>{f.name}: {f.value}</div>
      ))}
    </div>
  );
};

export default FeatureList;
```

### Adding a New Page/Route

**Step 1: Create Page Component (Frontend/src/pages/)**
```typescript
// pages/NewPage.tsx
import { AppLayout } from '@/components/Layout/AppLayout';
import { Card } from '@/components/ui/card';

const NewPage: React.FC = () => {
  return (
    <AppLayout>
      <div className="container mx-auto p-6">
        <Card>
          <h1>New Page</h1>
          {/* Page content */}
        </Card>
      </div>
    </AppLayout>
  );
};

export default NewPage;
```

**Step 2: Add Route (Frontend/src/App.tsx)**
```typescript
// App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import NewPage from './pages/NewPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/new-page" element={<NewPage />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}
```

**Step 3: Add Navigation Link (Frontend/src/components/Layout/Sidebar.tsx)**
```typescript
// Add to navigation items
const navItems = [
  { path: '/', label: 'Dashboard', icon: Home },
  { path: '/new-page', label: 'New Page', icon: FileText },
  // ...
];
```

### Modifying YOLO Detection Logic

**Location:** `Backend/app/services/road_services/AnalyzeOnRoadBase.py`

**Example: Add New Vehicle Class**
```python
class AnalyzeOnRoadBase:
    def __init__(self, ...):
        # Update class names
        self.classNames = ['Car', 'Motorcycle', 'Truck']  # Added Truck

        # Add counter
        self.count_truck = 0
        self.speed_truck = []

    def process_single_frame(self, frame_input):
        # ... existing code ...

        for track_id, cls in zip(ids, classes):
            if cls == 0:  # Car
                self.count_car += 1
                self.speed_car.append(speeds[track_id])
            elif cls == 1:  # Motorcycle
                self.count_motor += 1
                self.speed_motor.append(speeds[track_id])
            elif cls == 2:  # Truck (NEW)
                self.count_truck += 1
                self.speed_truck.append(speeds[track_id])

        # ... existing code ...
```

**Update API Response:**
```python
# api/v1/api_traffic.py
@router.get("/info/{road_name}")
async def get_traffic_info(road_name: str):
    data = state.get_data(road_name)
    return {
        "count_car": data.count_car,
        "count_motor": data.count_motor,
        "count_truck": data.count_truck,  # NEW
        "speed_car": data.avg_speed_car,
        "speed_motor": data.avg_speed_motor,
        "speed_truck": data.avg_speed_truck  # NEW
    }
```

**Update Frontend Interface:**
```typescript
// Update TrafficData interface
interface TrafficData {
  count_car: number;
  count_motor: number;
  count_truck: number;  // NEW
  speed_car: number;
  speed_motor: number;
  speed_truck: number;  // NEW
}

// Update display component
const TrafficStats = ({ data }: { data: TrafficData }) => (
  <div>
    <div>Cars: {data.count_car}</div>
    <div>Motorcycles: {data.count_motor}</div>
    <div>Trucks: {data.count_truck}</div>
  </div>
);
```

### Database Migrations

**Add New Column to Existing Table:**
```python
# Create migration script: migrations/add_column.py
from sqlalchemy import text
from app.db.base import engine

async def upgrade():
    async with engine.begin() as conn:
        await conn.execute(text("""
            ALTER TABLE traffic_violations
            ADD COLUMN severity VARCHAR(20) DEFAULT 'medium'
        """))

async def downgrade():
    async with engine.begin() as conn:
        await conn.execute(text("""
            ALTER TABLE traffic_violations
            DROP COLUMN severity
        """))

# Run migration
import asyncio
asyncio.run(upgrade())
```

**Update Model:**
```python
# models/traffic_violation.py
class TrafficViolation(Base):
    # ... existing columns ...
    severity = Column(String(20), default='medium')  # NEW
```

---

## Common Tasks & Examples

### Task: Add a New Violation Type

**1. Backend - Update Schema:**
```python
# schemas/violation.py
from typing import Literal

ViolationType = Literal[
    'red_light',
    'speeding',
    'wrong_lane',
    'illegal_parking'  # NEW
]

class ViolationCreate(BaseModel):
    violation_type: ViolationType
    # ... other fields
```

**2. Backend - Detection Logic:**
```python
# services/parking_detector.py
class ParkingViolationDetector:
    def __init__(self, no_parking_zones: List[dict]):
        self.zones = no_parking_zones
        self.model = YOLO(MODELS_PATH)

    def detect_violations(self, frame, track_data):
        violations = []
        boxes = track_data.xyxy.cpu().numpy()

        for box in boxes:
            x1, y1, x2, y2 = box
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            for zone in self.zones:
                if self.point_in_zone((center_x, center_y), zone):
                    violation = {
                        'camera_name': self.camera_name,
                        'violation_type': 'illegal_parking',
                        'position_x': int(center_x),
                        'position_y': int(center_y)
                    }
                    violations.append(violation)

        return violations

    def point_in_zone(self, point, zone):
        # Point-in-polygon algorithm
        pass
```

**3. Frontend - Update UI:**
```typescript
// Add icon mapping
const violationIcons = {
  red_light: AlertTriangle,
  speeding: Zap,
  wrong_lane: TrendingUp,
  illegal_parking: ParkingCircle  // NEW
};

// Add color mapping
const violationColors = {
  red_light: 'text-red-500',
  speeding: 'text-orange-500',
  wrong_lane: 'text-yellow-500',
  illegal_parking: 'text-purple-500'  // NEW
};
```

### Task: Export Data to Excel

**1. Backend - Install openpyxl:**
```bash
pip install openpyxl
```

**2. Backend - Create Export Endpoint:**
```python
# api/v1/api_reports.py
from fastapi import Response
from openpyxl import Workbook
from io import BytesIO

@router.get("/reports/export/excel")
async def export_excel(
    start_date: str,
    end_date: str,
    db: AsyncSession = Depends(get_db)
):
    # Fetch data
    query = select(TrafficViolation).filter(
        TrafficViolation.date >= start_date,
        TrafficViolation.date <= end_date
    )
    result = await db.execute(query)
    violations = result.scalars().all()

    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Violations"

    # Headers
    ws.append(['ID', 'Camera', 'Type', 'Vehicle', 'Time', 'Processed'])

    # Data rows
    for v in violations:
        ws.append([
            v.id,
            v.camera_name,
            v.violation_type,
            v.vehicle_type,
            str(v.violated_at),
            'Yes' if v.is_processed else 'No'
        ])

    # Save to bytes
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    # Return as download
    return Response(
        content=buffer.getvalue(),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': f'attachment; filename=violations_{start_date}_{end_date}.xlsx'
        }
    )
```

**3. Frontend - Download Handler:**
```typescript
// services/reportService.ts
export const downloadExcel = async (
  startDate: string,
  endDate: string
) => {
  const url = `${endpoints.base}/api/v1/reports/export/excel?start_date=${startDate}&end_date=${endDate}`;

  const response = await fetch(url);
  const blob = await response.blob();

  // Create download link
  const downloadUrl = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = downloadUrl;
  link.download = `violations_${startDate}_${endDate}.xlsx`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(downloadUrl);
};

// Usage in component
const handleExport = async () => {
  try {
    setExporting(true);
    await downloadExcel('2025-01-01', '2025-12-31');
    toast.success('Export completed');
  } catch (error) {
    toast.error('Export failed');
  } finally {
    setExporting(false);
  }
};
```

### Task: Add Real-time Notification

**1. Backend - WebSocket Notification Service:**
```python
# services/notification_service.py
from typing import Set
from fastapi import WebSocket

class NotificationManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

notification_manager = NotificationManager()

# api/v1/api_notifications.py
@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await notification_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_manager.disconnect(websocket)

# Trigger notification when violation detected
async def on_violation_detected(violation: dict):
    await notification_manager.broadcast({
        'type': 'new_violation',
        'data': violation
    })
```

**2. Frontend - Notification Hook:**
```typescript
// hooks/useNotifications.ts
import { useState, useEffect } from 'react';
import { toast } from 'sonner';

export const useNotifications = () => {
  const [notifications, setNotifications] = useState<any[]>([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/notifications');

    ws.onmessage = (event) => {
      const notification = JSON.parse(event.data);

      setNotifications(prev => [notification, ...prev]);

      // Show toast
      if (notification.type === 'new_violation') {
        toast.warning('New violation detected!', {
          description: `${notification.data.violation_type} at ${notification.data.camera_name}`
        });
      }
    };

    return () => ws.close();
  }, []);

  return { notifications };
};

// Usage
const Dashboard = () => {
  const { notifications } = useNotifications();

  return (
    <div>
      <NotificationBell count={notifications.length} />
    </div>
  );
};
```

---

## Testing & Quality Assurance

### Backend Testing

**Unit Tests (pytest):**
```python
# tests/test_violations.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_list_violations():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/violations/list")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_violation():
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "camera_name": "test_camera",
            "violation_type": "red_light",
            "vehicle_type": "car"
        }
        response = await client.post("/api/v1/violations/", json=payload)
        assert response.status_code == 200
        assert response.json()["camera_name"] == "test_camera"
```

**Run Tests:**
```bash
# Install pytest
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# With coverage
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
```

### Frontend Testing

**Component Tests (Vitest + React Testing Library):**
```typescript
// tests/TrafficDashboard.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import TrafficDashboard from '@/components/TrafficDashboard';

// Mock fetch
global.fetch = vi.fn();

describe('TrafficDashboard', () => {
  it('renders loading state', () => {
    render(<TrafficDashboard />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('fetches and displays traffic data', async () => {
    const mockData = {
      count_car: 10,
      count_motor: 5,
      speed_car: 30,
      speed_motor: 25
    };

    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData
    });

    render(<TrafficDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/10/)).toBeInTheDocument();
      expect(screen.getByText(/5/)).toBeInTheDocument();
    });
  });
});
```

**Run Tests:**
```bash
# Install dependencies
pnpm add -D vitest @testing-library/react @testing-library/jest-dom

# Run tests
pnpm run test

# With coverage
pnpm run test --coverage
```

### Manual Testing Checklist

**Backend API:**
- [ ] All endpoints return correct status codes
- [ ] Pydantic validation works (test invalid inputs)
- [ ] Database operations commit correctly
- [ ] WebSocket connections handle disconnects gracefully
- [ ] Authentication/authorization works correctly
- [ ] CORS headers allow frontend access

**Frontend UI:**
- [ ] All pages load without errors
- [ ] Forms validate inputs properly
- [ ] WebSocket connections auto-reconnect
- [ ] Loading states display correctly
- [ ] Error messages are user-friendly
- [ ] Responsive design works on mobile/tablet
- [ ] Dark/light theme switches properly

**Integration:**
- [ ] Video streaming works smoothly
- [ ] Real-time data updates correctly
- [ ] Chatbot responds to messages
- [ ] Violations are logged to database
- [ ] Notifications are sent (Telegram)
- [ ] Export functions generate correct files

---

## Deployment & Production

### Docker Deployment

**Build and Run:**
```bash
# Build both services
docker compose build

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

**Environment Variables:**
```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./app/traffic_monitor.db
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}

  frontend:
    environment:
      - VITE_API_HTTP_BASE=http://backend:8000
      - VITE_API_WS_BASE=ws://backend:8000
```

### Production Checklist

**Backend:**
- [ ] Set `DEBUG=false` in .env
- [ ] Use strong `JWT_SECRET_KEY` (generate with `openssl rand -hex 32`)
- [ ] Configure CORS to allow only production frontend URL
- [ ] Set up proper logging (file rotation)
- [ ] Use production ASGI server (Uvicorn with multiple workers)
- [ ] Enable HTTPS/SSL (reverse proxy like Nginx)
- [ ] Set up database backups
- [ ] Configure rate limiting
- [ ] Monitor CPU/RAM usage

**Frontend:**
- [ ] Build optimized production bundle (`pnpm run build`)
- [ ] Set correct API URLs in .env
- [ ] Enable compression (gzip/brotli)
- [ ] Set up CDN for static assets
- [ ] Configure caching headers
- [ ] Test on multiple browsers
- [ ] Optimize images
- [ ] Remove console.logs

**Security:**
- [ ] Change all default passwords
- [ ] Rotate API keys regularly
- [ ] Enable HTTPS everywhere
- [ ] Implement rate limiting
- [ ] Validate all inputs
- [ ] Sanitize database queries
- [ ] Use prepared statements
- [ ] Set secure cookie flags
- [ ] Implement CSRF protection

### Monitoring

**Backend Health Check:**
```python
# api/v1/api_health.py
@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Check database
        await db.execute(text("SELECT 1"))

        # Check video analyzer
        analyzer_status = "running" if analyzer.is_alive() else "stopped"

        return {
            "status": "healthy",
            "database": "connected",
            "analyzer": analyzer_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

**Logging:**
```python
# core/logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # File handler with rotation
    handler = RotatingFileHandler(
        "app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# Usage
logger = setup_logging()
logger.info("Application started")
logger.error("Error occurred", exc_info=True)
```

---

## Troubleshooting

### Common Backend Issues

**1. Port Already in Use:**
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

**2. Database Locked:**
```python
# SQLite doesn't support concurrent writes
# Solution: Use connection pooling
from sqlalchemy.pool import StaticPool

engine = create_async_engine(
    DATABASE_URL,
    poolclass=StaticPool,  # For SQLite
    echo=True
)
```

**3. YOLO Model Not Found:**
```bash
# Check model path
ls Backend/app/ai_models/model\ N/original\ model/best.pt

# If missing, download from Google Drive or retrain
```

**4. WebSocket Connection Failed:**
```python
# Check CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Common Frontend Issues

**1. Blank Page:**
```bash
# Check console for errors (F12)
# Common causes:
# - API endpoint incorrect
# - CORS blocked
# - JavaScript error

# Check network tab for failed requests
```

**2. WebSocket Not Connecting:**
```typescript
// Verify endpoint format
const ws = new WebSocket('ws://localhost:8000/ws/frames/Văn Phú');
// Not: http:// or wss://

// Check if backend is running
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log);
```

**3. Components Not Updating:**
```typescript
// Check if state is being set correctly
useEffect(() => {
  console.log('Data updated:', data);
}, [data]);

// Check if dependencies are correct
useEffect(() => {
  fetchData();
}, [dependency]);  // Make sure dependency is correct
```

**4. Build Errors:**
```bash
# Clear cache and rebuild
rm -rf node_modules
rm pnpm-lock.yaml
pnpm install
pnpm run build
```

### Performance Issues

**Backend Slow:**
```python
# Add database indexes
class TrafficViolation(Base):
    # ...
    camera_name = Column(String, index=True)  # Add index
    violated_at = Column(DateTime, index=True)

# Use connection pooling
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0
)

# Optimize queries
# Use .options(selectinload()) for eager loading
query = select(User).options(selectinload(User.violations))
```

**Frontend Slow:**
```typescript
// Use React.memo for expensive components
const VideoMonitor = React.memo(({ roadName, data }) => {
  // Component logic
});

// Debounce expensive operations
import { debounce } from 'lodash';

const debouncedSearch = debounce((query) => {
  performSearch(query);
}, 300);

// Virtualize long lists
import { useVirtualizer } from '@tanstack/react-virtual';
```

### Debugging Tips

**Backend:**
```python
# Add debug logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Processing frame: {frame.shape}")

# Use breakpoint()
def process_frame(frame):
    breakpoint()  # Drops into debugger
    # ... code

# Print request/response
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response: {response.status_code}")
    return response
```

**Frontend:**
```typescript
// Use React DevTools (browser extension)
// Inspect component props and state

// Add debug logs
useEffect(() => {
  console.log('Component mounted');
  console.log('Props:', { prop1, prop2 });
  return () => console.log('Component unmounted');
}, []);

// Use debugger
const handleClick = () => {
  debugger;  // Pauses execution
  processData();
};

// Monitor WebSocket messages
ws.onmessage = (event) => {
  console.log('WS Message:', event.data);
  // Process message
};
```

---

## Additional Resources

### Documentation
- **FastAPI:** https://fastapi.tiangolo.com/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **React:** https://react.dev/
- **TypeScript:** https://www.typescriptlang.org/docs/
- **Ultralytics YOLO:** https://docs.ultralytics.com/
- **shadcn/ui:** https://ui.shadcn.com/

### Internal Documentation
- `README.md` - User guide and installation
- `BAO_CAO_DU_AN.md` - Project report (Vietnamese)
- `HUONG_DAN_CAI_DAT.md` - Installation guide (Vietnamese)
- `HUONG_DAN_TEST.md` - Testing guide (Vietnamese)
- `CAU_TRUC_DU_AN.md` - Project structure (Vietnamese)

### AI Assistant Guidelines

When working with this codebase as an AI assistant:

1. **Read Before Modifying:** Always read existing files before suggesting changes
2. **Follow Patterns:** Maintain existing code patterns and conventions
3. **Type Safety:** Ensure TypeScript types are correct and Pydantic schemas match
4. **Test Changes:** Suggest testing strategies for new features
5. **Document Code:** Add docstrings to complex functions
6. **Security First:** Never expose secrets or create SQL injection vulnerabilities
7. **Error Handling:** Always include proper error handling and validation
8. **Async Patterns:** Use async/await correctly in both backend and frontend
9. **State Management:** Follow React hooks patterns for state
10. **Database Queries:** Use SQLAlchemy properly with async sessions

### Quick Reference Commands

```bash
# Backend
cd Backend/app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd Frontend
pnpm run dev

# Docker
docker compose up -d
docker compose logs -f backend
docker compose logs -f frontend

# Database
sqlite3 Backend/app/traffic_monitor.db
.tables
.schema traffic_violations
SELECT * FROM traffic_violations LIMIT 10;

# Git
git status
git add .
git commit -m "feat: add new feature"
git push origin main
```

---

**End of CLAUDE.md**

*This guide should be updated whenever significant architectural changes are made to the codebase.*
