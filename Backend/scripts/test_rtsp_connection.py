#!/bin/bash

# ========================================================================
#   SCRIPT KIỂM TRA RTSP CAMERA
#   Mục đích: Test kết nối camera RTSP trước khi tích hợp vào hệ thống
# ========================================================================

import cv2
import sys
from datetime import datetime

def test_rtsp_connection(rtsp_url, duration=10):
    """
    Test RTSP camera connection
    
    Args:
        rtsp_url: RTSP URL của camera
        duration: Thời gian test (giây)
    """
    print("="*70)
    print("  SMART TRAFFIC - RTSP CAMERA CONNECTION TEST")
    print("="*70)
    print(f"\n📹 RTSP URL: {rtsp_url}")
    print(f"⏱️  Duration: {duration} giây")
    print(f"🕒 Start time: {datetime.now().strftime('%H:%M:%S')}\n")
    
    # Mở camera
    print("⏳ Đang kết nối camera...")
    cap = cv2.VideoCapture(rtsp_url)
    
    if not cap.isOpened():
        print("❌ LỖI: Không thể kết nối camera!")
        print("\n🔍 Các nguyên nhân có thể:")
        print("   1. RTSP URL sai format")
        print("   2. IP camera không đúng")
        print("   3. Username/password sai")
        print("   4. Camera offline hoặc bị lỗi")
        print("   5. Firewall chặn port 554")
        print("   6. Network không kết nối được camera")
        return False
    
    print("✅ Kết nối thành công!\n")
    
    # Lấy thông tin camera
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print("📊 THÔNG TIN CAMERA:")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Codec: {cap.get(cv2.CAP_PROP_FOURCC)}")
    print()
    
    # Test đọc frames
    print(f"⏳ Đang test đọc frames trong {duration} giây...")
    print("   (Nhấn 'q' để dừng sớm)\n")
    
    frame_count = 0
    error_count = 0
    start_time = datetime.now()
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            error_count += 1
            print(f"⚠️  Frame {frame_count}: Lỗi đọc (total errors: {error_count})")
            if error_count > 10:
                print("\n❌ Quá nhiều lỗi! Dừng test.")
                break
            continue
        
        frame_count += 1
        
        # Hiển thị frame (resize nếu quá lớn)
        if width > 1280:
            scale = 1280 / width
            display_frame = cv2.resize(frame, None, fx=scale, fy=scale)
        else:
            display_frame = frame
            
        # Thêm thông tin lên frame
        cv2.putText(display_frame, f"Frame: {frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(display_frame, f"Time: {datetime.now().strftime('%H:%M:%S')}", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('RTSP Test - Press Q to quit', display_frame)
        
        # Check thời gian
        elapsed = (datetime.now() - start_time).total_seconds()
        if elapsed >= duration:
            break
            
        # Nhấn 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n⏹️  Người dùng dừng test")
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    # Kết quả
    actual_fps = frame_count / elapsed if elapsed > 0 else 0
    
    print("\n")
    print("="*70)
    print("  KẾT QUẢ TEST")
    print("="*70)
    print(f"✅ Tổng frames đọc được: {frame_count}")
    print(f"❌ Số lỗi: {error_count}")
    print(f"⏱️  Thời gian thực tế: {elapsed:.1f} giây")
    print(f"📈 FPS thực tế: {actual_fps:.1f}")
    print(f"📊 Tỷ lệ thành công: {(frame_count/(frame_count+error_count)*100):.1f}%")
    
    # Đánh giá
    print("\n🎯 ĐÁNH GIÁ:")
    if error_count == 0 and actual_fps >= fps * 0.8:
        print("   ✅ XUẤT SẮC - Camera hoạt động rất tốt!")
    elif error_count < 5 and actual_fps >= fps * 0.6:
        print("   ✅ TỐT - Camera hoạt động ổn định")
    elif error_count < 10:
        print("   ⚠️  TRUNG BÌNH - Camera có một số lỗi")
    else:
        print("   ❌ KÉM - Camera không ổn định, cần kiểm tra lại")
    
    print("\n💡 KHUYẾN NGHỊ:")
    if width >= 1920:
        print("   - Resolution cao (1080p+), cần CPU/GPU mạnh")
    if actual_fps < 10:
        print("   - FPS thấp, kiểm tra băng thông mạng")
    if error_count > 5:
        print("   - Nhiều lỗi frame, kiểm tra network và camera")
    
    print("\n")
    return True


if __name__ == "__main__":
    # Hướng dẫn
    if len(sys.argv) < 2:
        print("\n🎬 HƯỚNG DẪN SỬ DỤNG:")
        print("="*70)
        print("python test_rtsp_connection.py <rtsp_url> [duration]\n")
        print("VÍ DỤ:")
        print('  python test_rtsp_connection.py "rtsp://admin:pass@192.168.1.64:554/stream1"')
        print('  python test_rtsp_connection.py "rtsp://camera-ip:554/stream1" 20')
        print("\nFORMAT RTSP URL:")
        print('  rtsp://[username]:[password]@[ip]:[port]/[path]')
        print("\nCÁC HÃNG CAMERA PHỔ BIẾN:")
        print('  Hikvision: rtsp://admin:pass@ip:554/Streaming/Channels/101')
        print('  Dahua:     rtsp://admin:pass@ip:554/cam/realmonitor?channel=1&subtype=0')
        print('  Axis:      rtsp://root:pass@ip/axis-media/media.amp')
        print('  TP-Link:   rtsp://admin:pass@ip:554/stream1')
        print("="*70)
        sys.exit(1)
    
    rtsp_url = sys.argv[1]
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    try:
        test_rtsp_connection(rtsp_url, duration)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test bị dừng bởi người dùng")
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")
        import traceback
        traceback.print_exc()
