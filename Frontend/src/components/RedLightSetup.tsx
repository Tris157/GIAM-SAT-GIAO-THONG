import React, { useState, useRef, useEffect } from 'react';
import './RedLightSetup.css';
import { useAuth } from '../contexts/AuthContext';

interface Point {
  x: number;
  y: number;
}

interface ROI {
  x: number;
  y: number;
  w: number;
  h: number;
}

interface RedLightConfig {
  camera_name: string;
  traffic_light_roi: ROI;
  stop_line_y: number;
  camera_source?: string;
}

const RedLightSetup: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const videoRef = useRef<HTMLImageElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [currentStep, setCurrentStep] = useState<1 | 2>(1);
  const [roiPoints, setRoiPoints] = useState<Point[]>([]);
  const [stopLinePoints, setStopLinePoints] = useState<Point[]>([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [videoLoaded, setVideoLoaded] = useState(false);
  const [useUpload, setUseUpload] = useState(false);
  const [uploadedImageUrl, setUploadedImageUrl] = useState<string>('');
  const { isAdmin } = useAuth();

  // API base URL
  const API_BASE = 'http://localhost:8000';

  // Load config khi component mount
  useEffect(() => {
    loadConfig();
    if (!isAdmin) {
      setTimeout(() => alert('⚠️ Bạn đang ở chế độ Xem. Chỉ Admin mới có thể lưu cấu hình.'), 500);
    }
  }, [isAdmin]);

  // Vẽ lại canvas khi có thay đổi
  useEffect(() => {
    if (videoLoaded) {
      drawOverlay();
    }
  }, [roiPoints, stopLinePoints, currentStep, videoLoaded]);

  // Load config từ API
  const loadConfig = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/red-light-config/load`);
      const data = await response.json();

      if (data.success && data.config) {
        const config: RedLightConfig = data.config;

        // Convert ROI thành 4 điểm
        const roi = config.traffic_light_roi;
        setRoiPoints([
          { x: roi.x, y: roi.y },
          { x: roi.x + roi.w, y: roi.y },
          { x: roi.x + roi.w, y: roi.y + roi.h },
          { x: roi.x, y: roi.y + roi.h }
        ]);

        // Set stop line (2 điểm giả để tạo đường ngang)
        const stopY = config.stop_line_y;
        setStopLinePoints([
          { x: 0, y: stopY },
          { x: 100, y: stopY }
        ]);

        setMessage('✅ Đã tải cấu hình thành công!');
        setCurrentStep(2); // Chuyển sang bước 2
      }
    } catch (error: any) {
      console.log('Chưa có cấu hình, bắt đầu từ đầu');
    }
  };

  // Lưu config qua API
  const saveConfig = async () => {
    if (!isAdmin) {
      alert('⚠️ Bạn không có quyền thực hiện hành động này. Vui lòng đăng nhập với tài khoản Admin.');
      return;
    }
    setLoading(true);
    try {
      // Tính ROI bbox từ 4 điểm
      const xValues = roiPoints.map(p => p.x);
      const yValues = roiPoints.map(p => p.y);
      const roi: ROI = {
        x: Math.min(...xValues),
        y: Math.min(...yValues),
        w: Math.max(...xValues) - Math.min(...xValues),
        h: Math.max(...yValues) - Math.min(...yValues)
      };

      // Tính Stop Line Y trung bình
      const stopLineY = Math.round(
        (stopLinePoints[0].y + stopLinePoints[1].y) / 2
      );

      const config: RedLightConfig = {
        camera_name: 'camera_live',
        traffic_light_roi: roi,
        stop_line_y: stopLineY,
        camera_source: 'web_setup'
      };

      const response = await fetch(`${API_BASE}/api/v1/red-light-config/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config)
      });

      const data = await response.json();

      if (data.success) {
        setMessage('✅ Đã lưu cấu hình thành công!');
      } else {
        setMessage('❌ Lỗi khi lưu cấu hình!');
      }
    } catch (error: any) {
      setMessage('❌ Lỗi khi lưu cấu hình: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // Vẽ overlay lên canvas
  const drawOverlay = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;

    if (!canvas || !video) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Vẽ video frame (scale từ kích thước gốc lên canvas size)
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Enable smooth rendering
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';

    // === VẼ ROI ===
    if (roiPoints.length > 0) {
      // Vẽ các điểm
      roiPoints.forEach((point, index) => {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 6, 0, 2 * Math.PI);
        ctx.fillStyle = '#00ff00';
        ctx.fill();

        // Vẽ số thứ tự
        ctx.fillStyle = '#00ff00';
        ctx.font = 'bold 16px Arial';
        ctx.fillText(String(index + 1), point.x + 10, point.y + 10);
      });

      // Vẽ đường nối
      if (roiPoints.length > 1) {
        ctx.beginPath();
        ctx.moveTo(roiPoints[0].x, roiPoints[0].y);
        for (let i = 1; i < roiPoints.length; i++) {
          ctx.lineTo(roiPoints[i].x, roiPoints[i].y);
        }
        if (roiPoints.length === 4) {
          ctx.closePath();
        }
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      // Tô màu vùng ROI nếu đủ 4 điểm
      if (roiPoints.length === 4) {
        ctx.beginPath();
        ctx.moveTo(roiPoints[0].x, roiPoints[0].y);
        for (let i = 1; i < 4; i++) {
          ctx.lineTo(roiPoints[i].x, roiPoints[i].y);
        }
        ctx.closePath();
        ctx.fillStyle = 'rgba(0, 255, 0, 0.2)';
        ctx.fill();
      }
    }

    // === VẼ STOP LINE ===
    if (stopLinePoints.length > 0) {
      // Vẽ các điểm
      stopLinePoints.forEach((point) => {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 8, 0, 2 * Math.PI);
        ctx.fillStyle = '#ff0000';
        ctx.fill();
      });

      // Vẽ đường ngang nếu đủ 2 điểm (Ở GIỮA KHUNG HÌNH)
      if (stopLinePoints.length === 2) {
        const avgY = Math.round((stopLinePoints[0].y + stopLinePoints[1].y) / 2);
        const startX = canvas.width / 4;
        const endX = (3 * canvas.width) / 4;

        ctx.beginPath();
        ctx.moveTo(startX, avgY);
        ctx.lineTo(endX, avgY);
        ctx.strokeStyle = '#ff0000';
        ctx.lineWidth = 3;
        ctx.stroke();

        // Text
        ctx.fillStyle = '#ff0000';
        ctx.font = 'bold 14px Arial';
        ctx.fillText(`STOP LINE (Y=${avgY})`, startX + 10, avgY - 10);
      }
    }

    // === VẼ HƯỚNG DẪN ===
    const instructions = currentStep === 1
      ? [
        `BƯỚC 1: VẼ ROI ĐÈN TÍN HIỆU (${roiPoints.length}/4 điểm)`,
        'Click 4 góc bao quanh đèn tín hiệu',
        'Thứ tự: Trên trái → Trên phải → Dưới phải → Dưới trái',
      ]
      : [
        `BƯỚC 2: VẼ STOP LINE (${stopLinePoints.length}/2 điểm)`,
        'Click 2 điểm bất kỳ để tạo đường ngang',
        '(Đường sẽ tự động vẽ ở giữa khung hình)',
      ];

    let yOffset = 30;
    instructions.forEach((text) => {
      // Background
      const metrics = ctx.measureText(text);
      ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
      ctx.fillRect(5, yOffset - 20, metrics.width + 10, 25);

      // Text
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 14px Arial';
      ctx.fillText(text, 10, yOffset);
      yOffset += 30;
    });
  };

  // Xử lý click chuột trên canvas
  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();

    // Tính tọa độ click trên canvas (scale theo tỷ lệ canvas thật và canvas hiển thị)
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const x = Math.round((e.clientX - rect.left) * scaleX);
    const y = Math.round((e.clientY - rect.top) * scaleY);

    console.log('[DEBUG] Click:', e.clientX - rect.left, e.clientY - rect.top, '-> Scaled:', x, y);

    if (currentStep === 1) {
      // BƯỚC 1: Vẽ ROI
      if (roiPoints.length < 4) {
        setRoiPoints([...roiPoints, { x, y }]);

        if (roiPoints.length === 3) {
          setMessage('✅ Đã chọn đủ 4 điểm ROI! Nhấn "Lưu và Tiếp tục" để chuyển sang bước 2');
        }
      }
    } else {
      // BƯỚC 2: Vẽ Stop Line
      if (stopLinePoints.length < 2) {
        setStopLinePoints([...stopLinePoints, { x, y }]);

        if (stopLinePoints.length === 1) {
          setMessage('✅ Đã vẽ Stop Line! Nhấn "Lưu Cấu Hình" để hoàn tất');
        }
      }
    }
  };

  // Reset hiện tại
  const handleReset = () => {
    if (currentStep === 1) {
      setRoiPoints([]);
      setMessage('🔄 Đã xóa ROI, vẽ lại!');
    } else {
      setStopLinePoints([]);
      setMessage('🔄 Đã xóa Stop Line, vẽ lại!');
    }
  };

  // Lưu và chuyển bước
  const handleSaveAndNext = () => {
    if (currentStep === 1) {
      if (roiPoints.length === 4) {
        setCurrentStep(2);
        setMessage('✅ Đã lưu ROI! Chuyển sang bước 2: Vẽ Stop Line');
      } else {
        setMessage('⚠️ Cần chọn đủ 4 điểm ROI!');
      }
    } else {
      if (stopLinePoints.length === 2) {
        saveConfig();
      } else {
        setMessage('⚠️ Cần chọn 2 điểm Stop Line!');
      }
    }
  };

  // Handle image load (both camera and upload)
  const handleImageLoad = () => {
    const img = videoRef.current;
    const canvas = canvasRef.current;
    if (img && canvas) {
      let width = img.naturalWidth || 640;
      let height = img.naturalHeight || 480;

      // Scale lên nếu ảnh quá nhỏ (nhỏ hơn 800px)
      const minWidth = 800;
      if (width < minWidth) {
        const scale = minWidth / width;
        width = Math.round(width * scale);
        height = Math.round(height * scale);
      }

      console.log('[DEBUG] Image loaded:', img.naturalWidth, 'x', img.naturalHeight, '-> Canvas:', width, 'x', height);
      canvas.width = width;
      canvas.height = height;
      setVideoLoaded(true);
    }
  };

  // Handle file upload
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    console.log('[DEBUG] File selected:', file.name, file.type, file.size);

    // Reset state khi upload ảnh mới
    setVideoLoaded(false);
    setRoiPoints([]);
    setStopLinePoints([]);
    setCurrentStep(1);

    const reader = new FileReader();
    reader.onload = (event) => {
      if (event.target?.result) {
        console.log('[DEBUG] File read complete, base64 length:', (event.target.result as string).length);
        setUploadedImageUrl(event.target.result as string);
        setUseUpload(true);
        setMessage('✅ Đã tải ảnh thành công! Bắt đầu vẽ ROI.');
      }
    };
    reader.onerror = (error) => {
      console.error('[DEBUG] FileReader error:', error);
      setMessage('❌ Lỗi khi đọc file ảnh!');
    };
    reader.readAsDataURL(file);
  };

  // Refresh snapshot every 2 seconds (only if not using upload)
  useEffect(() => {
    if (useUpload) return;

    const interval = setInterval(() => {
      const img = videoRef.current;
      if (img) {
        // Force reload by adding timestamp
        img.src = `${API_BASE}/api/v1/rtsp/camera_live/snapshot?t=${Date.now()}`;
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [useUpload]);

  return (
    <div className="red-light-setup">
      <div className="setup-header">
        <h2>🚦 Thiết Lập Phát Hiện Vượt Đèn Đỏ</h2>
        <p>Vẽ ROI cho đèn tín hiệu và vạch dừng trực tiếp trên video</p>
      </div>

      <div className="setup-container">
        {/* Canvas để vẽ */}
        <div className="canvas-container">
          <img
            ref={videoRef}
            key={useUpload ? 'upload' : 'camera'}
            src={useUpload ? uploadedImageUrl : `${API_BASE}/api/v1/rtsp/camera_live/snapshot?t=${Date.now()}`}
            alt="Camera Live"
            style={{ display: 'none' }}
            crossOrigin={useUpload ? undefined : "anonymous"}
            onLoad={handleImageLoad}
            onError={(e) => {
              console.error('[DEBUG] Image load error:', e);
              if (!useUpload) {
                setMessage('⚠️ Không thể tải ảnh từ camera. Vui lòng upload ảnh để test.');
              }
            }}
          />
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
          />
          {videoLoaded ? (
            <canvas
              ref={canvasRef}
              onClick={handleCanvasClick}
              className="setup-canvas"
            />
          ) : (
            <div className="canvas-placeholder">
              <p>⏳ Đang tải camera...</p>
              <p style={{ fontSize: '0.9rem', opacity: 0.7, marginBottom: '20px' }}>
                Đảm bảo backend đang chạy tại {API_BASE}
              </p>
              <div style={{ marginTop: '20px' }}>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  style={{
                    padding: '12px 24px',
                    background: '#667eea',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '1rem',
                    fontWeight: 'bold',
                    cursor: 'pointer',
                  }}
                >
                  📁 Hoặc Upload Ảnh Để Test
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Control panel */}
        <div className="control-panel">
          <div className="step-indicator">
            <div className={`step ${currentStep === 1 ? 'active' : 'completed'}`}>
              <span className="step-number">1</span>
              <span className="step-label">Vẽ ROI</span>
            </div>
            <div className={`step ${currentStep === 2 ? 'active' : ''}`}>
              <span className="step-number">2</span>
              <span className="step-label">Vẽ Stop Line</span>
            </div>
          </div>

          {message && (
            <div className="message-box">
              {message}
            </div>
          )}

          <div className="button-group">
            <button onClick={handleReset} className="btn btn-secondary">
              🔄 Vẽ Lại
            </button>

            <button
              onClick={handleSaveAndNext}
              className="btn btn-primary"
              disabled={loading || (!isAdmin && currentStep === 2)}
              style={!isAdmin ? { opacity: 0.5, cursor: 'not-allowed' } : {}}
            >
              {currentStep === 1 ? '💾 Lưu và Tiếp Tục' : '✅ Lưu Cấu Hình (Admin)'}
            </button>
          </div>

          <div className="instructions">
            <h4>📋 Hướng Dẫn:</h4>
            {currentStep === 1 ? (
              <ul>
                <li><strong>Bước 1:</strong> Click chọn 4 góc bao quanh đèn tín hiệu</li>
                <li>Thứ tự: Trên trái → Trên phải → Dưới phải → Dưới trái</li>
                <li>Sau khi chọn đủ 4 điểm, nhấn "Lưu và Tiếp Tục"</li>
              </ul>
            ) : (
              <ul>
                <li><strong>Bước 2:</strong> Click 2 điểm bất kỳ để tạo đường ngang</li>
                <li>Đường Stop Line sẽ tự động vẽ ở giữa khung hình</li>
                <li>Sau khi chọn 2 điểm, nhấn "Lưu Cấu Hình"</li>
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RedLightSetup;
