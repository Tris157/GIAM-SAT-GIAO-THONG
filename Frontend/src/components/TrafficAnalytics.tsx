import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Legend,
  AreaChart,
  Area,
} from "recharts";
import {
  TrendingUp,
  Activity,
  Car,
  Bike,
  BarChart3,
  PieChart as PieChartIcon,
  LineChart as LineChartIcon,
  Gauge,
  MapPin,
  Zap,
  ChevronDown,
  ChevronUp,
  Eye,
  EyeOff,
  Grid3x3,
  Layout,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface VehicleData {
  count_car: number;
  count_motor: number;
  speed_car: number;
  speed_motor: number;
}

interface TrafficData {
  [roadName: string]: VehicleData;
}

interface TrafficAnalyticsProps {
  trafficData: TrafficData;
  allowedRoads: string[];
}

interface HistoricalData {
  time: string;
  [key: string]: string | number;
}

const TrafficAnalytics = ({
  trafficData,
  allowedRoads,
}: TrafficAnalyticsProps) => {
  const [historicalData, setHistoricalData] = useState<HistoricalData[]>([]);
  const [activeTab, setActiveTab] = useState("overview");
  const [layoutMode, setLayoutMode] = useState<"tabs" | "grid">("grid"); // New: grid layout by default
  const [visiblePanels, setVisiblePanels] = useState({
    vehicleCount: true,
    speed: true,
    trends: true,
    distribution: true,
    roadComparison: true,
  });

  // Refs for smooth scrolling
  const overviewRef = useRef<HTMLDivElement>(null);
  const trendsRef = useRef<HTMLDivElement>(null);
  const distributionRef = useRef<HTMLDivElement>(null);

  const togglePanel = (panel: keyof typeof visiblePanels) => {
    setVisiblePanels(prev => ({ ...prev, [panel]: !prev[panel] }));
  };

  // Store historical data
  useEffect(() => {
    if (Object.keys(trafficData).length > 0) {
      const now = new Date();
      const timeString = now.toLocaleTimeString("vi-VN", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });

      const newDataPoint: HistoricalData = {
        time: timeString,
        ...Object.entries(trafficData).reduce((acc, [road, data]) => {
          acc[`${road}_cars`] = data.count_car;
          acc[`${road}_motors`] = data.count_motor;
          acc[`${road}_car_speed`] = data.speed_car;
          acc[`${road}_motor_speed`] = data.speed_motor;
          acc[`${road}_total`] = data.count_car + data.count_motor;
          return acc;
        }, {} as Record<string, number>),
      };

      setHistoricalData((prev) => {
        const updated = [...prev, newDataPoint];
        return updated.slice(-20);
      });
    }
  }, [trafficData]);

  // Prepare data for charts
  const vehicleCountData = allowedRoads.map((road) => {
    const data = trafficData[road];
    return {
      road: road.length > 10 ? road.substring(0, 10) + "..." : road,
      fullRoad: road,
      cars: data?.count_car || 0,
      motors: data?.count_motor || 0,
      total: (data?.count_car || 0) + (data?.count_motor || 0),
    };
  });

  const speedData = allowedRoads.map((road) => {
    const data = trafficData[road];
    return {
      road: road.length > 10 ? road.substring(0, 10) + "..." : road,
      fullRoad: road,
      carSpeed: data?.speed_car || 0,
      motorSpeed: data?.speed_motor || 0,
    };
  });

  const pieData = allowedRoads
    .map((road) => {
      const data = trafficData[road];
      const total = (data?.count_car || 0) + (data?.count_motor || 0);
      return {
        name: road,
        value: total,
        cars: data?.count_car || 0,
        motors: data?.count_motor || 0,
      };
    })
    .filter((item) => item.value > 0);

  const COLORS = ["#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#3B82F6"];

  const getTotalVehicles = () => {
    return Object.values(trafficData).reduce(
      (sum, data) => sum + data.count_car + data.count_motor,
      0
    );
  };

  const getAverageSpeed = () => {
    const roads = Object.values(trafficData);
    if (roads.length === 0) return { car: 0, motor: 0 };

    const avgCarSpeed =
      roads.reduce((sum, data) => sum + data.speed_car, 0) / roads.length;
    const avgMotorSpeed =
      roads.reduce((sum, data) => sum + data.speed_motor, 0) / roads.length;

    return { car: avgCarSpeed, motor: avgMotorSpeed };
  };

  const getBusiestRoad = () => {
    let maxVehicles = 0;
    let busiestRoad = "";

    Object.entries(trafficData).forEach(([road, data]) => {
      const total = data.count_car + data.count_motor;
      if (total > maxVehicles) {
        maxVehicles = total;
        busiestRoad = road;
      }
    });

    return { road: busiestRoad, vehicles: maxVehicles };
  };

  const totalVehicles = getTotalVehicles();
  const averageSpeed = getAverageSpeed();
  const busiestRoad = getBusiestRoad();

  // Quick navigation buttons data
  const quickNavItems = [
    { id: "overview", label: "Tổng quan", icon: BarChart3, ref: overviewRef },
    { id: "trends", label: "Xu hướng", icon: LineChartIcon, ref: trendsRef },
    { id: "distribution", label: "Phân bố", icon: PieChartIcon, ref: distributionRef },
  ];

  const scrollToSection = (ref: React.RefObject<HTMLDivElement>, tabId: string) => {
    setActiveTab(tabId);
    ref.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div className="space-y-4">
      {/* Enhanced Sticky Navigation Bar */}
      <div className="sticky top-0 z-20 bg-background/95 backdrop-blur-xl border-b border-border/50 -mx-4 px-4 py-3 shadow-lg">
        <div className="flex items-center justify-between gap-2 flex-wrap">
          {/* Quick Stats */}
          <div className="hidden md:flex items-center gap-3">
            <div className="flex items-center gap-1.5 px-3 py-1.5 bg-cyan-500/10 rounded-lg border border-cyan-500/20">
              <Activity className="h-4 w-4 text-cyan-400" />
              <span className="text-sm font-medium">{totalVehicles} xe</span>
            </div>
            <div className="flex items-center gap-1.5 px-3 py-1.5 bg-green-500/10 rounded-lg border border-green-500/20">
              <Gauge className="h-4 w-4 text-green-400" />
              <span className="text-sm font-medium">{averageSpeed.car.toFixed(0)} km/h</span>
            </div>
          </div>

          {/* Layout Mode Toggle */}
          <div className="flex items-center gap-2">
            <div className="flex items-center bg-secondary/50 rounded-lg p-1">
              <button
                onClick={() => setLayoutMode("tabs")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                  layoutMode === "tabs"
                    ? "bg-cyan-500 text-white shadow-md"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <Layout className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Tabs</span>
              </button>
              <button
                onClick={() => setLayoutMode("grid")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                  layoutMode === "grid"
                    ? "bg-cyan-500 text-white shadow-md"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <Grid3x3 className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Grid</span>
              </button>
            </div>

            {/* Panel Visibility Toggles - Only show in grid mode */}
            {layoutMode === "grid" && (
              <div className="flex items-center gap-1 ml-2">
                {Object.entries(visiblePanels).map(([key, visible]) => (
                  <button
                    key={key}
                    onClick={() => togglePanel(key as keyof typeof visiblePanels)}
                    className={`p-1.5 rounded-md transition-all ${
                      visible
                        ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                        : "bg-secondary/50 text-muted-foreground hover:text-foreground"
                    }`}
                    title={`Toggle ${key}`}
                  >
                    {visible ? <Eye className="h-3.5 w-3.5" /> : <EyeOff className="h-3.5 w-3.5" />}
                  </button>
                ))}
              </div>
            )}

            {/* Quick Navigation Buttons - Only in tabs mode */}
            {layoutMode === "tabs" && (
              <div className="flex items-center gap-2">
                {quickNavItems.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => scrollToSection(item.ref, item.id)}
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium
                      transition-all duration-300
                      ${activeTab === item.id
                        ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/30'
                        : 'bg-secondary/50 hover:bg-secondary text-muted-foreground hover:text-foreground'
                      }
                    `}
                  >
                    <item.icon className="h-4 w-4" />
                    <span className="hidden sm:inline">{item.label}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="bg-gradient-to-br from-cyan-500/10 to-cyan-500/5 border-cyan-500/20">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-cyan-500/20 rounded-xl">
                  <Activity className="h-5 w-5 text-cyan-400" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Tổng xe</p>
                  <p className="text-xl font-bold">{totalVehicles}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
        >
          <Card className="bg-gradient-to-br from-green-500/10 to-green-500/5 border-green-500/20">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-green-500/20 rounded-xl">
                  <Car className="h-5 w-5 text-green-400" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">TB ô tô</p>
                  <p className="text-xl font-bold">{averageSpeed.car.toFixed(1)}<span className="text-xs ml-1">km/h</span></p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card className="bg-gradient-to-br from-purple-500/10 to-purple-500/5 border-purple-500/20">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-purple-500/20 rounded-xl">
                  <Bike className="h-5 w-5 text-purple-400" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">TB xe máy</p>
                  <p className="text-xl font-bold">{averageSpeed.motor.toFixed(1)}<span className="text-xs ml-1">km/h</span></p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
        >
          <Card className="bg-gradient-to-br from-orange-500/10 to-orange-500/5 border-orange-500/20">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-orange-500/20 rounded-xl">
                  <MapPin className="h-5 w-5 text-orange-400" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Đông nhất</p>
                  <p className="text-sm font-bold truncate max-w-[100px]" title={busiestRoad.road}>
                    {busiestRoad.road || "N/A"}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Charts Sections - Dynamic Layout */}
      {layoutMode === "tabs" ? (
        // TABS MODE - Original tab-based layout
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
          <TabsList className="grid w-full grid-cols-3 h-12">
            <TabsTrigger value="overview" className="flex items-center gap-2 text-sm">
              <BarChart3 className="h-4 w-4" />
              <span>Tổng quan</span>
            </TabsTrigger>
            <TabsTrigger value="trends" className="flex items-center gap-2 text-sm">
              <LineChartIcon className="h-4 w-4" />
              <span>Xu hướng</span>
            </TabsTrigger>
            <TabsTrigger value="distribution" className="flex items-center gap-2 text-sm">
              <PieChartIcon className="h-4 w-4" />
              <span>Phân bố</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" ref={overviewRef} className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {/* Vehicle Count Chart */}
              <Card className="border-border/50">
                <CardHeader className="pb-2">
                  <CardTitle className="text-base flex items-center gap-2">
                    <Zap className="h-4 w-4 text-cyan-400" />
                    Số lượng xe theo tuyến
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={280}>
                    <BarChart data={vehicleCountData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                      <XAxis dataKey="road" tick={{ fontSize: 11 }} />
                      <YAxis tick={{ fontSize: 11 }} />
                      <Tooltip
                        contentStyle={{ background: '#1e293b', border: '1px solid rgba(6,182,212,0.3)', borderRadius: '8px' }}
                        formatter={(value, name) => [
                          value,
                          name === "cars" ? "Ô tô" : "Xe máy",
                        ]}
                        labelFormatter={(label) => {
                          const item = vehicleCountData.find((d) => d.road === label);
                          return item?.fullRoad || label;
                        }}
                      />
                      <Bar dataKey="cars" fill="#06B6D4" name="cars" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="motors" fill="#10B981" name="motors" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Speed Chart */}
              <Card className="border-border/50">
                <CardHeader className="pb-2">
                  <CardTitle className="text-base flex items-center gap-2">
                    <Gauge className="h-4 w-4 text-orange-400" />
                    Tốc độ trung bình (km/h)
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={280}>
                    <BarChart data={speedData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                      <XAxis dataKey="road" tick={{ fontSize: 11 }} />
                      <YAxis tick={{ fontSize: 11 }} />
                      <Tooltip
                        contentStyle={{ background: '#1e293b', border: '1px solid rgba(6,182,212,0.3)', borderRadius: '8px' }}
                        formatter={(value, name) => [
                          `${Number(value).toFixed(1)} km/h`,
                          name === "carSpeed" ? "Ô tô" : "Xe máy",
                        ]}
                        labelFormatter={(label) => {
                          const item = speedData.find((d) => d.road === label);
                          return item?.fullRoad || label;
                        }}
                      />
                      <Bar dataKey="carSpeed" fill="#F59E0B" name="carSpeed" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="motorSpeed" fill="#8B5CF6" name="motorSpeed" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="trends" ref={trendsRef}>
            <Card className="border-border/50">
              <CardHeader className="pb-2">
                <CardTitle className="text-base flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-cyan-400" />
                  Xu hướng giao thông theo thời gian
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={350}>
                  <LineChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis dataKey="time" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip
                      contentStyle={{ background: '#1e293b', border: '1px solid rgba(6,182,212,0.3)', borderRadius: '8px' }}
                    />
                    <Legend />
                    {allowedRoads.map((road, index) => (
                      <Line
                        key={road}
                        type="monotone"
                        dataKey={`${road}_total`}
                        stroke={COLORS[index % COLORS.length]}
                        name={road}
                        strokeWidth={2}
                        dot={{ r: 3 }}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="distribution" ref={distributionRef}>
            <Card className="border-border/50">
              <CardHeader className="pb-2">
                <CardTitle className="text-base flex items-center gap-2">
                  <PieChartIcon className="h-4 w-4 text-cyan-400" />
                  Phân bố xe theo tuyến đường
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={350}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) =>
                        `${name} (${(percent * 100).toFixed(0)}%)`
                      }
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {pieData.map((_, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ background: '#1e293b', border: '1px solid rgba(6,182,212,0.3)', borderRadius: '8px' }}
                      formatter={(value, _, props) => [
                        `${value} xe (${props.payload.cars} ô tô, ${props.payload.motors} xe máy)`,
                        "Tổng số xe",
                      ]}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      ) : (
        // GRID MODE - All charts visible at once with collapsible panels
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          {/* Vehicle Count Chart */}
          <AnimatePresence>
            {visiblePanels.vehicleCount && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <Card className="border-border/50">
                  <CardHeader className="pb-2 flex flex-row items-center justify-between">
                    <CardTitle className="text-base flex items-center gap-2">
                      <Zap className="h-4 w-4 text-cyan-400" />
                      Số lượng xe theo tuyến
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={280}>
                      <BarChart data={vehicleCountData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis dataKey="road" tick={{ fontSize: 11 }} />
                        <YAxis tick={{ fontSize: 11 }} />
                        <Tooltip
                          contentStyle={{ background: '#1e293b', border: '1px solid rgba(6,182,212,0.3)', borderRadius: '8px' }}
                          formatter={(value, name) => [
                            value,
                            name === "cars" ? "Ô tô" : "Xe máy",
                          ]}
                          labelFormatter={(label) => {
                            const item = vehicleCountData.find((d) => d.road === label);
                            return item?.fullRoad || label;
                          }}
                        />
                        <Bar dataKey="cars" fill="#06B6D4" name="cars" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="motors" fill="#10B981" name="motors" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Speed Chart */}
          <AnimatePresence>
            {visiblePanels.speed && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <Card className="border-border/50">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base flex items-center gap-2">
                      <Gauge className="h-4 w-4 text-orange-400" />
                      Tốc độ trung bình (km/h)
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={280}>
                      <BarChart data={speedData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis dataKey="road" tick={{ fontSize: 11 }} />
                        <YAxis tick={{ fontSize: 11 }} />
                        <Tooltip
                          contentStyle={{ background: '#1e293b', border: '1px solid rgba(6,182,212,0.3)', borderRadius: '8px' }}
                          formatter={(value, name) => [
                            `${Number(value).toFixed(1)} km/h`,
                            name === "carSpeed" ? "Ô tô" : "Xe máy",
                          ]}
                          labelFormatter={(label) => {
                            const item = speedData.find((d) => d.road === label);
                            return item?.fullRoad || label;
                          }}
                        />
                        <Bar dataKey="carSpeed" fill="#F59E0B" name="carSpeed" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="motorSpeed" fill="#8B5CF6" name="motorSpeed" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Trends Chart - Full width */}
          <AnimatePresence>
            {visiblePanels.trends && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
                className="xl:col-span-2"
              >
                <Card className="border-border/50">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-cyan-400" />
                      Xu hướng giao thông theo thời gian
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <AreaChart data={historicalData}>
                        <defs>
                          {allowedRoads.map((_, index) => (
                            <linearGradient key={index} id={`gradient${index}`} x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor={COLORS[index % COLORS.length]} stopOpacity={0.3} />
                              <stop offset="95%" stopColor={COLORS[index % COLORS.length]} stopOpacity={0} />
                            </linearGradient>
                          ))}
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis dataKey="time" tick={{ fontSize: 11 }} />
                        <YAxis tick={{ fontSize: 11 }} />
                        <Tooltip
                          contentStyle={{ background: '#1e293b', border: '1px solid rgba(6,182,212,0.3)', borderRadius: '8px' }}
                        />
                        <Legend />
                        {allowedRoads.map((road, index) => (
                          <Area
                            key={road}
                            type="monotone"
                            dataKey={`${road}_total`}
                            stroke={COLORS[index % COLORS.length]}
                            fill={`url(#gradient${index})`}
                            name={road}
                            strokeWidth={2}
                          />
                        ))}
                      </AreaChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Distribution Pie Chart */}
          <AnimatePresence>
            {visiblePanels.distribution && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <Card className="border-border/50">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base flex items-center gap-2">
                      <PieChartIcon className="h-4 w-4 text-cyan-400" />
                      Phân bố xe theo tuyến đường
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={pieData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }) =>
                            `${name} (${(percent * 100).toFixed(0)}%)`
                          }
                          outerRadius={100}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {pieData.map((_, index) => (
                            <Cell
                              key={`cell-${index}`}
                              fill={COLORS[index % COLORS.length]}
                            />
                          ))}
                        </Pie>
                        <Tooltip
                          contentStyle={{ background: '#1e293b', border: '1px solid rgba(6,182,212,0.3)', borderRadius: '8px' }}
                          formatter={(value, _, props) => [
                            `${value} xe (${props.payload.cars} ô tô, ${props.payload.motors} xe máy)`,
                            "Tổng số xe",
                          ]}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Road Comparison Table - New Panel */}
          <AnimatePresence>
            {visiblePanels.roadComparison && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <Card className="border-border/50">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base flex items-center gap-2">
                      <MapPin className="h-4 w-4 text-purple-400" />
                      So sánh chi tiết các tuyến
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="overflow-auto max-h-[300px]">
                      <table className="w-full text-sm">
                        <thead className="sticky top-0 bg-secondary/50 backdrop-blur-sm">
                          <tr className="border-b border-border">
                            <th className="text-left p-2 font-medium">Tuyến đường</th>
                            <th className="text-right p-2 font-medium">Ô tô</th>
                            <th className="text-right p-2 font-medium">Xe máy</th>
                            <th className="text-right p-2 font-medium">Tổng</th>
                            <th className="text-right p-2 font-medium">Tốc độ TB</th>
                          </tr>
                        </thead>
                        <tbody>
                          {vehicleCountData.map((item, idx) => (
                            <tr key={idx} className="border-b border-border/30 hover:bg-secondary/30 transition-colors">
                              <td className="p-2 font-medium" title={item.fullRoad}>{item.road}</td>
                              <td className="text-right p-2 text-cyan-400">{item.cars}</td>
                              <td className="text-right p-2 text-green-400">{item.motors}</td>
                              <td className="text-right p-2 font-semibold">{item.total}</td>
                              <td className="text-right p-2 text-orange-400">
                                {((speedData[idx]?.carSpeed || 0) + (speedData[idx]?.motorSpeed || 0) / 2).toFixed(1)} km/h
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
};

export default TrafficAnalytics;
