/**
 * ViolationsStatistics Component - Thống kê và biểu đồ vi phạm
 *
 * Component này hiển thị các biểu đồ thống kê về vi phạm giao thông:
 * - Xu hướng vi phạm theo thời gian (Line Chart)
 * - Phân loại vi phạm (Pie Chart)
 * - Vi phạm theo camera (Bar Chart)
 * - Các chỉ số tổng quan (Cards)
 */

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Camera,
  CheckCircle,
  Clock,
} from 'lucide-react';
import {
  getViolations,
  getDailySummary,
  type Violation,
  type DailySummary,
} from '@/services/violationService';

/**
 * Interface cho thống kê tổng quan
 */
interface OverviewStats {
  total: number;
  unprocessed: number;
  processed: number;
  todayCount: number;
  trendPercentage: number;
}

/**
 * Interface cho thống kê theo loại
 */
interface ViolationTypeStats {
  name: string;
  value: number;
  color: string;
  label: string;
}

/**
 * Interface cho thống kê theo camera
 */
interface CameraStats {
  camera: string;
  count: number;
}

/**
 * Màu sắc cho biểu đồ
 */
const COLORS = {
  red_light: '#ef4444',
  speeding: '#f97316',
  wrong_lane: '#eab308',
  primary: '#6366f1',
  success: '#10b981',
  warning: '#f59e0b',
};

/**
 * Component chính - Thống kê vi phạm
 */
export default function ViolationsStatistics() {
  // ==================== STATE MANAGEMENT ====================

  const [violations, setViolations] = useState<Violation[]>([]);
  const [dailySummary, setDailySummary] = useState<DailySummary[]>([]);
  const [overviewStats, setOverviewStats] = useState<OverviewStats>({
    total: 0,
    unprocessed: 0,
    processed: 0,
    todayCount: 0,
    trendPercentage: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  // ==================== DATA FETCHING ====================

  /**
   * Tải dữ liệu thống kê
   */
  const fetchStatistics = async () => {
    setIsLoading(true);

    try {
      // Lấy tất cả vi phạm
      const allViolations = await getViolations({ limit: 1000 });

      // Lấy tổng hợp theo ngày
      const summary = await getDailySummary();

      setViolations(allViolations);
      setDailySummary(summary);

      // Tính toán các chỉ số
      calculateOverviewStats(allViolations, summary);
    } catch (error) {
      console.error('Error fetching statistics:', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Tính toán các chỉ số tổng quan
   */
  const calculateOverviewStats = (
    allViolations: Violation[],
    summary: DailySummary[]
  ) => {
    const total = allViolations.length;
    const unprocessed = allViolations.filter((v) => !v.is_processed).length;
    const processed = allViolations.filter((v) => v.is_processed).length;

    // Vi phạm hôm nay
    const today = new Date().toISOString().split('T')[0];
    const todayCount = allViolations.filter(
      (v) => v.date === today
    ).length;

    // Tính xu hướng (so với hôm qua)
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    const yesterdayCount = allViolations.filter(
      (v) => v.date === yesterday
    ).length;

    const trendPercentage =
      yesterdayCount > 0
        ? ((todayCount - yesterdayCount) / yesterdayCount) * 100
        : 0;

    setOverviewStats({
      total,
      unprocessed,
      processed,
      todayCount,
      trendPercentage,
    });
  };

  /**
   * Load data khi component mount
   */
  useEffect(() => {
    fetchStatistics();

    // Refresh mỗi 30 giây
    const interval = setInterval(fetchStatistics, 30000);
    return () => clearInterval(interval);
  }, []);

  // ==================== DATA PROCESSING ====================

  /**
   * Thống kê theo loại vi phạm
   */
  const violationTypeStats: ViolationTypeStats[] = [
    {
      name: 'red_light',
      value: violations.filter((v) => v.violation_type === 'red_light').length,
      color: COLORS.red_light,
      label: 'Vượt đèn đỏ',
    },
    {
      name: 'speeding',
      value: violations.filter((v) => v.violation_type === 'speeding').length,
      color: COLORS.speeding,
      label: 'Vượt tốc độ',
    },
    {
      name: 'wrong_lane',
      value: violations.filter((v) => v.violation_type === 'wrong_lane').length,
      color: COLORS.warning,
      label: 'Đi sai làn',
    },
  ].filter((item) => item.value > 0);

  /**
   * Thống kê theo camera
   */
  const cameraStats: CameraStats[] = Array.from(
    new Set(violations.map((v) => v.camera_name))
  )
    .map((camera) => ({
      camera,
      count: violations.filter((v) => v.camera_name === camera).length,
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  /**
   * Dữ liệu cho biểu đồ xu hướng theo ngày
   */
  const trendData = dailySummary
    .slice(0, 30)
    .reverse()
    .map((item) => ({
      date: new Date(item.date).toLocaleDateString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
      }),
      violations: item.total_violations,
    }));

  /**
   * Thống kê theo giờ trong ngày
   */
  const hourlyStats = Array.from({ length: 24 }, (_, hour) => {
    const count = violations.filter((v) => v.hour_of_day === hour).length;
    return {
      hour: `${hour}:00`,
      count,
    };
  });

  // ==================== RENDER ====================

  if (isLoading) {
    return (
      <div className="py-12 text-center text-muted-foreground">
        Đang tải thống kê...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Tổng vi phạm */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Tổng vi phạm</p>
                <p className="text-3xl font-bold mt-2">{overviewStats.total}</p>
              </div>
              <div className="size-12 rounded-full bg-destructive/10 flex items-center justify-center">
                <AlertTriangle className="size-6 text-destructive" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Chưa xử lý */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Chưa xử lý</p>
                <p className="text-3xl font-bold mt-2 text-warning">
                  {overviewStats.unprocessed}
                </p>
              </div>
              <div className="size-12 rounded-full bg-warning/10 flex items-center justify-center">
                <Clock className="size-6 text-warning" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Đã xử lý */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Đã xử lý</p>
                <p className="text-3xl font-bold mt-2 text-success">
                  {overviewStats.processed}
                </p>
              </div>
              <div className="size-12 rounded-full bg-success/10 flex items-center justify-center">
                <CheckCircle className="size-6 text-success" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Hôm nay */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Hôm nay</p>
                <p className="text-3xl font-bold mt-2">{overviewStats.todayCount}</p>
                <div className="flex items-center gap-1 mt-1">
                  {overviewStats.trendPercentage >= 0 ? (
                    <TrendingUp className="size-4 text-destructive" />
                  ) : (
                    <TrendingDown className="size-4 text-success" />
                  )}
                  <span
                    className={`text-sm ${
                      overviewStats.trendPercentage >= 0
                        ? 'text-destructive'
                        : 'text-success'
                    }`}
                  >
                    {Math.abs(overviewStats.trendPercentage).toFixed(1)}%
                  </span>
                </div>
              </div>
              <div className="size-12 rounded-full bg-primary/10 flex items-center justify-center">
                <Camera className="size-6 text-primary" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Biểu đồ xu hướng theo ngày */}
      <Card>
        <CardHeader>
          <CardTitle>Xu hướng vi phạm 30 ngày gần đây</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={trendData}>
              <defs>
                <linearGradient id="colorViolations" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={COLORS.primary} stopOpacity={0.3} />
                  <stop offset="95%" stopColor={COLORS.primary} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis
                dataKey="date"
                stroke="#9ca3af"
                style={{ fontSize: '12px' }}
              />
              <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: '1px solid #374151',
                  borderRadius: '8px',
                }}
                labelStyle={{ color: '#f3f4f6' }}
              />
              <Area
                type="monotone"
                dataKey="violations"
                stroke={COLORS.primary}
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorViolations)"
                name="Vi phạm"
              />
            </AreaChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Biểu đồ phân loại vi phạm */}
        <Card>
          <CardHeader>
            <CardTitle>Phân loại vi phạm</CardTitle>
          </CardHeader>
          <CardContent>
            {violationTypeStats.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={violationTypeStats}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) =>
                      `${violationTypeStats.find((v) => v.name === name)?.label} ${(
                        percent * 100
                      ).toFixed(0)}%`
                    }
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {violationTypeStats.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1f2937',
                      border: '1px solid #374151',
                      borderRadius: '8px',
                    }}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                Chưa có dữ liệu
              </div>
            )}
          </CardContent>
        </Card>

        {/* Biểu đồ theo camera */}
        <Card>
          <CardHeader>
            <CardTitle>Vi phạm theo camera</CardTitle>
          </CardHeader>
          <CardContent>
            {cameraStats.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={cameraStats}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis
                    dataKey="camera"
                    stroke="#9ca3af"
                    style={{ fontSize: '12px' }}
                  />
                  <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1f2937',
                      border: '1px solid #374151',
                      borderRadius: '8px',
                    }}
                    labelStyle={{ color: '#f3f4f6' }}
                  />
                  <Bar
                    dataKey="count"
                    fill={COLORS.primary}
                    radius={[8, 8, 0, 0]}
                    name="Số vi phạm"
                  />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                Chưa có dữ liệu
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Biểu đồ theo giờ trong ngày */}
      <Card>
        <CardHeader>
          <CardTitle>Vi phạm theo giờ trong ngày</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={hourlyStats}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis
                dataKey="hour"
                stroke="#9ca3af"
                style={{ fontSize: '12px' }}
              />
              <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: '1px solid #374151',
                  borderRadius: '8px',
                }}
                labelStyle={{ color: '#f3f4f6' }}
              />
              <Line
                type="monotone"
                dataKey="count"
                stroke={COLORS.success}
                strokeWidth={2}
                dot={{ fill: COLORS.success, r: 4 }}
                name="Số vi phạm"
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
