# 💰 BẢNG CHỨNG MINH TÍNH KINH TẾ: DỰ ÁN VS. SẢN PHẨM THỊ TRƯỜNG

> **Mục tiêu:** Cung cấp các con số và luận điểm đanh thép để thuyết phục ban giám khảo rằng giải pháp của bạn có khả năng tiết kiệm hàng tỷ đồng khi triển khai thực tế.

---

## 📊 BẢNG SO SÁNH TRỰC QUAN

| Hạng mục | Hệ thống truyền thống (Thị trường) | Giải pháp của chúng em | Mức tiết kiệm |
| :--- | :--- | :--- | :--- |
| **Phần cứng xử lý** | Đòi hỏi GPU NVIDIA cao cấp (RTX 3060+) | Chạy trên CPU Intel/Mini PC nhờ **OpenVINO** | **60% - 80%** |
| **Camera đầu cuối** | Cần camera AI chuyên dụng hoặc cảm biến từ | Tận dụng **camera an ninh sẵn có** (IP/RTSP) | **100% (tận dụng cũ)** |
| **Băng thông mạng** | Truyền video HD liên tục về trung tâm | Chỉ truyền Metadata và ảnh vi phạm | **90% chi phí mạng** |
| **Bản quyền (License)** | Phí bản quyền theo kênh (camera) hàng năm | Mã nguồn mở (Python, FastAPI, YOLOv8) | **Gần như 0đ** |
| **Hạ tầng lưu trữ** | Cần hệ thống lưu trữ video tập trung khổng lồ | Lưu trữ phân tán, chỉ lưu kết quả thống kê | **70% chi phí Storage** |

---

## 🛡️ 3 LUẬN ĐIỂM CHỨNG MINH SỰ VƯỢT TRỘI VỀ CHI PHÍ

### 1. Phá bỏ "Rào cản GPU" (NVIDIA Barrier)
Trên thị trường, để chạy nhận diện 10 camera thời gian thực, bạn cần một Server có Card đồ họa NVIDIA đắt tiền (khoảng 20-40 triệu VNĐ). 
*   **Dự án của em:** Nhờ tối ưu hóa bằng **OpenVINO (Intel)**, chúng ta có thể tận dụng các dòng máy tính văn phòng Core i5 có sẵn hoặc Mini PC giá rẻ (khoảng 5-7 triệu VNĐ). 
*   => **Kết luận:** Giảm chi phí đầu tư thiết bị xử lý xuống ít nhất 3 lần.

### 2. Tận dụng "Tài nguyên ngủ quên"
Hầu hết các thành phố hiện nay đều đã phủ kín Camera an ninh nhưng chỉ dùng để "ghi hình và xem lại" khi có sự cố. 
*   **Hệ thống thị trường:** Thường yêu cầu thay mới sang Camera tích hợp AI để có độ chính xác cao.
*   **Dự án của em:** Hoạt động như một "Bộ não bổ sung" cho hệ thống cũ. Chỉ cần lấy link RTSP là có thể biến camera thường thành camera thông minh.
*   => **Kết luận:** Tận dụng 100% hạ tầng cũ, không cần đào đường, đục tường để lắp thiết bị mới.

### 3. Chiến lược "Xử lý tại biên" (Edge Computing)
*   **Hệ thống cũ:** Truyền video HD từ 100 nút giao về trung tâm tốn băng thông cực lớn (phí Internet hàng tháng rất cao).
*   **Dự án của em:** Xử lý ngay tại máy tính đặt ở nút giao. Khi có xe đi qua, nó chỉ gửi về 1 dòng tin nhắn: `{"road": "A", "count": 1}` (vài byte).
*   => **Kết luận:** Tiết kiệm hàng trăm triệu tiền phí Internet mỗi năm cho thành phố.

---

## 🎤 CÁCH TRẢ LỜI KHI GIÁM KHẢO HỎI VỀ TÍNH KINH TẾ

> *"Thưa thầy cô, nếu một giải pháp AI có giá hàng tỷ đồng thì nó rất khó để phủ khắp các vùng quê hay các nút giao nhỏ. Hệ thống của em ra đời để giải quyết bài toán đó. Bằng cách kết hợp giữa **mã nguồn mở** và công nghệ **tối ưu phần cứng của Intel**, chúng em đã tạo ra một 'Hệ thống AI bình dân' nhưng hiệu quả không thua kém sản phẩm thương mại, giúp mở đường cho việc xây dựng Smart City với chi phí thấp nhất có thể."*

---

> [!IMPORTANT]
> **Nhấn mạnh:** "Rẻ không phải là yếu, mà là rẻ vì chúng ta biết **tối ưu hóa phần mềm** để bù đắp cho gánh nặng phần cứng."
