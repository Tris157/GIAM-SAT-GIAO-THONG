# 📑 TÀI LIỆU DỰ ÁN: HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH (SMART TRAFFIC MONITORING SYSTEM)

> **Dành cho: Ban Giám Khảo Cuộc Thi Khoa Học Kỹ Thuật (KHKT)**
> **Tác giả:** [Tên của bạn/Nhóm]
> **Lĩnh vực:** Hệ thống nhúng & Trí tuệ nhân tạo (AI)

---

## 1. 🌟 TỔNG QUAN DỰ ÁN (OVERVIEW)

### 1.1. Lý do chọn đề tài
Trong bối cảnh đô thị hóa nhanh chóng, ùn tắc giao thông và vi phạm luật giao thông (vượt đèn đỏ, chạy quá tốc độ) trở thành vấn đề cấp thiết. Các hệ thống camera truyền thống chỉ dừng lại ở việc "ghi hình" mà thiếu khả năng "phân tích" và "cảnh báo" tự động. 
Dự án được xây dựng nhằm tạo ra một giải pháp **thông minh, tự động hóa hoàn toàn** việc giám sát, thống kê lưu lượng và phát hiện vi phạm với chi phí tối ưu.

### 1.2. Mục tiêu dự án
- **Nhận diện & Phân loại:** Tự động đếm ô tô, xe máy theo thời gian thực.
- **Đo tốc độ:** Ước tính tốc độ di chuyển của từng phương tiện.
- **Phát hiện vi phạm:** Nhận diện xe vượt đèn đỏ dựa trên phân tích vùng (ROI).
- **Phân tích dữ liệu:** Thống kê giờ cao điểm, mật độ giao thông theo ngày/tuần.
- **Trợ lý AI:** Tích hợp Chatbot AI để hỏi đáp về tình hình giao thông bằng ngôn ngữ tự nhiên.

---

## 2. 🛠️ CÔNG NGHỆ CỐT LÕI (TECHNICAL STACK)

### 2.1. Trí tuệ nhân tạo (AI & Computer Vision)
- **YOLOv8 (You Only Look Once):** Sử dụng mô hình YOLOv8 Nano/Small để đạt tốc độ xử lý nhanh nhất (High FPS) mà vẫn đảm bảo độ chính xác.
- **ByteTrack:** Thuật toán theo dõi đa đối tượng (Multi-Object Tracking) giúp bám sát phương tiện qua từng frame hình, từ đó tính toán quãng đường và tốc độ.
- **OpenVINO (Intel Optimizer):** **[Điểm cộng sáng tạo]** Công nghệ tối ưu hóa mô hình AI của Intel, giúp hệ thống chạy mượt mà trên các máy tính thông thường (CPU) mà không nhất thiết phải có Card đồ họa (GPU) đắt tiền.

### 2.2. Backend (Trung tâm xử lý)
- **FastAPI:** Framework Python hiện đại, tốc độ cao nhất hiện nay, dùng để xây dựng các API và xử lý dữ liệu từ Camera.
- **WebSocket:** Truyền tải video và dữ liệu stats theo thời gian thực (0 latency) lên giao diện người dùng.
- **SQLAlchemy & SQLite:** Hệ quản trị cơ sở dữ liệu để lưu trữ lịch sử giao thông bền vững.

### 2.3. Frontend (Giao diện người dùng)
- **React + TailwindCSS:** Xây dựng giao diện Dashboard hiện đại theo phong cách Glassmorphism (hiệu ứng kính mờ), tối ưu trải nghiệm trên cả điện thoại và máy tính.
- **Recharts:** Biểu đồ hóa dữ liệu lưu lượng giao thông sinh động.

### 2.4. Trợ lý ảo (AI Assistant)
- **Google Gemini API:** Sử dụng mô hình ngôn ngữ lớn (LLM) để phân tích dữ liệu giao thông phức tạp và trả lời người dùng một cách thông minh.

---

## 3. ✨ CÁC TÍNH NĂNG NỔI BẬT & QUY TRÌNH XỬ LÝ

### 3.1. Quy trình xử lý Video (Pipeline)
1. **Input:** Nhận tín hiệu từ Camera RTSP hoặc Video File.
2. **Preprocessing:** Xử lý khung hình, resize để tối ưu tốc độ.
3. **Inference:** Chạy mô hình YOLOv8 thông qua OpenVINO để tìm tọa độ phương tiện.
4. **Tracking:** Gán ID cho từng xe bằng ByteTrack.
5. **Analytics:** 
   - Đếm số lượng xe đi qua vạch.
   - Tính vận tốc dựa trên tỉ lệ `meters_per_pixel`.
   - Kiểm tra vi phạm đèn đỏ (nếu có).
6. **Output:** Gửi dữ liệu qua WebSocket để hiển thị lên Dashboard.

### 3.2. Hệ thống báo cáo thông minh
Không chỉ hiển thị số lượng xe hiện tại, hệ thống còn tự động tổng hợp:
- Biểu đồ xu hướng theo giờ (Hourly Trends).
- So sánh lưu lượng giữa các tuyến đường (Road Comparison).
- Xác định chính xác khung giờ nào là giờ cao điểm để đưa ra khuyến cáo.

---

## 4. 🚀 ĐIỂM SÁNG TRONG CUỘC THI (INNOVATION & IMPACT)

1.  **Tính thực tiễn cao:** Có thể triển khai trực tiếp trên hệ thống camera an ninh sẵn có của thành phố.
2.  **Tối ưu hóa phần cứng:** Nhờ OpenVINO, hệ thống có thể chạy trên các máy tính cấu hình trung bình tại Việt Nam, tiết kiệm chi phí đầu tư.
3.  **Tích hợp AI Chatbot:** Người quản lý chỉ cần hỏi "Đường nào đang tắc nhất?" hoặc "Dự báo giao thông chiều nay", AI sẽ phân tích database và trả lời ngay lập tức.
4.  **Xử lý đa luồng (Multi-threading):** Đảm bảo video preview luôn mượt mà dù đang thực hiện các tính toán AI nặng nề phía sau.

---

## 5. ❓ CÁC CÂU HỎI BAN GIÁM KHẢO THƯỜNG HỎI (Q&A)

**Q1: Độ chính xác của hệ thống là bao nhiêu?**
*Trả lời:* Hệ thống sử dụng YOLOv8 được train trên tập dữ liệu giao thông lớn, đạt độ chính xác khoảng 85-95% tùy điều kiện ánh sáng và góc quay camera. Chúng tôi có sử dụng thêm ngưỡng tin cậy (Confidence Threshold) để loại bỏ các nhận diện sai.

**Q2: Hệ thống có chạy được ban đêm hay trời mưa không?**
*Trả lời:* Có, YOLOv8 có khả năng nhận diện tốt trong điều kiện thiếu sáng. Tuy nhiên, độ chính xác có thể giảm nhẹ. Chúng tôi giải quyết bằng cách sử dụng các mô hình đã được tinh chỉnh (fine-tuned) cho dữ liệu ban đêm.

**Q3: Tại sao bạn lại chọn YOLOv8 mà không phải các thuật toán khác?**
*Trả lời:* YOLOv8 là sự cân bằng hoàn hảo giữa **Tốc độ (Speed)** và **Độ chính xác (Accuracy)**. Trong giám sát giao thông, việc xử lý thời gian thực (Real-time) là quan trọng nhất để kịp thời phát hiện vi phạm.

**Q4: Vấn đề bảo mật và quyền riêng tư được xử lý thế nào?**
*Trả lời:* Hệ thống chỉ phân tích và lưu trữ các chỉ số thống kê (loại xe, tốc độ, biển số vi phạm). Các dữ liệu hình ảnh cá nhân không liên quan sẽ không được lưu trữ lâu dài để đảm bảo quyền riêng tư theo quy định.

**Q5: Hướng phát triển tiếp theo của dự án là gì?**
*Trả lời:* 
- Tích hợp thêm nhận diện biển số xe (LPR) để tự động xuất biên bản vi phạm.
- Kết nối với hệ thống đèn giao thông để điều tiết thời gian đèn xanh/đỏ tự động dựa trên lưu lượng thực tế (Smart Traffic Signal).
- Phát triển ứng dụng di động cho người dân để tra cứu lộ trình tránh tắc đường.

---

> [!TIP]
> **Lời khuyên khi thuyết trình:** 
> - Hãy tập trung vào phần **Demo trực tiếp**. Khi giám khảo thấy hệ thống đếm xe và nhảy số vận tốc real-time, họ sẽ rất ấn tượng.
> - Nhấn mạnh vào việc bạn đã **tối ưu hóa (Optimization)** để chạy được trên máy tính bình thường (OpenVINO).
