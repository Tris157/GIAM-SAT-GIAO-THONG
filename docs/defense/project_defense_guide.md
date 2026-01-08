# Hướng Dẫn Bảo Vệ Dự Án: Smart Traffic Monitoring System

Tài liệu này tổng hợp chi tiết về kiến trúc, chức năng và cơ chế hoạt động của hệ thống để bạn chuẩn bị cho buổi bảo vệ đồ án.

## 1. Tổng Quan Dự Án

### Tên Đề Tài
Hệ thống giám sát và phân tích giao thông thông minh (Smart Traffic Monitoring System).

### Mục Tiêu
Xây dựng hệ thống Real-time (thời gian thực) để:
1.  **Đếm lưu lượng phương tiện**: Ô tô, xe máy.
2.  **Đo tốc độ trung bình**: Cảnh báo tắc nghẽn.
3.  **Phát hiện vi phạm**: Vượt đèn đỏ, chạy quá tốc độ (đang phát triển).
4.  **Phân tích & Báo cáo**: Xu hướng giao thông theo giờ/ngày.
5.  **Trợ lý AI**: Chatbot hỗ trợ tra cứu thông tin giao thông.

### Công Nghệ Cốt Lõi (Tech Stack)

| Thành Phần | Công Nghệ | Lý Do Sử Dụng |
| :--- | :--- | :--- |
| **AI Model** | YOLOv8 + OpenVINO | YOLOv8 cho độ chính xác cao. OpenVINO giúp tối ưu chạy nhanh trên CPU (INT8 quantization). |
| **Tracking** | ByteTrack | Thuật toán tracking mạnh mẽ, giúp theo dõi xe qua nhiều frame mà không bị mất ID. |
| **Backend** | FastAPI (Python) | Hiệu năng cao (Async), hỗ trợ WebSocket tốt cho streaming video. |
| **Frontend** | React + TypeScript | Giao diện hiện đại, SPA (Single Page Application) mượt mà. |
| **Database** | SQLite + SQLAlchemy | Nhẹ, dễ triển khai deployment, đủ dùng cho ứng dụng vừa và nhỏ. |
| **Real-time** | WebSockets | Truyền tải frame video và data liên tục mà không cần reload trang. |

---

## 2. Chi Tiết Kỹ Thuật (Deep Dive)

Đây là phần quan trọng để trả lời các câu hỏi chuyên sâu của hội đồng.

### A. Luồng Xử Lý AI (`AnalyzeOnRoadBase.py`)

Quy trình xử lý 1 frame hình ảnh diễn ra như sau:

1.  **Input**: Đọc frame từ Video hoặc RTSP Stream (OpenCV).
2.  **Preprocessing**: Resize ảnh về kích thước chuẩn (600x400) để tối ưu tốc độ.
3.  **Inference (Dự đoán)**:
    *   Sử dụng `YOLO` model để phát hiện bounding box (vị trí xe) và class (loại xe).
    *   OpenVINO giúp tăng tốc độ xử lý (FPS) lên 2-3 lần so với PyTorch thuần trên CPU.
4.  **Tracking (Theo dõi)**:
    *   Sử dụng `ByteTrack` để gán ID duy nhất cho từng xe.
    *   Giúp hệ thống hiểu "xe A ở frame 1" và "xe A ở frame 2" là cùng một xe.
5.  **Speed Estimation (Tính tốc độ)**:
    *   Dựa trên sự di chuyển của tâm (centroid) bounding box qua các frame.
    *   Công thức: $V = \frac{\Delta d}{\Delta t} \times scale$
    *   Trong đó `scale` (`meter_per_pixel`) là hệ số quy đổi từ pixel sang mét thực tế (được cấu hình riêng cho từng cam).
6.  **Violation Detection (Phát hiện vi phạm)**:
    *   **Vượt đèn đỏ**: Kiểm tra tọa độ xe ($y > stop\_line$) khi đèn tín hiệu (được crop theo ROI) đang màu đỏ.
    *   **Logic**: Class `SpeedViolationDetector` (tên hơi lạ nhưng xử lý cả đèn đỏ) check trạng thái đèn và vị trí xe.

### B. Kiến Trúc Backend (FastAPI)

Hệ thống sử dụng **Multiprocessing** (Đa tiến trình) để xử lý nhiều camera cùng lúc:
*   Mỗi Camera chạy trên một Process riêng biệt (tránh bị block bởi GIL của Python).
*   Giao tiếp giữa các Process thông qua `Manager().dict()` (Shared Memory).
*   API Layer (`api_vehicles_frames.py`) đọc dữ liệu từ Shared Memory này để trả về cho Frontend.

### C. Quản Lý Dữ Liệu

*   **TrafficViolations Table**: Lưu trữ các vụ vi phạm (Ảnh, Thời gian, Loại xe, Loại lỗi).
*   **TrafficReports**: Dữ liệu thống kê lưu trong SQLite để vẽ biểu đồ.

---

## 3. Các Chức Năng Chính & Demo

Khi demo, bạn nên đi theo luồng này:

1.  **Dashboard Giám Sát**:
    *   Show video real-time.
    *   Chỉ vào các chỉ số: Số xe, Tốc độ (nhảy số liên tục -> chứng tỏ real-time).
    *   Mở 1 tab khác hoặc dùng điện thoại truy cập để thấy đồng bộ.
2.  **Phát Hiện Vi Phạm (Nên chuẩn bị video test có vi phạm)**:
    *   Vào tab "Cấu hình" -> Bật Red Light Detection.
    *   Chạy video test -> Show log vi phạm hiện ra ngay lập tức kèm ảnh chụp.
3.  **Báo Cáo & Thống Kê**:
    *   Mở tab Analytics.
    *   Show biểu đồ "Giờ cao điểm" (Tính năng này rất thực tế).
    *   Thử Export CSV.
4.  **Chatbot AI**:
    *   Hỏi: "Đường nào đang tắc nhất?" -> AI trả lời dựa trên data hiện tại.

---

## 4. Bộ Câu Hỏi Phản Biện (Q&A)

**Q1: Làm sao hệ thống tính được tốc độ xe? Độ chính xác bao nhiêu?**
> **A:** Hệ thống tính dựa trên khoảng cách di chuyển của điểm trung tâm xe giữa các frame liên tiếp, nhân với hệ số `meter_per_pixel` (số mét tương ứng 1 pixel). Độ chính xác phụ thuộc vào việc cấu hình hệ số này (bước Calibration). Trong điều kiện lý tưởng góc quay cố định, sai số khoảng 10-15%.

**Q2: Tại sao dùng YOLO mà không dùng SSD hay Faster R-CNN?**
> **A:** YOLO (You Only Look Once) là mô hình One-stage detector, cân bằng tốt nhất giữa Tốc Độ và Độ Chính Xác. Với bài toán giao thông cần real-time (>20 FPS), Faster R-CNN quá chậm dù chính xác hơn. Bản YOLOv8 Nano/Small em dùng cực nhẹ, phù hợp chạy trên thiết bị biên (Edge devices).

**Q3: Hệ thống xử lý được bao nhiêu camera cùng lúc?**
> **A:** Phụ thuộc phần cứng. Với máy em (Core i5/i7, ko GPU rời), chạy tốt 1-2 cam nhờ OpenVINO. Nếu có GPU NVIDIA (CUDA), có thể scale lên 4-8 cam. Kiến trúc Multiprocessing của em cho phép mở rộng dễ dàng.

**Q4: Xử lý thế nào khi trời tối hoặc mưa?**
> **A:** Hiện tại model train trên dữ liệu ban ngày là chính. Để xử lý ban đêm, cần retrain model với dataset ban đêm (Night scenes) và áp dụng các bộ lọc xử lý ảnh (Gamma correction) trước khi đưa vào model. Đây là hướng phát triển trong tương lai.

**Q5: Tracking bị mất dấu (Id switch) khi xe che khuất nhau thì sao?**
> **A:** Em sử dụng thuật toán **ByteTrack**. Khác với DeepSORT cũ, ByteTrack tận dụng cả những box có điểm tin cậy thấp (low confidence) để match lại với các track bị mất, giúp giảm đáng kể hiện tượng mất dấu khi bị che khuất một phần (occlusion).

**Q6: WebSocket có bị trễ (latency) không?**
> **A:** Có độ trễ nhỏ (<500ms). Em đã tối ưu bằng cách gửi frame dạng binary (bytes) thay vì base64 string để giảm kích thước gói tin, và chỉnh `asyncio.sleep` phù hợp để cân bằng tải server.

---

## 5. Điểm Cần Lưu Ý/Cải Thiện

*   **Calibration**: Hệ số `meter_per_pixel` hiện đang hard-code hoặc ước lượng. Thực tế cần vẽ 4 điểm trên đường để tính Homography matrix.
*   **Database**: SQLite sẽ chậm nếu dữ liệu lên hàng triệu dòng. Cần migrate sang PostgreSQL cho production.
*   **Security**: API hiện tại chưa có Auth chặt chẽ (đang phát triển JWT).

---
*Chúc bạn bảo vệ thành công!*
