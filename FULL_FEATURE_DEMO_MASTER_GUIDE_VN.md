# 🏆 KỊCH BẢN THUYẾT TRÌNH DEMO TỔNG THỂ (ALL-IN-ONE MASTER GUIDE)

> **Hướng dẫn:** Đây là bản đồ dẫn đường cho bạn từ lúc bắt đầu đến khi kết thúc buổi demo, đảm bảo không bỏ sót bất kỳ tính năng nào của dự án.

---

## 🕒 MỞ ĐẦU: XÁC THỰC & PHÂN QUYỀN (LOGIN)

**Hành động:** Mở trang Login.
**Lời nói:** 
> "Kính thưa Ban giám khảo, hệ thống của chúng em được thiết kế với tính bảo mật cao, hỗ trợ phân quyền người dùng (Admin và Staff). Em xin phép đăng nhập với quyền Admin để trình diễn toàn bộ các tính năng quản trị."

---

## 📹 PHẦN 1: GIÁM SÁT ĐA TUYẾN THỜI GIAN THỰC (MONITORING)

**Hành động:** Vào trang Dashboard, chuyển đổi qua lại giữa các tuyến đường (Văn Phú, Nguyễn Trãi...).
**Lời nói:** 
> "Đây là giao diện giám sát trung tâm. Hệ thống có khả năng quản lý **đa luồng (Multi-streaming)** từ nhiều camera RTSP cùng lúc. 
> - **Chức năng nhận diện:** Thầy cô thấy đó, AI đang tự động khoanh vùng và phân loại ô tô, xe máy với độ trễ cực thấp (<200ms).
> - **Đo tốc độ:** Mỗi phương tiện được gán một ID và tính toán vận tốc tức thời. Nếu xe nào đi quá tốc độ, hệ thống sẽ cảnh báo bằng màu sắc.
> - **Trạng thái giao thông:** Dựa trên mật độ xe/phút, hệ thống tự động đánh giá: Xanh (Thông), Vàng (Đông), Đỏ (Tắc) giúp điều tiết giao thông từ xa."

---

## 🚦 PHẦN 2: PHÁT HIỆN VI PHẠM & CAMERA LIVE (RE_LIGHT VIOLATION)

**Hành động:** Chọn tab Camera Live (RTSP), chỉ vào phần cấu hình vạch dừng.
**Lời nói:** 
> "Đây là tính năng thực thi pháp luật tự động. Chúng em cho phép người quản lý thiết lập **Vùng đèn giao thông (ROI)** và **Vạch dừng (Stop Line)** trực tiếp trên giao diện.
> - Khi đèn tín hiệu đỏ: Hệ thống kích hoạt chế độ 'Giám sát vi phạm'.
> - Bất kỳ xe nào chạm vạch dừng lúc này sẽ bị hệ thống **chụp ảnh bằng chứng** tự động và lưu trữ vào cơ sở dữ liệu vi phạm kèm theo thời gian và hình ảnh xe."

---

## 📊 PHẦN 3: PHÂN TÍCH & BÁO CÁO CHUYÊN SÂU (ANALYTICS)

**Hành động:** Vào Tab Analytics/Reports. Di chuột qua biểu đồ xu hướng 24h.
**Lời nói:** 
> "Dòng chảy giao thông được chúng em lưu trữ bền vững. 
> - **Biểu đồ Hourly Trend:** Giúp nhận diện chính xác các khung giờ cao điểm để đưa ra phương án phân luồng.
> - **So sánh tuyến đường:** Cho biết đường nào đang chịu tải lớn nhất trong thành phố.
> - **Xuất báo cáo:** Chúng em hỗ trợ xuất dữ liệu ra định dạng **CSV và JSON** chỉ với một cú click, giúp các chuyên gia giao thông có dữ liệu sạch để nghiên cứu."

---

## 🤖 PHẦN 4: TRỢ LÝ AI ASSISTANT (CHATBOT) - ĐIỂM NHẤN SÁNG TẠO

**Hành động:** Mở Chatbot, gõ: *"So sánh lưu lượng đường Văn Phú và Nguyễn Trãi lúc này?"*
**Lời nói:** 
> "Điểm độc đáo nhất của dự án là khả năng 'Giao tiếp với hệ thống'. Thay vì tra bảng biểu phức tạp, em dùng **AI Gemini** để hỏi đáp ngôn ngữ tự nhiên. 
> AI sẽ tự 'đọc' Database hiện tại và trả lời thầy cô như một trợ lý thực thụ: 'Đường Nguyễn Trãi đang đông hơn Văn Phú 20%, thầy cô nên lưu ý khu vực này'."

---

## ⚙️ PHẦN 5: CẤU HÌNH & TRẠNG THÁI HỆ THỐNG (SYSTEM LOGS)

**Hành động:** Vào phần Settings hoặc System Status.
**Lời nói:** 
> "Cuối cùng, để vận hành ổn định, chúng em tích hợp Dashboard theo dõi **Sức khỏe hệ thống (System Metrics)**. 
> Nhờ tối ưu hóa bằng **OpenVINO**, dù đang xử lý nhiều luồng AI nhưng CPU vẫn duy trì ở ngưỡng an toàn, minh chứng cho tính khả thi cao khi triển khai trên diện rộng với chi phí thấp."

---

## 🏁 KẾT LUẬN

**Lời nói:** 
> "Từ **Giám sát trực tiếp** -> **Phát hiện vi phạm** -> **Thống kê báo cáo** -> đến **Tư vấn bằng AI**, hệ thống của chúng em đã khép kín một quy trình quản lý giao thông thông minh hoàn chỉnh. Em xin chân thành cảm ơn!"

---

> [!TIP]
> **Hãy chuẩn bị sẵn 1 video vi phạm đèn đỏ** trong máy để demo tính năng capture ảnh nếu camera live lúc đó không có ai vi phạm. Điều này đảm bảo buổi demo luôn "có biến" để giám khảo thấy tính năng hoạt động.
