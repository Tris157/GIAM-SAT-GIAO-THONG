CUỘC THI KHOA HỌC KỸ THUẬT
Năm 2025

BÁO CÁO TÓM TẮT

Tên dự án:
HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH
SỬ DỤNG TRÍ TUỆ NHÂN TẠO

Lĩnh vực dự thi: PHẦN MỀM - TRÍ TUỆ NHÂN TẠO

---

MỤC LỤC

LỜI CẢM ƠN ............................................................................................................ 3

BẢNG DANH MỤC VIẾT TẮT ............................................................................... 4

TÓM TẮT DỰ ÁN "HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH
SỬ DỤNG TRÍ TUỆ NHÂN TẠO" .......................................................................... 5

I. VẤN ĐỀ NGHIÊN CỨU ................................................................................. 6
1. Lý do chọn đề tài .......................................................................................... 6
2. Tiêu chí của vấn đề nghiên cứu .................................................................... 8

II. THIẾT KẾ VÀ PHƯƠNG PHÁP ................................................................... 9
1. Quá trình nghiên cứu .................................................................................... 9
2. Thiết kế mô hình ......................................................................................... 10
3. Một số thư viện và công nghệ sử dụng ...................................................... 11
4. Các tham số khởi tạo .................................................................................. 11
5. Hàm sử dụng ............................................................................................... 12
6. Sơ đồ chi tiết hệ thống và thuật toán .......................................................... 13
7. Chức năng và dữ liệu hiện hành ................................................................. 16

III. CHẾ TẠO VÀ KIỂM TRA ......................................................................... 17
1. Chuẩn bị ...................................................................................................... 17
2. Thực hiện hệ thống mô phỏng .................................................................... 17
3. Chương trình mô phỏng trên máy tính ....................................................... 18

IV. KẾT LUẬN.................................................................................................. 18
1. Kết quả thực hiện dự án .............................................................................. 18
2. Hướng phát triển đề tài ............................................................................... 20

V. NGUỒN THAM KHẢO ............................................................................... 21

---

LỜI CẢM ƠN

Trong quá trình tìm hiểu về tình trạng giao thông và những thách thức trong công tác quản lý giao thông tại Việt Nam, chúng em nhận thấy sự cần thiết của các hệ thống giám sát thông minh sử dụng công nghệ trí tuệ nhân tạo nhằm giảm thiểu tai nạn, giảm ùn tắc và nâng cao hiệu quả quản lý. Đặc biệt, việc áp dụng công nghệ AI tiên tiến với chi phí hợp lý là giải pháp phù hợp trong bối cảnh hiện nay.

Chính từ mong muốn đó, chúng em đã thực hiện dự án "Hệ thống giám sát giao thông thông minh sử dụng trí tuệ nhân tạo". Sau một thời gian nghiên cứu và phát triển, chúng em rất vui mừng khi dự án đã hoàn thành với những tính năng hữu ích như: phát hiện và đếm phương tiện tự động, tính toán tốc độ trung bình, phân tích trạng thái giao thông, thống kê giờ cao điểm và AI Chatbot tư vấn. Hy vọng rằng, dự án sẽ góp phần nhỏ vào việc xây dựng hệ thống giao thông thông minh và hỗ trợ công tác quản lý một cách hiệu quả hơn.

Dự án hoàn thành, chúng em xin gửi lời cảm ơn chân thành đến Ban tổ chức Cuộc thi Sáng tạo Khoa học Kỹ thuật dành cho học sinh trung học đã tạo ra một sân chơi bổ ích và khuyến khích chúng em phát huy năng lực sáng tạo. Và cũng xin bày tỏ lòng biết ơn sâu sắc đến Ban Giám hiệu Trường cùng các thầy cô giáo hướng dẫn, những người đã luôn đồng hành, tạo điều kiện thuận lợi và hỗ trợ chúng em trong suốt quá trình thực hiện dự án.

Trân trọng cảm ơn!

---

BẢNG DANH MỤC VIẾT TẮT

| Tên viết tắt | Tên đầy đủ | Ý nghĩa |
|--------------|------------|---------|
| AI | Artificial Intelligence | Trí tuệ nhân tạo |
| API | Application Programming Interface | Giao diện lập trình ứng dụng |
| CSDL | - | Cơ sở dữ liệu |
| CSGT | - | Cảnh sát giao thông |
| CV | Computer Vision | Thị giác máy tính |
| FPS | Frames Per Second | Số khung hình trên giây |
| ML | Machine Learning | Học máy |
| NMS | Non-Maximum Suppression | Loại bỏ hộp giới hạn trùng lặp |
| OCR | Optical Character Recognition | Nhận dạng ký tự quang học |
| ROI | Region of Interest | Vùng quan tâm |
| TNGT | - | Tai nạn giao thông |
| UI/UX | User Interface/User Experience | Giao diện/Trải nghiệm người dùng |
| YOLO | You Only Look Once | Thuật toán phát hiện đối tượng |

---

TÓM TẮT DỰ ÁN "HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH SỬ DỤNG TRÍ TUỆ NHÂN TẠO"

**Bối cảnh:**

Theo Ủy ban An toàn giao thông Quốc gia, 10 tháng đầu năm 2025, cả nước xảy ra 15.251 vụ tai nạn giao thông, làm chết 8.515 người và bị thương 10.204 người. Bên cạnh đó, tình trạng ùn tắc giao thông ngày càng nghiêm trọng do số lượng phương tiện tăng nhanh trong khi hạ tầng chưa theo kịp.

Hiện nay, công tác giám sát giao thông chủ yếu dựa vào camera ghi hình thông thường, chưa có khả năng phân tích dữ liệu tự động. Cơ quan quản lý thiếu số liệu về lưu lượng xe, tốc độ trung bình, giờ cao điểm để lập kế hoạch điều phối hiệu quả.

**Giải pháp:**

Dự án xây dựng hệ thống giám sát giao thông thông minh sử dụng trí tuệ nhân tạo với các tính năng chính:

- **Phát hiện và đếm phương tiện tự động**: Sử dụng YOLO v11 để nhận diện ô tô, xe máy với độ chính xác 90-95%
- **Tính toán tốc độ trung bình**: Theo dõi xe qua nhiều khung hình (ByteTrack) để tính vận tốc
- **Phân tích trạng thái giao thông**: Tự động phân loại thông thoáng/đông đúc/ùn tắc
- **Thống kê và báo cáo**: Biểu đồ xu hướng, giờ cao điểm/thấp điểm, export CSV/JSON
- **AI Chatbot tư vấn**: Trợ lý ảo giúp tra cứu thông tin, gợi ý tuyến đường

**Kết quả:**

- Độ chính xác: 90-95%
- Tốc độ xử lý: 20 FPS (50ms/frame)
- Hỗ trợ 5 tuyến đường đồng thời
- Chi phí: 5-10 triệu đồng (thấp hơn 80-90% so với giải pháp thương mại)

**Ý nghĩa:**

Hệ thống giúp cơ quan quản lý có dữ liệu thống kê chi tiết, phát hiện ùn tắc kịp thời, lập kế hoạch điều phối khoa học. Đồng thời hỗ trợ người dân tra cứu thông tin giao thông, chọn tuyến đường phù hợp, tiết kiệm thời gian.

---

I. VẤN ĐỀ NGHIÊN CỨU

**1. Lý do chọn đề tài**

**❖ Thực trạng giao thông hiện nay**

Theo Tổng Cục Thống kê, 10 tháng đầu năm 2025 (tính từ ngày 15/12/2024 đến ngày 14/10/2025), toàn quốc xảy ra **15.251 vụ tai nạn giao thông**, làm chết **8.515 người**, bị thương **10.204 người**. So với cùng kỳ năm trước, số vụ tai nạn giảm 22,7%; số người chết giảm 7,2% và số người bị thương giảm 30,2%.

Riêng tại tỉnh Quảng Nam, theo báo cáo của Ban An toàn giao thông tỉnh, 6 tháng đầu năm 2025 xảy ra **217 vụ tai nạn giao thông**, làm chết **90 người** và bị thương **186 người**.

Điển hình như toàn cảnh một số vụ TNGT nghiêm trọng: Tai nạn liên hoàn trên cao tốc Đà Nẵng - Quảng Ngãi khiến 2 người tử vong và 7 người bị thương (ngày 19/6/2025).

![Hình 1. Tai nạn giao thông nghiêm trọng](https://placeholder-image.com/traffic-accident.jpg)

**Nguyên nhân chính:**

- **Ùn tắc giao thông**: Số lượng xe cộ gia tăng nhanh chóng (trung bình 10%/năm), trong khi hệ thống đường không phát triển tương xứng. Điều này dẫn đến tắc nghẽn, chen chúc và thiếu dữ liệu để phân tích, lập kế hoạch điều phối.

- **Quản lý giao thông hạn chế**: Công tác quản lý giao thông ở Việt Nam đang gặp nhiều khó khăn. Sự phát triển nhanh của xe cộ và cơ sở hạ tầng tạo áp lực lớn cho cơ quan chức năng. Đặc biệt, việc thu thập dữ liệu về lưu lượng xe, tốc độ, giờ cao điểm chủ yếu dựa vào quan sát thủ công, không thể hoạt động liên tục 24/7.

- **Thiếu hệ thống phân tích thông minh**: Các camera giám sát hiện có chủ yếu chỉ ghi hình, chưa có khả năng phân tích tự động để đếm xe, tính tốc độ, phát hiện ùn tắc hay cung cấp thống kê phục vụ công tác quản lý.

**❖ Sự phát triển của công nghệ AI trong giám sát giao thông**

Trí tuệ nhân tạo (AI) và thị giác máy tính (Computer Vision) đang được ứng dụng rộng rãi trong giám sát giao thông. Các hệ thống sử dụng AI có khả năng phát hiện và phân tích tự động, giúp giảm can thiệp của con người và nâng cao hiệu quả.

**Công nghệ AI trong giám sát giao thông bao gồm:**

- **Phát hiện đối tượng (Object Detection)**: Sử dụng mô hình YOLO v11 để phát hiện và phân loại phương tiện (ô tô, xe máy, xe tải, xe buýt) với độ chính xác >90%.

- **Theo dõi đối tượng (Object Tracking)**: Sử dụng ByteTrack để theo dõi chuyển động xe qua nhiều khung hình, tính toán tốc độ trung bình.

- **Phân tích lưu lượng**: Đếm số xe theo từng loại, tính tốc độ, phân loại trạng thái đường (thông thoáng/đông đúc/ùn tắc).

- **AI Chatbot**: Sử dụng Google Gemini để tạo trợ lý ảo tư vấn giao thông.

**❖ Một số vấn đề công nghệ liên quan:**

- **Độ tin cậy và độ chính xác**: Hệ thống AI cần đảm bảo độ chính xác cao (>90%) để tránh sai số trong thống kê và ra quyết định.

- **Hiệu suất xử lý real-time**: Cần xử lý video với tốc độ ≥15 FPS để giám sát kịp thời, đòi hỏi thuật toán tối ưu.

- **Chi phí triển khai**: Giải pháp thương mại có chi phí cao (50-100 triệu đồng/điểm). Cần giải pháp chi phí thấp hơn (5-10 triệu) nhưng vẫn hiệu quả.

- **Tích hợp và mở rộng**: Hệ thống cần dễ tích hợp với camera hiện có và mở rộng thêm tính năng.

Từ những vấn đề nêu trên cùng kiến thức đã học, chúng em thực hiện dự án "Hệ thống giám sát giao thông thông minh sử dụng trí tuệ nhân tạo" với phương châm **"thông minh, hiệu quả và tiết kiệm"**.

---

**2. Tiêu chí của vấn đề nghiên cứu**

Cần phải đảm bảo tính khả thi và hiệu quả của hệ thống. Các bước thực hiện được chia làm hai giai đoạn:

**Giai đoạn 1: Xây dựng hệ thống mô phỏng và kiểm chứng**

- **Mục tiêu thứ nhất**: Xây dựng cơ sở dữ liệu và nền tảng hệ thống.

Sử dụng công nghệ mã nguồn mở: Python (Backend), React (Frontend), YOLO v11 (phát hiện đối tượng), ByteTrack (tracking), Google Gemini (AI Chatbot). Tận dụng khả năng xử lý nhanh, chính xác của các thuật toán hiện đại.

- **Mục tiêu thứ hai**: Tiến hành thử nghiệm mô phỏng và thống kê thông số.

Thử nghiệm với video giao thông từ 5 tuyến đường, đo lường độ chính xác, thời gian xử lý, khả năng phát hiện và đếm xe.

- **Mục tiêu thứ ba**: Đưa ra công nghệ với chi phí thấp.

Chi phí mục tiêu: 5-10 triệu đồng/điểm (thấp hơn 80-90% so với giải pháp thương mại 50-100 triệu).

- **Mục tiêu thứ tư**: Tích hợp nhiều tính năng hiện đại.

Giám sát real-time, giao diện web, thống kê báo cáo, AI Chatbot, export CSV/JSON.

**Giai đoạn 2: Triển khai và mở rộng vào thực tiễn**

- **Mục tiêu thứ nhất**: Trở thành công cụ hỗ trợ cho công tác quản lý giao thông.

Cung cấp dữ liệu thống kê chi tiết, phát hiện ùn tắc kịp thời, hỗ trợ lập kế hoạch điều phối.

- **Mục tiêu thứ hai**: Phát triển mã nguồn mở và cộng đồng.

Chia sẻ mã nguồn, tài liệu để cộng đồng học tập và đóng góp cải tiến.

- **Mục tiêu thứ ba**: Mở rộng phát hiện thêm tình huống khác.

Nhận diện biển số xe (OCR), phát hiện vi phạm vượt đèn đỏ, dừng đỗ sai quy định, đi sai làn.

**Tính mới của đề tài:**

Hiện tại, các hệ thống thương mại giá cao (50-100 triệu) và chủ yếu chỉ ghi hình. Mục tiêu của chúng em là:

✓ Phát triển hệ thống chi phí thấp (5-10 triệu), hiệu quả cao
✓ Sử dụng YOLO v11 (mới nhất), kết hợp ByteTrack và Gemini AI
✓ Phát hiện, đếm xe tự động + tính tốc độ + phân tích trạng thái
✓ Thống kê giờ cao điểm/thấp điểm, xu hướng theo giờ
✓ AI Chatbot tư vấn giao thông bằng ngôn ngữ tự nhiên
✓ Giao diện web hiện đại, responsive, dark theme
✓ Mã nguồn mở, cộng đồng có thể tham gia phát triển

---

II. THIẾT KẾ VÀ PHƯƠNG PHÁP

**1. Quá trình nghiên cứu**

Hệ thống được phát triển theo quy trình nghiên cứu khoa học gồm 7 giai đoạn:

**Giai đoạn 1: Nghiên cứu lý thuyết (2 tuần)**
- Tìm hiểu Computer Vision, Deep Learning
- Nghiên cứu YOLO, ByteTrack, Speed Calculation
- Tìm hiểu FastAPI, React, Google Gemini

**Giai đoạn 2: Thiết kế kiến trúc (1 tuần)**
- Xác định 5 layers: Camera, AI Detection, Backend, Frontend, Data Analysis
- Thiết kế database, API endpoints, UI/UX

**Giai đoạn 3: Thu thập dữ liệu (2 tuần)**
- Thu thập 5 video giao thông từ Youtube và tự quay
- Chuẩn bị cho 5 tuyến: Văn Phú, Văn Quán, Đường Láng, Ngã Tư Sở, Nguyễn Trãi

**Giai đoạn 4: Phát triển module (4 tuần)**
- Module YOLO detection
- Module ByteTrack tracking
- Module speed calculation
- Backend API, Frontend UI, AI Chatbot

**Giai đoạn 5: Tích hợp và kiểm thử (3 tuần)**
- Tích hợp các module
- Kiểm thử từng chức năng và toàn bộ hệ thống
- Đo hiệu suất, độ chính xác

**Giai đoạn 6: Tối ưu hóa (2 tuần)**
- Tối ưu tham số: confidence threshold, frame skip
- Cải thiện tốc độ xử lý

**Giai đoạn 7: Hoàn thiện (1 tuần)**
- Viết tài liệu, chuẩn bị demo, hoàn thiện báo cáo

**Giả thuyết khoa học:**

Bằng cách kết hợp YOLO v11 + ByteTrack + Speed Calculation, có thể xây dựng hệ thống giám sát giao thông với độ chính xác ≥90%, tốc độ xử lý ≥15 FPS, chi phí <10 triệu đồng.

---

**2. Thiết kế mô hình**

**❖ Hệ thống mô phỏng trên máy tính**

- **Về công nghệ**: Dự kiến xây dựng thành công sau 6 tháng nghiên cứu:

  + Lập trình Backend: Python với FastAPI, hỗ trợ REST API và WebSocket streaming. Tích hợp YOLO v11, ByteTrack, OpenCV.

  + Lập trình Frontend: TypeScript với React 19, TailwindCSS, Vite. Giao diện responsive, dark theme, glass morphism effects.

  + Database: SQLite (có thể nâng cấp PostgreSQL). Hỗ trợ async operations với SQLAlchemy ORM.

  + AI Chatbot: Google Gemini 2.5 Flash với LangGraph ReActAgent.

  + Giao diện: 4 tabs chính (Giám sát, Phân tích, Báo cáo, Chatbot).

  + Cơ sở dữ liệu: Truy vấn nhanh, hỗ trợ export CSV/JSON.

- **Về chức năng**: Hệ thống cung cấp đầy đủ:

  + **Giám sát video real-time**: Stream từ 5 tuyến đường, 15-20 FPS, hiển thị bounding boxes, số xe, tốc độ.

  + **Phát hiện và đếm**: YOLO v11 phát hiện ô tô, xe máy với độ chính xác >90%.

  + **Tính tốc độ**: ByteTrack tracking qua ít nhất 5 frames, tính vận tốc trung bình riêng cho ô tô và xe máy.

  + **Phân tích trạng thái**: Tự động phân loại:
    - Ùn tắc: Tổng xe ≥15 VÀ Tốc độ <12 km/h
    - Đông đúc: Tổng xe ≥8 VÀ Tốc độ <30 km/h
    - Thông thoáng: Ngược lại

  + **Thống kê báo cáo**:
    - Giờ cao điểm/thấp điểm
    - Xu hướng theo giờ (Area Chart)
    - So sánh tuyến đường (Bar Chart)
    - Xu hướng real-time (Line Chart)

  + **Export dữ liệu**: CSV và JSON

  + **AI Chatbot**: Trả lời câu hỏi, gợi ý tuyến đường, cung cấp hình ảnh

**Kiến trúc hệ thống: 5 layers**

```
┌─────────────────────────────────┐
│    1. CAMERA LAYER              │
│    5 video files (có thể RTSP)  │
└──────────────┬──────────────────┘
               │ Video Stream
               ▼
┌─────────────────────────────────┐
│    2. AI DETECTION LAYER        │
│    YOLO v11 + ByteTrack + Speed │
│    (28ms + 8ms + 5ms = 41ms)    │
└──────────────┬──────────────────┘
               │ Results
               ▼
┌─────────────────────────────────┐
│    3. BACKEND LAYER             │
│    FastAPI + SQLite + WebSocket │
└──────────────┬──────────────────┘
               │ HTTP/WS
               ▼
┌─────────────────────────────────┐
│    4. FRONTEND LAYER            │
│    React: 4 tabs (Monitor,      │
│    Analytics, Reports, Chatbot) │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│    5. DATA ANALYSIS LAYER       │
│    Statistics + Gemini Chatbot  │
└─────────────────────────────────┘
```

---

**3. Một số thư viện và công nghệ sử dụng**

**✓ Backend (Python)**
- **Python 3.12**: Ngôn ngữ lập trình chính
- **FastAPI**: Web framework hiệu suất cao
- **Ultralytics**: YOLO v11 object detection
- **OpenCV**: Xử lý video, đọc frame
- **NumPy**: Tính toán mảng, ma trận
- **SQLAlchemy**: ORM cho database

**✓ Frontend (React)**
- **React 19.2**: UI framework hiện đại
- **TypeScript 5.6**: Type safety
- **Vite 7.0**: Build tool nhanh
- **TailwindCSS 3.4**: Utility-first CSS
- **Recharts 2.15**: Biểu đồ thống kê

**✓ AI/ML**
- **YOLO v11n**: Phát hiện đối tượng (2.6M parameters)
- **ByteTrack**: Tracking với Kalman Filter
- **Google Gemini 2.5 Flash**: AI Chatbot

---

**4. Các tham số khởi tạo**

**YOLO Detection:**
- Confidence Threshold: 0.5
- Classes: [2, 3, 5, 7] (car, motorcycle, bus, truck)
- Input Size: 640x640 pixels

**ByteTrack Tracking:**
- Track Buffer: 30 frames
- Match Threshold: 0.8

**Speed Calculation:**
- Min Frames: 5
- Moving Average Window: 5

**Traffic Status:**
- Ùn tắc: Total ≥15 AND Speed <12
- Đông đúc: Total ≥8 AND Speed <30
- Thông thoáng: Ngược lại

---

**5. Hàm sử dụng**

**Hàm process_frame**: Xử lý một khung hình

```
Input: frame (ảnh RGB)
Process:
  1. YOLO phát hiện xe → bounding boxes
  2. ByteTrack gán ID → track IDs
  3. Tính tốc độ → speeds
  4. Phân loại trạng thái → status
  5. Vẽ bounding boxes → processed_frame
Output: processed_frame, traffic_info
```

**Hàm calculate_speeds**: Tính tốc độ

```
Input: track_history (lịch sử vị trí)
Process:
  1. Lấy 5 vị trí gần nhất
  2. Tính khoảng cách (pixels)
  3. Chuyển sang meters
  4. Tính thời gian
  5. Speed = Distance/Time × 3.6
Output: speeds (km/h)
```

**Hàm classify_traffic_status**: Phân loại

```
Input: count_car, count_motor, speed_car, speed_motor
Logic:
  total = count_car + count_motor
  avg_speed = (speed_car + speed_motor) / 2

  IF total ≥ 15 AND avg_speed < 12:
    RETURN "Ùn tắc"
  ELSE IF total ≥ 8 AND avg_speed < 30:
    RETURN "Đông đúc"
  ELSE:
    RETURN "Thông thoáng"
```

---

**6. Sơ đồ chi tiết hệ thống và thuật toán**

**Sơ đồ 1: Thuật toán YOLO v11 - Phát hiện đối tượng**

```
┌────────────────────────┐
│ Input: Frame 1920x1080 │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 1. Preprocessing       │
│ - Resize → 640x640     │
│ - Normalize → [0,1]    │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 2. YOLO Backbone       │
│ - CSPDarknet           │
│ - Extract features     │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 3. YOLO Head           │
│ - Bbox regression      │
│ - Classification       │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 4. Post-processing     │
│ - NMS                  │
│ - Filter conf > 0.5    │
│ - Filter class [2,3,5,7│
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ Output: Detections     │
│ [x,y,w,h, conf, class] │
└────────────────────────┘

Thời gian: ~28ms
```

**Sơ đồ 2: Thuật toán ByteTrack - Tracking**

```
┌────────────────────────┐
│ Input: Detections      │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 1. Kalman Prediction   │
│ - Dự đoán vị trí       │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 2. IoU Matching        │
│ - Tính IoU             │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 3. Hungarian Algorithm │
│ - Optimal assignment   │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 4. Track Management    │
│ - Update/Create/Remove │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ Output: Tracks with ID │
└────────────────────────┘

Thời gian: ~8ms
```

**Sơ đồ 3: Thuật toán Speed Calculation**

```
┌────────────────────────┐
│ Input: Track History   │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ Check: ≥5 frames?      │
│ NO → Skip              │
└───────────┬────────────┘
            │ YES
            ▼
┌────────────────────────┐
│ Calculate Distance     │
│ - In pixels            │
│ - Convert to meters    │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ Calculate Time         │
│ - timestamp difference │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ Calculate Speed        │
│ speed = dist/time × 3.6│
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ Moving Average Filter  │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ Output: Speed (km/h)   │
└────────────────────────┘

Thời gian: ~5ms
```

**Sơ đồ 4: Sơ đồ tổng thể hệ thống**

![Hình 2. Sơ đồ kiến trúc tổng thể hệ thống](https://placeholder-image.com/system-architecture.png)

---

**7. Chức năng và dữ liệu hiện hành**

**Các chức năng chính:**

1. **Giám sát video real-time**
   - Stream từ 5 tuyến đường (15-20 FPS)
   - Hiển thị bounding boxes, track ID
   - Số xe, tốc độ, trạng thái real-time

2. **Phân tích lưu lượng**
   - Đếm ô tô, xe máy riêng biệt
   - Tính tốc độ trung bình từng loại
   - Phân loại trạng thái tự động

3. **Thống kê báo cáo**
   - Giờ cao điểm/thấp điểm: Top 3 giờ
   - Xu hướng theo giờ: Area Chart 24h
   - So sánh tuyến đường: Bar Chart
   - Xu hướng real-time: Line Chart

4. **Export dữ liệu**
   - CSV: Time, Road, Counts, Speeds, Status
   - JSON: Cấu trúc chi tiết với metadata

5. **AI Chatbot**
   - Trả lời câu hỏi về giao thông
   - Gợi ý tuyến đường
   - Cung cấp hình ảnh từ camera

**Dữ liệu lưu trữ (Bảng traffic_records):**

| Trường | Kiểu | Mô tả |
|--------|------|-------|
| id | INTEGER | Khóa chính |
| road_name | VARCHAR | Tên tuyến đường |
| timestamp | DATETIME | Thời gian |
| count_car | INTEGER | Số ô tô |
| count_motor | INTEGER | Số xe máy |
| speed_car | FLOAT | Tốc độ TB ô tô (km/h) |
| speed_motor | FLOAT | Tốc độ TB xe máy (km/h) |
| status | VARCHAR | Trạng thái |
| created_at | DATETIME | Thời gian tạo |

**Chu kỳ lưu:** Mỗi 5 giây/lần

---

III. CHẾ TẠO VÀ KIỂM TRA

**1. Chuẩn bị**

- **Hệ thống máy tính**: Intel Core i5-8400, RAM 8GB (khuyến nghị 16GB), SSD 256GB
- **Ngôn ngữ lập trình**: Python 3.12 (Backend), TypeScript/React (Frontend)
- **Các kho dữ liệu và thư viện**: FastAPI, Ultralytics, OpenCV, NumPy, SQLAlchemy, React, TailwindCSS, Recharts
- **Dữ liệu video**: 5 video giao thông cho 5 tuyến đường (Văn Phú, Văn Quán, Đường Láng, Ngã Tư Sở, Nguyễn Trãi)
- **Mô hình AI**: YOLO v11n (yolo11n.pt, ~6MB)
- **Nguồn kinh phí**: 0 đồng (sử dụng công nghệ mã nguồn mở, Gemini API free tier)

---

**2. Thực hiện hệ thống mô phỏng**

**Giai đoạn 1**: Nghiên cứu lý thuyết về AI, YOLO, ByteTrack, FastAPI, React (2 tuần)

**Giai đoạn 2**: Thu thập video giao thông và thiết kế kiến trúc hệ thống (2 tuần)

**Giai đoạn 3**: Xây dựng Backend - Module YOLO, ByteTrack, Speed Calculation, FastAPI endpoints, SQLite database (4 tuần)

**Giai đoạn 4**: Xây dựng Frontend - React components, WebSocket integration, Charts, Responsive design (3 tuần)

**Giai đoạn 5**: Tích hợp AI Chatbot với Google Gemini và LangGraph (1 tuần)

**Giai đoạn 6**: Tích hợp Backend ↔ Frontend, kiểm thử, đo hiệu suất, tối ưu hóa (3 tuần)

**Giai đoạn 7**: Hoàn thiện tài liệu, chuẩn bị demo, video, báo cáo (1 tuần)

---

**3. Chương trình mô phỏng trên máy tính**

**Các bước thực hiện:**

1. Cài đặt Python 3.12 và Node.js 20
2. Cài thư viện Backend: `pip install fastapi uvicorn ultralytics opencv-python numpy sqlalchemy`
3. Cài thư viện Frontend: `cd Frontend && pnpm install`
4. Chuẩn bị 5 video vào folder `Backend/app/video_test/`
5. Chạy Backend: `cd Backend/app && python -m uvicorn main:app --reload`
6. Chạy Frontend: `cd Frontend && pnpm run dev`
7. Truy cập: http://localhost:5173

---

IV. KẾT LUẬN

**1. Kết quả thực hiện dự án**

Sau 6 tháng (5/2025 - 11/2025), dự án đã hoàn thành với kết quả:

**✓ Về mặt kỹ thuật:**

- Xây dựng thành công hệ thống 5 layers
- Tích hợp YOLO v11 + ByteTrack + Speed Calculation
- Backend FastAPI với REST API + WebSocket
- Frontend React với 4 tabs chức năng
- AI Chatbot Google Gemini
- Database SQLite

**✓ Hiệu suất đạt được:**

| Chỉ tiêu | Mục tiêu | Kết quả | Đạt |
|----------|----------|---------|-----|
| Độ chính xác | ≥90% | 90-95% | ✓ |
| Tốc độ xử lý | ≥15 FPS | 20 FPS | ✓ |
| Thời gian/frame | <100ms | 50ms | ✓ |
| Số tuyến | ≥3 | 5 | ✓ |
| Chi phí | <10 triệu | 5-10 triệu | ✓ |

**✓ Về mặt chức năng:**

1. **Tab Giám sát**: Stream video 15-20 FPS, hiển thị bounding boxes, số xe, tốc độ, trạng thái

2. **Tab Phân tích**: Area Chart (xu hướng 24h), Bar Chart (so sánh 5 tuyến), Line Chart (real-time), Peak Hour

3. **Tab Báo cáo**: Export CSV/JSON, lọc theo thời gian

4. **Tab Chatbot**: Trả lời câu hỏi, gợi ý tuyến đường, cung cấp hình ảnh

**✓ So sánh với giải pháp thương mại:**

| Tiêu chí | Hệ thống này | Thương mại |
|----------|--------------|------------|
| Độ chính xác | 90-95% | 95-98% |
| Tốc độ | 20 FPS | 30 FPS |
| **Chi phí** | **5-10 triệu** | **50-100 triệu** |
| AI Chatbot | ✓ | ✗ |
| Export CSV/JSON | ✓ | Hạn chế |
| Mã nguồn mở | ✓ | ✗ |

**→ Đạt 90-95% hiệu quả nhưng chi phí chỉ 10%, rất phù hợp triển khai rộng rãi.**

**✓ Hạn chế:**

- Độ chính xác thấp hơn 3-5% so với thương mại
- Chưa có OCR nhận diện biển số
- Chưa test kỹ ban đêm, mưa

***Một số hình ảnh thực nghiệm chương trình:***

![Hình 3. Giao diện đăng nhập](https://placeholder-image.com/login.png)

![Hình 4. Tab Giám sát - Video streaming với bounding boxes](https://placeholder-image.com/monitor.png)

![Hình 5. Tab Phân tích - Biểu đồ xu hướng](https://placeholder-image.com/analytics.png)

![Hình 6. Tab Báo cáo - Export CSV/JSON](https://placeholder-image.com/reports.png)

![Hình 7. Tab Chatbot - AI tư vấn](https://placeholder-image.com/chatbot.png)

---

**2. Hướng phát triển đề tài**

**Ngắn hạn (3-6 tháng):**

+ Tích hợp OCR nhận diện biển số xe (PaddleOCR/EasyOCR)
+ Nâng cấp database lên PostgreSQL
+ Fine-tune YOLO với 10.000 ảnh giao thông VN → độ chính xác 95%+

**Trung hạn (6-12 tháng):**

+ Phát triển Mobile App (React Native)
+ Hỗ trợ multi-camera RTSP real-time
+ Thêm phát hiện vi phạm vượt đèn đỏ, dừng đỗ sai, đi sai làn

**Dài hạn (1-2 năm):**

+ Dự đoán ùn tắc bằng LSTM/Transformer
+ Tích hợp Smart City platform
+ Mở rộng ra các tỉnh thành, xây dựng cộng đồng mã nguồn mở

---

V. NGUỒN THAM KHẢO

1. Nguyễn Xuân Huy, *Sáng tạo trong thuật toán và lập trình với Python*, Đại học quốc gia Hà Nội, 2021.

2. Trần Thông Quế, *Bài tập lập trình với ngôn ngữ Python*, Đại học quốc gia Hà Nội, 2022.

3. Redmon, J., & Farhadi, A. (2018). *YOLOv3: An Incremental Improvement*. arXiv:1804.02767.

4. Zhang, Y., et al. (2022). *ByteTrack: Multi-Object Tracking*. ECCV.

5. Ultralytics YOLOv11 Documentation. https://docs.ultralytics.com/

6. FastAPI Documentation. https://fastapi.tiangolo.com/

7. React Documentation. https://react.dev/

8. OpenCV Documentation. https://docs.opencv.org/

9. Google Gemini API Documentation. https://ai.google.dev/

10. Ủy ban An toàn giao thông Quốc gia. (2025). *Báo cáo TNGT 10 tháng 2025*.

11. Công an tỉnh Quảng Nam. (2025). *Báo cáo giao thông 6 tháng 2025*.

12. GitHub - Cộng đồng mã nguồn mở. https://github.com

13. Stack Overflow. https://stackoverflow.com

14. Papers with Code. https://paperswithcode.com

---

**HẾT**
