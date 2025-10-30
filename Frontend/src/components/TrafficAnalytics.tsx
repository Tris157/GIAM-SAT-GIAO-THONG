import { useState, useEffect } from "react";
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
} from "recharts";
import {
  TrendingUp,
  Activity,
  Car,
  Bike,
  BarChart3,
  PieChart as PieChartIcon,
  LineChart as LineChartIcon,
} from "lucide-react";
import { motion } from "framer-motion";

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
  // const [selectedMetric, setSelectedMetric] = useState<"vehicles" | "speed">(
  //   "vehicles"
  // );

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
        // Keep only last 20 data points
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

  const COLORS = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"];

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

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          whileHover={{ y: -4 }}
        >
          <Card className="relative overflow-hidden glass border-white/20 dark:border-white/10 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 to-cyan-500" />
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-3 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl shadow-lg">
                    <Activity className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-xs sm:text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                      Tổng xe
                    </p>
                    <p className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-400 dark:to-cyan-400 bg-clip-text text-transparent">
                      {totalVehicles}
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          whileHover={{ y: -4 }}
        >
          <Card className="relative overflow-hidden glass border-white/20 dark:border-white/10 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-green-500 to-emerald-500" />
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg">
                    <Car className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-xs sm:text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                      Tốc độ TB ô tô
                    </p>
                    <p className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 dark:from-green-400 dark:to-emerald-400 bg-clip-text text-transparent">
                      {averageSpeed.car.toFixed(1)}
                      <span className="text-base sm:text-lg ml-1">km/h</span>
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          whileHover={{ y: -4 }}
        >
          <Card className="relative overflow-hidden glass border-white/20 dark:border-white/10 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 to-pink-500" />
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl shadow-lg">
                    <Bike className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-xs sm:text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                      Tốc độ TB xe máy
                    </p>
                    <p className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 dark:from-purple-400 dark:to-pink-400 bg-clip-text text-transparent">
                      {averageSpeed.motor.toFixed(1)}
                      <span className="text-base sm:text-lg ml-1">km/h</span>
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          whileHover={{ y: -4 }}
        >
          <Card className="relative overflow-hidden glass border-white/20 dark:border-white/10 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-orange-500 to-red-500" />
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-3 bg-gradient-to-br from-orange-500 to-red-600 rounded-xl shadow-lg">
                    <TrendingUp className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-xs sm:text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                      Đông nhất
                    </p>
                    <p className="text-base sm:text-lg font-bold bg-gradient-to-r from-orange-600 to-red-600 dark:from-orange-400 dark:to-red-400 bg-clip-text text-transparent">
                      {busiestRoad.road || "N/A"}
                    </p>
                    <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 font-medium">
                      {busiestRoad.vehicles} xe
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Charts */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3 h-14 glass rounded-xl p-1.5 shadow-lg border border-white/20 dark:border-white/10">
          <TabsTrigger
            value="overview"
            className="flex items-center space-x-2 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-500 data-[state=active]:to-purple-600 data-[state=active]:text-white transition-all duration-300"
          >
            <BarChart3 className="h-4 w-4" />
            <span className="hidden sm:inline">Tổng quan</span>
          </TabsTrigger>
          <TabsTrigger
            value="trends"
            className="flex items-center space-x-2 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-500 data-[state=active]:to-pink-600 data-[state=active]:text-white transition-all duration-300"
          >
            <LineChartIcon className="h-4 w-4" />
            <span className="hidden sm:inline">Xu hướng</span>
          </TabsTrigger>
          <TabsTrigger
            value="distribution"
            className="flex items-center space-x-2 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-orange-600 data-[state=active]:text-white transition-all duration-300"
          >
            <PieChartIcon className="h-4 w-4" />
            <span className="hidden sm:inline">Phân bố</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Vehicle Count Chart */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              <Card className="glass border-white/20 dark:border-white/10 shadow-lg overflow-hidden">
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 to-purple-500" />
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
                      <BarChart3 className="h-4 w-4 text-white" />
                    </div>
                    <span>Số lượng xe theo tuyến đường</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-6">
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={vehicleCountData}>
                      <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
                      <XAxis dataKey="road" className="text-xs" />
                      <YAxis className="text-xs" />
                      <Tooltip
                        formatter={(value, name) => [
                          value,
                          name === "cars" ? "Ô tô" : "Xe máy",
                        ]}
                        labelFormatter={(label) => {
                          const item = vehicleCountData.find(
                            (d) => d.road === label
                          );
                          return item?.fullRoad || label;
                        }}
                        contentStyle={{
                          backgroundColor: "rgba(255, 255, 255, 0.9)",
                          border: "1px solid rgba(0, 0, 0, 0.1)",
                          borderRadius: "8px",
                        }}
                      />
                      <Bar dataKey="cars" fill="url(#colorCars)" name="cars" radius={[8, 8, 0, 0]} />
                      <Bar dataKey="motors" fill="url(#colorMotors)" name="motors" radius={[8, 8, 0, 0]} />
                      <defs>
                        <linearGradient id="colorCars" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="#3B82F6" stopOpacity={1} />
                          <stop offset="100%" stopColor="#1E40AF" stopOpacity={0.8} />
                        </linearGradient>
                        <linearGradient id="colorMotors" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="#10B981" stopOpacity={1} />
                          <stop offset="100%" stopColor="#047857" stopOpacity={0.8} />
                        </linearGradient>
                      </defs>
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </motion.div>

            {/* Speed Chart */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 }}
            >
              <Card className="glass border-white/20 dark:border-white/10 shadow-lg overflow-hidden">
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-orange-500 to-yellow-500" />
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <div className="p-2 bg-gradient-to-br from-orange-500 to-yellow-600 rounded-lg">
                      <LineChartIcon className="h-4 w-4 text-white" />
                    </div>
                    <span>Tốc độ trung bình (km/h)</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-6">
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={speedData}>
                      <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
                      <XAxis dataKey="road" className="text-xs" />
                      <YAxis className="text-xs" />
                      <Tooltip
                        formatter={(value, name) => [
                          `${Number(value).toFixed(1)} km/h`,
                          name === "carSpeed" ? "Ô tô" : "Xe máy",
                        ]}
                        labelFormatter={(label) => {
                          const item = speedData.find((d) => d.road === label);
                          return item?.fullRoad || label;
                        }}
                        contentStyle={{
                          backgroundColor: "rgba(255, 255, 255, 0.9)",
                          border: "1px solid rgba(0, 0, 0, 0.1)",
                          borderRadius: "8px",
                        }}
                      />
                      <Bar dataKey="carSpeed" fill="url(#colorCarSpeed)" name="carSpeed" radius={[8, 8, 0, 0]} />
                      <Bar dataKey="motorSpeed" fill="url(#colorMotorSpeed)" name="motorSpeed" radius={[8, 8, 0, 0]} />
                      <defs>
                        <linearGradient id="colorCarSpeed" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="#F59E0B" stopOpacity={1} />
                          <stop offset="100%" stopColor="#D97706" stopOpacity={0.8} />
                        </linearGradient>
                        <linearGradient id="colorMotorSpeed" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="#8B5CF6" stopOpacity={1} />
                          <stop offset="100%" stopColor="#7C3AED" stopOpacity={0.8} />
                        </linearGradient>
                      </defs>
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </TabsContent>

        <TabsContent value="trends">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="glass border-white/20 dark:border-white/10 shadow-lg overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 to-pink-500" />
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-600 rounded-lg">
                    <LineChartIcon className="h-4 w-4 text-white" />
                  </div>
                  <span>Xu hướng giao thông theo thời gian</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
                    <XAxis dataKey="time" className="text-xs" />
                    <YAxis className="text-xs" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "rgba(255, 255, 255, 0.9)",
                        border: "1px solid rgba(0, 0, 0, 0.1)",
                        borderRadius: "8px",
                      }}
                    />
                    <Legend />
                    {allowedRoads.map((road, index) => (
                      <Line
                        key={road}
                        type="monotone"
                        dataKey={`${road}_total`}
                        stroke={COLORS[index % COLORS.length]}
                        name={road}
                        strokeWidth={3}
                        dot={{ r: 4 }}
                        activeDot={{ r: 6 }}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </motion.div>
        </TabsContent>

        <TabsContent value="distribution">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="glass border-white/20 dark:border-white/10 shadow-lg overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-pink-500 to-orange-500" />
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <div className="p-2 bg-gradient-to-br from-pink-500 to-orange-600 rounded-lg">
                    <PieChartIcon className="h-4 w-4 text-white" />
                  </div>
                  <span>Phân bố xe theo tuyến đường</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <ResponsiveContainer width="100%" height={400}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={{
                        stroke: "rgba(99, 102, 241, 0.5)",
                        strokeWidth: 2,
                      }}
                      label={({ name, percent }) =>
                        `${name} (${(percent * 100).toFixed(0)}%)`
                      }
                      outerRadius={140}
                      fill="#8884d8"
                      dataKey="value"
                      paddingAngle={2}
                    >
                      {pieData.map((_, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                          className="hover:opacity-80 transition-opacity cursor-pointer"
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(value, _, props) => [
                        `${value} xe (${props.payload.cars} ô tô, ${props.payload.motors} xe máy)`,
                        "Tổng số xe",
                      ]}
                      contentStyle={{
                        backgroundColor: "rgba(255, 255, 255, 0.95)",
                        border: "1px solid rgba(0, 0, 0, 0.1)",
                        borderRadius: "8px",
                        boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
                      }}
                    />
                    <Legend
                      verticalAlign="bottom"
                      height={36}
                      iconType="circle"
                    />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </motion.div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default TrafficAnalytics;
