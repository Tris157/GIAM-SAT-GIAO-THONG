CUỘC THI KHOA HỌC KỸ THUẬT
Năm 2025-2026





KẾ HOẠCH NGHIÊN CỨU DỰ ÁN


Dự án: HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH
Lĩnh vực dự thi: PHẦN MỀM HỆ THỐNG






















MỤC LỤC

| Nội dung | Trang |
|----------|-------|
| **A. LÍ DO CHỌN ĐỀ TÀI** | 1 |
| **B. PHÁT BIỂU GIẢ THUYẾT KHOA HỌC, CÂU HỎI NGHIÊN CỨU** | 2 |
| **C. MÔ TẢ CHI TIẾT PHƯƠNG PHÁP NGHIÊN CỨU VÀ CÁC KẾT LUẬN** | 3 |
| a. Tiến trình | 3 |
| b. Rủi ro và an toàn | 5 |
| c. Phân tích dữ liệu | 6 |
| d. Kết luận | 6 |
| **D. TÀI LIỆU THAM KHẢO** | 7 |

---

KẾ HOẠCH NGHIÊN CỨU DỰ ÁN
"HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH"


A. Lí do chọn đề tài: Mô tả ngắn gọn tóm tắt cơ sở khoa học của vấn đề nghiên cứu và giải thích tại sao vấn đề đó được quan tâm trong khoa học. Nếu có thể, giải thích về bất kì tác động xã hội nào của vấn đề nghiên cứu.

Với thực trạng tai nạn giao thông nghiêm trọng tại Việt Nam (năm 2025 có 21.260 vụ tai nạn, 9.527 người chết), việc xây dựng hệ thống giám sát giao thông thông minh trở nên cấp thiết. Hệ thống giúp hỗ trợ công tác quản lý giao thông, giảm thiểu tai nạn và nâng cao hiệu quả giám sát.

Dự án nghiên cứu sử dụng các công nghệ AI tiên tiến và mã nguồn mở: YOLO v11 (phát hiện đối tượng), ByteTrack (theo dõi đối tượng), OpenCV (xử lý ảnh), FastAPI (Backend), React (Frontend), Google Gemini (AI Chatbot). Các công nghệ này tận dụng khả năng xử lý nhanh, chính xác của các thuật toán hiện đại với chi phí thấp.

Hệ thống sẽ được thử nghiệm mô phỏng trên máy tính với video giao thông thực tế và thống kê các thông số đạt được (độ chính xác, thời gian xử lý, tỷ lệ phát hiện đúng). Các thuật toán chính bao gồm: phát hiện và đếm phương tiện giao thông, tính toán tốc độ trung bình loại xe, phân tích lưu lượng giao thông, phát hiện các tuyến đường ùn tắc, đông đúc, và chatbot tư vấn giao thông thông minh.

Ưu điểm nổi bật của dự án là chi phí thấp (5-10 triệu đồng mỗi điểm giám sát) so với các giải pháp thương mại (50-100 triệu đồng), phù hợp để triển khai rộng rãi tại các địa phương.

B. Phát biểu giả thuyết khoa học, câu hỏi nghiên cứu, mục tiêu kĩ thuật, kết quả mong đợi. Chúng được đưa ra dựa trên lí do đã mô tả ở trên như thế nào?

Từ thực trạng giao thông hiện nay, dự án đặt ra các câu hỏi nghiên cứu:
- Làm thế nào để giám sát lưu lượng giao thông 24/7 một cách tự động?
- Làm thế nào để phát hiện và cảnh báo tình trạng ùn tắc giao thông kịp thời?
- Làm thế nào để thu thập dữ liệu giao thông để phân tích xu hướng và lập kế hoạch?

Từ sự phát triển của công nghệ AI mới, dự án đặt ra các câu hỏi kỹ thuật:
- Có thể sử dụng AI để tự động phát hiện và đếm phương tiện không?
- Độ chính xác của AI có đủ tin cậy cho ứng dụng thực tế không?
- Chi phí triển khai hệ thống AI như thế nào?
- Hệ thống có hoạt động real-time không?

Từ nhu cầu thực tiễn, dự án đặt ra các yêu cầu:
- Hệ thống phải hoạt động ổn định 24/7
- Giao diện thân thiện, dễ sử dụng
- Cung cấp thống kê và báo cáo chi tiết
- Hỗ trợ AI Chatbot để tương tác với người dùng
- Có khả năng mở rộng để phát hiện thêm các tình huống khác

Kết quả mong đợi: Xây dựng thành công "Hệ thống giám sát giao thông thông minh sử dụng trí tuệ nhân tạo" đáp ứng tất cả các yêu cầu trên với độ chính xác 90-95%, tốc độ xử lý 20 FPS, và chi phí thấp.

C. Mô tả chi tiết Phương pháp nghiên cứu và các Kết luận:

a. Tiến trình: mô tả chi tiết tiến trình và thiết kế thí nghiệm (thực nghiệm), bao gồm phương pháp thu thập số liệu và phân tích dữ liệu của mình nghiên cứu, nội dung mình thực hiện bởi người hướng dẫn hay bởi những người khác.

Hệ thống sử dụng các công nghệ AI mã nguồn mở hiện đại, mang lại tính linh hoạt cao và chi phí thấp:

Phần backend: Hệ thống được phát triển bằng Python, kết hợp FastAPI làm web framework chính với khả năng lập trình bất đồng bộ, giúp tối ưu tốc độ xử lý theo thời gian thực. Hệ thống sử dụng SQL làm cầu nối hỗ trợ truy vấn database bất đồng bộ, đảm bảo quản lý dữ liệu linh hoạt và hiệu quả. Các thư viện OpenCV và NumPy được tích hợp để xử lý ảnh và video, phục vụ phân tích hình ảnh giao thông. Mô hình YOLO v11 từ Ultralytics đóng vai trò cốt lõi trong phát hiện và nhận diện đối tượng trên đường.

Phần frontend: Giao diện người dùng được phát triển bằng React 19.2 kết hợp TypeScript 5.6 để đảm bảo tính hiện đại và dễ bảo trì. Hệ thống sử dụng Vite 7.0 giúp xây dựng nhanh, TailwindCSS 3.4 để tối ưu giao diện hiển thị linh hoạt trên nhiều thiết bị. Các thành phần sẵn có được hỗ trợ bởi Shadcn/ui, biểu đồ thống kê được hiển thị qua Recharts 2.15, và hiệu ứng động mượt mà nhờ Framer Motion.

AI và Machine Learning: Hệ thống ứng dụng mô hình YOLO v11n nhẹ và nhanh (2.6 triệu tham số, tối ưu tốc độ thời gian thực). ByteTrack được tích hợp để bám đối tượng chuyển động. Tính năng chatbot AI sử dụng Google Gemini 2.5 Flash. Hệ thống logic ra quyết định theo hướng phản ứng – hành động (ReAct) được xây dựng qua LangGraph.

Giao tiếp truyền dữ liệu: Hệ thống sử dụng WebSocket để truyền video trực tuyến theo thời gian thực, REST API để quản lý dữ liệu (tạo–đọc–sửa–xóa), và các giao thức HTTP/HTTPS nhằm đảm bảo truyền tải ổn định, bảo mật.

Thiết kế mô hình: Hệ thống gồm 5 lớp chính:
- Lớp camera: Dữ liệu video từ 5 tuyến đường (Văn Phú, Văn Quán, Đường Láng, Ngã Tư Sở, Nguyễn Trãi)
- Lớp nhận diện: YOLO v11 phát hiện đối tượng, ByteTrack bám phương tiện, tính tốc độ
- Backend xử lý: FastAPI quản lý dữ liệu và logic hệ thống
- Giao diện người dùng: 4 tab chính (Giám sát, Phân tích, Báo cáo, Chatbot)
- Lớp phân tích dữ liệu: Thống kê và xuất báo cáo

Các chức năng chính:
- Giám sát video trực tuyến: Truyền và hiển thị phương tiện theo thời gian thực, đếm xe, tính tốc độ
- Phát hiện và bám phương tiện: Nhận diện ô tô, xe máy với độ chính xác cao (>90%)
- Tính toán tốc độ: Phân tích vận tốc trung bình dựa trên bám khung hình liên tục
- Phân tích tình trạng giao thông: Tự động phân loại (Thông thoáng – Đông – Tắc nghẽn)
- Thống kê & báo cáo: Biểu đồ xu hướng, xác định giờ cao/thấp điểm, so sánh tuyến đường
- Xuất dữ liệu: Hỗ trợ xuất file (CSV, JSON, PDF, EXCEL)
- Chatbot AI: Trả lời câu hỏi, gợi ý tuyến đường, phân tích xu hướng

Kế hoạch chi tiết thực hiện:

| STT | Thời gian | Nội dung | Địa điểm | Kết quả |
|-----|-----------|----------|----------|---------|
| 1 | 05/02/2025 | Tìm hiểu thực trạng giao thông, phân tích các vấn đề | Tại nhà | Xác định được bài toán trọng tâm: giám sát giao thông thông minh bằng AI |
| 2 | 09/02/2025 | Thu thập tài liệu về AI, YOLO, ByteTrack, FastAPI, React | Tại nhà | Tổng hợp 40+ tài liệu, đủ cơ sở lý thuyết để phát triển hệ thống |
| 3 | 15/02/2025 | Thảo luận và đặt tên đề tài | Tại lớp | Hoàn thiện tên: "Hệ thống giám sát giao thông thông minh" |
| 4 | 20/02/2025 | Thiết kế kiến trúc 5 lớp (Camera – AI – Backend – Frontend – Analytics) | Tại phòng thực hành Tin 3 | Sơ đồ hệ thống rõ ràng, thuận lợi cho triển khai từng phần |
| 5 | 22/02/2025 | Nghiên cứu YOLO v11 | Tại phòng thực hành Tin 3 | Hiểu được pipeline phát hiện sẵn sàng triển khai detection |
| 6 | 25/02/2025 | Nghiên cứu ByteTrack | Tại phòng thực hành Tin 3 | Nắm vững cơ chế tracking, giải được bài toán gán ID ổn định |
| 7 | 01/03/2025 | Thu thập nhiều video về lưu lượng giao thông | Tại nhà | Xây dựng dataset đa dạng, gồm nhiều loại tuyến đường, trạng thái giao thông |
| 8 | 05/03/2025 | Cài môi trường Python, FastAPI, OpenCV, SQL | Tại phòng thực hành Tin 3 | Backend chạy ổn định, không lỗi phụ thuộc |
| 9 | 10/06/2025 | Xây dựng module YOLO detection | Tại phòng thực hành Tin 3 | Precision 90%+, detect tốt xe máy – ô tô – xe tải |
| 10 | 15/06/2025 | Xây dựng ByteTrack tracking | Tại phòng thực hành Tin 3 | Gán ID ổn định 92–95%, hạn chế mất dấu vật thể |
| 11 | 20/06/2025 | Module tính tốc độ | Tại phòng thực hành Tin 3 | Sai số tốc độ dưới 8%, đo chính xác trong video 30 FPS |
| 12 | 25/06/2025 | Phân loại trạng thái giao thông | Tại phòng thực hành Tin 3 | Nhận diện đúng trạng thái với độ chính xác cao |
| 13 | 01/07/2025 | Xây dựng FastAPI server | Tại phòng thực hành Tin 3 | API chạy mượt, hiển thị được trên UI |
| 14 | 10/07/2025 | Tạo database SQL | Tại phòng thực hành Tin 3 | Lưu hơn 20.000 bản ghi giao thông, truy vấn nhanh |
| 15 | 20/07/2025 | Xây dựng VideoMonitor bằng WebSocket | Tại phòng thực hành Tin 3 | Stream video real-time 15-20 FPS thành công |
| 16 | 01/08/2025 | Xây dựng biểu đồ hiển thị | Tại phòng thực hành Tin 3 | Biểu đồ line/area/bar hiển thị 5 tuyến đường, rõ xu hướng giờ cao điểm |
| 17 | 25/08/2025 | Tích hợp Frontend – Backend – WebSocket | Tại phòng thực hành Tin 3 | Hệ thống hoạt động liền mạch, không lỗi mất kết nối |
| 18 | 15/09/2025 | Tích hợp Backend – Frontend – WebSocket | Tại phòng thực hành Tin 3 | Hệ thống kết nối mượt, truyền dữ liệu real-time ổn định |
| 19 | 25/10/2025 | Tối ưu mô hình và hoàn thiện sản phẩm | Tại phòng thực hành Tin 3 | Độ chính xác được nâng lên cao, hoàn thành giao diện của dự án |
| 20 | 30/10 – 26/11/2025 | Viết, sửa và hoàn thiện báo cáo nộp ban tổ chức | Tại nhà và văn phòng đoàn | Hoàn thành báo cáo và hồ sơ dự thi |

b. Rủi ro và an toàn: Xác định bất kì rủi ro tiềm năng nào có thể và những cảnh báo an toàn cần thiết.

Dự án không có rủi ro về an toàn vật lý vì:
- Hệ thống hoạt động hoàn toàn trên môi trường mô phỏng máy tính
- Không sử dụng thiết bị nguy hiểm, hóa chất, hoặc vật liệu dễ cháy nổ
- Không tiếp xúc với điện áp cao hay thiết bị công suất lớn
- Môi trường thực hiện: phòng máy tính có đầy đủ trang thiết bị an toàn

Về bảo mật và đạo đức nghiên cứu:
- Dữ liệu sử dụng là video giao thông công khai, không vi phạm quyền riêng tư
- Không thu thập thông tin cá nhân hay hình ảnh nhận diện khuôn mặt
- Không sử dụng động vật có xương sống trong thí nghiệm
- Tuân thủ quy định về bảo vệ dữ liệu cá nhân theo pháp luật Việt Nam

Các biện pháp đảm bảo an toàn:
- Sao lưu dữ liệu thường xuyên để tránh mất mát
- Sử dụng máy tính có cấu hình phù hợp để tránh quá tải
- Nghỉ giải lao định kỳ khi làm việc với máy tính (mỗi 45-60 phút)
- Tuân thủ hướng dẫn từ giáo viên hướng dẫn trong quá trình thực hiện

c. Phân tích dữ liệu: Mô tả tiến trình sẽ sử dụng để phân tích dữ liệu kết quả để trả lời câu hỏi nghiên cứu hay giả thuyết khoa học.

Hệ thống thu thập dữ liệu từ video giao thông, sử dụng YOLO v11 để phát hiện phương tiện (ô tô, xe máy, xe tải), ByteTrack để theo dõi chuyển động qua nhiều frames và tính tốc độ. Dữ liệu được lưu vào database SQL với cấu trúc: road_name, timestamp, count_car, count_motor, speed_car, speed_motor, status. Phân tích bằng các biểu đồ thống kê (Line Chart, Area Chart, Bar Chart) để xác định xu hướng, giờ cao điểm, và so sánh lưu lượng giữa các tuyến đường. Xuất dữ liệu ra CSV, JSON, PDF, EXCEL để phân tích sâu hơn.

d. Kết luận:

Hệ thống giám sát giao thông thông minh dùng AI để hỗ trợ quản lý, phân tích dữ liệu, cảnh báo ùn tắc và gợi ý tuyến đường an toàn với chi phí thấp. Hệ thống nhận diện phương tiện đạt độ chính xác 90-95%, chi phí 5–10 triệu/điểm, mã nguồn mở và có khả năng mở rộng phát hiện vi phạm như OCR biển số, mũ bảo hiểm, sai làn và quá tốc độ. Dự án hướng đến xây dựng nền tảng giao thông thông minh, an toàn và tiết kiệm cho Việt Nam.

D. Tài liệu tham khảo: Liệt kê ít nhất 5 tài liệu tham khảo chính (Ví dụ: các bài báo khoa học, sách, trang web) mà bạn đã nghiên cứu. Nếu Kế hoạch nghiên cứu của bạn có sử dụng động vật có xương sống, phải là báo về động vật trong Sổ tay về hình.

1. Ultralytics YOLO v11 Documentation - Tài liệu chính thức về YOLO v11 (https://docs.ultralytics.com)

2. Zhang, Y., et al. (2022) "ByteTrack: Multi-Object Tracking by Associating Every Detection Box" - Bài báo nghiên cứu về thuật toán ByteTrack

3. FastAPI Official Documentation - Hướng dẫn phát triển REST API và WebSocket (https://fastapi.tiangolo.com)

4. React 19 Documentation - Tài liệu chính thức về React 19 (https://react.dev)

5. Google Gemini API Documentation - Hướng dẫn sử dụng Google Gemini AI (https://ai.google.dev/gemini-api)

6. OpenCV Python Tutorials - Hướng dẫn xử lý ảnh và video với OpenCV (https://docs.opencv.org)

7. LangGraph Documentation - Framework xây dựng AI Agent (https://langchain-ai.github.io/langgraph)

Chọn và sử dụng thống nhất một kiểu trình bày tài liệu tham khảo trong Kế hoạch nghiên cứu.

Có thể tham khảo hướng dẫn trong Sổ tay về sinh học thực hiện.

Có thể tham khảo hướng dẫn trong Sổ tay để bản xướng vật.
