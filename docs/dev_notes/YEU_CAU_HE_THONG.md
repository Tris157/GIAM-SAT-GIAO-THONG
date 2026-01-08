# 🖥️ YÊU CẦU HỆ THỐNG CHI TIẾT

**Dành cho:** Triển khai Smart Traffic Monitoring System  
**Phiên bản:** 3.0.0  
**Ngày:** 11/12/2024

---

## 📋 TỔNG QUAN YÊU CẦU

Tài liệu này mô tả chi tiết các yêu cầu phần cứng, mạng và môi trường để triển khai hệ thống.

---

## 💻 YÊU CẦU PHẦN CỨNG

### CẤU HÌNH TỐI THIỂU (1-2 camera)

| Thành phần | Yêu cầu | Ghi chú |
|------------|---------|---------|
| **CPU** | Intel Core i5-8400 (6 cores) hoặc AMD Ryzen 5 2600 | Clock >= 2.8 GHz |
| **RAM** | 8 GB DDR4 | Dùng được nhưng sẽ lag khi nhiều camera |
| **GPU** | Không bắt buộc | CPU inference ~10-15 FPS |
| **Ổ cứng** | 50 GB HDD | Cho OS + App + Data 1 tuần |
| **Network Card** | 100 Mbps Ethernet | WiFi không khuyến nghị |
| **Monitor** | 1366x768 | Để hiển thị dashboard |

**Hiệu suất:**
- 1 camera 720p: 10-12 FPS
- 2 camera 720p: 5-8 FPS mỗi camera
- Độ trễ: 1-2 giây

---

### CẤU HÌNH KHUYẾN NGHỊ (5-10 camera)

| Thành phần | Yêu cầu | Ghi chú |
|------------|---------|---------|
| **CPU** | Intel Core i7-10700 (8 cores) hoặc AMD Ryzen 7 3700X | Clock >= 3.6 GHz |
| **RAM** | 16 GB DDR4 | 32 GB nếu > 10 camera |
| **GPU** | NVIDIA GTX 1650 (4GB VRAM) | Hoặc RTX 3050 |
| **Ổ cứng** | 120 GB SSD (OS) + 500 GB HDD (Data) | SSD tăng tốc đáng kể |
| **Network Card** | 1 Gbps Ethernet | Gigabit LAN |
| **UPS** | 1000 VA | Phòng mất điện đột ngột |

**Hiệu suất:**
- 5 camera 1080p: 15-20 FPS mỗi camera
- 10 camera 720p: 12-15 FPS mỗi camera
- Độ trễ: < 500ms

---

### CẤU HÌNH CAO CẤP (20+ camera, Production)

| Thành phần | Yêu cầu | Ghi chú |
|------------|---------|---------|
| **CPU** | Intel Xeon E-2288G hoặc AMD EPYC 7302P | 16+ cores |
| **RAM** | 64 GB DDR4 ECC | Error-correcting memory |
| **GPU** | NVIDIA RTX 3060 (12GB) hoặc RTX 4060 Ti | 2x GPU nếu > 30 camera |
| **Storage** | 256 GB NVMe SSD (OS) + 2 TB Enterprise HDD (Data) | RAID 1 khuyến nghị |
| **Network** | 10 Gbps Fiber hoặc Dual 1Gbps bonded | Redundancy |
| **UPS** | 2000 VA với auto-shutdown | Runtime >= 30 phút |
| **Cooling** | Rack cooling system | Nhiệt độ phòng < 25°C |

**Hiệu suất:**
- 20 camera 1080p: 20-25 FPS mỗi camera
- 50 camera 720p: 15-20 FPS mỗi camera
- Độ trễ: < 200ms

---

## 🌐 YÊU CẦU MẠNG

### Băng Thông Internet

| Số Camera | Resolution | FPS | Băng thông upload | Băng thông download |
|-----------|-----------|-----|-------------------|---------------------|
| 1 | 720p (HD) | 15 | 2 Mbps | 1 Mbps |
| 1 | 1080p (Full HD) | 30 | 5-8 Mbps | 1 Mbps |
| **2 (chính + phụ)** | **1080p + 1080p** | **30 + 15** | **7-10 Mbps** | **2 Mbps** |
| 5 | 720p | 15 | 10 Mbps | 2 Mbps |
| 5 | 1080p | 20 | 25-40 Mbps | 5 Mbps |
| 10 | 720p | 15 | 20 Mbps | 5 Mbps |
| 10 | 1080p | 20 | 50-80 Mbps | 10 Mbps |

**Lưu ý:**
- Upload cao vì camera stream về server, Download thấp vì chỉ gửi API/dashboard
- **Hệ thống vượt đèn đỏ cần 2 camera:** camera chính (giám sát đường) + camera phụ (nhìn đèn)

---

### Cấu Hình Mạng LAN

#### Switch/Router yêu cầu:
- **Gigabit LAN ports** (1000 Mbps)
- **VLAN support** (tách traffic camera riêng)
- **QoS (Quality of Service)** để ưu tiên camera traffic
- **PoE (Power over Ethernet)** nếu camera hỗ trợ

#### IP Configuration:
```
Server IP: 192.168.1.100 (Static)
Camera Pool: 192.168.1.101 - 192.168.1.199
Gateway: 192.168.1.1
Subnet: 255.255.255.0 (/24)
DNS: 8.8.8.8, 8.8.4.4
```

---

### Độ Trễ (Latency) \u0026 Packet Loss

| Metric | Tối đa chấp nhận | Khuyến nghị | Ảnh hưởng nếu vượt |
|--------|------------------|-------------|--------------------|
| **Latency** | 500 ms | < 100 ms | Video giật, trễ phát hiện |
| **Jitter** | 50 ms | < 20 ms | Frame bị drop |
| **Packet Loss** | 5% | < 1% | Mất khung hình |

**Test latency:**
```bash
# Ping camera
ping -n 100 192.168.1.101

# Iperf test bandwidth
iperf3 -c 192.168.1.101 -t 30
```

---

### Ports Cần Mở

#### Inbound (Vào server):
| Port | Protocol | Mục đích |
|------|----------|----------|
| 8000 | TCP | Backend API |
| 5173 | TCP | Frontend Dev Server (production: 80/443) |
| 554 | TCP/UDP | RTSP camera streams |
| 1935 | TCP | RTMP streams (nếu dùng) |

#### Outbound (Ra internet):
| Port | Protocol | Mục đích |
|------|----------|----------|
| 443 | TCP | HTTPS API calls (Google Gemini, Telegram) |
| 80 | TCP | HTTP requests |

**Firewall rules:**
```bash
# Windows Firewall
netsh advfirewall firewall add rule name="Traffic Backend" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="RTSP Cameras" dir=in action=allow protocol=TCP localport=554

# Linux UFW
sudo ufw allow 8000/tcp
sudo ufw allow 554/tcp
sudo ufw allow 554/udp
```

---

## 📹 YÊU CẦU CAMERA

### Hệ Thống 2 Camera (Phát Hiện Vượt Đèn Đỏ)

Để phát hiện vi phạm vượt đèn đỏ chính xác (độ chính xác 95%+), hệ thống yêu cầu:

**Camera Chính (Giám Sát Giao Thông):**
- Mục đích: Phát hiện và theo dõi xe cộ trên làn đường
- Vị trí: Nhìn xuống đường, bao quát 2-3 làn xe
- Resolution: 1280x720 (khuyến nghị 1920x1080)
- FPS: 15-30
- Góc nhìn: 30-45° xuống đường

**Camera Phụ (Giám Sát Đèn Tín Hiệu) - BẮT BUỘC:**
- Mục đích: Nhận diện màu đèn tín hiệu (đỏ-vàng-xanh)
- Vị trí: Nhìn thẳng vào mặt đèn tín hiệu
- Resolution: 1920x1080 (Full HD) - **BẮT BUỘC**
- FPS: 15-30
- Góc lệch: < 30° so với trục đèn
- Khoảng cách: 10-30m từ đèn
- Yêu cầu đặc biệt:
  - ✅ Chống ngược sáng (WDR/HDR)
  - ✅ Hoạt động tốt ban đêm (Low Light/IR)
  - ✅ Đèn tín hiệu chiếm 5-10% khung hình
  - ✅ Nhìn rõ cả 3 đèn (đỏ-vàng-xanh)

**Khuyến nghị mua camera phụ:**
- Hikvision DS-2CD2043G0-I (2MP, WDR, IR 30m)
- Dahua IPC-HFW2231S-S-S2 (2MP, Starlight, WDR)
- AXIS M3045-V (1080p, WDR, PoE)
- Giá tham khảo: 2-5 triệu VNĐ

### Thông Số Kỹ Thuật Camera Chung

| Tham số | Tối thiểu | Khuyến nghị | Tối đa |
|---------|-----------|-------------|--------|
| **Resolution** | 640x480 (VGA) | 1280x720 (HD) | 1920x1080 (Full HD) |
| **Frame Rate** | 10 FPS | 15-20 FPS | 30 FPS |
| **Bitrate** | 512 Kbps | 2-4 Mbps | 8 Mbps |
| **Codec** | H.264 | H.264/H.265 | H.265 (HEVC) |
| **Protocol** | RTSP | RTSP hoặc RTMP | RTSP + Onvif |

### Vị Trí Lắp Đặt Camera

**Chiều cao:** 4-6 mét từ mặt đất  
**Góc nghiêng:** 30-45 độ xuống đường  
**Tầm nhìn:** Bao quát 2-3 làn xe  
**Ánh sáng:** Đủ sáng hoặc có IR night vision  

**Góc camera tốt:**
```
      [Camera]
         /|\
        / | \
       /  |  \
      /   |   \
     /    ↓    \
    [====Road====]
    30-45° angle
```

**Góc camera XẤU (không nên):**
- Quá cao (> 8m): Xe nhỏ, khó nhận diện
- Quá thấp (< 3m): Bị che khuất
- Nghiêng quá 60°: Chỉ thấy nóc xe
- Ngược sáng: Ảnh tối, AI hoạt động kém

---

### RTSP URL Format

**Chuẩn RTSP URL:**
```
rtsp://[username]:[password]@[camera-ip]:[port]/[path]
```

**Ví dụ các hãng camera:**

| Hãng | URL Format |
|------|-----------|
| **Hikvision** | `rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101` |
| **Dahua** | `rtsp://admin:password@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0` |
| **Axis** | `rtsp://root:password@192.168.1.100/axis-media/media.amp` |
| **Foscam** | `rtsp://admin:password@192.168.1.50:554/videoMain` |
| **TP-Link** | `rtsp://admin:password@192.168.1.20:554/stream1` |
| **Generic** | `rtsp://192.168.1.xxx:554/stream` |

**Test RTSP bằng VLC:**
```
1. Mở VLC Media Player
2. Media → Open Network Stream
3. Nhập RTSP URL
4. Click Play
→ Nếu thấy video = OK
```

---

## 🔐 YÊU CẦU BẢO MẬT

### Tài Khoản Hệ Thống

**Backend Admin:**
- Username: admin
- Password: >= 12 ký tự, có chữ hoa, số, ký tự đặc biệt
- 2FA: Khuyến nghị bật

**Database:**
- Mật khẩu riêng, không dùng "admin/root"
- Backup tự động hàng ngày

**Camera:**
- Đổi password mặc định ngay khi lắp
- Không dùng "admin/admin" hoặc "admin/12345"

---

### Network Security

**Checklist:**
- [ ] Camera và server trong VLAN riêng
- [ ] Firewall chặn truy cập ngoài không cần thiết
- [ ] VPN cho remote access
- [ ] SSL/TLS cho web interface (HTTPS)
- [ ] Định kỳ update firmware camera

---

## 💾 YÊU CẦU LƯU TRỮ

### Ước Tính Dung Lượng

**Database (SQLite):**
| Records | Dung lượng |
|---------|-----------|
| 10,000 records | ~10 MB |
| 100,000 records | ~100 MB |
| 1,000,000 records | ~1 GB |

**Ảnh vi phạm:**
| Số ảnh/ngày | Độ phân giải | Dung lượng/ngày | Dung lượng/tháng |
|-------------|--------------|-----------------|------------------|
| 100 | 720p | ~50 MB | ~1.5 GB |
| 500 | 1080p | ~300 MB | ~9 GB |
| 1000 | 1080p | ~600 MB | ~18 GB |

**Tổng dung lượng cần (1 tháng):**
- 5 camera, 500 vi phạm/ngày: ~15 GB
- 10 camera, 1000 vi phạm/ngày: ~30 GB

**Chiến lược lưu trữ:**
```
- Tuần 1-2: Giữ full quality
- Tuần 3-4: Nén xuống 80% quality
- > 1 tháng: Archive hoặc xóa
```

---

## ⚡ YÊU CẦU ĐIỆN NĂNG

### Công Suất Tiêu Thụ

| Thiết bị | Công suất | Số lượng | Tổng |
|----------|-----------|---------|------|
| Server (i7 + GTX 1650) | 200W | 1 | 200W |
| Monitor 24" | 30W | 1 | 30W |
| Switch Gigabit 16 ports | 15W | 1 | 15W |
| Camera IP PoE | 5-10W | 10 | 100W |
| **Tổng cộng** | | | **345W** |

**UPS khuyến nghị:** 1000 VA (600W)  
**Thời gian backup:** 20-30 phút

**Hóa đơn điện ước tính (24/7):**
```
345W x 24h x 30 ngày = 248 kWh/tháng
Giá điện ~2500đ/kWh → ~620,000 VNĐ/tháng
```

---

## 🌡️ YÊU CẦU MÔI TRƯỜNG

### Nhiệt Độ \u0026 Độ Ẩm

| Thành phần | Nhiệt độ | Độ ẩm |
|------------|----------|-------|
| **Server** | 10°C - 35°C | 20% - 80% |
| **Camera ngoài trời** | -10°C - 50°C | 0% - 95% |
| **UPS** | 0°C - 40°C | < 90% |

**Khuyến nghị:**
- Phòng máy có điều hòa
- Hệ thống thông gió tốt
- Tránh ánh nắng trực tiếp vào camera

---

## ✅ CHECKLIST TỔNG HỢP

### Trước Khi Triển Khai:
- [ ] Đã kiểm tra phần cứng đủ yêu cầu
- [ ] Băng thông internet >= 10 Mbps/camera
- [ ] Switch hỗ trợ Gigabit LAN
- [ ] Camera có thể truy cập qua RTSP
- [ ] Đã chuẩn bị IP tĩnh cho server
- [ ] UPS dự phòng
- [ ] Ổ cứng dự trữ >= 100 GB

### Sau Khi Cài Đặt:
- [ ] Server chạy ổn định > 24h
- [ ] CPU usage < 70% khi full load
- [ ] RAM usage < 80%
- [ ] Network latency < 100ms
- [ ] Tất cả camera stream OK
- [ ] AI detection accuracy > 80%
- [ ] Backup tự động đã cấu hình

---

**© 2024 Smart Traffic Monitoring System - Yêu cầu hệ thống v3.0**
