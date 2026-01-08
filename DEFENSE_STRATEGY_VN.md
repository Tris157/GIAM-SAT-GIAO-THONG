# 🛡️ CHIẾN THUẬT PHÒNG THỦ: CÁC CÂU HỎI "XOÁY" VÀO ĐIỂM YẾU

> **Mục tiêu:** Giám khảo cuộc thi KHKT thường hỏi vào điểm yếu để xem bạn có hiểu sâu vấn đề hay không. Bí quyết là: **Thừa nhận hạn chế + Đưa ra giải pháp kỹ thuật + Hướng phát triển**.

---

## 1. NHÓM CÂU HỎI VỀ ĐỘ CHÍNH XÁC (ACCURACY)

### Q1: "Tôi thấy xe che khuất nhau thì hệ thống đếm sai, bạn xử lý thế nào?"
*   **Điểm yếu:** Xe tải che xe máy, xe đi sát nhau bị nhận diện thành 1.
*   **Cách trả lời "Ăn điểm":** 
    > "Thưa thầy cô, đây là bài toán **Occlusion (Che khuất)** - một thách thức lớn trong Computer Vision. Hiện tại hệ thống của em sử dụng **ByteTrack**, thuật toán này giúp duy trì ID của xe ngay cả khi nó bị mất dấu tạm thời trong vài frame. Tuy nhiên, nếu bị che hoàn toàn lâu dài, độ chính xác sẽ giảm. 
    > **Giải pháp:** Trong thực tế, chúng ta sẽ lắp camera ở góc cao (Top-down view) để giảm góc khuất, hoặc sử dụng hệ thống Camera đa góc nhìn (Multi-view) để bù đắp dữ liệu cho nhau."

### Q2: "Buổi đêm hoặc trời mưa to thì AI của bạn có chạy được không?"
*   **Điểm yếu:** Hình ảnh nhiễu, ánh sáng yếu làm model YOLO "mù".
*   **Cách trả lời "Ăn điểm":**
    > "Hiện tại model YOLOv8 em đang dùng được train chủ yếu trên tập dữ liệu ban ngày nên độ chính xác ban đêm sẽ thấp hơn khoảng 20-30%. 
    > **Hướng giải quyết:** Để triển khai thực tế, em sẽ cần thực hiện **Data Augmentation** (làm giàu dữ liệu) bằng cách thêm các ảnh ban đêm, ảnh nhiễu vào tập train. Đồng thời có thể sử dụng các thuật toán tiền xử lý ảnh như **Histogram Equalization** để làm rõ chi tiết trước khi đưa vào AI."

---

## 2. NHÓM CÂU HỎI VỀ TÍNH TOÁN & TỐC ĐỘ (TECHNICAL DEPTH)

### Q3: "Bạn tính tốc độ dựa trên pixel, nhưng thực tế camera đặt chéo thì pixel ở xa khác pixel ở gần. Kết quả này đâu có tin cậy?"
*   **Điểm yếu:** Đây là điểm yếu cực lớn nếu chỉ dùng tỉ lệ `meter_per_pixel` cố định.
*   **Cách trả lời "Ăn điểm":**
    > "Dạ, nhận xét của thầy/cô rất chính xác. Phương pháp hiện tại của em đang dùng tỉ lệ pixel trung bình nên sẽ có sai số về phối cảnh (Perspective). 
    > **Giải pháp kỹ thuật:** Để chính xác tuyệt đối, em đã tìm hiểu về **Homography Matrix** (Ma trận đồng dạng). Chúng ta sẽ lấy 4 điểm mốc trên mặt đường thực tế để tạo ma trận chuyển đổi không gian từ từ 2D (ảnh) sang 3D (mặt đất). Đây là tính năng em đang nghiên cứu để nâng cấp trong phiên bản tiếp theo."

### Q4: "Tại sao hệ thống đôi khi bị lag hoặc tụt FPS khi mở nhiều camera?"
*   **Điểm yếu:** Giới hạn của CPU và xử lý đa luồng.
*   **Cách trả lời "Ăn điểm":**
    > "Dạ, vì việc chạy mô hình Deep Learning cực kỳ ngốn tài nguyên. Em đã tối ưu bằng **OpenVINO** để tận dụng tối đa sức mạnh CPU Intel. 
    > **Kỹ thuật:** Để giảm tải, em áp dụng kỹ thuật **Frame Skipping** (chỉ xử lý mỗi 2-3 frame một lần thay vì toàn bộ) mà vẫn đảm bảo tracking không bị đứt đoạn. Nếu có thêm phần cứng chuyên dụng như GPU NVIDIA, hệ thống có thể chạy mượt 10-20 camera cùng lúc."

---

## 3. NHÓM CÂU HỎI VỀ TÍNH MỚI & ĐÓNG GÓP (NOVELTY)

### Q5: "Code này tôi thấy trên mạng nhiều, phần nào là do bạn tự làm?"
*   **Câu hỏi nguy hiểm:** Giám khảo nghi ngờ bạn chỉ copy-paste.
*   **Cách trả lời "Ăn điểm":**
    > "Dạ, các thư viện như YOLO hay FastAPI là mã nguồn mở, nhưng việc **kết hợp và tối ưu hóa** chúng thành một hệ thống hoàn chỉnh là đóng góp của em. Cụ thể:
    > 1. Em tự thiết kế cấu trúc **Multiprocessing** để Backend không bị kẹt khi xử lý video.
    > 2. Em xây dựng bộ **Chatbot AI Assistant** có khả năng đọc hiểu Database giao thông (điểm mà các dự án khác thường thiếu).
    > 3. Em lập trình phần **Giao diện Dashboard** theo thời gian thực sử dụng WebSocket."

---

## 4. NHÓM CÂU HỎI VỀ PHÁP LÝ & ĐẠO ĐỨC (PRIVACY)

### Q6: "Hệ thống của bạn có vi phạm quyền riêng tư khi chụp ảnh người đi đường không?"
*   **Điểm yếu:** Vấn đề nhạy cảm về dữ liệu cá nhân.
*   **Cách trả lời "Ăn điểm":**
    > "Dự án của em tập trung vào **giám sát hạ tầng và thống kê lưu lượng**. Hệ thống không thực hiện nhận diện khuôn mặt. 
    > Về mặt kỹ thuật, dữ liệu hình ảnh vi phạm chỉ được lưu trữ nội bộ trên Server bảo mật. Trong tương lai, em có thể tích hợp thuật toán tự động **làm mờ khuôn mặt (Blur)** ngay khi xử lý để đảm bảo tuân thủ các quy định về quyền riêng tư."

---

## 🌟 LỜI KHUYÊN KHI BỊ "DỒN":
1.  **Đừng cãi:** Hãy bắt đầu bằng: *"Dạ, một câu hỏi rất hay/rất sâu sắc ạ. Em xin phép giải trình như sau..."*
2.  **Dùng từ chuyên môn:** Dùng các từ như `Deep Learning`, `Latency`, `Inference`, `Optimization`, `Database Schema`... để thể hiện sự am hiểu.
3.  **Luôn có hướng mở:** Nếu không biết trả lời, hãy nói: *"Đây là biến số em đang đưa vào danh mục thực nghiệm tiếp theo để hoàn thiện sản phẩm."*
