# 🎬 KỊCH BẢN DEMO DỰ ÁN: SMART TRAFFIC MONITORING SYSTEM

> **Mục tiêu:** Cho Ban giám khảo thấy sự hoạt động mượt mà, tính thông minh và giá trị thực tế của hệ thống chỉ trong 3-5 phút demo.

---

## 🏗️ BƯỚC 0: CHUẨN BỊ (TRƯỚC KHI GIÁM KHẢO ĐẾN)

1.  **Khởi động hệ thống:** Đảm bảo cả Backend và Frontend đều đang chạy.
2.  **Mở sẵn các Tab:**
    *   Tab 1: **Giám sát (Monitoring)** - Chọn tuyến đường có lưu lượng ổn định nhất.
    *   Tab 2: **Phân tích (Analytics)** - Đảm bảo đã có dữ liệu biểu đồ.
    *   Tab 3: **Trợ lý AI (Chatbot)** - Mẫu câu hỏi sẵn trong đầu.
3.  **Kiểm tra đèn đỏ:** Nếu có tính năng đèn đỏ, hãy chuẩn bị video test có xe vi phạm để demo "bắt" lỗi.

---

## ⏱️ BƯỚC 1: GIÁM SÁT THỜI GIAN THỰC (0:00 - 1:30)

**Hành động:** Mở tab **Giám sát**. Chỉ vào màn hình video đang phát.

**Lời thoại gợi ý:**
> "Kính thưa Ban giám khảo, đây là giao diện chính của hệ thống. Các thầy cô có thể thấy camera đang truyền tải hình ảnh thời gian thực. 
> 
> Ngay lập tức, mô hình **YOLOv8** đã được tối ưu hóa qua **OpenVINO** đang nhận diện từng phương tiện. 
> - Màu xanh là ô tô, màu đỏ là xe máy. 
> - Các con số trên đầu mỗi xe chính là **vận tốc tức thời** được tính toán bởi thuật toán tracking **ByteTrack**. 
> - Phía bên phải, hệ thống tự động tổng hợp tổng số xe và đưa ra trạng thái giao thông (Thông thoáng/Đông đúc) dựa trên mật độ thực tế."

---

## ⏱️ BƯỚC 2: PHÂN TÍCH DỮ LIỆU THÔNG MINH (1:30 - 2:30)

**Hành động:** Chuyển sang tab **Phân tích (Analytics)**. Chỉ vào các biểu đồ.

**Lời thoại gợi ý:**
> "Không chỉ dừng lại ở việc xem video, điểm mạnh của dự án nằm ở khả năng **số hóa giao thông**. 
> 
> Như thầy cô thấy trên biểu đồ xu hướng, hệ thống tự động lưu trữ dữ liệu vào SQLite và phân tích ra các **khung giờ cao điểm**. Ví dụ, tại tuyến đường này, lưu lượng tăng đột biến vào lúc 17h chiều. 
> 
> Dữ liệu này cực kỳ quý giá cho các nhà quản lý đô thị để điều tiết đèn giao thông hoặc quy hoạch đường sá. Chúng em cũng hỗ trợ **Export dữ liệu ra file CSV/JSON** để phục vụ báo cáo chuyên sâu."

---

## ⏱️ BƯỚC 3: TRỢ LÝ ẢO AI ASSISTANT (2:30 - 3:30)

**Hành động:** Chuyển sang tab **Chatbot**. Gõ câu hỏi: *"Tình hình giao thông hiện tại thế nào?"* hoặc *"Tuyến đường nào đang tắc nhất?"*.

**Lời thoại gợi ý:**
> "Để làm cho hệ thống trở nên thân thiện và dễ tiếp cận hơn, chúng em đã tích hợp **Trợ lý AI sử dụng Google Gemini**. 
> 
> Thay vì phải nhìn vào những con số khô khan, người quản lý chỉ cần 'hỏi' hệ thống bằng ngôn ngữ tự nhiên. AI sẽ truy vấn trực tiếp vào database giao thông, phân tích và đưa ra câu trả lời thông minh như: 'Đường Nguyễn Trãi đang có 25 xe, trạng thái tắc nghẽn, bạn nên điều hướng xe sang tuyến Văn Phú'."

---

## ⏱️ BƯỚC 4: PHÁT HIỆN VI PHẠM (NẾU CÓ) (3:30 - 4:30)

**Hành động:** Chỉ vào danh sách vi phạm hoặc demo trực tiếp trên video có vạch dừng đỏ.

**Lời thoại gợi ý:**
> "Cuối cùng, hệ thống còn hỗ trợ giám sát an toàn giao thông. Chúng em đã thiết lập các **vùng nhận diện (ROI)** và **vạch dừng ảo**. 
> 
> Khi đèn tín hiệu chuyển sang màu đỏ, nếu có phương tiện băng qua vạch, hệ thống sẽ tự động chụp ảnh bằng chứng, ghi lại biển số (định hướng phát triển) và thời gian vi phạm để phục vụ việc 'phạt nguội' tự động."

---

## 🏁 BƯỚC 5: KẾT THÚC & MỜI ĐẶT CÂU HỎI

**Lời thoại gợi ý:**
> "Dự án của chúng em hướng tới một giải pháp toàn diện: **Nhìn thấy - Hiểu được - Và Hỗ trợ ra quyết định**. 
> 
> Em xin kết thúc phần demo tại đây và rất mong nhận được những góp ý, câu hỏi từ phía Ban giám khảo để hoàn thiện dự án hơn nữa. Em xin cảm ơn!"

---

### 💡 LƯU Ý KHI DEMO:
- **Thao tác tay:** Hãy dùng ngón tay chỉ vào màn hình hoặc dùng chuột di chuyển chậm để giám khảo dễ theo dõi.
- **Tương tác:** Nếu giám khảo hỏi bất chợt, hãy dừng lại trả lời ngay rồi mới tiếp tục script.
- **Phong thái:** Luôn mỉm cười và tự tin. Nếu hệ thống gặp lỗi lag nhẹ, hãy bình tĩnh nói: *"Do đang xử lý đồng thời nhiều luồng dữ liệu AI nặng nên có độ trễ nhỏ, điểm này chúng em sẽ tối ưu thêm bằng cách sử dụng GPU thay vì CPU trong tương lai"*.
