import { useState, useEffect, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import {
  Download,
  FileText,
  TrendingUp,
  TrendingDown,
  Clock,
  Calendar,
  BarChart3,
  Activity,
  FileSpreadsheet,
  File,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { format, subDays, startOfDay, endOfDay } from "date-fns";
import { vi } from "date-fns/locale";
import { endpoints } from "../config";

interface VehicleData {
  count_car: number;
  count_motor: number;
  speed_car: number;
  speed_motor: number;
}

interface TrafficData {
  [roadName: string]: VehicleData;
}

interface TrafficReportsProps {
  trafficData: TrafficData;
  allowedRoads: string[];
}

interface HistoricalPoint {
  timestamp: number;
  time: string;
  [key: string]: number | string;
}

interface HourlyStats {
  hour: number;
  avgVehicles: number;
  avgSpeed: number;
  status: string;
}

const TrafficReports = ({ trafficData, allowedRoads }: TrafficReportsProps) => {
  const [period, setPeriod] = useState<"day" | "week" | "month">("day");
  const [selectedRoads, setSelectedRoads] = useState<string[]>(allowedRoads);
  const [historicalData, setHistoricalData] = useState<HistoricalPoint[]>([]);

  const COLORS = {
    primary: "#6366f1",
    secondary: "#8b5cf6",
    success: "#10b981",
    warning: "#f59e0b",
    danger: "#ef4444",
    info: "#06b6d4",
  };

  const CHART_COLORS = [
    COLORS.primary,
    COLORS.success,
    COLORS.warning,
    COLORS.danger,
    COLORS.info,
    COLORS.secondary,
  ];

  // Collect historical data
  useEffect(() => {
    if (Object.keys(trafficData).length > 0) {
      const now = new Date();
      const newPoint: HistoricalPoint = {
        timestamp: now.getTime(),
        time: format(now, "HH:mm:ss", { locale: vi }),
        ...Object.entries(trafficData).reduce((acc, [road, data]) => {
          acc[`${road}_total`] = data.count_car + data.count_motor;
          acc[`${road}_cars`] = data.count_car;
          acc[`${road}_motors`] = data.count_motor;
          acc[`${road}_speed`] = (data.speed_car + data.speed_motor) / 2;
          return acc;
        }, {} as Record<string, number>),
      };

      setHistoricalData((prev) => {
        const updated = [...prev, newPoint];
        // Keep last 50 points
        return updated.slice(-50);
      });
    }
  }, [trafficData]);

  // Calculate hourly statistics
  const hourlyStats = useMemo((): HourlyStats[] => {
    const stats: Record<number, { totalVehicles: number[]; totalSpeed: number[]; count: number }> = {};

    historicalData.forEach((point) => {
      const hour = new Date(point.timestamp).getHours();
      if (!stats[hour]) {
        stats[hour] = { totalVehicles: [], totalSpeed: [], count: 0 };
      }

      selectedRoads.forEach((road) => {
        const vehicles = (point[`${road}_total`] as number) || 0;
        const speed = (point[`${road}_speed`] as number) || 0;
        stats[hour].totalVehicles.push(vehicles);
        stats[hour].totalSpeed.push(speed);
      });
      stats[hour].count++;
    });

    return Object.entries(stats).map(([hour, data]) => {
      const avgVehicles =
        data.totalVehicles.reduce((a, b) => a + b, 0) / data.totalVehicles.length || 0;
      const avgSpeed =
        data.totalSpeed.reduce((a, b) => a + b, 0) / data.totalSpeed.length || 0;

      let status = "clear";
      if (avgVehicles > 15) status = "congested";
      else if (avgVehicles > 8) status = "busy";

      return {
        hour: parseInt(hour),
        avgVehicles,
        avgSpeed,
        status,
      };
    }).sort((a, b) => a.hour - b.hour);
  }, [historicalData, selectedRoads]);

  // Find peak and off-peak hours
  const peakAnalysis = useMemo(() => {
    if (hourlyStats.length === 0) return null;

    const sorted = [...hourlyStats].sort((a, b) => b.avgVehicles - a.avgVehicles);
    return {
      peakHour: sorted[0],
      offPeakHour: sorted[sorted.length - 1],
    };
  }, [hourlyStats]);

  // Road comparison data
  const roadComparisonData = useMemo(() => {
    return selectedRoads.map((road) => {
      const roadData = trafficData[road];
      const total = roadData ? roadData.count_car + roadData.count_motor : 0;
      const avgSpeed = roadData
        ? (roadData.speed_car + roadData.speed_motor) / 2
        : 0;

      let status = "clear";
      if (total > 15) status = "congested";
      else if (total > 8) status = "busy";

      return {
        road: road.length > 12 ? road.substring(0, 12) + "..." : road,
        fullRoad: road,
        totalVehicles: total,
        cars: roadData?.count_car || 0,
        motors: roadData?.count_motor || 0,
        avgSpeed: avgSpeed,
        status,
      };
    });
  }, [trafficData, selectedRoads]);

  // Trend data for the selected period
  const trendData = useMemo(() => {
    const now = Date.now();
    const periodMs = period === "day" ? 24 * 60 * 60 * 1000 : period === "week" ? 7 * 24 * 60 * 60 * 1000 : 30 * 24 * 60 * 60 * 1000;
    const startTime = now - periodMs;

    return historicalData
      .filter((point) => point.timestamp >= startTime)
      .map((point) => ({
        time: point.time,
        ...selectedRoads.reduce((acc, road) => {
          acc[road] = (point[`${road}_total`] as number) || 0;
          return acc;
        }, {} as Record<string, number>),
      }));
  }, [historicalData, period, selectedRoads]);

  // Export functions
  const exportToCSV = () => {
    const headers = ["Time", ...selectedRoads.flatMap((road) => [`${road} Vehicles`, `${road} Speed`])];
    const rows = historicalData.map((point) => [
      point.time,
      ...selectedRoads.flatMap((road) => [
        point[`${road}_total`] || 0,
        point[`${road}_speed`] || 0,
      ]),
    ]);

    const csvContent = [
      headers.join(","),
      ...rows.map((row) => row.join(",")),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `traffic-report-${format(new Date(), "yyyy-MM-dd-HHmmss")}.csv`;
    link.click();
  };

  const exportToJSON = () => {
    const data = {
      exportedAt: new Date().toISOString(),
      period,
      roads: selectedRoads,
      data: historicalData,
      summary: {
        hourlyStats,
        roadComparison: roadComparisonData,
        peakAnalysis,
      },
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `traffic-report-${format(new Date(), "yyyy-MM-dd-HHmmss")}.json`;
    link.click();
  };

  const exportToPDF = async () => {
    try {
      const endDate = format(new Date(), "yyyy-MM-dd");
      const startDate = format(
        period === "day"
          ? subDays(new Date(), 1)
          : period === "week"
            ? subDays(new Date(), 7)
            : subDays(new Date(), 30),
        "yyyy-MM-dd"
      );

      const response = await fetch(`${endpoints.base}/api/v1/reports/export/pdf`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          road_names: selectedRoads,
          start_date: startDate,
          end_date: endDate,
          period: period,
        }),
      });

      if (!response.ok) throw new Error("Export failed");

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `traffic-report-${format(new Date(), "yyyy-MM-dd-HHmmss")}.pdf`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("PDF export error:", error);
      alert("Lỗi khi export PDF. Vui lòng thử lại.");
    }
  };

  const exportToExcel = async () => {
    try {
      const endDate = format(new Date(), "yyyy-MM-dd");
      const startDate = format(
        period === "day"
          ? subDays(new Date(), 1)
          : period === "week"
            ? subDays(new Date(), 7)
            : subDays(new Date(), 30),
        "yyyy-MM-dd"
      );

      const response = await fetch(`${endpoints.base}/api/v1/reports/export/excel`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          road_names: selectedRoads,
          start_date: startDate,
          end_date: endDate,
          period: period,
        }),
      });

      if (!response.ok) throw new Error("Export failed");

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `traffic-report-${format(new Date(), "yyyy-MM-dd-HHmmss")}.xlsx`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Excel export error:", error);
      alert("Lỗi khi export Excel. Vui lòng thử lại.");
    }
  };

  return (
    <div className="space-y-6">
      {/* Header with controls */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-2xl p-6 border border-white/10"
      >
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
          <div>
            <h2 className="text-2xl font-bold gradient-text">Báo Cáo Thống Kê</h2>
            <p className="text-gray-400 text-sm mt-1">
              Phân tích chi tiết lưu lượng giao thông
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Select value={period} onValueChange={(v: any) => setPeriod(v)}>
              <SelectTrigger className="w-[140px] glass border-white/20">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="day">Hôm nay</SelectItem>
                <SelectItem value="week">7 ngày</SelectItem>
                <SelectItem value="month">30 ngày</SelectItem>
              </SelectContent>
            </Select>

            <div className="flex flex-wrap gap-2">
              <Button
                onClick={exportToCSV}
                variant="outline"
                size="sm"
                className="glass border-white/20 hover:bg-white/10"
              >
                <Download className="h-4 w-4 mr-2" />
                CSV
              </Button>
              <Button
                onClick={exportToJSON}
                variant="outline"
                size="sm"
                className="glass border-white/20 hover:bg-white/10"
              >
                <FileText className="h-4 w-4 mr-2" />
                JSON
              </Button>
              <Button
                onClick={exportToPDF}
                variant="outline"
                size="sm"
                className="glass border-white/20 hover:bg-white/10 hover:border-red-400/50"
              >
                <File className="h-4 w-4 mr-2 text-red-400" />
                PDF
              </Button>
              <Button
                onClick={exportToExcel}
                variant="outline"
                size="sm"
                className="glass border-white/20 hover:bg-white/10 hover:border-green-400/50"
              >
                <FileSpreadsheet className="h-4 w-4 mr-2 text-green-400" />
                Excel
              </Button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Peak Hours Analysis */}
      {peakAnalysis && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card className="glass border border-white/10">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-red-400" />
                  <span className="gradient-text">Giờ Cao Điểm</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <Clock className="h-8 w-8 text-red-400" />
                  <div className="text-right">
                    <p className="text-3xl font-bold">{peakAnalysis.peakHour.hour}:00</p>
                    <p className="text-sm text-gray-400">
                      {peakAnalysis.peakHour.avgVehicles.toFixed(0)} xe trung bình
                    </p>
                  </div>
                </div>
                <Badge
                  variant="destructive"
                  className="w-full justify-center py-2"
                >
                  {peakAnalysis.peakHour.status === "congested"
                    ? "Tắc nghẽn"
                    : peakAnalysis.peakHour.status === "busy"
                      ? "Đông đúc"
                      : "Thông thoáng"}
                </Badge>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="glass border border-white/10">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingDown className="h-5 w-5 text-green-400" />
                  <span className="gradient-text">Giờ Thấp Điểm</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <Clock className="h-8 w-8 text-green-400" />
                  <div className="text-right">
                    <p className="text-3xl font-bold">{peakAnalysis.offPeakHour.hour}:00</p>
                    <p className="text-sm text-gray-400">
                      {peakAnalysis.offPeakHour.avgVehicles.toFixed(0)} xe trung bình
                    </p>
                  </div>
                </div>
                <Badge variant="default" className="w-full justify-center py-2 bg-green-500">
                  Thông thoáng
                </Badge>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      )}

      {/* Hourly Trend Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <Card className="glass border border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-indigo-400" />
              <span className="gradient-text">Xu Hướng Theo Giờ</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={hourlyStats}>
                <defs>
                  <linearGradient id="colorVehicles" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={COLORS.primary} stopOpacity={0.8} />
                    <stop offset="95%" stopColor={COLORS.primary} stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis
                  dataKey="hour"
                  tickFormatter={(hour) => `${hour}:00`}
                  stroke="#9ca3af"
                />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "rgba(15, 23, 42, 0.9)",
                    border: "1px solid rgba(99, 102, 241, 0.3)",
                    borderRadius: "8px",
                  }}
                  labelFormatter={(hour) => `${hour}:00`}
                />
                <Area
                  type="monotone"
                  dataKey="avgVehicles"
                  stroke={COLORS.primary}
                  fillOpacity={1}
                  fill="url(#colorVehicles)"
                  name="Số xe TB"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </motion.div>

      {/* Road Comparison */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <Card className="glass border border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-cyan-400" />
              <span className="gradient-text">So Sánh Tuyến Đường</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={roadComparisonData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="road" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "rgba(15, 23, 42, 0.9)",
                    border: "1px solid rgba(99, 102, 241, 0.3)",
                    borderRadius: "8px",
                  }}
                  labelFormatter={(_, payload) => {
                    if (payload && payload.length > 0) {
                      return payload[0].payload.fullRoad;
                    }
                    return "";
                  }}
                />
                <Legend />
                <Bar dataKey="cars" stackId="vehicles" fill={COLORS.primary} name="Ô tô" />
                <Bar dataKey="motors" stackId="vehicles" fill={COLORS.success} name="Xe máy" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </motion.div>

      {/* Traffic Trend Over Time */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <Card className="glass border border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-purple-400" />
              <span className="gradient-text">Biểu Đồ Xu Hướng</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="time" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "rgba(15, 23, 42, 0.9)",
                    border: "1px solid rgba(99, 102, 241, 0.3)",
                    borderRadius: "8px",
                  }}
                />
                <Legend />
                {selectedRoads.map((road, index) => (
                  <Line
                    key={road}
                    type="monotone"
                    dataKey={road}
                    stroke={CHART_COLORS[index % CHART_COLORS.length]}
                    strokeWidth={2}
                    dot={false}
                    name={road}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default TrafficReports;
