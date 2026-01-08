# 🎙️ BẢN THUYẾT MINH DEMO CHI TIẾT (MASTER COMMENTARY)

> **Hướng dẫn:** Đây là bản thuyết hiện chi tiết từng phần, giúp bạn giải thích "phần chìm" của tảng băng trôi (kỹ thuật bên dưới) khi đang demo "phần nổi" (giao diện).

---

## 🏎️ PHẦN 1: TẠI TAB GIÁM SÁT (NHÌN THẤY AI HOẠT ĐỘNG)

**Hành động:** Trỏ chuột vào các Frame Video đang nhảy số.

**Nội dung thuyết minh:**
> "Kính thưa Ban giám khảo, đây là linh hồn của dự án. Khi video được nạp vào, hệ thống thực hiện 3 công đoạn cực kỳ phức tạp trong chưa đầy **0.05 giây**:
> 
> 1. **Nhận diện (Detection):** Thuật toán **YOLOv8** quét qua toàn bộ khung ảnh, trích xuất đặc trưng để phân biệt đâu là 'car' (ô tô), đâu là 'motor' (xe máy). Em đã sử dụng phiên bản Nano để tối ưu tốc độ xử lý real-time.
> 2. **Theo dõi (Tracking):** Đây là phần quan trọng. Thông thường AI chỉ biết 'đây là cái xe', nhưng nhờ **ByteTrack**, hệ thống gán cho mỗi xe một số ID duy nhất. ID này giúp chúng ta không bị đếm lặp một chiếc xe nhiều lần.
> 3. **Ước tính vận tốc:** Dựa trên sự thay đổi tọa độ của xe giữa các khung hình và hệ số tỉ lệ thực tế, hệ thống tính toán ra vận tốc. Thầy cô có thể thấy vận tốc nhảy liên tục, giúp phát hiện ngay các trường hợp phóng nhanh vượt ẩu."

---

## 📈 PHẦN 2: TẠI TAB PHÂN TÍCH (BIẾN DỮ LIỆU THÀNH TRI THỨC)

**Hành động:** Chỉ vào các biểu đồ đường và biểu đồ cột.

**Nội dung thuyết minh:**
> "Dữ liệu từ Camera nếu chỉ để xem thì rất lãng phí. Dự án của em đã **số hóa toàn bộ dòng chảy giao thông**. 
> 
> *   **Biểu đồ xu hướng:** Mỗi khi một chiếc xe đi qua, một bản ghi được lưu vào database **SQLite**. Hệ thống tự động xử lý hậu kỳ (Post-processing) để vẽ nên bức tranh giao thông theo thời gian thực.
> *   **Phân tích giờ cao điểm:** Thuật toán thống kê của em tự động gom nhóm dữ liệu theo từng giờ trong ngày. Thầy cô có thể thấy 'đỉnh' của biểu đồ chính là lúc kẹt xe. Điều này thay thế hoàn toàn việc con người phải ngồi đếm xe thủ công, giúp chính xác hóa việc quy hoạch hạ tầng giao thông."

---

## 🤖 PHẦN 3: TẠI TAB TRỢ LÝ AI (GIAO TIẾP VỚI HỆ THỐNG)

**Hành động:** Gõ câu hỏi và đợi AI trả lời.

**Nội dung thuyết minh:**
> "Đây là bước đột phá về trải nghiệm người dùng. Chúng em không muốn người quản lý phải là một chuyên gia dữ liệu. 
> 
> Nhờ tích hợp **Large Language Model (Gemini AI)** thông qua kỹ thuật **RAG (Retrieval-Augmented Generation)** đơn giản:
> - Khi em hỏi, hệ thống sẽ 'nhúng' (embed) câu hỏi.
> - Nó tự động trích xuất các thông số mới nhất từ cơ sở dữ liệu (số xe, tốc độ, tình trạng kẹt đường).
> - AI sẽ tổng hợp dữ liệu đó và trả lời bằng ngôn ngữ tự nhiên. 
> 
> Cách tiếp cận này giúp bất kỳ ai cũng có thể 'trò chuyện' với camera giao thông để nắm bắt tình hình thành phố."

---

## 🚦 PHẦN 4: VỀ TÍNH TOÀN VẸN VÀ TỐI ƯU (CÂU CHỐT KỸ THUẬT)

**Hành động:** Quay lại Dashboad chung.

**Nội dung thuyết minh:**
> "Điểm mà em tự hào nhất là toàn bộ quy trình nặng nề này — từ xử lý ảnh, tracking, lưu database đến chạy Chatbot — đều được em thiết kế theo mô hình **Đa tiến trình (Multiprocessing)**. 
> 
> Điều này đảm bảo rằng dù AI đang tính toán rất nặng ở phía sau, thì giao diện người dùng vẫn mượt mà, không bị treo. Và đặc biệt, nhờ **OpenVINO**, chúng ta có thể triển khai hệ thống này trên những máy tính văn phòng bình thường, tiết kiệm hàng tỷ đồng chi phí đầu tư Card đồ họa cho nhà nước."

---

### 💡 LỜI KHUYÊN ĐỂ GIÁM KHẢO "HIỂU CHI TIẾT":
- **Dùng từ "Tại sao":** Đừng chỉ nói "đây là biểu đồ", hãy nói "Tại sao chúng ta cần biểu đồ này...".
- **Dùng từ "Làm thế nào":** Giải thích ngắn gọn cơ chế (ví dụ: "Nhờ ByteTrack nên nó không đếm lặp").
- **Nhấn mạnh vào "Sự kết nối":** Cho giám khảo thấy video -> dữ liệu -> biểu đồ -> chatbot là một chuỗi thống nhất.

> [!IMPORTANT]
> **Hãy nhớ:** Bạn là "người phiên dịch" giúp giám khảo hiểu đống code phức tạp kia đang làm nên những điều kỳ diệu gì cho xã hội.
