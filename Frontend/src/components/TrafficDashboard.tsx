import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  MapPin,
  Car,
  Bike,
  AlertTriangle,
  CheckCircle,
  Clock,
  Settings,
  Moon,
  Sun,
  Maximize2,
  Minimize2,
  MessageCircle,
  Video,
  LogOut,
  User,
} from "lucide-react";
import { useTheme } from "next-themes";
import { useAuth } from "../contexts/AuthContext";
import VideoMonitor from "./VideoMonitor";
import ChatInterface from "./ChatInterface";
import TrafficAnalytics from "./TrafficAnalytics";
import TrafficReports from "./TrafficReports";
import RTSPLiveStream from "./RTSPLiveStream";
import WeatherWidget from "./WeatherWidget";
import ViolationsManagement from "./ViolationsManagement";
import { motion, AnimatePresence } from "framer-motion";
import { useMultipleTrafficInfo, useMultipleFrameStreams } from "../hooks/useWebSocket";
import { endpoints } from "../config";

// Import types from the WebSocket hook
type VehicleData = {
  count_car: number;
  count_motor: number;
  speed_car: number;
  speed_motor: number;
};

const TrafficDashboard = () => {
  const [selectedRoad, setSelectedRoad] = useState<string | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const { theme, setTheme } = useTheme();
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const [allowedRoads, setAllowedRoads] = useState<string[]>([]);

  useEffect(() => {
    const fetchRoads = async () => {
      try {
        const res = await fetch(endpoints.roadNames);
        const json = await res.json();
        const names: string[] = json?.road_names ?? [];
        setAllowedRoads(names);
      } catch {
        // fallback to known demo names if API not ready
        setAllowedRoads(["Văn Phú", "Nguyễn Trãi", "Ngã Tư Sở", "Đường Láng", "Văn Quán"]);
      }
    };
    fetchRoads();
  }, []);

  // Use WebSocket for traffic data
  const { trafficData, isAnyConnected } = useMultipleTrafficInfo(allowedRoads);
  const { frameData: frames } = useMultipleFrameStreams(allowedRoads);

  const loading = !isAnyConnected;

  const getTrafficStatus = (roadName: string) => {
    const data = trafficData[roadName] as VehicleData | undefined;
    if (!data) return { status: "unknown", color: "gray", icon: Clock };

    const totalVehicles = data.count_car + data.count_motor;
    if (totalVehicles > 15)
      return { status: "congested", color: "red", icon: AlertTriangle };
    if (totalVehicles > 8)
      return { status: "busy", color: "yellow", icon: Clock };
    return { status: "clear", color: "green", icon: CheckCircle };
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "congested":
        return "Tắc nghẽn";
      case "busy":
        return "Đông đúc";
      case "clear":
        return "Thông thoáng";
      default:
        return "Không rõ";
    }
  };

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8 space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="relative"
      >
        <div className="glass rounded-2xl p-6 shadow-2xl border border-white/10">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <motion.div
                whileHover={{ scale: 1.05, rotate: 5 }}
                whileTap={{ scale: 0.95 }}
                className="relative p-3 bg-gradient-to-br from-indigo-500 via-purple-500 to-cyan-500 rounded-xl text-white shadow-lg animate-glow"
              >
                <MapPin className="h-8 w-8" />
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-400 to-cyan-400 rounded-xl opacity-0 hover:opacity-20 transition-opacity"></div>
              </motion.div>
              <div>
                <h1 className="text-3xl md:text-4xl font-bold gradient-text">
                  Hệ Thống Giám Sát Giao Thông Thông Minh
                </h1>
                <p className="text-gray-400 dark:text-gray-400 mt-1 flex items-center space-x-2">
                  <span className="inline-block w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                  <span>Giám sát và phân tích giao thông thời gian thực</span>
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              {/* User info badge */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
                className="hidden md:flex items-center space-x-2 px-4 py-2 glass rounded-xl border border-white/10"
              >
                <User className="h-4 w-4 text-blue-400" />
                <div className="flex flex-col">
                  <span className="text-sm font-semibold text-white">
                    {user?.full_name || user?.username}
                  </span>
                  {isAdmin && (
                    <span className="text-xs text-yellow-400 font-medium">Admin</span>
                  )}
                </div>
              </motion.div>

              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                  className="glass border-white/20 hover:bg-white/10 hover:border-white/30 transition-all duration-300"
                >
                  {theme === "dark" ? (
                    <Sun className="h-4 w-4 text-yellow-400" />
                  ) : (
                    <Moon className="h-4 w-4 text-blue-400" />
                  )}
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => setIsFullscreen(!isFullscreen)}
                  className="glass border-white/20 hover:bg-white/10 hover:border-white/30 transition-all duration-300"
                >
                  {isFullscreen ? (
                    <Minimize2 className="h-4 w-4 text-cyan-400" />
                  ) : (
                    <Maximize2 className="h-4 w-4 text-purple-400" />
                  )}
                </Button>
              </motion.div>

              {/* Logout button */}
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={handleLogout}
                  className="glass border-white/20 hover:bg-red-500/20 hover:border-red-400/30 transition-all duration-300"
                  title="Logout"
                >
                  <LogOut className="h-4 w-4 text-red-400" />
                </Button>
              </motion.div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <Tabs defaultValue="monitor" className="space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <TabsList className="glass grid w-full grid-cols-5 h-14 p-1 border border-white/10 shadow-xl">
            <TabsTrigger
              value="monitor"
              className="text-base py-3 px-6 font-medium data-[state=active]:bg-gradient-to-r data-[state=active]:from-indigo-500 data-[state=active]:to-purple-500 data-[state=active]:text-white transition-all duration-300 rounded-lg"
            >
              <motion.div
                className="flex items-center space-x-2"
                whileHover={{ scale: 1.05 }}
              >
                <MapPin className="h-5 w-5" />
                <span>Giám Sát</span>
              </motion.div>
            </TabsTrigger>
            <TabsTrigger
              value="live"
              className="text-base py-3 px-6 font-medium data-[state=active]:bg-gradient-to-r data-[state=active]:from-green-500 data-[state=active]:to-emerald-500 data-[state=active]:text-white transition-all duration-300 rounded-lg"
            >
              <motion.div
                className="flex items-center space-x-2"
                whileHover={{ scale: 1.05 }}
              >
                <Video className="h-5 w-5" />
                <span>Camera Live</span>
              </motion.div>
            </TabsTrigger>
            <TabsTrigger
              value="analytics"
              className="text-base py-3 px-6 font-medium data-[state=active]:bg-gradient-to-r data-[state=active]:from-cyan-500 data-[state=active]:to-blue-500 data-[state=active]:text-white transition-all duration-300 rounded-lg"
            >
              <motion.div
                className="flex items-center space-x-2"
                whileHover={{ scale: 1.05 }}
              >
                <Settings className="h-5 w-5" />
                <span>Phân Tích</span>
              </motion.div>
            </TabsTrigger>
            <TabsTrigger
              value="violations"
              className="text-base py-3 px-6 font-medium data-[state=active]:bg-gradient-to-r data-[state=active]:from-red-500 data-[state=active]:to-orange-500 data-[state=active]:text-white transition-all duration-300 rounded-lg"
            >
              <motion.div
                className="flex items-center space-x-2"
                whileHover={{ scale: 1.05 }}
              >
                <AlertTriangle className="h-5 w-5" />
                <span>Vi Phạm</span>
              </motion.div>
            </TabsTrigger>
            <TabsTrigger
              value="chat"
              className="text-base py-3 px-6 font-medium data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-500 data-[state=active]:to-pink-500 data-[state=active]:text-white transition-all duration-300 rounded-lg"
            >
              <motion.div
                className="flex items-center space-x-2"
                whileHover={{ scale: 1.05 }}
              >
                <MessageCircle className="h-5 w-5" />
                <span>Trợ Lý AI</span>
              </motion.div>
            </TabsTrigger>
          </TabsList>
        </motion.div>

        <TabsContent value="monitor" className="space-y-6">
          <div
            className={`grid gap-6 ${
              isFullscreen ? "grid-cols-1" : "grid-cols-1 lg:grid-cols-4"
            }`}
          >
            {/* Video Monitoring */}
            <div className={isFullscreen ? "col-span-1" : "col-span-3"}>
              <VideoMonitor
                frameData={frames}
                trafficData={trafficData}
                allowedRoads={allowedRoads}
                selectedRoad={selectedRoad}
                setSelectedRoad={setSelectedRoad}
                loading={loading}
                isFullscreen={isFullscreen}
              />
            </div>

            {/* Traffic Status Cards & Weather */}
            {!isFullscreen && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
                className="space-y-4"
              >
                {/* Weather Widget */}
                <WeatherWidget />

                <Card className="glass border border-white/10 shadow-2xl">
                  <CardHeader className="border-b border-white/10">
                    <CardTitle className="flex items-center space-x-2 text-lg">
                      <motion.div
                        animate={{ rotate: [0, 360] }}
                        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                      >
                        <MapPin className="h-5 w-5 text-indigo-400" />
                      </motion.div>
                      <span className="gradient-text">Tình Trạng Giao Thông</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3 pt-6">
                    <AnimatePresence>
                      {allowedRoads.map((road, index) => {
                        const {
                          status,
                          color,
                          icon: Icon,
                        } = getTrafficStatus(road);
                        const data = trafficData[road];

                        return (
                          <motion.div
                            key={road}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ scale: 1.02, x: 5 }}
                            whileTap={{ scale: 0.98 }}
                            className="relative group flex items-center justify-between p-4 rounded-xl glass border border-white/10 hover:border-indigo-400/50 transition-all duration-300 cursor-pointer overflow-hidden"
                            onClick={() => setSelectedRoad(road)}
                          >
                            {/* Hover gradient background */}
                            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

                            <div className="relative flex items-center space-x-3">
                              <motion.div
                                animate={{ scale: [1, 1.2, 1] }}
                                transition={{ duration: 2, repeat: Infinity }}
                              >
                                <Icon className={`h-4 w-4 ${color === 'red' ? 'text-red-500' : color === 'yellow' ? 'text-yellow-500' : 'text-green-500'}`} />
                              </motion.div>
                              <span className="font-medium text-white">{road}</span>
                            </div>
                            <div className="relative flex items-center space-x-2">
                              <Badge
                                variant={
                                  color === "red"
                                    ? "destructive"
                                    : color === "yellow"
                                    ? "secondary"
                                    : "default"
                                }
                                className="shadow-lg"
                              >
                                {getStatusText(status)}
                              </Badge>
                              {data && (
                                <div className="text-xs text-gray-300 flex items-center space-x-1 glass px-2 py-1 rounded-lg">
                                  <Car className="h-3 w-3 text-blue-400" />
                                  <span>{String(data.count_car)}</span>
                                  <Bike className="h-3 w-3 text-cyan-400" />
                                  <span>{String(data.count_motor)}</span>
                                </div>
                              )}
                            </div>
                          </motion.div>
                        );
                      })}
                    </AnimatePresence>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </div>
        </TabsContent>

        <TabsContent value="live">
          <RTSPLiveStream streamName="camera_live" />
        </TabsContent>

        <TabsContent value="analytics">
          <TrafficReports
            trafficData={trafficData}
            allowedRoads={allowedRoads}
          />
        </TabsContent>

        <TabsContent value="violations">
          <ViolationsManagement />
        </TabsContent>

        <TabsContent value="chat">
          <ChatInterface trafficData={trafficData} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default TrafficDashboard;
