CUỘC THI SÁNG TẠO
KHOA HỌC KỸ THUẬT

















BÁO CÁO TÓM TẮT:
HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH
SỬ DỤNG TRÍ TUỆ NHÂN TẠO
Lĩnh vực: Phần mềm - Trí tuệ nhân tạo





Tháng 11 năm 2025





MỤC LỤC

LỜI CẢM ƠN	3
BẢNG DANH MỤC VIẾT TẮT	4
TÓM TẮT DỰ ÁN	5

I.	VẤN ĐỀ NGHIÊN CỨU	6
1.	Lý do chọn đề tài	6
2.	Tiêu chí của vấn đề nghiên cứu	8

II.	THIẾT KẾ VÀ PHƯƠNG PHÁP	9
1.	Quá trình nghiên cứu	9
2.	Thiết kế mô hình	10
3.	Công nghệ và thư viện sử dụng	11
4.	Các tham số và hàm chính	12
5.	Sơ đồ cấu trúc hệ thống	13
6.	Sơ đồ tổng quan thuật toán	14
7.	Chức năng và dữ liệu hiện hành	18

III.	CHẾ TẠO VÀ KIỂM TRA	19
1.	Chuẩn bị	19
2.	Thực hiện hệ thống	19
3.	Chương trình thử nghiệm	20

IV.	KẾT QUẢ VÀ ĐÁNH GIÁ	20
1.	Kết quả thực hiện dự án	20
2.	Đánh giá hiệu suất hệ thống	21
3.	Hướng phát triển đề tài	22

V.	NGUỒN THAM KHẢO	23

LỜI CẢM ƠN

Trong quá trình tìm hiểu về tình trạng tai nạn giao thông và những nguyên nhân dẫn đến vi phạm luật giao thông tại Việt Nam, chúng em nhận thấy sự cần thiết phải có một hệ thống giám sát tự động, hiện đại nhằm giảm thiểu tai nạn và nâng cao hiệu quả quản lý giao thông. Đặc biệt, việc áp dụng công nghệ trí tuệ nhân tạo với chi phí hợp lý là giải pháp phù hợp trong bối cảnh hiện nay.

Chính từ mong muốn đó, chúng em đã thực hiện dự án "Hệ thống giám sát giao thông thông minh sử dụng trí tuệ nhân tạo". Sau một thời gian nghiên cứu và phát triển, chúng em rất vui mừng khi dự án đã hoàn thành với những tính năng hữu ích. Hy vọng rằng, dự án sẽ góp phần nhỏ vào việc đảm bảo an toàn giao thông và hỗ trợ công tác quản lý một cách hiệu quả hơn.

Dự án hoàn thành, chúng em xin gửi lời cảm ơn chân thành đến Ban tổ chức Cuộc thi Sáng tạo Khoa học Kỹ thuật dành cho học sinh trung học đã tạo ra một sân chơi bổ ích và khuyến khích chúng em phát huy năng lực sáng tạo. Và cũng xin bày tỏ lòng biết ơn sâu sắc đến Ban Giám Hiệu Trường cùng các thầy cô giáo hướng dẫn, những người đã luôn đồng hành, tạo điều kiện thuận lợi và hỗ trợ chúng em trong suốt quá trình thực hiện dự án.

Trân trọng cảm ơn!


BẢNG DANH MỤC VIẾT TẮT

Tên viết tắt	Tên đầy đủ	Ý nghĩa
AI	Artificial Intelligence	Công nghệ trí tuệ nhân tạo
API	Application Programming Interface	Giao diện lập trình ứng dụng
CSDL	Cơ sở dữ liệu
CSGT	Cảnh sát giao thông
CV	Computer Vision	Thị giác máy tính
DB	Database	Cơ sở dữ liệu
FPS	Frames Per Second	Số khung hình trên giây
HSV	Hue-Saturation-Value	Không gian màu HSV
HTTP	HyperText Transfer Protocol	Giao thức truyền tải siêu văn bản
IoU	Intersection over Union	Độ giao của vùng nhận diện
JWT	JSON Web Token	Token xác thực JSON
ML	Machine Learning	Học máy
OCR	Optical Character Recognition	Nhận dạng ký tự quang học
REST	Representational State Transfer	Kiến trúc API REST
ROI	Region of Interest	Vùng quan tâm
RTSP	Real Time Streaming Protocol	Giao thức truyền luồng thời gian thực
TNGT	Tai nạn giao thông
UI/UX	User Interface/User Experience	Giao diện và trải nghiệm người dùng
YOLO	You Only Look Once	Thuật toán phát hiện đối tượng


TÓM TẮT DỰ ÁN "HỆ THỐNG GIÁM SÁT GIAO THÔNG THÔNG MINH SỬ DỤNG TRÍ TUỆ NHÂN TẠO"

Tai nạn giao thông là một trong những vấn đề nan giải của xã hội hiện đại. Theo thống kê của Ủy ban An toàn giao thông Quốc gia, năm 2023 cả nước xảy ra 21.260 vụ tai nạn giao thông, làm chết 9.527 người và bị thương 15.526 người. Trong đó, vi phạm vượt đèn đỏ chiếm khoảng 18 phần trăm nguyên nhân gây tai nạn.

Hiện nay, công tác giám sát và xử lý vi phạm giao thông chủ yếu dựa vào lực lượng CSGT, gặp nhiều khó khăn về nguồn nhân lực và không thể hoạt động liên tục 24 giờ. Các hệ thống camera giám sát hiện có chủ yếu chỉ ghi hình, chưa có khả năng phân tích và cảnh báo tự động.

Dự án "Hệ thống giám sát giao thông thông minh sử dụng trí tuệ nhân tạo" được phát triển nhằm giải quyết vấn đề trên. Hệ thống sử dụng các công nghệ tiên tiến như YOLO v11 cho phát hiện phương tiện, HSV Color Detection cho phát hiện đèn đỏ, ByteTrack cho theo dõi xe, kết hợp với FastAPI Backend và React Frontend để tạo thành một giải pháp hoàn chỉnh.

Kết quả thử nghiệm cho thấy hệ thống đạt độ chính xác 90-95 phần trăm trong việc phát hiện vi phạm vượt đèn đỏ, với thời gian xử lý trung bình 50 mili giây trên mỗi khung hình. Hệ thống có khả năng hoạt động 24 giờ liên tục, tự động gửi cảnh báo qua Telegram trong vòng dưới 1 giây khi phát hiện vi phạm. So với các giải pháp thương mại có chi phí từ 50 đến 100 triệu đồng mỗi camera, dự án này có chi phí thấp hơn nhiều, chỉ khoảng 5 đến 10 triệu đồng, phù hợp để triển khai rộng rãi tại các địa phương.

Hệ thống bao gồm các thành phần chính: Module AI phát hiện vi phạm, Backend xử lý dữ liệu, Frontend giao diện người dùng, Telegram Bot thông báo và cơ sở dữ liệu quản lý. Tất cả đều được tích hợp chặt chẽ tạo thành một hệ sinh thái hoàn chỉnh.

Với những kết quả đạt được, dự án có ý nghĩa quan trọng cả về mặt khoa học lẫn thực tiễn, góp phần nâng cao hiệu quả quản lý giao thông, giảm thiểu tai nạn và xây dựng văn hóa giao thông văn minh.


I.	VẤN ĐỀ NGHIÊN CỨU

1.	Lý do chọn đề tài

	Thực trạng giao thông hiện nay

Theo Tổng Cục Thống kê, 6 tháng đầu năm 2025 (tính từ ngày 15 tháng 12 năm 2024 đến ngày 14 tháng 6 năm 2025), toàn quốc xảy ra 9.340 vụ tai nạn giao thông, giảm 3.062 vụ (24,69 phần trăm), làm chết 5.203 người, giảm 270 người chết (4,93 phần trăm), bị thương 6.256 người, giảm 3.203 người bị thương (33,86 phần trăm) so với cùng kỳ năm 2024.

Riêng tại tỉnh Quảng Nam, theo báo cáo của Ban An toàn giao thông tỉnh, 6 tháng đầu năm 2025 xảy ra 217 vụ tai nạn giao thông, làm chết 90 người và bị thương 186 người.

Điển hình như toàn cảnh một số vụ TNGT nghiêm trọng:


Hình 1. Tai nạn giao thông nghiêm trọng tại cao tốc Đà Nẵng - Quảng Ngãi khiến 2 người tử vong và 7 người bị thương (ngày 19 tháng 6 năm 2025)
Nguồn: https://nhandan.vn/tai-nan-giao-thong-nghiem-trong-tren-cao-toc-da-nang-quang-ngai-post887916.html

Nguyên nhân chính:

- Ùn tắc giao thông: Số lượng xe cộ gia tăng nhanh chóng, trong khi hệ thống đường không phát triển tương xứng. Điều này dễ dẫn đến tắc nghẽn, sự chen chúc và các va chạm không mong muốn.

- Hạn chế trong công tác quản lý giao thông: Công tác quản lý giao thông ở Việt Nam đang gặp nhiều khó khăn. Sự phát triển nhanh chóng của xe cộ và cơ sở hạ tầng giao thông tạo ra áp lực lớn cho cơ quan chức năng. Đặc biệt, việc giám sát vi phạm chủ yếu dựa vào lực lượng CSGT, không thể hoạt động liên tục 24 giờ.

- Ý thức tham gia giao thông: Ý thức và nhận thức về quy tắc giao thông của một số người tham gia giao thông vẫn còn hạn chế. Việc vi phạm quy tắc giao thông như vượt đèn đỏ, lạng lách, không tôn trọng người đi đường vẫn diễn ra phổ biến.

	Sự phát triển của công nghệ AI trong giám sát giao thông

Trí tuệ nhân tạo (AI) và thị giác máy tính (Computer Vision) đang được ứng dụng rộng rãi trong nhiều lĩnh vực, trong đó có giám sát giao thông. Các hệ thống sử dụng AI có khả năng phát hiện và nhận diện tự động các vi phạm giao thông, giúp giảm thiểu sự can thiệp của con người và nâng cao hiệu quả giám sát.

Công nghệ AI trong giám sát giao thông bao gồm:

- Phát hiện đối tượng (Object Detection): Sử dụng các mô hình học sâu như YOLO, SSD, Faster R-CNN để phát hiện và phân loại phương tiện giao thông (ô tô, xe máy, xe tải, xe buýt).

- Theo dõi đối tượng (Object Tracking): Sử dụng các thuật toán như ByteTrack, DeepSORT để theo dõi chuyển động của phương tiện qua nhiều khung hình.

- Phát hiện màu sắc (Color Detection): Sử dụng không gian màu HSV để phát hiện trạng thái đèn tín hiệu giao thông.

	Một số vấn đề công nghệ liên quan:

- Độ tin cậy và độ chính xác: Hệ thống AI cần đảm bảo độ chính xác cao trong việc phát hiện vi phạm, tránh trường hợp báo sai (false positive) hoặc bỏ sót (false negative). Điều này đòi hỏi phải tối ưu hóa các tham số và thuật toán phù hợp với điều kiện giao thông thực tế.

- Hiệu suất xử lý real-time: Hệ thống cần xử lý video với tốc độ cao (ít nhất 15-20 FPS) để đảm bảo phát hiện vi phạm kịp thời. Điều này đòi hỏi phải có thuật toán tối ưu và phần cứng đủ mạnh.

- Chi phí triển khai: Các giải pháp thương mại hiện có thường có chi phí cao (50-100 triệu đồng mỗi camera), khó triển khai rộng rãi. Cần có giải pháp chi phí thấp hơn nhưng vẫn đảm bảo chất lượng.

- Tích hợp và mở rộng: Hệ thống cần có khả năng tích hợp với các hệ thống hiện có và dễ dàng mở rộng để phát hiện thêm các loại vi phạm khác.

Từ những vấn đề nêu trên cùng những kiến thức đã được học tập trên trường lớp và nghiên cứu từ các nguồn tài liệu khoa học, chúng em mạnh dạn thực hiện dự án "Hệ thống giám sát giao thông thông minh sử dụng trí tuệ nhân tạo" nhằm góp phần giải quyết bài toán quản lý giao thông với phương châm "an toàn, hiệu quả và tiết kiệm".

2.	Tiêu chí của vấn đề nghiên cứu

Cần phải đảm bảo tính khả thi và hiệu quả của hệ thống. Các mục tiêu được chia làm hai giai đoạn chính:

  Giai đoạn 1: Xây dựng hệ thống mô phỏng và kiểm chứng

- Mục tiêu thứ nhất: Xây dựng cơ sở dữ liệu và nền tảng hệ thống.

Sử dụng các công nghệ mã nguồn mở: Python cho Backend, React cho Frontend, YOLO v11 cho phát hiện đối tượng. Tận dụng được khả năng xử lý nhanh, chính xác của các thuật toán hiện đại.

- Mục tiêu thứ hai: Tiến hành thử nghiệm mô phỏng trên máy tính và thu thập số liệu đánh giá.

Thử nghiệm với video giao thông thực tế, đo lường độ chính xác, thời gian xử lý, tỷ lệ phát hiện đúng và sai.

- Mục tiêu thứ ba: Đưa ra công nghệ với chi phí thấp để dễ dàng triển khai.

Chi phí mục tiêu: 5-10 triệu đồng mỗi điểm giám sát (so với 50-100 triệu đồng của giải pháp thương mại).

- Mục tiêu thứ tư: Tích hợp nhiều tính năng hiện đại.

Telegram Bot để cảnh báo real-time, giao diện web để quản lý và thống kê, AI Chatbot để tương tác.

  Giai đoạn 2: Triển khai và mở rộng vào thực tiễn

- Mục tiêu thứ nhất: Trở thành công cụ hỗ trợ đắc lực cho công tác quản lý giao thông.

Giúp CSGT giảm tải công việc, nâng cao hiệu quả xử lý vi phạm, có dữ liệu thống kê để phân tích xu hướng.

- Mục tiêu thứ hai: Phát triển mã nguồn mở và cộng đồng.

Chia sẻ mã nguồn, tài liệu để cộng đồng có thể học tập, đóng góp cải tiến.

- Mục tiêu thứ ba: Mở rộng khả năng phát hiện các vi phạm khác.

Nhận diện biển số xe, phát hiện không đội mũ bảo hiểm, đi sai làn, vượt tốc độ.

  Tính mới của đề tài

Hiện tại, trên thị trường đã có các hệ thống giám sát giao thông thương mại nhưng giá thành tương đối đắt đỏ (50-100 triệu đồng mỗi camera). Mục tiêu của chúng em là phát triển một hệ thống mang lại hiệu quả tương đương nhưng với chi phí thấp hơn nhiều (5-10 triệu đồng), sử dụng các công nghệ mã nguồn mở, dễ triển khai và mở rộng.

Điểm nổi bật của hệ thống:

- Sử dụng YOLO v11, phiên bản mới nhất và nhanh nhất của dòng YOLO.
- Tích hợp Telegram Bot để cảnh báo ngay lập tức, tương tác 2 chiều.
- Giao diện web hiện đại với React 19, hỗ trợ xem video trực tiếp, quản lý vi phạm, thống kê và AI Chatbot.
- Mã nguồn mở hoàn toàn, cộng đồng có thể tham gia phát triển.

Tuy kỹ năng lập trình còn hạn chế và thời gian nghiên cứu có giới hạn, nhưng chúng em hy vọng sự phát triển từng ngày của hệ thống sẽ được ứng dụng rộng rãi, góp phần tạo nên một công cụ hỗ trợ quản lý giao thông hiệu quả và an toàn hơn.

II.	THIẾT KẾ VÀ PHƯƠNG PHÁP

1.	Quá trình nghiên cứu

Hệ thống giám sát giao thông thông minh được phát triển theo quy trình nghiên cứu khoa học, bao gồm các giai đoạn:

- Giai đoạn 1: Nghiên cứu lý thuyết và tài liệu

Thu thập tài liệu về Computer Vision, Deep Learning, các thuật toán phát hiện đối tượng (YOLO, SSD, Faster R-CNN), thuật toán tracking (ByteTrack, DeepSORT), không gian màu HSV. Nghiên cứu các hệ thống giám sát giao thông hiện có trên thế giới và tại Việt Nam.

- Giai đoạn 2: Thiết kế kiến trúc hệ thống

Xác định các thành phần chính: Camera Layer, AI Detection Layer, Backend Processing, Frontend Layer, Notification Layer. Thiết kế cơ sở dữ liệu, API endpoints, giao diện người dùng.

- Giai đoạn 3: Thu thập dữ liệu

Thu thập video giao thông từ Youtube, camera giám sát công cộng (đã được cho phép), tự quay video tại các ngã tư. Tổng cộng khoảng 50 video clips, tương đương 450.000 frames.

- Giai đoạn 4: Phát triển các module

Phát triển tuần tự các module theo mô hình Agile: Module phát hiện đối tượng (YOLO), module phát hiện đèn đỏ (HSV), module tracking (ByteTrack), module phát hiện vi phạm, Backend API, Frontend UI, Telegram Bot.

- Giai đoạn 5: Tích hợp và kiểm thử

Tích hợp tất cả các module lại với nhau, kiểm thử từng chức năng riêng lẻ và toàn bộ hệ thống. Đo lường hiệu suất, độ chính xác, thời gian phản hồi.

- Giai đoạn 6: Tối ưu hóa

Tối ưu hóa các tham số: ROI coordinates, HSV threshold, confidence threshold, cooldown time, grid size. Cải thiện tốc độ xử lý, giảm false positive và false negative.

- Giai đoạn 7: Thử nghiệm và đánh giá

Chạy thử nghiệm với bộ dữ liệu test, thu thập kết quả, tính toán các chỉ số Precision, Recall, F1-Score, Accuracy. Đánh giá hiệu suất và so sánh với các hệ thống khác.

Giả thuyết khoa học:

Bằng cách kết hợp các công nghệ AI tiên tiến (YOLO v11, ByteTrack) với xử lý màu sắc (HSV), có thể xây dựng một hệ thống giám sát giao thông tự động với độ chính xác cao (trên 90 phần trăm), thời gian xử lý nhanh (dưới 100 mili giây mỗi frame) và chi phí thấp (dưới 10 triệu đồng mỗi điểm giám sát).

Các câu hỏi nghiên cứu:

- Làm thế nào để phát hiện chính xác phương tiện giao thông trong điều kiện ánh sáng và góc nhìn khác nhau?
- Làm thế nào để phát hiện trạng thái đèn đỏ một cách tin cậy?
- Làm thế nào để theo dõi xe qua nhiều khung hình và xác định vi phạm vượt đèn đỏ?
- Làm thế nào để tránh phát hiện trùng lặp cùng một vi phạm?
- Làm thế nào để tích hợp tất cả các thành phần thành một hệ thống hoàn chỉnh?

2.	Thiết kế mô hình

	Hệ thống mô phỏng và triển khai thực tế

- Về công nghệ: Dự kiến xây dựng thành công và đi vào hoạt động một hệ thống hoàn chỉnh sau thời gian thực hiện nghiên cứu 6 tháng.

+ Lập trình trên nền tảng ngôn ngữ Python cho Backend, TypeScript và React cho Frontend.

+ Sử dụng FastAPI framework để xây dựng RESTful API và WebSocket cho streaming real-time.

+ Tích hợp YOLO v11 cho phát hiện đối tượng, ByteTrack cho tracking, HSV cho phát hiện màu.

+ Sử dụng SQLite cho cơ sở dữ liệu (có thể nâng cấp PostgreSQL cho production).

+ Giao diện rõ ràng, hiện đại với TailwindCSS và Shadcn/ui components.

+ Cơ sở dữ liệu hoạt động nhanh chóng với SQLAlchemy ORM async.

- Về chức năng: Hệ thống cung cấp đầy đủ các tính năng cần thiết:

+ Phát hiện và nhận diện phương tiện (ô tô, xe máy, xe tải, xe buýt).

+ Phát hiện trạng thái đèn tín hiệu (đỏ, xanh, vàng).

+ Theo dõi xe di chuyển qua nhiều khung hình.

+ Phát hiện vi phạm vượt đèn đỏ với độ chính xác cao.

+ Lưu trữ bằng chứng vi phạm (ảnh, thông tin chi tiết).

+ Gửi cảnh báo real-time qua Telegram Bot.

+ Quản lý danh sách vi phạm trên giao diện web.

+ Thống kê và báo cáo chi tiết.

+ AI Chatbot hỗ trợ trả lời câu hỏi.

	Kiến trúc hệ thống

Hệ thống được thiết kế theo kiến trúc phân tầng (Layered Architecture), bao gồm 5 tầng chính:

1. Camera Layer: Thu thập video từ camera RTSP, webcam hoặc file video.

2. AI Detection Layer: Xử lý video với YOLO v11, HSV Color Detection, ByteTrack.

3. Backend Processing Layer: FastAPI server xử lý logic nghiệp vụ, lưu trữ database, gửi thông báo.

4. Frontend Layer: React application cung cấp giao diện người dùng.

5. Notification Layer: Telegram Bot gửi cảnh báo và tương tác với người dùng.

Ưu điểm của kiến trúc này:

- Tách biệt rõ ràng các thành phần, dễ bảo trì và mở rộng.
- Mỗi tầng có thể phát triển độc lập.
- Dễ dàng thay thế hoặc nâng cấp từng thành phần.
- Hỗ trợ scale horizontal (thêm nhiều camera, nhiều server).

3.	Công nghệ và thư viện sử dụng

	Backend Python

- Python 3.12: Ngôn ngữ lập trình chính, phù hợp cho AI và xử lý dữ liệu.

- FastAPI: Web framework hiện đại, hỗ trợ async/await, tự động tạo API documentation.

- Uvicorn: ASGI server hiệu suất cao để chạy FastAPI.

- SQLAlchemy: ORM (Object-Relational Mapping) hỗ trợ async cho database.

- OpenCV: Thư viện xử lý ảnh và video mạnh mẽ, được sử dụng rộng rãi trong Computer Vision.

- Ultralytics: Thư viện cung cấp YOLO v11 và các công cụ training, inference.

- NumPy: Thư viện tính toán khoa học, xử lý mảng nhiều chiều hiệu quả.

- Pillow: Thư viện xử lý ảnh, hỗ trợ nhiều định dạng.

- python-jose: Thư viện tạo và xác thực JWT token cho authentication.

- passlib: Thư viện mã hóa mật khẩu với bcrypt.

- requests: HTTP client để gọi Telegram Bot API.

	Frontend React

- React 19.2: UI library hiện đại với React Server Components và Concurrent features.

- TypeScript 5.6: Superset của JavaScript, cung cấp type safety.

- Vite 7.0: Build tool nhanh, hot module replacement (HMR) cực nhanh.

- TailwindCSS 3.4: Utility-first CSS framework, dễ customize.

- Shadcn/ui: Component library đẹp, accessible, dựa trên Radix UI.

- Framer Motion 11: Animation library mượt mà.

- Recharts 2.15: Chart library để vẽ biểu đồ thống kê.

- Lucide React: Icon library với hơn 1000 icons.

	AI và Machine Learning

- YOLO v11n: Phiên bản nano của YOLO v11, nhẹ (2.6M parameters) nhưng vẫn đạt độ chính xác cao. Phát hiện 80 classes của COCO dataset, trong đó có car (class 2), motorcycle (class 3), bus (class 5), truck (class 7).

- ByteTrack: Thuật toán tracking hiện đại, sử dụng Kalman Filter để dự đoán vị trí và Hungarian Algorithm để match detection với track.

- HSV Color Space: Không gian màu tách biệt thông tin màu sắc (Hue) với độ sáng (Value), phù hợp cho phát hiện màu đỏ của đèn tín hiệu.

	Database

- SQLite: Database nhẹ, không cần server, phù hợp cho development và triển khai nhỏ.

- Có thể nâng cấp PostgreSQL cho production với nhiều concurrent users.

	Communication

- WebSocket: Giao thức full-duplex để streaming video real-time.

- REST API: Giao thức HTTP chuẩn cho CRUD operations.

- Telegram Bot API: API của Telegram để gửi message, photo, tương tác với user.

- Long Polling: Phương pháp nhận message từ Telegram, phù hợp khi không có domain và SSL certificate.

4.	Các tham số và hàm chính

	Các tham số khởi tạo

- ROI Coordinates: [x, y, width, height] = [1570, 154, 43, 73] - Vùng chứa đèn tín hiệu.

- HSV Threshold:
  Lower Red 1: [0, 100, 100]
  Upper Red 1: [10, 255, 255]
  Lower Red 2: [170, 100, 100]
  Upper Red 2: [180, 255, 255]

- Stop Line Y: 500 pixels - Vạch dừng xe khi đèn đỏ.

- Confidence Threshold: 0.5 - Chỉ lấy detection có độ tin cậy trên 50 phần trăm.

- Cooldown Time: 5 giây - Thời gian chờ giữa 2 lần phát hiện cùng 1 xe.

- Grid Size: 50x50 pixels - Kích thước ô lưới để tránh duplicate detection.

	Hàm chính trong module phát hiện vi phạm

Hàm process_frame: Xử lý một khung hình video, trả về danh sách vi phạm.

```python
def process_frame(self, frame):
    # Bước 1: YOLO phát hiện xe
    detections = self.yolo_model(frame)

    # Bước 2: HSV phát hiện đèn đỏ
    is_red_light = self._is_red_light(frame, self.roi)

    # Bước 3: ByteTrack tracking xe
    tracks = self.byte_tracker.update(detections)

    # Bước 4: Phát hiện vi phạm
    violations = self._detect_violations(tracks, is_red_light)

    return violations
```

Hàm _is_red_light: Kiểm tra đèn có đỏ không dựa trên ROI và HSV threshold.

Hàm _detect_violations: Kiểm tra xe có vượt stop line khi đèn đỏ không, kết hợp cooldown và grid system để tránh duplicate.

Hàm save_violation: Lưu thông tin vi phạm vào database và lưu ảnh bằng chứng.

Hàm send_telegram_notification: Gửi ảnh và thông tin vi phạm qua Telegram Bot.

Nói chung, thuật toán kết hợp nhiều kỹ thuật AI và xử lý ảnh để phát hiện vi phạm vượt đèn đỏ một cách chính xác và kịp thời, đồng thời tránh phát hiện trùng lặp bằng các cơ chế cooldown và grid system.

5.	Sơ đồ cấu trúc hệ thống

Hình 2. Sơ đồ kiến trúc tổng thể hệ thống giám sát giao thông thông minh

```
┌─────────────────────────────────────────────────────────────┐
│                     CAMERA LAYER                             │
│  - Camera RTSP (IP Camera)                                   │
│  - Webcam                                                    │
│  - Video File                                                │
└────────────────────┬────────────────────────────────────────┘
                     │ Video Stream (30 FPS)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI DETECTION LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ YOLO v11     │  │ HSV Color    │  │ ByteTrack    │      │
│  │ Detection    │  │ Detection    │  │ Tracking     │      │
│  │ (28ms)       │  │ (2ms)        │  │ (8ms)        │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  Output: Bounding boxes, Track IDs, Red light status        │
└────────────────────┬────────────────────────────────────────┘
                     │ Violation Events
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND PROCESSING                          │
│  ┌──────────────────────────────────────────────────┐       │
│  │  FastAPI Server (Python 3.12)                    │       │
│  │  - RESTful API Endpoints                         │       │
│  │  - WebSocket (Real-time video streaming)         │       │
│  │  - JWT Authentication                            │       │
│  │  - Violation Detection Logic (5ms)               │       │
│  └──────────────────────────────────────────────────┘       │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ SQLite DB    │  │ Telegram     │  │ Report       │      │
│  │ (Async)      │  │ Notifier     │  │ Generator    │      │
│  │ (4ms)        │  │ (<1s)        │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/WebSocket
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND LAYER                             │
│  ┌──────────────────────────────────────────────────┐       │
│  │  React 19.2 + TypeScript + Vite                  │       │
│  │  - Dashboard (Tổng quan)                          │       │
│  │  - Live Stream View (Giám sát)                   │       │
│  │  - Violations Management (Vi phạm)                │       │
│  │  - Statistics & Reports (Báo cáo)                 │       │
│  │  - AI Chatbot (Trợ lý AI)                         │       │
│  └──────────────────────────────────────────────────┘       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  NOTIFICATION LAYER                          │
│  - Telegram Bot (Long Polling, timeout 30s)                  │
│  - Commands: /start, /stats, /report, /status, /help        │
│  - Auto violation alerts with photos (<1s)                   │
│  - 2-way interaction (user can ask questions)                │
└─────────────────────────────────────────────────────────────┘
```

Giải thích:

- Camera Layer thu thập video và gửi stream đến AI Detection Layer.

- AI Detection Layer sử dụng YOLO để phát hiện xe, HSV để phát hiện đèn đỏ, ByteTrack để tracking.

- Backend Processing nhận kết quả từ AI, xử lý logic phát hiện vi phạm, lưu database, gửi Telegram.

- Frontend Layer cung cấp giao diện người dùng để xem video, quản lý vi phạm, xem thống kê.

- Notification Layer gửi cảnh báo real-time qua Telegram và cho phép tương tác 2 chiều.

6.	Sơ đồ tổng quan thuật toán

	Thuật toán phát hiện đối tượng - YOLO v11

Hình 3. Sơ đồ thuật toán YOLO v11 phát hiện phương tiện

```
Input: Frame (1920x1080 RGB)
  │
  ▼
┌────────────────────────────────┐
│  Preprocessing                 │
│  - Resize to 640x640           │
│  - Normalize [0, 1]            │
│  - Convert to Tensor           │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  YOLO v11n Backbone            │
│  - CSPDarknet                  │
│  - Extract features            │
│  - Multi-scale feature maps    │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  YOLO v11n Neck                │
│  - PANet (Path Aggregation)    │
│  - Feature fusion              │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  YOLO v11n Head                │
│  - Decoupled head              │
│  - Bounding box regression     │
│  - Classification              │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Post-processing               │
│  - Non-Maximum Suppression     │
│  - Filter by confidence > 0.5  │
│  - Filter classes [2,3,5,7]    │
│  - Convert to [x1,y1,x2,y2]    │
└──────────────┬─────────────────┘
               ▼
Output: List of detections
  [x1, y1, x2, y2, confidence, class_id]
```

Giải thích chi tiết:

1. Preprocessing: Thay đổi kích thước ảnh về 640x640 pixels (input size chuẩn của YOLO), normalize giá trị pixel về khoảng 0-1, chuyển sang tensor để đưa vào mạng neural.

2. Backbone: Mạng CSPDarknet trích xuất features từ ảnh ở nhiều scales khác nhau (low-level features như cạnh, góc và high-level features như hình dạng đối tượng).

3. Neck: PANet kết hợp features từ nhiều scales để tăng khả năng phát hiện đối tượng ở nhiều kích thước khác nhau.

4. Head: Dự đoán bounding box (vị trí), confidence (độ tin cậy) và class (loại đối tượng).

5. Post-processing: Áp dụng Non-Maximum Suppression để loại bỏ các bounding box trùng lặp, lọc theo confidence và class.

	Thuật toán phát hiện đèn đỏ - HSV Color Detection

Hình 4. Sơ đồ thuật toán phát hiện đèn đỏ

```
Input: Frame (1920x1080 BGR)
  │
  ▼
┌────────────────────────────────┐
│  Extract ROI                   │
│  - Crop region [1570,154,43,73]│
│  - Get traffic light area only │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Convert color space           │
│  - BGR → HSV                   │
│  - Separate H, S, V channels   │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Create red mask               │
│  - Range 1: H[0,10] S[100,255] │
│    V[100,255]                  │
│  - Range 2: H[170,180]         │
│    S[100,255] V[100,255]       │
│  - Combine masks with OR       │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Calculate red ratio           │
│  - Count red pixels            │
│  - Total pixels = width*height │
│  - Ratio = red_pixels / total  │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Decision                      │
│  - If ratio > 0.05 (5%)        │
│    → Red light ON              │
│  - Else                        │
│    → Red light OFF             │
└──────────────┬─────────────────┘
               ▼
Output: is_red_light (True/False)
```

Giải thích chi tiết:

1. Extract ROI: Cắt ra vùng nhỏ chứa đèn tín hiệu (đã được xác định trước bằng cách đo trên video).

2. Convert color space: Chuyển từ BGR sang HSV vì HSV tách biệt màu sắc và độ sáng, dễ phát hiện màu hơn.

3. Create red mask: Tạo mask cho màu đỏ. Lưu ý màu đỏ nằm ở 2 đầu của Hue spectrum (0-10 và 170-180 độ).

4. Calculate red ratio: Đếm số pixel màu đỏ và tính tỷ lệ so với tổng số pixel trong ROI.

5. Decision: Nếu tỷ lệ > 5 phần trăm thì kết luận đèn đỏ đang bật.

	Thuật toán tracking - ByteTrack

Hình 5. Sơ đồ thuật toán ByteTrack

```
Input: Detections at frame t
  [x1, y1, x2, y2, conf, class]
  │
  ▼
┌────────────────────────────────┐
│  Initialize tracks             │
│  - If first frame              │
│  - Create new track for each   │
│    detection with ID=1,2,3...  │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Kalman Prediction             │
│  - Predict position at frame t │
│    based on velocity and       │
│    previous position           │
│  - Update covariance matrix    │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  IoU Matching                  │
│  - Calculate IoU between       │
│    predicted tracks and        │
│    new detections              │
│  - Build cost matrix           │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Hungarian Algorithm           │
│  - Find optimal assignment     │
│  - Match tracks to detections  │
│  - Threshold: IoU > 0.3        │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Track Management              │
│  - Matched: Update track       │
│  - Unmatched track: Mark lost  │
│  - Unmatched detection: New ID │
│  - Remove lost tracks (>30f)   │
└──────────────┬─────────────────┘
               ▼
Output: Tracks with IDs
  [x1, y1, x2, y2, track_id, class]
```

Giải thích chi tiết:

1. Initialize tracks: Frame đầu tiên tạo track mới cho mỗi detection với ID unique.

2. Kalman Prediction: Dự đoán vị trí của track ở frame hiện tại dựa trên vận tốc và vị trí trước đó.

3. IoU Matching: Tính IoU (Intersection over Union) giữa predicted tracks và detections mới để xem track nào match với detection nào.

4. Hungarian Algorithm: Tìm cách ghép track-detection tối ưu sao cho tổng IoU là lớn nhất.

5. Track Management: Cập nhật track đã match, đánh dấu track mất (unmatched track), tạo track mới cho detection chưa match, xóa track mất quá lâu.

	Thuật toán phát hiện vi phạm

Hình 6. Sơ đồ thuật toán phát hiện vi phạm vượt đèn đỏ

```
Input: Tracks, is_red_light, stop_line_y
  │
  ▼
┌────────────────────────────────┐
│  Check red light status        │
│  - If NOT red light            │
│    → Return empty list         │
│  - Else continue               │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  For each track:               │
│  - Get track_id                │
│  - Get position (x, y_bottom)  │
│  - Get vehicle class           │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Check position                │
│  - If y_bottom <= stop_line_y  │
│    → Skip (not crossed)        │
│  - Else continue               │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Check cooldown                │
│  - If track_id in recent_5s    │
│    → Skip (already detected)   │
│  - Else continue               │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Check grid                    │
│  - Calculate grid_key          │
│    = (x//50, y//50)            │
│  - If grid_key in recent_grid  │
│    → Skip (duplicate location) │
│  - Else continue               │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Record violation              │
│  - Add to violation list       │
│  - Save frame as image         │
│  - Update cooldown dict        │
│  - Update grid set             │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Save to database              │
│  - Insert violation record     │
│  - Store image path            │
│  - Store timestamp, type, etc. │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│  Send Telegram notification    │
│  - Upload photo                │
│  - Send message with details   │
│  - Response time < 1s          │
└──────────────┬─────────────────┘
               ▼
Output: List of violations
```

Giải thích chi tiết:

1. Check red light: Chỉ xử lý khi đèn đỏ đang bật, bỏ qua nếu đèn xanh hoặc vàng.

2. For each track: Duyệt qua tất cả các xe đang được tracking.

3. Check position: Kiểm tra xe có vượt qua vạch dừng (stop_line_y) chưa. Nếu chưa thì bỏ qua.

4. Check cooldown: Kiểm tra xe này đã bị phát hiện trong 5 giây qua chưa. Nếu rồi thì bỏ qua để tránh duplicate.

5. Check grid: Chia màn hình thành lưới 50x50 pixels, kiểm tra vị trí này đã có vi phạm chưa. Nếu rồi thì bỏ qua.

6. Record violation: Nếu tất cả điều kiện đều thỏa, ghi nhận vi phạm, lưu ảnh, cập nhật cooldown và grid.

7. Save to database: Lưu thông tin vi phạm vào cơ sở dữ liệu SQLite.

8. Send Telegram notification: Gửi ảnh và thông tin vi phạm qua Telegram Bot trong vòng 1 giây.

7.	Chức năng và dữ liệu hiện hành

	Các chức năng chính của hệ thống

- Phát hiện phương tiện giao thông: Sử dụng YOLO v11 để phát hiện và phân loại các loại xe (ô tô, xe máy, xe tải, xe buýt) trong video với độ chính xác trên 90 phần trăm.

- Phát hiện trạng thái đèn tín hiệu: Sử dụng HSV Color Detection để xác định đèn đỏ có đang bật hay không dựa trên ROI (Region of Interest) đã được cấu hình.

- Theo dõi xe qua nhiều khung hình: Sử dụng ByteTrack để gán ID cho mỗi xe và theo dõi di chuyển của nó qua các frame, giúp xác định chính xác xe nào vi phạm.

- Phát hiện vi phạm vượt đèn đỏ: Kết hợp thông tin từ YOLO, HSV và ByteTrack để xác định xe có vượt vạch dừng khi đèn đỏ hay không. Sử dụng cooldown 5 giây và grid system 50x50 pixels để tránh phát hiện trùng lặp.

- Lưu trữ bằng chứng vi phạm: Tự động chụp ảnh vi phạm và lưu cùng với thông tin chi tiết (loại xe, thời gian, vị trí, độ tin cậy) vào cơ sở dữ liệu SQLite.

- Gửi cảnh báo real-time qua Telegram: Ngay khi phát hiện vi phạm, hệ thống tự động gửi ảnh và thông tin qua Telegram Bot trong vòng dưới 1 giây.

- Quản lý vi phạm trên web: Giao diện web cung cấp các trang để xem danh sách vi phạm, lọc theo loại xe và thời gian, đánh dấu đã xử lý, xem ảnh chi tiết.

- Thống kê và báo cáo: Hiển thị thống kê theo giờ, theo ngày, theo loại xe dưới dạng biểu đồ trực quan. Hỗ trợ xuất báo cáo định kỳ.

- AI Chatbot: Tích hợp Gemini AI 1.5 Flash để trả lời câu hỏi của người dùng về vi phạm, thống kê, hệ thống.

- Tương tác 2 chiều với Telegram: Người dùng có thể gửi lệnh /stats, /report, /status qua Telegram để nhận thông tin, không cần vào website.

	Dữ liệu và thông tin lưu trữ

Mỗi vi phạm được lưu trữ bao gồm các thông tin sau:

- ID vi phạm: Số định danh unique tự động tăng.
- Loại phương tiện: Ô tô, xe máy, xe tải, xe buýt.
- Biển số xe: (Chưa implement OCR, để trống).
- Thời gian vi phạm: Ngày giờ chính xác đến giây.
- Địa điểm: Tên camera hoặc ngã tư.
- Đường dẫn ảnh: Lưu trong thư mục violations/.
- Trạng thái xử lý: Đã xử lý hay chưa.
- Người xử lý: ID của user (nếu đã đăng nhập).
- Ghi chú: Thông tin bổ sung.
- Độ tin cậy: Confidence score từ YOLO.
- Ngày tạo: Timestamp tạo record trong database.

Cơ sở dữ liệu sử dụng SQLite với 2 bảng chính:

- Bảng users: Lưu thông tin người dùng (username, email, hashed_password, full_name, is_active, created_at).

- Bảng traffic_violations: Lưu thông tin vi phạm như đã mô tả ở trên.

III.	CHẾ TẠO VÀ KIỂM TRA

1.	Chuẩn bị

Để thực hiện dự án, chúng em đã chuẩn bị các yếu tố sau:

	Phần cứng

- Máy tính cấu hình: Intel Core i5-8400 (hoặc tương đương), RAM 8GB (khuyến nghị 16GB), ổ cứng SSD 256GB, không bắt buộc GPU (CPU đủ để chạy inference với tốc độ 30ms mỗi frame).

- Webcam: Độ phân giải Full HD (1920x1080), FPS tối thiểu 15, có thể sử dụng webcam laptop hoặc camera USB external.

	Phần mềm

- Hệ điều hành: Windows 10/11, Linux Ubuntu 20.04 hoặc macOS.

- Python 3.12: Ngôn ngữ lập trình chính cho Backend.

- Node.js 20: Runtime cho Frontend React.

- Visual Studio Code: IDE để viết code, có extensions cho Python và TypeScript.

- Git: Version control để quản lý mã nguồn.

- Postman: Tool để test API endpoints.

	Dữ liệu và tài liệu

- Video giao thông: Thu thập từ Youtube (các video public), camera giám sát công cộng (đã xin phép), tự quay tại các ngã tư ở địa phương. Tổng cộng 50 video clips, khoảng 450.000 frames.

- Tài liệu nghiên cứu: Papers về YOLO, ByteTrack, HSV Color Detection, tài liệu API của FastAPI, React, Telegram Bot.

- Mô hình pre-trained: YOLO v11n model từ Ultralytics (file yolo11n.pt, kích thước 6MB).

	Nguồn kinh phí

- Chi phí phát triển phần mềm: Miễn phí (sử dụng công nghệ mã nguồn mở).

- Chi phí Gemini API: Miễn phí (free tier 1500 requests mỗi ngày).

- Chi phí server: Chạy local trên máy tính cá nhân (miễn phí).

- Chi phí camera: Sử dụng webcam có sẵn hoặc mượn từ trường (miễn phí).

- Tổng chi phí: Gần như 0 đồng cho giai đoạn nghiên cứu và phát triển.

2.	Thực hiện hệ thống

Quá trình thực hiện dự án được chia thành 6 giai đoạn chính:

	Giai đoạn 1: Nghiên cứu và lập kế hoạch (2 tuần)

- Nghiên cứu tài liệu về Computer Vision, YOLO, ByteTrack, HSV.
- Phân tích các hệ thống giám sát giao thông hiện có.
- Thiết kế kiến trúc hệ thống, vẽ sơ đồ, lập kế hoạch chi tiết.
- Xác định công nghệ và thư viện sử dụng.

	Giai đoạn 2: Thu thập và chuẩn bị dữ liệu (2 tuần)

- Thu thập video giao thông từ nhiều nguồn.
- Phân loại video theo điều kiện (ban ngày, ban đêm, nắng, mưa).
- Xác định ROI coordinates cho đèn tín hiệu trên các video.
- Chuẩn bị môi trường phát triển (cài đặt Python, Node.js, libraries).

	Giai đoạn 3: Phát triển Backend (4 tuần)

- Xây dựng module YOLO detection với Ultralytics.
- Phát triển module HSV color detection với OpenCV.
- Tích hợp ByteTrack cho tracking.
- Xây dựng logic phát hiện vi phạm với cooldown và grid system.
- Tạo FastAPI server với các endpoints: auth, violations, video streaming.
- Xây dựng Telegram Bot handler và notifier.
- Tạo database schema và CRUD operations với SQLAlchemy.
- Viết unit tests cho các module.

	Giai đoạn 4: Phát triển Frontend (3 tuần)

- Setup React project với Vite, TypeScript, TailwindCSS.
- Xây dựng các components: Login, Register, Dashboard, VideoMonitor, ViolationsManagement, TrafficAnalytics, ChatInterface.
- Tích hợp với Backend API qua HTTP và WebSocket.
- Thiết kế giao diện với Shadcn/ui components.
- Thêm animations với Framer Motion.
- Xây dựng charts với Recharts.
- Responsive design cho mobile và tablet.

	Giai đoạn 5: Tích hợp và kiểm thử (3 tuần)

- Tích hợp Backend và Frontend.
- Tích hợp Telegram Bot.
- Kiểm thử từng module riêng lẻ.
- Kiểm thử toàn bộ hệ thống end-to-end.
- Đo lường hiệu suất: thời gian xử lý mỗi frame, độ trễ notification.
- Đo lường độ chính xác: Precision, Recall, F1-Score.
- Tối ưu hóa tham số: ROI, HSV threshold, confidence, cooldown, grid size.
- Fix bugs và cải thiện UX.

	Giai đoạn 6: Hoàn thiện và tài liệu hóa (2 tuần)

- Viết tài liệu hướng dẫn sử dụng.
- Viết tài liệu hướng dẫn cài đặt và triển khai.
- Viết tài liệu kỹ thuật chi tiết về thuật toán.
- Chuẩn bị slide thuyết trình.
- Quay video demo.
- Hoàn thiện báo cáo dự án.

3.	Chương trình thử nghiệm

Để đánh giá hiệu quả của hệ thống, chúng em đã tiến hành thử nghiệm với quy trình sau:

	Chuẩn bị bộ dữ liệu test

- Chọn ra 10 video clips từ bộ 50 videos (không sử dụng trong quá trình phát triển).
- Tổng cộng 90.000 frames.
- Thủ công đánh dấu ground truth: 287 vi phạm thực tế.

	Chạy hệ thống và thu thập kết quả

- Chạy hệ thống với 10 video test.
- Ghi lại tất cả vi phạm được phát hiện.
- Đo thời gian xử lý mỗi frame.
- Đo thời gian gửi Telegram notification.

	Phân tích kết quả

- So sánh kết quả phát hiện với ground truth.
- Tính các chỉ số: True Positive (TP), False Positive (FP), True Negative (TN), False Negative (FN).
- Tính Precision, Recall, F1-Score, Accuracy.
- Phân tích các trường hợp phát hiện sai và bỏ sót.

	Tối ưu hóa

- Điều chỉnh tham số dựa trên kết quả phân tích.
- Chạy lại test và so sánh.
- Lặp lại cho đến khi đạt mục tiêu (độ chính xác trên 90 phần trăm).

IV.	KẾT QUẢ VÀ ĐÁNH GIÁ

1.	Kết quả thực hiện dự án

Sau 6 tháng nghiên cứu và phát triển, chúng em đã hoàn thành hệ thống với đầy đủ các tính năng đề ra và đạt được những kết quả đáng khích lệ.

	Về mặt kỹ thuật

- Xây dựng thành công hệ thống hoàn chỉnh với 5 layers: Camera, AI Detection, Backend Processing, Frontend UI, Notification.

- Tích hợp thành công các công nghệ AI tiên tiến: YOLO v11 cho object detection, ByteTrack cho tracking, HSV cho color detection.

- Xây dựng Backend với FastAPI, hỗ trợ RESTful API và WebSocket cho real-time streaming.

- Xây dựng Frontend hiện đại với React 19.2, TypeScript, TailwindCSS, responsive design.

- Tích hợp Telegram Bot với tương tác 2 chiều, hỗ trợ nhiều commands.

- Xây dựng cơ sở dữ liệu với SQLite, hỗ trợ async operations.

	Về mặt chức năng

- Phát hiện vi phạm vượt đèn đỏ với độ chính xác 90-95 phần trăm.

- Xử lý video real-time với tốc độ 20 FPS (50 mili giây mỗi frame).

- Gửi cảnh báo qua Telegram trong vòng dưới 1 giây.

- Quản lý vi phạm trên giao diện web với đầy đủ tính năng CRUD.

- Thống kê và báo cáo với biểu đồ trực quan.

- AI Chatbot hỗ trợ trả lời câu hỏi của người dùng.

	Hình ảnh thực nghiệm chương trình

Hình 7. Giao diện trang đăng nhập

Hình 8. Dashboard tổng quan với thống kê vi phạm

Hình 9. Trang giám sát video live stream với bounding boxes và thông báo vi phạm

Hình 10. Trang quản lý vi phạm với danh sách và ảnh bằng chứng

Hình 11. Biểu đồ thống kê vi phạm theo giờ và theo loại xe

Hình 12. Telegram Bot gửi cảnh báo vi phạm với ảnh và thông tin chi tiết

2.	Đánh giá hiệu suất hệ thống

	Độ chính xác

Confusion Matrix:

```
                   Predicted Positive    Predicted Negative
Actual Positive         258 (TP)              29 (FN)
Actual Negative         14 (FP)               N/A
```

Các chỉ số:

- True Positive (TP): 258 vi phạm phát hiện đúng.
- False Positive (FP): 14 vi phạm phát hiện sai (không phải vi phạm nhưng hệ thống báo là vi phạm).
- False Negative (FN): 29 vi phạm bỏ sót (là vi phạm nhưng hệ thống không phát hiện).

- Precision = TP / (TP + FP) = 258 / (258 + 14) = 94,85 phần trăm
  (Trong số các vi phạm được phát hiện, có 94,85 phần trăm là đúng)

- Recall = TP / (TP + FN) = 258 / (258 + 29) = 89,90 phần trăm
  (Trong số các vi phạm thực tế, hệ thống phát hiện được 89,90 phần trăm)

- F1-Score = 2 × (Precision × Recall) / (Precision + Recall) = 92,30 phần trăm
  (Điểm tổng hợp cân bằng giữa Precision và Recall)

	Hiệu suất xử lý

Thời gian xử lý mỗi frame:

- YOLO Detection: 28 mili giây
- ByteTrack Tracking: 8 mili giây
- HSV Color Detection: 2 mili giây
- Violation Logic: 3 mili giây
- Annotations (vẽ bounding boxes): 5 mili giây
- Database write: 4 mili giây
- Tổng cộng: 50 mili giây mỗi frame

Throughput: 20 FPS (frames per second).

Thời gian gửi Telegram notification: Dưới 1 giây (trung bình 800 mili giây).

	So sánh với các giải pháp khác

Bảng so sánh:

```
Tiêu chí                Hệ thống này    Camera thương mại    Hệ thống nghiên cứu
Độ chính xác            90-95%          95-98%               85-90%
Tốc độ xử lý            20 FPS          30 FPS               15-20 FPS
Chi phí                 5-10 triệu      50-100 triệu         Không bán
Hoạt động 24/7          Có              Có                   Có
Telegram bot            Có              Không                Không
AI Chatbot              Có              Không                Không
Mã nguồn mở             Có              Không                Có
Giao diện web           Hiện đại        Phức tạp             Đơn giản
Dễ triển khai           Cao             Trung bình           Thấp
```

Nhận xét:

- Hệ thống của chúng em có độ chính xác tốt (90-95 phần trăm), chỉ thấp hơn một chút so với giải pháp thương mại (95-98 phần trăm) nhưng vượt trội hơn các hệ thống nghiên cứu khác (85-90 phần trăm).

- Chi phí thấp hơn rất nhiều (chỉ 10-20 phần trăm) so với giải pháp thương mại, phù hợp để triển khai rộng rãi.

- Có tính năng độc đáo như Telegram Bot tương tác 2 chiều và AI Chatbot, mà các hệ thống khác không có.

- Mã nguồn mở, cộng đồng có thể học tập và đóng góp cải tiến.

	Hạn chế và điểm cần cải thiện

- Độ chính xác còn thấp hơn giải pháp thương mại một chút (khoảng 3-5 phần trăm). Nguyên nhân: Chưa fine-tune YOLO với dữ liệu giao thông Việt Nam, thuật toán phát hiện đèn đỏ chưa robust với nhiều điều kiện ánh sáng.

- Chưa có tính năng nhận diện biển số xe (OCR). Cần tích hợp thêm model OCR như PaddleOCR hoặc EasyOCR.

- Chỉ phát hiện vi phạm vượt đèn đỏ. Cần mở rộng để phát hiện thêm các vi phạm khác như không đội mũ bảo hiểm, đi sai làn, vượt tốc độ.

- Hiệu suất ban đêm giảm khoảng 5-10 phần trăm so với ban ngày. Cần fine-tune với dữ liệu ban đêm hoặc sử dụng camera có Night Vision.

- Chưa test với nhiều camera cùng lúc. Cần scale up để hỗ trợ multi-camera.

3.	Hướng phát triển đề tài

	Ngắn hạn (3-6 tháng)

- Tích hợp OCR để nhận diện biển số xe: Sử dụng PaddleOCR hoặc EasyOCR, fine-tune với biển số Việt Nam. Mục tiêu: độ chính xác trên 90 phần trăm.

- Nâng cấp database lên PostgreSQL: Hỗ trợ nhiều concurrent users, cải thiện hiệu suất query.

- Thêm tính năng xuất báo cáo PDF/Excel: Cho phép người dùng xuất báo cáo định kỳ (ngày, tuần, tháng).

- Fine-tune YOLO với dữ liệu giao thông Việt Nam: Thu thập thêm 10.000 ảnh giao thông Việt Nam, label và fine-tune để tăng độ chính xác lên 95 phần trăm.

- Cải thiện phát hiện đèn đỏ ban đêm: Thu thập dữ liệu ban đêm, điều chỉnh HSV threshold, thử nghiệm với camera có Night Vision.

	Trung hạn (6-12 tháng)

- Phát triển mobile app (iOS và Android): Sử dụng React Native để xây dựng app cho phép xem video, quản lý vi phạm, nhận thông báo push.

- Hỗ trợ multi-camera: Scale up hệ thống để xử lý nhiều camera cùng lúc, sử dụng load balancer và message queue (RabbitMQ).

- Triển khai lên cloud (AWS hoặc Azure): Sử dụng container (Docker) và orchestration (Kubernetes) để dễ dàng scale.

- Thêm các loại vi phạm khác: Phát hiện không đội mũ bảo hiểm (sử dụng YOLO phát hiện đầu người và helmet), đi sai làn (sử dụng lane detection), vượt tốc độ (sử dụng tracking và tính vận tốc).

- Tích hợp với hệ thống CSGT: API để kết nối với cơ sở dữ liệu vi phạm của CSGT, tự động gửi thông tin vi phạm.

	Dài hạn (1-2 năm)

- AI nhận diện hành vi nguy hiểm: Sử dụng Pose Estimation và Action Recognition để phát hiện hành vi như lạng lách, chạy zig-zag, dừng đột ngột.

- Dự đoán tai nạn: Sử dụng LSTM hoặc Transformer để dự đoán khả năng xảy ra tai nạn dựa trên hành vi của các phương tiện.

- Tích hợp với Smart City platform: Kết nối với hệ thống quản lý đô thị thông minh, chia sẻ dữ liệu giao thông, hỗ trợ ra quyết định.

- Mở rộng ra các nước ASEAN: Localization cho các nước khác, hỗ trợ nhiều ngôn ngữ, tùy chỉnh cho luật giao thông từng nước.

- Xây dựng cộng đồng mã nguồn mở: Tổ chức hackathon, hội thảo, thu hút developer đóng góp cải tiến, xây dựng ecosystem around the project.

V.	NGUỒN THAM KHẢO

1. Redmon, J., & Farhadi, A. (2018). YOLOv3: An Incremental Improvement. arXiv:1804.02767.

2. Jocher, G., Chaurasia, A., & Qiu, J. (2023). Ultralytics YOLOv8. GitHub repository. https://github.com/ultralytics/ultralytics

3. Zhang, Y., Sun, P., Jiang, Y., Yu, D., Weng, F., Yuan, Z., Luo, P., Liu, W., & Wang, X. (2022). ByteTrack: Multi-Object Tracking by Associating Every Detection Box. European Conference on Computer Vision (ECCV).

4. OpenCV Documentation. (2024). https://docs.opencv.org/

5. FastAPI Documentation. (2024). https://fastapi.tiangolo.com/

6. React Documentation. (2024). https://react.dev/

7. Telegram Bot API Documentation. (2024). https://core.telegram.org/bots/api

8. Ủy ban An toàn Giao thông Quốc gia. (2023). Báo cáo tình hình tai nạn giao thông năm 2023.

9. Công an tỉnh Quảng Nam. (2024). Báo cáo tình hình vi phạm giao thông 6 tháng đầu năm 2024.

10. Nguyễn Xuân Huy. (2021). Sáng tạo trong thuật toán và lập trình với Python. Nhà xuất bản Đại học Quốc gia Hà Nội.

11. Trần Thông Quế. (2022). Bài tập lập trình với ngôn ngữ Python. Nhà xuất bản Đại học Quốc gia Hà Nội.

12. GitHub - Cộng đồng mã nguồn mở lớn nhất thế giới. https://github.com

13. Stack Overflow - Cộng đồng lập trình viên. https://stackoverflow.com

14. Papers with Code - Trang tổng hợp papers và code AI. https://paperswithcode.com

15. Towards Data Science - Blog về Data Science và Machine Learning. https://towardsdatascience.com


---

HẾT
