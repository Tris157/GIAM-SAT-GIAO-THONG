/**
 * Violation Service - Dịch vụ quản lý vi phạm giao thông
 *
 * Service này xử lý tất cả các API calls liên quan đến vi phạm giao thông:
 * - Lấy danh sách vi phạm
 * - Xem chi tiết vi phạm
 * - Đánh dấu đã xử lý
 * - Xóa vi phạm
 * - Lấy thống kê
 * - Cấu hình phát hiện đèn đỏ
 */

import { endpoints } from '@/config';

// ==================== TYPES & INTERFACES ====================

/**
 * Interface cho một vi phạm giao thông
 */
export interface Violation {
  id: number;
  camera_name: string;
  violation_type: string; // 'red_light', 'speeding', 'wrong_lane'
  vehicle_type: string; // 'car', 'motor'
  image_path: string;
  position_x: number;
  position_y: number;
  traffic_light_status: string; // 'red', 'yellow', 'green'
  violated_at: string; // ISO datetime
  date?: string; // YYYY-MM-DD
  hour_of_day?: number; // 0-23
  is_processed: boolean;
  note?: string;
  confidence: number;
}

/**
 * Interface cho bộ lọc danh sách vi phạm
 */
export interface ViolationFilters {
  camera_name?: string;
  is_processed?: boolean;
  limit?: number;
  offset?: number;
}

/**
 * Interface cho thống kê vi phạm
 */
export interface ViolationStats {
  camera_name: string;
  total_violations: number;
  current_light_status: string;
  is_monitoring: boolean;
}

/**
 * Interface cho cấu hình phát hiện đèn đỏ
 */
export interface RedLightConfig {
  camera_name: string;
  traffic_light_roi: {
    x: number;
    y: number;
    w: number;
    h: number;
  };
  stop_line_y: number;
  enable: boolean;
}

/**
 * Interface cho tổng hợp vi phạm theo ngày
 */
export interface DailySummary {
  date: string;
  total_violations: number;
  unique_vehicle_types: number;
}

// ==================== API FUNCTIONS ====================

/**
 * Lấy danh sách vi phạm với bộ lọc
 *
 * @param filters - Bộ lọc (camera, processed status, pagination)
 * @returns Promise<Violation[]> - Danh sách vi phạm
 */
export const getViolations = async (
  filters: ViolationFilters = {}
): Promise<Violation[]> => {
  try {
    // Tạo query params từ filters
    const params = new URLSearchParams();

    if (filters.camera_name) {
      params.append('camera_name', filters.camera_name);
    }

    if (filters.is_processed !== undefined) {
      params.append('is_processed', filters.is_processed.toString());
    }

    if (filters.limit) {
      params.append('limit', filters.limit.toString());
    }

    if (filters.offset) {
      params.append('offset', filters.offset.toString());
    }

    const url = `${endpoints.base}/api/v1/violations/list?${params.toString()}`;

    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to fetch violations: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching violations:', error);
    throw error;
  }
};

/**
 * Lấy chi tiết một vi phạm theo ID
 *
 * @param violationId - ID của vi phạm
 * @returns Promise<Violation> - Chi tiết vi phạm
 */
export const getViolationById = async (
  violationId: number
): Promise<Violation> => {
  try {
    const url = `${endpoints.base}/api/v1/violations/${violationId}`;

    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to fetch violation: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching violation ${violationId}:`, error);
    throw error;
  }
};

/**
 * Đánh dấu vi phạm đã xử lý
 *
 * @param violationId - ID của vi phạm
 * @param note - Ghi chú (optional)
 * @returns Promise<{message: string}> - Kết quả
 */
export const markViolationProcessed = async (
  violationId: number,
  note?: string
): Promise<{ message: string; violation_id: number; is_processed: boolean }> => {
  try {
    const url = `${endpoints.base}/api/v1/violations/${violationId}/process`;

    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ note }),
    });

    if (!response.ok) {
      throw new Error(`Failed to mark violation as processed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error marking violation ${violationId} as processed:`, error);
    throw error;
  }
};

/**
 * Xóa vi phạm
 *
 * @param violationId - ID của vi phạm
 * @returns Promise<{message: string}> - Kết quả
 */
export const deleteViolation = async (
  violationId: number
): Promise<{ message: string; violation_id: number }> => {
  try {
    const url = `${endpoints.base}/api/v1/violations/${violationId}`;

    const response = await fetch(url, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`Failed to delete violation: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error deleting violation ${violationId}:`, error);
    throw error;
  }
};

/**
 * Lấy thống kê vi phạm của camera
 *
 * @param cameraName - Tên camera
 * @returns Promise<ViolationStats> - Thống kê
 */
export const getViolationStats = async (
  cameraName: string
): Promise<ViolationStats> => {
  try {
    const url = `${endpoints.base}/api/v1/violations/statistics/${cameraName}`;

    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to fetch violation stats: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching violation stats for ${cameraName}:`, error);
    throw error;
  }
};

/**
 * Lấy tổng hợp vi phạm theo ngày
 *
 * @param cameraName - Tên camera (optional)
 * @returns Promise<DailySummary[]> - Tổng hợp theo ngày
 */
export const getDailySummary = async (
  cameraName?: string
): Promise<DailySummary[]> => {
  try {
    const params = cameraName ? `?camera_name=${cameraName}` : '';
    const url = `${endpoints.base}/api/v1/violations/summary/daily${params}`;

    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to fetch daily summary: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching daily summary:', error);
    throw error;
  }
};

/**
 * Cấu hình phát hiện đèn đỏ cho camera
 *
 * @param config - Cấu hình (ROI, stop line, enable)
 * @returns Promise<{message: string}> - Kết quả
 */
export const configureRedLightDetection = async (
  config: RedLightConfig
): Promise<{ message: string; config: any }> => {
  try {
    const url = `${endpoints.base}/api/v1/violations/config`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });

    if (!response.ok) {
      throw new Error(`Failed to configure red light detection: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error configuring red light detection:', error);
    throw error;
  }
};

/**
 * Bật/tắt giám sát vi phạm cho camera
 *
 * @param cameraName - Tên camera
 * @param enable - true = bật, false = tắt
 * @returns Promise<{message: string}> - Kết quả
 */
export const enableViolationMonitoring = async (
  cameraName: string,
  enable: boolean
): Promise<{ message: string; camera_name: string; enabled: boolean }> => {
  try {
    const url = `${endpoints.base}/api/v1/violations/enable/${cameraName}?enable=${enable}`;

    const response = await fetch(url, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Failed to enable/disable violation monitoring: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error enabling violation monitoring for ${cameraName}:`, error);
    throw error;
  }
};

/**
 * Setup nhanh cho camera_live (với config mặc định)
 *
 * @returns Promise<{message: string}> - Kết quả
 */
export const quickSetupCameraLive = async (): Promise<{
  message: string;
  config: any;
}> => {
  try {
    const url = `${endpoints.base}/api/v1/violations/quick-setup/camera_live`;

    const response = await fetch(url, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Failed to quick setup camera_live: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error in quick setup camera_live:', error);
    throw error;
  }
};

// ==================== UTILITY FUNCTIONS ====================

/**
 * Format datetime cho hiển thị
 *
 * @param isoString - ISO datetime string
 * @returns Formatted string (DD/MM/YYYY HH:mm:ss)
 */
export const formatViolationTime = (isoString: string): string => {
  const date = new Date(isoString);

  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();

  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const seconds = date.getSeconds().toString().padStart(2, '0');

  return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
};

/**
 * Lấy màu badge cho loại vi phạm
 *
 * @param type - Loại vi phạm
 * @returns Tailwind color class
 */
export const getViolationTypeColor = (type: string): string => {
  const colors: Record<string, string> = {
    red_light: 'bg-red-500',
    speeding: 'bg-orange-500',
    wrong_lane: 'bg-yellow-500',
  };

  return colors[type] || 'bg-gray-500';
};

/**
 * Lấy label tiếng Việt cho loại vi phạm
 *
 * @param type - Loại vi phạm
 * @returns Label tiếng Việt
 */
export const getViolationTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    red_light: 'Vượt đèn đỏ',
    speeding: 'Vượt tốc độ',
    wrong_lane: 'Đi sai làn',
  };

  return labels[type] || type;
};

/**
 * Lấy label tiếng Việt cho loại xe
 *
 * @param type - Loại xe
 * @returns Label tiếng Việt
 */
export const getVehicleTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    car: 'Ô tô',
    motor: 'Xe máy',
    motorcycle: 'Xe máy',
  };

  return labels[type] || type;
};

/**
 * Lấy URL ảnh bằng chứng
 *
 * @param imagePath - Đường dẫn ảnh từ API
 * @returns Full URL
 */
export const getViolationImageUrl = (imagePath: string): string => {
  // imagePath format: "./app/static/violation_images/violation_camera_live_20251109_165944.jpg"
  const filename = imagePath.split('/').pop();
  return `${endpoints.base}/static/violation_images/${filename}`;
};
