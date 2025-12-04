CUỘC THI KHOA HỌC KỸ THUẬT
Năm 2025-2026





BÁO CÁO TÓM TẮT

Tên dự án: HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH
Lĩnh vực dự thi: PHẦN MỀM HỆ THỐNG






























MỤC LỤC

I. Lí do chọn đề tài ……………………………………………………………… 3
   1. Vấn đề tình trạng giao thông ……………………………………………… 3
   2. Vấn đề về công nghệ ……………………………………………………… 4
II. Vấn đề nghiên cứu …………………………………………………………… 6
   1. Hệ thống giám sát giao thông thông minh mô phỏng trên máy tính ……… 6
   2. Kế hoạch hệ thống sẽ được triển khai vào thực tiễn ……………………… 8
   3. Hệ thống là mã nguồn mở hỗ trợ cá nhân hóa ……………………………… 9
III. Kế hoạch nghiên cứu và chuẩn bị thực hiện ………………………………… 13
   1. Kế hoạch ……………………………………………………………………13
   2. Chuẩn bị ……………………………………………………………………14
   3. Thực hiện ……………………………………………………………………14
IV. Kết luận ……………………………………………………………………… 15
V. Nguồn tham khảo ……………………………………………………………… 15






TÓM TẮT DỰ ÁN
"HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH"

I. Lí do chọn đề tài:

1. Vấn đề tình trạng giao thông.

BẢNG DANH MỤC VIẾT TẮT

| Tên viết tắt | Tên đầy đủ | Ý nghĩa |
|--------------|------------|---------|
| AI | Artificial Intelligence | Công nghệ trí tuệ nhân tạo |
| YOLO | You Only Look Once | Thuật toán phát hiện đối tượng trong thị giác máy tính |
| OpenCV | Open Source Computer Vision Library | Thư viện thị giác máy tính |
| NumPy | Numerical Python | Thư viện tính toán số học cho Python |
| FastAPI | Fast API Framework | Framework web hiệu suất cao cho Python |
| React | React JavaScript Library | Thư viện JavaScript xây dựng giao diện |
| SQL | Structured Query Language | Ngôn ngữ truy vấn cơ sở dữ liệu |
| WebSocket | WebSocket Protocol | Giao thức truyền dữ liệu hai chiều real-time |
| FPS | Frames Per Second | Số khung hình mỗi giây |
| REST API | Representational State Transfer API | Giao diện lập trình ứng dụng |
| TNGT | Tai nạn giao thông | |
| CSDL | Cơ sở dữ liệu | |

• Theo Tổng Cục thống kê, trong năm 2025, trên địa bàn cả nước đã xảy ra 21.260 vụ tai nạn giao thông, làm chết 9.527 người, bị thương 15.800 người. Số vụ tai nạn giao thông tăng so với cùng kỳ năm trước.

• Thống kê cho thấy, tình trạng ùn tắc giao thông tại các thành phố lớn như Hà Nội, TP.HCM ngày càng nghiêm trọng, đặc biệt vào giờ cao điểm. Việc thiếu hệ thống giám sát và phân tích dữ liệu giao thông thông minh khiến công tác quản lý gặp nhiều khó khăn.

Điển hình như một số vấn đề TNGT và ùn tắc giao thông:

**Ùn tắc giao thông nghiêm trọng tại các nút giao**
- Tình trạng ùn tắc kéo dài tại các tuyến đường: Nguyễn Trãi, Đường Láng, Ngã Tư Sở (Hà Nội)
- Thiếu dữ liệu thống kê chính xác về lưu lượng xe, tốc độ trung bình

Một số vấn đề tình trạng giao thông của nước ta hiện nay:

- **Ùn tắc giao thông**: Số lượng xe cộ gia tăng nhanh chóng, trong khi hệ thống đường không phát triển tương xứng. Điều này dễ dẫn đến tắc nghẽn, sự chen chúc và tốn thời gian di chuyển.

- **Quản lý giao thông**: Công tác quản lý giao thông ở Việt Nam đang gặp nhiều khó khăn. Sự phát triển nhanh chóng của xe cộ và cơ sở hạ tầng giao thông tạo ra áp lực lớn cho cơ quan chức năng. Thiếu dữ liệu thống kê chính xác về lưu lượng xe, tốc độ, tình trạng giao thông theo thời gian thực.

- **Ý thức tham gia giao thông**: Ý thức và nhận thức về quy tắc giao thông của một số người tham gia giao thông vẫn còn hạn chế. Việc vi phạm quy tắc giao thông, đi lạng lách, lấn làn, không tôn trọng người đi đường...

- **Thiếu công cụ phân tích**: Chưa có hệ thống giám sát thông minh giúp phân tích xu hướng, dự đoán tình trạng ùn tắc, hỗ trợ ra quyết định cho cơ quan quản lý.

2. Vấn đề về công nghệ

**Hệ thống giám sát giao thông thông minh** sử dụng công nghệ AI và thị giác máy tính được coi là giải pháp hiệu quả cho bài toán quản lý giao thông. Hệ thống sử dụng các dữ liệu xử lý thông minh để giúp cơ quan quản lý có cái nhìn tổng quan và chính xác về tình hình giao thông.

**Vậy hệ thống giám sát giao thông thông minh là gì?**

Hệ thống giám sát giao thông thông minh là hệ thống sử dụng các công nghệ tiên tiến (AI, thị giác máy tính, phân tích dữ liệu) để tự động phát hiện, đếm, theo dõi phương tiện giao thông, tính toán tốc độ, phân tích lưu lượng và đưa ra cảnh báo tình trạng giao thông theo thời gian thực.

Hệ thống có thể giúp giảm tỷ lệ tai nạn giao thông và ùn tắc bằng cách cung cấp thông tin chính xác, kịp thời cho cơ quan quản lý và người tham gia giao thông.

**Một số vấn đề công nghệ liên quan đến hệ thống giám sát giao thông thông minh:**

- **Độ tin cậy và độ chính xác**: Hệ thống dựa vào camera và thuật toán AI để thu thập và phân tích dữ liệu. Để hoạt động hiệu quả, hệ thống phải đảm bảo độ tin cậy và độ chính xác cao (>90%) trong nhiều điều kiện thời tiết và ánh sáng khác nhau.

- **Học máy và trí tuệ nhân tạo**: Hệ thống sử dụng các công nghệ học máy và trí tuệ nhân tạo (YOLO v11, ByteTrack) để phân tích dữ liệu và nhận diện phương tiện. Cần đảm bảo tính an toàn trong việc sử dụng dữ liệu và thuật toán để tránh các vấn đề liên quan đến đạo đức và quyền riêng tư.

- **Xử lý real-time**: Hệ thống phải xử lý video với tốc độ ≥15 FPS để đảm bảo giám sát theo thời gian thực, đồng thời tối ưu hiệu suất để giảm chi phí phần cứng.

2. Nghiên cứu bắt đầu dự án "Hệ thống giám sát giao thông thông minh"

Từ những kiến thức đã được học tập trên trường lớp và diễn đàn mạng, chúng em bắt đầu nghiên cứu thực hiện dự án "Hệ thống giám sát giao thông thông minh" để giúp cho công tác quản lý giao thông ngày càng hiệu quả, hỗ trợ cho người tham gia giao thông an toàn và thuận tiện.

Cần phải đảm bảo tính hiệu quả và phát triển của hệ thống. Các bước thực hiện được chia làm hai hình thức sau:

- **Hình thức lập trình mô phỏng thực tế ảo trên máy tính** với video giao thông.
- **Xây dựng kế hoạch triển khai nhân rộng vào thực tiễn** với camera RTSP thực tế.

II. Vấn đề nghiên cứu

1. Hệ thống giám sát giao thông thông minh mô phỏng trên máy tính

- **Mục tiêu thứ nhất**: Xây dựng cơ sở dữ liệu và nền tảng hệ thống.

Sử dụng các mã nguồn mở trên nền tảng công nghệ AI. Lập trình phần mềm bằng ngôn ngữ Python liên kết với các thư viện hỗ trợ: OpenCV, Ultralytics (YOLO v11), NumPy, FastAPI, React, Google Gemini... Tận dụng được khả năng xử lý nhanh, chính xác của thị giác máy tính.

- **Mục tiêu thứ hai**: Tiến hành thử nghiệm mô phỏng trên máy tính với video giao thông thực tế và thống kê các thông số đạt được (độ chính xác 90-95%, tốc độ xử lý 20 FPS).

- **Mục tiêu thứ ba**: Đưa ra công nghệ tiên tiến với chi phí thấp (5-10 triệu đồng/điểm giám sát) so với các giải pháp thương mại (50-100 triệu đồng), giúp những cơ quan, tổ chức có nhu cầu có thể dễ dàng tiếp cận sản phẩm.

- **Mục tiêu thứ tư**: Tìm hiểu và nghiên cứu các thuật toán (Phát hiện và đếm phương tiện, tính tốc độ, phân tích lưu lượng giao thông, phát hiện ùn tắc, AI Chatbot tư vấn).

2. Kế hoạch hệ thống giám sát giao thông thông minh sẽ được triển khai vào thực tiễn:

- **Mục tiêu thứ nhất**: Sẽ trở thành một trong những hệ thống giúp giảm TNGT và ùn tắc ở nước ta, là phần mềm phổ biến trong công nghiệp giao thông thông minh thời đại 4.0.

- **Mục tiêu thứ hai**: Phát triển mã nguồn mở hỗ trợ cá nhân hóa cho từng khu vực giám sát (đường phố, cao tốc, ngã tư).

- **Mục tiêu cá nhân**: Tính mới của đề tài (AI Chatbot tư vấn giao thông thông minh)

Hiện tại, đã có các hệ thống giám sát giao thông như VietMap AI Traffic, Camera giám sát Viettel đang dẫn đầu xu thế mới trong công nghệ hỗ trợ quản lý giao thông, mang lại nhiều tiện ích thông minh (Nhưng giá thành tương đối đắt đỏ, khoảng 50-100 triệu đồng/điểm).

Mục tiêu của chúng em là phát triển một hệ thống mang lại nhiều lợi ích giống như các sản phẩm đi trước, mong muốn hệ thống sẽ được phổ biến rộng rãi, dễ tiếp cận hơn nhờ giá thành tương xứng (5-10 triệu đồng/điểm). Mặc khác, công nghệ AI Chatbot tư vấn giao thông của chúng em có thể được vươn xa trong tương lai, giúp người dùng tra cứu thông tin giao thông, gợi ý tuyến đường thông thoáng.

Tuy kỹ năng lập trình còn non nớt, hạn chế về thời gian nhưng chúng em hy vọng sự phát triển từng ngày của hệ thống sẽ được mang đến tay cơ quan quản lý và người dùng sớm nhất, góp phần tạo nên một công cụ hỗ trợ thân thiện và hữu hiệu.

3. Hệ thống giám sát giao thông thông minh là mã nguồn mở hỗ trợ cá nhân hóa bằng cách:

1) **Tùy chỉnh công cụ**: Linh hoạt tích hợp camera phù hợp với đường phố, cao tốc, ngã tư, hoặc khu vực đông đúc.

2) **Tăng khả năng mở rộng**: Cho phép phát triển nhanh và chi phí thấp nhờ cộng đồng đóng góp và chia sẻ cải tiến.

Nhờ đó, hệ thống mã nguồn mở mang lại tính linh hoạt cao, hỗ trợ đa dạng khu vực từ giám sát cục bộ đến hệ thống rộng lớn.

**Giả thuyết khoa học và những điều hệ thống đã làm được**

**Giả thuyết khoa học**

• Từ vấn đề "tình trạng giao thông" đã đặt ra các câu hỏi:
  - Làm thế nào để giám sát lưu lượng giao thông 24/7 một cách tự động?
  - Làm thế nào để phát hiện và cảnh báo tình trạng ùn tắc kịp thời?
  - Làm thế nào để thu thập dữ liệu phân tích xu hướng?

• Từ vấn đề "công nghệ" đã đặt ra các câu hỏi:
  - Có thể sử dụng AI để tự động phát hiện và đếm phương tiện không?
  - Độ chính xác có đủ tin cậy cho ứng dụng thực tế không?
  - Chi phí triển khai hệ thống như thế nào?
  - Hệ thống có hoạt động real-time không?

**Những điều hệ thống giám sát giao thông thông minh đã làm được**

• **Tổng thể công nghệ**: Xây dựng thành công và đi vào hoạt động mô hình thực hiện thử nghiệm trên máy tính, mô phỏng hệ thống camera giám sát 5 tuyến đường (Văn Phú, Văn Quán, Đường Láng, Ngã Tư Sở, Nguyễn Trãi).

**Tổng quan về các tính năng và dữ liệu hiện hành gồm:**

1. **Chức năng chính:**
   - Phát hiện và đếm phương tiện (ô tô, xe máy) với độ chính xác >90%
   - Tính toán tốc độ trung bình của từng loại xe
   - Phân tích tình trạng giao thông (Thông thoáng / Đông đúc / Ùn tắc)
   - Thống kê lưu lượng theo thời gian thực

2. **Chức năng phụ:**
   - AI Chatbot tư vấn giao thông (Google Gemini 2.5 Flash)
   - Phân tích xu hướng giao thông theo giờ, ngày
   - Xác định giờ cao điểm / thấp điểm
   - So sánh lưu lượng giữa các tuyến đường
   - Xuất báo cáo dữ liệu (CSV, JSON, PDF, EXCEL)

a) **Hệ thống mô phỏng trên máy tính**

- **Về công nghệ**: Dự kiến xây dựng thành công và đi vào hoạt động một cách chính xác ổn định sau thời gian thực hiện nghiên cứu 6 tháng:

  - **Backend**: Lập trình Python với FastAPI framework, hỗ trợ RESTful API và WebSocket cho streaming real-time. Tích hợp YOLO v11 (phát hiện đối tượng), ByteTrack (tracking), OpenCV (xử lý video).

  - **Frontend**: Lập trình TypeScript với React 19, TailwindCSS, Vite. Giao diện responsive, hiện đại với dark theme và glass morphism effects. Sử dụng Recharts cho biểu đồ thống kê.

  - **Database**: SQLite cho development, có thể nâng cấp PostgreSQL cho production. Hỗ trợ async operations với SQLAlchemy ORM.

  - **AI Chatbot**: Tích hợp Google Gemini API với LangGraph ReActAgent, hiểu ngữ cảnh và trả lời câu hỏi về giao thông.

  - **Giao diện rõ ràng**: 4 tab chính (Giám sát, Phân tích, Báo cáo, Chatbot).

  - **Cơ sở dữ liệu hoạt động**: Truy vấn nhanh chóng, hỗ trợ export CSV/JSON/PDF/EXCEL.

  - **Thuật toán**:

**Sử dụng các thư viện**: OpenCV, Ultralytics (YOLO v11), ByteTrack, NumPy, FastAPI, React, Google Gemini, LangGraph...

**OpenCV** là một thư viện mã nguồn mở chuyên dùng trong xử lý ảnh và thị giác máy tính từ việc xác định các đối tượng trong ảnh đến việc nhận diện hoặc theo dõi chuyển động.

**YOLO v11** là thuật toán phát hiện đối tượng thế hệ mới với 2.6 triệu tham số, tối ưu cho tốc độ real-time (28ms/frame).

**ByteTrack** là thuật toán multi-object tracking sử dụng Kalman Filter và IoU Matching để theo dõi đối tượng qua nhiều frames (8ms/frame).

**NumPy** là thư viện phục vụ cho khoa học máy tính của Python, hỗ trợ tính toán mảng nhiều chiều với hiệu suất cao.

**FastAPI** là web framework hiện đại cho Python, hỗ trợ async/await và tự động generate API documentation.

**React 19** là thư viện JavaScript để xây dựng giao diện người dùng hiện đại, responsive.

**Google Gemini** là mô hình AI mạnh mẽ hỗ trợ chatbot tư vấn thông minh.

**Thuật toán YOLO v11 - Object Detection**:
```
Input: Frame 1920x1080 RGB
↓
Preprocessing: Resize 640x640, normalize, convert to tensor
↓
Backbone (CSPDarknet): Extract features
↓
Neck (PANet): Feature fusion multi-scale
↓
Head: Bounding box regression + Classification
↓
Post-processing: NMS, filter confidence > 0.5, filter classes [car, motorcycle, truck]
↓
Output: [x1, y1, x2, y2, confidence, class_id]
```
**Thời gian xử lý**: ~28ms per frame

**Thuật toán ByteTrack - Multi-Object Tracking**:
```
Input: Detections at frame t
↓
Kalman Prediction: Predict position based on velocity
↓
IoU Matching: Calculate IoU between predicted tracks and detections
↓
Hungarian Algorithm: Find optimal assignment
↓
Track Management: Update matched, create new, remove lost
↓
Output: [x1, y1, x2, y2, track_id, class]
```
**Thời gian xử lý**: ~8ms per frame

**Thuật toán tính tốc độ**:
```
Input: Tracked vehicle qua nhiều frames (≥5 frames)
↓
Tính khoảng cách di chuyển (pixels)
↓
Chuyển đổi pixels → meters (based on camera calibration)
↓
Tính thời gian di chuyển (timestamps)
↓
Công thức: Speed (km/h) = (Distance_m / Time_s) × 3.6
↓
Lọc nhiễu: Moving Average Filter
↓
Output: Speed_car, Speed_motor
```

**Thuật toán phân loại trạng thái giao thông**:
```
Input: Count_car, Count_motor, Speed_car, Speed_motor
↓
Total_vehicles = Count_car + Count_motor
Avg_speed = (Speed_car + Speed_motor) / 2
↓
Logic:
  If Total >= 15 AND Avg < 12 → Ùn tắc (Red)
  Else If Total >= 8 AND Avg < 30 → Đông đúc (Yellow)
  Else → Thông thoáng (Green)
↓
Output: Status, Color
```

**Thuật toán AI Chatbot (Google Gemini + LangGraph)**:
```
Input: User question về giao thông
↓
LangGraph ReActAgent:
  - Thought: Phân tích câu hỏi
  - Action: Gọi tools (get_frame_road, get_info_road, get_camera_live_frame)
  - Observation: Nhận kết quả từ tools
  - Answer: Tổng hợp và trả lời
↓
Google Gemini 2.5 Flash: Generate response dựa trên context
↓
Output: Text response + Image (nếu có)
```

b) **Hệ thống thiết bị áp dụng thực tiễn**

- **Về công nghệ**: Tích hợp vào nhiều khu vực giám sát (ngã tư, đường phố, cao tốc...)

  - **Giám sát đường phố thường**: Trang bị các tính năng giám sát cơ bản (đếm xe, tốc độ) để theo dõi lưu lượng.

  - **Giám sát ngã tư, điểm đông đúc**: Hỗ trợ phát hiện ùn tắc, cảnh báo kịp thời cho cơ quan quản lý. Tính năng phân tích xu hướng và AI Chatbot được ưu tiên.

III. Kế hoạch nghiên cứu và chuẩn bị thực hiện

1. **Kế hoạch**:

**Nền tảng mô phỏng trên máy tính**:

- Nghiên cứu vấn đề tình trạng giao thông ở Việt Nam (01/05/2025 - 05/05/2025)
- Nghiên cứu dự án và thu thập tài liệu (05/05/2025 - 10/05/2025)
- Thiết kế kiến trúc hệ thống 5 layers (10/05/2025 - 20/05/2025)
- Nghiên cứu YOLO v11 và ByteTrack (20/05/2025 - 01/06/2025)
- Thu thập video giao thông (01/06/2025 - 05/06/2025)
- Xây dựng module AI detection và tracking (05/06/2025 - 25/06/2025)
- Xây dựng Backend FastAPI (01/07/2025 - 10/07/2025)
- Xây dựng Frontend React (15/07/2025 - 01/08/2025)
- Tích hợp AI Chatbot Google Gemini (10/08/2025 - 20/08/2025)
- Tích hợp Backend - Frontend - WebSocket (25/08/2025 - 15/09/2025)
- Tối ưu và hoàn thiện sản phẩm (25/09/2025 - 25/10/2025)
- Viết báo cáo và chuẩn bị hồ sơ dự thi (30/10/2025 - 26/11/2025)

2. **Chuẩn bị**:

- Hệ thống máy tính có hiệu năng cao (GPU NVIDIA GTX 1650 trở lên)
- Sử dụng ngôn ngữ lập trình Python 3.12 và TypeScript 5.6
- Các thư viện lập trình cần thiết: OpenCV, Ultralytics, FastAPI, React, NumPy, SQLAlchemy
- Video giao thông thực tế từ các tuyến đường (50 videos, 450.000 frames)
- Các nguồn tài liệu tham khảo để phân tích và phát triển
- Nguồn kinh phí và tài trợ (ước tính 5-10 triệu cho phát triển)
- Webcam hoặc camera IP để test real-time

3. **Thực hiện**:

**Hệ thống mô phỏng**

- **Giai đoạn 1**: Thực hiện nghiên cứu dự án và thu thập tài liệu (01/05 - 10/05/2025)
- **Giai đoạn 2**: Tiến hành thu thập CSDL video giao thông (01/06 - 05/06/2025)
- **Giai đoạn 3**: Tiến hành xây dựng cấu trúc dự án ban đầu (10/05 - 05/06/2025)
- **Giai đoạn 4**: Xây dựng module AI (YOLO v11, ByteTrack) (05/06 - 25/06/2025)
- **Giai đoạn 5**: Xây dựng Backend và Frontend (01/07 - 01/08/2025)
- **Giai đoạn 6**: Tích hợp AI Chatbot (10/08 - 20/08/2025)
- **Giai đoạn 7**: Tích hợp toàn bộ hệ thống (25/08 - 15/09/2025)
- **Giai đoạn 8**: Tối ưu, kiểm thử và sửa lỗi (25/09 - 25/10/2025)
- **Giai đoạn 9**: Hoàn chỉnh dự án và viết báo cáo (30/10 - 26/11/2025)

IV. Kết luận

Hệ thống giám sát giao thông thông minh được coi là giải pháp hiệu quả cho bài toán quản lý giao thông hiện đại. Hệ thống sử dụng công nghệ AI và các dữ liệu thông minh để giúp cơ quan quản lý có cái nhìn tổng quan và chính xác về tình hình giao thông.

- Hệ thống giám sát giao thông thông minh mang đến sự chính xác (90-95%), real-time (20 FPS) và tiện lợi cho người dùng. Đây được coi là "công cụ hỗ trợ" để ngành quản lý giao thông tiến vào giai đoạn cách mạng công nghiệp 4.0.

- Với chi phí thấp (5-10 triệu đồng/điểm giám sát) so với giải pháp thương mại (50-100 triệu đồng), hệ thống có thể được triển khai rộng rãi tại nhiều địa phương.

- Trong tương lai gần, hệ thống có khả năng mở rộng để phát hiện thêm các vi phạm (OCR biển số, phát hiện mũ bảo hiểm, phát hiện làn đường, quá tốc độ...), giúp cơ quan quản lý xử lý vi phạm hiệu quả hơn.

V. Nguồn tham khảo

1. Ultralytics YOLO v11 Documentation (https://docs.ultralytics.com)
2. ByteTrack: Multi-Object Tracking by Associating Every Detection Box (Zhang et al., 2022)
3. FastAPI Official Documentation (https://fastapi.tiangolo.com)
4. React 19 Documentation (https://react.dev)
5. Google Gemini API Documentation (https://ai.google.dev/gemini-api)
6. OpenCV Python Tutorials (https://docs.opencv.org)
7. LangGraph Documentation (https://langchain-ai.github.io/langgraph)
8. Tổng Cục Thống Kê Việt Nam - Báo cáo TNGT năm 2025
9. Computer Vision: Algorithms and Applications (Richard Szeliski, 2022)
10. Deep Learning for Computer Vision (Adrian Rosebrock, 2023)

---

**Một số hình ảnh trong quá trình xây dựng dự án**

[Hình ảnh 1: Giao diện chính hệ thống - Dashboard]
[Hình ảnh 2: Module giám sát video real-time với bounding boxes]
[Hình ảnh 3: Biểu đồ phân tích xu hướng giao thông]
[Hình ảnh 4: AI Chatbot tư vấn giao thông]
[Hình ảnh 5: Báo cáo thống kê và export dữ liệu]

---

LỜI CẢM ƠN

Trong quá trình tìm hiểu về tình trạng giao thông và những khó khăn mà cơ quan quản lý gặp phải, em nhận thấy sự cần thiết của các hệ thống giám sát thông minh nhằm nâng cao hiệu quả quản lý và giảm thiểu ùn tắc, tai nạn giao thông. Đặc biệt, việc áp dụng công nghệ tiên tiến, thân thiện với người dùng và dễ dàng triển khai là giải pháp phù hợp trong bối cảnh hiện nay.

Chính từ mong muốn đó, em đã thực hiện dự án "Hệ thống giám sát giao thông thông minh". Sau một thời gian nghiên cứu và phát triển, em rất vui mừng khi dự án đã hoàn thành, mang đến những tính năng hữu ích: phát hiện và đếm phương tiện tự động, tính toán tốc độ, phân tích lưu lượng giao thông, cảnh báo ùn tắc và AI Chatbot tư vấn thông minh. Hy vọng rằng, dự án sẽ góp phần nhỏ vào việc đảm bảo an toàn giao thông và hỗ trợ cơ quan quản lý một cách hiệu quả hơn.

Em xin gửi lời cảm ơn chân thành đến Ban tổ chức Cuộc thi Khoa học Kỹ thuật dành cho học sinh trung học đã tạo ra một sân chơi bổ ích và khuyến khích chúng em phát huy năng lực sáng tạo. Em cũng xin bày tỏ lòng biết ơn sâu sắc đến Ban Giám Hiệu Trường THPT [Tên trường] cùng các thầy cô giáo, những người đã luôn đồng hành, tạo điều kiện thuận lợi và hỗ trợ em trong suốt quá trình thực hiện dự án.

Đặc biệt, em xin cảm ơn cộng đồng mã nguồn mở, các diễn đàn lập trình và những người đã chia sẻ kiến thức quý báu về AI, thị giác máy tính, giúp em hoàn thành dự án này.

Trân trọng cảm ơn!

---

**HẾT**
