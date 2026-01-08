# 📚 CÂU HỎI ÔN TẬP BẢO VỆ ĐỀ TÀI KHKT

## 📌 THÔNG TIN ĐỀ TÀI
- **Tên đề tài**: Hệ Thống Giám Sát Giao Thông Thông Minh Sử Dụng AI
- **Sinh viên thực hiện**: Đoàn Bá Trí
- **Công nghệ chính**: YOLO v11, ByteTrack, FastAPI, React, Google Gemini

---

# PHẦN A: TRẢ LỜI 24 CÂU HỎI (BẢN TÓM TẮT)

## Câu 1: Rà soát lỗi báo cáo (hình thức + nội dung)

**Lỗi hình thức:**
- Một số tiêu đề thiếu dấu chấm cuối câu
- Bảng thống kê cần căn giữa tiêu đề cột
- Biểu đồ cần xoay trục X 45 độ để tránh chồng chéo

**Lỗi nội dung:**
- Thiếu giải thích ý nghĩa các chỉ số thống kê
- Chưa có phần khuyến nghị dựa trên dữ liệu
- Cần bổ sung đánh giá hiệu quả hệ thống

---

## Câu 2: Nhiệm vụ đề tài làm gì?

Đề tài có **5 nhiệm vụ chính**:

1. **Giám sát giao thông real-time**: Phát hiện và đếm phương tiện (ô tô, xe máy), tính toán tốc độ, hỗ trợ 5 tuyến đường

2. **Phân tích dữ liệu**: Xác định giờ cao/thấp điểm, phân tích xu hướng lưu lượng, so sánh mật độ giao thông

3. **Cảnh báo tình trạng giao thông**: Phân loại Thông thoáng/Đông đúc/Tắc nghẽn, gửi cảnh báo qua Telegram Bot

4. **Lưu trữ và báo cáo**: Lưu vào SQLite, tạo báo cáo theo ngày/tuần/tháng, export CSV/JSON/PDF

5. **Hỗ trợ ra quyết định**: Chatbot AI tư vấn tuyến đường tối ưu

---

## Câu 3: Hệ thống có những chức năng nào?

Hệ thống có **10 chức năng chính**:

| STT | Chức năng | Mô tả |
|-----|-----------|-------|
| 1 | Video Streaming | WebSocket streaming 15-30 FPS, hiển thị bounding boxes |
| 2 | Đếm phương tiện | Đếm ô tô (car, truck, bus), xe máy |
| 3 | Tính toán tốc độ | Speed = Distance / Time, đơn vị km/h |
| 4 | Phân tích giờ cao điểm | Tự động phát hiện giờ đông nhất trong ngày |
| 5 | Xu hướng theo thời gian | Area Chart, Line Chart, Daily trends |
| 6 | So sánh tuyến đường | Bar Chart so sánh 5 tuyến đường |
| 7 | Tạo báo cáo tự động | Báo cáo ngày/tuần/tháng, export đa định dạng |
| 8 | AI Chatbot | Google Gemini trả lời câu hỏi về traffic |
| 9 | Telegram Bot | Cảnh báo real-time, báo cáo hàng ngày |
| 10 | Authentication | Đăng nhập/Đăng ký, JWT token |

---

## Câu 4: Đề tài viết mới hay kế thừa?

**Tính chất**: Đề tài có **tính kế thừa và phát triển** (40% kế thừa, 60% phát triển mới)

**Phần kế thừa (40%):**
- Mô hình AI: YOLO v11 (Ultralytics), ByteTrack, OpenVINO
- Framework: FastAPI, React, SQLAlchemy

**Phần phát triển mới (60%):**
- Kiến trúc multiprocessing: Xử lý 5 tuyến đường song song
- Real-time Analytics Dashboard với 4 loại biểu đồ
- AI Chatbot Integration (Google Gemini)
- Telegram Bot Notification
- UI/UX hiện đại với dark theme, glass morphism

**So sánh với đề tài cũ:**
| Tiêu chí | Đề tài cũ | Đề tài của em |
|----------|-----------|---------------|
| Số tuyến đường | 1-2 | 5 (song song) |
| Real-time | Batch processing | WebSocket streaming |
| AI Assistant | Không | Gemini chatbot |
| Performance | CPU only | OpenVINO + FP16 |

---

## Câu 5: Kiến thức quan trọng nhất trong đề tài?

**5 kiến thức quan trọng:**

1. **Computer Vision & Deep Learning (40%)**
   - YOLO: CNN-based object detection
   - ByteTrack: Object tracking với Kalman Filter
   - Transfer Learning: Fine-tune trên custom dataset

2. **Backend Development (25%)**
   - FastAPI: Async/await programming
   - WebSocket: Full-duplex communication
   - Database: SQL, ORM, indexing

3. **Frontend Development (20%)**
   - React Hooks (useState, useEffect)
   - Data Visualization với Recharts
   - State Management

4. **Multiprocessing (10%)**
   - Python Multiprocessing
   - Thread Safety, Queue for IPC

5. **Performance Optimization (5%)**
   - OpenVINO, INT8 quantization
   - Caching Strategies

---

## Câu 6: Thuật toán YOLO v11 là gì? Chức năng?

**⚠️ Lưu ý**: Đề tài sử dụng **YOLO v11**, phiên bản mới nhất 2024

**Định nghĩa:**
YOLO (You Only Look Once) là thuật toán phát hiện đối tượng (object detection) sử dụng Deep Learning. Phiên bản 11 phát triển bởi Ultralytics (10/2024).

**Kiến trúc:**
```
Input Image (640x640)
        ↓
   BACKBONE (CSPDarknet) ← Feature Extraction
        ↓
   NECK (PANet) ← Multi-scale Features
        ↓
   HEAD (Detect) ← Predictions
        ↓
Output: [x, y, w, h, confidence, class]
```

**Chức năng trong đề tài:**
- Phát hiện phương tiện (car, motorcycle, bus, truck)
- Tốc độ: ~200 FPS (YOLO v11n trên GPU)
- Độ chính xác: >90% mAP

**Tại sao chọn YOLO?**
- One-stage detector → Nhanh
- End-to-end training → Đơn giản
- Open source + Active community

---

## Câu 7: Thuật toán ByteTrack là gì? Chức năng?

**Định nghĩa:**
ByteTrack là thuật toán **Multi-Object Tracking (MOT)** - theo dõi nhiều đối tượng qua video, phát triển năm 2021 bởi ByteDance.

**Mục đích:** Gán **ID duy nhất** cho mỗi xe, theo dõi xe qua nhiều frames

**Vấn đề giải quyết:**
```
Không tracking:
Frame 1: 3 xe → Tổng 3
Frame 2: 3 xe → Tổng 6
Frame 3: 4 xe → Tổng 10 ❌

Có tracking:
Frame 1: Xe A, B, C
Frame 2: Xe A, B, C (same IDs)
Frame 3: Xe A, B, C, D
→ Tổng = 4 xe ✅
```

**Thuật toán:**
1. **Kalman Filter**: Dự đoán vị trí xe ở frame tiếp theo
2. **IoU Matching**: Tính độ overlap giữa predicted và detected boxes
3. **Hungarian Algorithm**: Optimal assignment

**Chức năng trong đề tài:**
- Đếm xe chính xác (không đếm trùng)
- Tính tốc độ dựa trên trajectory
- Phát hiện vi phạm

---

## Câu 8: Hệ thống cần lắp đặt ở đâu?

Hệ thống lắp đặt ở **3 vị trí chính**:

**1. Camera giám sát:**
- Vị trí: Giao lộ đèn đỏ, đầu đường cao tốc, khu vực hay tắc nghẽn
- Chiều cao: 4-6m
- Góc nhìn: 30-45°
- Yêu cầu: ≥1080p, ≥25fps, IP Camera RTSP, IP66/IP67

**2. Server xử lý:**
- Option 1: On-premise (trụ sở CSGT) - CPU Xeon, RAM 32GB+, GPU NVIDIA T4
- Option 2: Edge Computing (gần camera) - NVIDIA Jetson Orin
- Option 3: Cloud Server (AWS, GCP)

**3. Trạm giám sát:**
- Vị trí: Phòng điều hành CSGT, Sở GTVT
- Thiết bị: PC i5, 8GB RAM, màn hình 24-27 inch

**Chi phí ước tính:**
- 1 điểm giám sát: ~6 triệu VNĐ
- Hệ thống 5 cameras: ~200 triệu VNĐ
- Vận hành: ~7 triệu VNĐ/tháng

---

## Câu 9: Phương án lưu trữ dữ liệu lâu dài?

**4 phương án:**

| Phương án | Chi phí/năm | Dung lượng | Độ phức tạp |
|-----------|-------------|------------|-------------|
| 1. Tiered Storage | 53 triệu | ~30TB | Trung bình |
| 2. Smart Compression | 6.6 triệu | 241GB | Thấp |
| 3. Database only | 300k | 37.5GB | Cao |
| 4. Hybrid | 10 triệu | ~5TB | Cao |

**Khuyến nghị:**
- **Cho KHKT (quy mô nhỏ)**: Phương án 2 - Smart Compression
- **Cho thực tế (quy mô lớn)**: Phương án 4 - Hybrid

**Chi tiết Phương án 2:**
- Chỉ lưu frames có xe (~30% thời gian)
- Metadata JSON + Thumbnails
- Tiết kiệm 163× so với lưu full video

---

## Câu 10-11: Bộ dữ liệu huấn luyện và nguồn gốc?

Đề tài sử dụng **3 bộ dữ liệu**:

**1. COCO Dataset (Pre-training)** - ĐÃ CÓ SẴN
- Nguồn: Microsoft COCO
- Kích thước: 330K images, 1.5M instances
- Classes: 80 classes (có car, motorcycle, bus, truck)

**2. Custom Vietnam Traffic Dataset (Fine-tuning)** - TỰ THU THẬP
- Kích thước: 10,000 images (sau augmentation)
- Classes: 4 (car, motorcycle, truck, bus)
- Distribution: car 56%, motorcycle 35%, truck 6%, bus 3%

**3. Test Videos** - LẤY TỪ YOUTUBE/CAMERA
- 5 videos x 30 phút = 150 phút, 6.2GB
- Tuyến đường: Văn Phú, Văn Quán, Nguyễn Trãi, Ngã Tư Sở, Đường Láng

---

## Câu 12: Tại sao không demo với dữ liệu nơi sinh sống?

**Lý do chọn dữ liệu Hà Nội:**

1. **Đa dạng tình huống**: Hà Nội có mật độ xe cao, nhiều loại xe, nhiều giao lộ phức tạp → Thử nghiệm toàn diện hơn

2. **Dữ liệu sẵn có**: Camera giao thông công cộng Hà Nội có chất lượng tốt, dễ truy cập qua YouTube

3. **Tính đại diện**: Hà Nội đại diện cho giao thông đô thị lớn tại Việt Nam

4. **Hạn chế thực tế**: 
   - Quảng Nam/nơi sinh sống: Camera ít, chất lượng thấp
   - Việc lắp camera riêng cần xin phép, chi phí cao

**Kế hoạch tương lai**: Khi triển khai thực tế, sẽ thu thập và test với dữ liệu địa phương

---

## Câu 13: Sơ đồ hoạt động của hệ thống

```
┌─────────────────────────────────────────────────────────────────┐
│                    SƠ ĐỒ HOẠT ĐỘNG HỆ THỐNG                     │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │  1. CAMERA      │  ← Video từ 5 tuyến đường
    │  (Video Input)  │
    └────────┬────────┘
             │ Video Stream
             ▼
    ┌─────────────────┐
    │ 2. AI DETECTION │  ← YOLO v11 phát hiện xe
    │    (YOLO v11)   │    ByteTrack gán track ID
    │                 │    Speed Calculation
    └────────┬────────┘
             │ Detection Results
             ▼
    ┌─────────────────┐
    │  3. BACKEND     │  ← FastAPI xử lý logic
    │    (FastAPI)    │    SQLite lưu trữ
    │                 │    WebSocket streaming
    └────────┬────────┘
             │ HTTP/WebSocket
             ▼
    ┌─────────────────┐
    │  4. FRONTEND    │  ← React hiển thị
    │    (React)      │    4 tabs: Monitor, Analytics,
    │                 │    Reports, Chatbot
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 5. OUTPUT       │
    │  - Dashboard    │  ← Hiển thị theo dõi real-time
    │  - Telegram Bot │  ← Cảnh báo tắc nghẽn
    │  - AI Chatbot   │  ← Tư vấn giao thông
    │  - Export Data  │  ← CSV, JSON, PDF
    └─────────────────┘
```

---

## Câu 14: Hệ thống viết bằng ngôn ngữ gì?

| Thành phần | Ngôn ngữ/Framework | Phiên bản |
|------------|-------------------|-----------|
| **Backend** | Python + FastAPI | Python 3.12, FastAPI 0.115 |
| **Frontend** | TypeScript + React | React 19.2, TypeScript 5.6, Vite 7.0 |
| **AI/ML** | Python + YOLO | Ultralytics 8.3, yolo11n.pt |
| **Database** | SQLite + SQLAlchemy | SQLAlchemy 2.0 |
| **Chatbot** | Google Gemini | gemini-2.5-flash |
| **Chart** | Recharts | Recharts 2.15 |
| **Styling** | TailwindCSS | TailwindCSS 3.4 |

---

## Câu 15: Làm thế nào tích hợp camera thực tế?

**Các bước tích hợp camera RTSP:**

**Bước 1: Cấu hình camera**
- Bật chức năng RTSP trên camera
- Lấy URL RTSP (ví dụ: `rtsp://admin:password@192.168.1.100:554/stream`)

**Bước 2: Cập nhật file cấu hình**
```python
# Backend/app/config/cameras.py
CAMERA_SOURCES = {
    "van_phu": "rtsp://admin:123456@192.168.1.10:554/stream1",
    "van_quan": "rtsp://admin:123456@192.168.1.11:554/stream1",
    # ... thêm camera khác
}
```

**Bước 3: Sử dụng OpenCV đọc stream**
```python
cap = cv2.VideoCapture("rtsp://...")
while True:
    ret, frame = cap.read()
    if ret:
        # Xử lý frame
        detections = yolo.detect(frame)
```

**Lưu ý:**
- Camera phải chung mạng LAN hoặc có IP tĩnh
- Đảm bảo bandwidth đủ (2-4 Mbps/camera)
- Cần UPS để tránh mất điện

---

## Câu 16: Tại sao dùng Telegram thay vì Zalo/Messenger/Gmail?

| Tiêu chí | Telegram | Zalo | Messenger | Gmail |
|----------|----------|------|-----------|-------|
| **Bot API** | ✅ Miễn phí, dễ dùng | ❌ Phải đăng ký OA | ❌ Khó approve | ✅ Có API |
| **Rate limit** | 30 msg/s | 500 msg/ngày | 200 msg/ngày | 500 email/ngày |
| **Media** | ✅ Ảnh, video, file | ⚠️ Hạn chế | ⚠️ Hạn chế | ✅ Attachment |
| **Realtime** | ✅ Instant | ⚠️ Delay | ⚠️ Delay | ❌ Không realtime |
| **Đọc lại** | ✅ Dễ dàng | ✅ OK | ✅ OK | ⚠️ Khó search |
| **Miễn phí** | ✅ 100% | ⚠️ Có phí OA | ⚠️ Có phí | ✅ Miễn phí |

**Kết luận**: Telegram là lựa chọn tốt nhất vì:
- Bot API miễn phí, không giới hạn
- Gửi tin nhắn instant, hỗ trợ ảnh/video
- Dễ lập trình, nhiều tài liệu
- Không cần đăng ký doanh nghiệp

---

## Câu 17: Dạng microservice là gì?

**Định nghĩa:**
Microservice là kiến trúc chia ứng dụng thành nhiều **service độc lập**, mỗi service xử lý một chức năng cụ thể.

**So sánh:**
```
Monolithic (1 khối):           Microservice (nhiều service):
┌─────────────────┐            ┌─────────┐  ┌─────────┐
│   Backend       │            │ Auth    │  │ Video   │
│   - Auth        │     VS     │ Service │  │ Service │
│   - Video       │            └────┬────┘  └────┬────┘
│   - DB          │                 │            │
└─────────────────┘            ┌────▼────────────▼────┐
                               │      API Gateway     │
                               └──────────────────────┘
```

**Ưu điểm:**
- Dễ scale (tăng số lượng service cần thiết)
- Dễ bảo trì (sửa 1 service không ảnh hưởng service khác)
- Công nghệ linh hoạt (mỗi service có thể dùng ngôn ngữ khác nhau)

**Trong đề tài này**: Đề tài sử dụng kiến trúc **microservice-ready** (Backend và Frontend tách biệt)

---

## Câu 18: Dạng streaming (Kafka, MQTT) là gì?

**Định nghĩa:**
Streaming là phương thức truyền dữ liệu **liên tục, real-time** giữa các thành phần hệ thống.

**Các công nghệ streaming:**

| Công nghệ | Mô tả | Use case |
|-----------|-------|----------|
| **Kafka** | Message broker phân tán | Big data, log processing |
| **MQTT** | Protocol nhẹ cho IoT | Sensor, thiết bị nhúng |
| **WebSocket** | Full-duplex qua HTTP | Web real-time |
| **RabbitMQ** | Message queue đơn giản | Task queue |

**Trong đề tài này:**
- Sử dụng **WebSocket** cho video streaming
- Có thể upgrade lên **Kafka** khi scale lớn (100+ cameras)

**Ví dụ Kafka:**
```
Camera → Kafka Topic → Consumer → YOLO → Kafka Topic → Dashboard
                ↑                                  ↓
        (video_frames)                     (detection_results)
```

---

## Câu 19: Công nghệ blockchain là gì?

**Định nghĩa:**
Blockchain là công nghệ lưu trữ dữ liệu phân tán, **không thể sửa đổi** (immutable), được xác thực bởi nhiều node.

**Đặc điểm:**
- Phân tán: Dữ liệu lưu ở nhiều máy
- Bất biến: Không thể sửa dữ liệu đã ghi
- Minh bạch: Mọi người có thể xác thực

**Ứng dụng cho giao thông:**
1. **Lưu trữ vi phạm không thể sửa đổi** - Bằng chứng pháp lý
2. **Smart Contract tự động phạt** - Khi phát hiện vi phạm → Tự động trừ tiền
3. **Chia sẻ dữ liệu giữa các cơ quan** - Minh bạch, không giả mạo

**Trong đề tài hiện tại**: Chưa áp dụng blockchain, nhưng có thể là hướng phát triển tương lai

---

## Câu 20: Chi phí 2-5 triệu đồng/điểm - còn chi phí lắp đặt?

**Chi phí ước tính đầy đủ:**

**1 điểm giám sát (1 camera):**
| Hạng mục | Chi phí |
|----------|---------|
| Camera IP 1080p | 2,500,000 VNĐ |
| Bracket + mount | 300,000 VNĐ |
| Cáp mạng Cat6 (50m) | 500,000 VNĐ |
| Switch POE | 1,200,000 VNĐ |
| Nguồn điện + UPS | 800,000 VNĐ |
| Vật tư | 200,000 VNĐ |
| **Nhân công lắp đặt** | **500,000 VNĐ** |
| **TỔNG** | **~6,000,000 VNĐ** |

**Hệ thống 5 cameras:**
| Hạng mục | Chi phí |
|----------|---------|
| 5× Camera setup | 30,000,000 VNĐ |
| Server | 80,000,000 VNĐ |
| GPU (NVIDIA T4) | 25,000,000 VNĐ |
| Storage (4TB SSD) | 12,000,000 VNĐ |
| Networking | 10,000,000 VNĐ |
| **Lắp đặt + Training** | **15,000,000 VNĐ** |
| **TỔNG** | **~200,000,000 VNĐ** |

**Chi phí vận hành (tháng):**
- Điện: 3 triệu
- Internet: 1 triệu
- Bảo trì: 2 triệu
- **Tổng: ~7 triệu/tháng**

---

## Câu 21: Đề tài thực hiện được gì?

**Kết quả đạt được:**

✅ **Về mặt kỹ thuật:**
- Xây dựng thành công hệ thống 5 layers
- Tích hợp YOLO v11 + ByteTrack + Speed Calculation
- Backend FastAPI với REST API + WebSocket
- Frontend React với 4 tabs chức năng
- AI Chatbot Google Gemini
- Database SQLite

✅ **Hiệu suất:**
| Chỉ tiêu | Mục tiêu | Kết quả |
|----------|----------|---------|
| Độ chính xác | ≥90% | 90-95% ✅ |
| Tốc độ xử lý | ≥15 FPS | 20 FPS ✅ |
| Thời gian/frame | <100ms | 50ms ✅ |
| Số tuyến | ≥3 | 5 ✅ |
| Chi phí | <10 triệu | 5-10 triệu ✅ |

✅ **So sánh với thương mại:**
- Đạt 90-95% hiệu quả
- Chi phí chỉ **10%** (5-10 triệu vs 50-100 triệu)
- Có AI Chatbot (thương mại không có)
- Mã nguồn mở

---

## Câu 22: Tồn tại của đề tài là gì?

**Các hạn chế:**

1. **Về độ chính xác:**
   - Thấp hơn 3-5% so với giải pháp thương mại
   - Khó phát hiện xe rất nhỏ (<32px)
   - Có thể nhầm lẫn xe gần nhau

2. **Về chức năng:**
   - Chưa có OCR nhận diện biển số
   - Chưa phát hiện vi phạm vượt đèn đỏ, làn đường
   - Chưa dự đoán ùn tắc

3. **Về điều kiện:**
   - Chưa test kỹ ban đêm
   - Chưa test điều kiện mưa, sương mù
   - Chỉ test với video, chưa test camera thực tế

4. **Về quy mô:**
   - Hiện chỉ hỗ trợ 5 tuyến đường
   - Database SQLite không phù hợp cho quy mô lớn

---

## Câu 23: Hướng phát triển đề tài?

**Ngắn hạn (3-6 tháng):**

1. **OCR nhận diện biển số xe**
   - Công nghệ: PaddleOCR hoặc EasyOCR
   - Biện pháp: Fine-tune model với biển số Việt Nam
   - Dự kiến: Độ chính xác > 85%

2. **Nâng cấp database**
   - Chuyển từ SQLite → PostgreSQL
   - Thêm partitioning theo thời gian

**Trung hạn (6-12 tháng):**

3. **Phát hiện mũ bảo hiểm**
   - Công nghệ: YOLO v11 + custom dataset
   - Quy trình: Thu thập 5,000 ảnh, label, train
   - Ứng dụng: Phát hiện người không đội mũ

4. **Phát hiện quá tốc độ**
   - Công nghệ: Speed calculation + threshold
   - Kết hợp GPS mapping để xác định tốc độ giới hạn

5. **Phát hiện sai làn đường**
   - Công nghệ: Lane detection + YOLO
   - Dùng thuật toán Hough Transform hoặc Deep Learning

**Dài hạn (1-2 năm):**

6. **Dự đoán ùn tắc bằng AI**
   - Công nghệ: LSTM/Transformer
   - Dữ liệu: Lịch sử lưu lượng theo giờ, ngày, thời tiết

7. **Mobile App**
   - Công nghệ: React Native
   - Chức năng: Xem traffic, nhận cảnh báo, chat AI

8. **Tích hợp Smart City**
   - Kết nối với đèn giao thông thông minh
   - Điều chỉnh tín hiệu đèn tự động

---

## Câu 24: Bài thuyết trình 3 phút + Demo 3 phút

*(Xem phần B bên dưới)*

---

# PHẦN B: BÀI THUYẾT TRÌNH 3 PHÚT

## 🎤 KỊCH BẢN THUYẾT TRÌNH (3 phút)

### Phút 1: Giới thiệu vấn đề và giải pháp (60 giây)

> "Kính thưa quý thầy cô và các bạn,
>
> Em tên là Đoàn Bá Trí, em xin trình bày đề tài: **Hệ thống giám sát giao thông thông minh sử dụng trí tuệ nhân tạo**.
>
> **[SLIDE VẤN ĐỀ]**
> Theo Ủy ban An toàn giao thông Quốc gia, 10 tháng đầu năm 2025, cả nước xảy ra hơn 15,000 vụ tai nạn giao thông, làm chết hơn 8,500 người. Một trong những nguyên nhân chính là **thiếu hệ thống giám sát thông minh** - các camera hiện nay chỉ ghi hình, chưa có khả năng phân tích tự động.
>
> **[SLIDE GIẢI PHÁP]**
> Để giải quyết vấn đề này, em đã xây dựng hệ thống sử dụng **YOLO v11** để phát hiện xe, **ByteTrack** để theo dõi xe, và **AI Chatbot** để tư vấn giao thông - với chi phí chỉ **5-10 triệu đồng**, thấp hơn 90% so với giải pháp thương mại."

### Phút 2: Giới thiệu kết quả (60 giây)

> **[SLIDE KẾT QUẢ]**
> "Hệ thống đạt được các kết quả sau:
>
> - **Độ chính xác 90-95%** trong phát hiện xe
> - **Tốc độ xử lý 20 FPS** - đủ cho giám sát real-time
> - Hỗ trợ **5 tuyến đường đồng thời**
>
> **[SLIDE CHỨC NĂNG]**
> Hệ thống có 4 chức năng chính:
> 1. **Tab Giám sát**: Stream video real-time, hiển thị bounding boxes quanh xe
> 2. **Tab Phân tích**: Biểu đồ giờ cao điểm, xu hướng lưu lượng
> 3. **Tab Báo cáo**: Export dữ liệu CSV, JSON
> 4. **Tab Chatbot**: AI tư vấn tuyến đường tối ưu
>
> Ngoài ra còn có **Telegram Bot** gửi cảnh báo khi phát hiện tắc nghẽn."

### Phút 3: Kết luận và hướng phát triển (60 giây)

> **[SLIDE KẾT LUẬN]**
> "Tổng kết, đề tài đã hoàn thành các mục tiêu đề ra:
> ✅ Giám sát giao thông real-time
> ✅ Phân tích dữ liệu tự động
> ✅ Chi phí thấp, hiệu quả cao
>
> **[SLIDE HƯỚNG PHÁT TRIỂN]**
> Trong tương lai, em dự định phát triển thêm:
> - **Nhận diện biển số xe** bằng OCR
> - **Phát hiện vi phạm** vượt đèn đỏ, quá tốc độ
> - **Dự đoán ùn tắc** bằng Deep Learning
>
> Em xin cảm ơn thầy cô và các bạn đã lắng nghe. Em xin được chuyển sang phần demo."

---

# PHẦN C: DEMO 3 PHÚT

## 🖥️ KỊCH BẢN DEMO (3 phút)

### Bước 1: Giới thiệu giao diện (30 giây)

> "Đây là giao diện chính của hệ thống với 4 tabs. Em sẽ demo từng phần."

**Thao tác:**
- Mở trình duyệt → http://localhost:5173
- Đăng nhập với tài khoản demo

### Bước 2: Demo Tab Giám sát (60 giây)

> "Tab Giám sát cho phép xem video real-time từ 5 tuyến đường."

**Thao tác:**
- Click vào camera "Văn Phú"
- Chỉ vào bounding boxes: "Đây là các xe được YOLO phát hiện"
- Chỉ vào track ID: "Mỗi xe có ID riêng nhờ ByteTrack"
- Chỉ vào tốc độ: "Tốc độ trung bình được tính tự động"
- Chỉ vào trạng thái: "Hệ thống tự phân loại Thông thoáng/Đông đúc/Tắc nghẽn"

### Bước 3: Demo Tab Phân tích (45 giây)

> "Tab Phân tích hiển thị biểu đồ thống kê"

**Thao tác:**
- Click tab "Phân tích"
- Chỉ Area Chart: "Biểu đồ này hiển thị xu hướng lưu lượng theo 24 giờ"
- Chỉ Peak Hour: "Giờ cao điểm là 17:00-18:00 với 1,234 lượt xe"
- Chỉ Bar Chart: "So sánh 5 tuyến đường - Ngã Tư Sở đông nhất"

### Bước 4: Demo Tab Báo cáo (30 giây)

> "Tab Báo cáo cho phép export dữ liệu"

**Thao tác:**
- Click tab "Báo cáo"
- Chọn khoảng thời gian
- Click "Export CSV" → File được tải về
- Mở file CSV để show dữ liệu

### Bước 5: Demo AI Chatbot (45 giây)

> "Cuối cùng là Tab Chatbot - AI tư vấn giao thông"

**Thao tác:**
- Click tab "Chatbot"
- Gõ: "Tuyến đường nào đang thông thoáng nhất?"
- Đợi AI trả lời
- Gõ: "Giờ cao điểm hôm nay là mấy giờ?"
- Đợi AI trả lời với dữ liệu thực

### Kết thúc (10 giây)

> "Đó là toàn bộ demo của em. Em xin cảm ơn và sẵn sàng trả lời câu hỏi từ quý thầy cô."

---

# PHẦN D: CÂU HỎI THƯỜNG GẶP

## Q1: YOLO là gì?
**A:** YOLO (You Only Look Once) là thuật toán phát hiện đối tượng sử dụng Deep Learning, có thể phát hiện và phân loại nhiều đối tượng trong một lần xử lý ảnh.

## Q2: ByteTrack khác YOLO thế nào?
**A:** YOLO chỉ phát hiện xe trong 1 frame. ByteTrack theo dõi xe qua nhiều frames, gán ID duy nhất để đếm chính xác và tính tốc độ.

## Q3: Tại sao dùng Python?
**A:** Python có nhiều thư viện AI/ML (YOLO, OpenCV, NumPy), FastAPI hiệu suất cao, cộng đồng lớn, dễ học.

## Q4: Chi phí thực tế bao nhiêu?
**A:** Phần mềm: 0 đồng (mã nguồn mở). Phần cứng 1 camera: ~6 triệu. Hệ thống 5 cameras: ~200 triệu.

## Q5: Có thể dùng camera điện thoại không?
**A:** Có, nhưng cần chuyển stream qua RTSP. Khuyến nghị dùng IP Camera chuyên dụng cho chất lượng và độ ổn định.

---

**HẾT**

*Tài liệu này được tạo để hỗ trợ ôn tập bảo vệ đề tài KHKT*
