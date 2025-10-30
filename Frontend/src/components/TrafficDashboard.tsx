import { useState, useEffect } from "react";
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
} from "lucide-react";
import { useTheme } from "next-themes";
import VideoMonitor from "./VideoMonitor";
import ChatInterface from "./ChatInterface";
import TrafficAnalytics from "./TrafficAnalytics";
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
    <div className="min-h-screen p-4 sm:p-6 lg:p-8 space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="relative"
      >
        {/* Decorative background gradient */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 rounded-2xl blur-3xl -z-10" />

        <div className="glass rounded-2xl p-6 shadow-xl border border-white/20 dark:border-white/10">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex items-center space-x-4">
              <motion.div
                className="relative p-4 bg-gradient-to-br from-blue-500 via-purple-600 to-pink-500 rounded-2xl text-white shadow-lg"
                whileHover={{ scale: 1.05, rotate: 5 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <MapPin className="h-8 w-8 relative z-10" />
                <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-purple-500 rounded-2xl blur opacity-50 animate-pulse-glow" />
              </motion.div>

              <div>
                <motion.h1
                  className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-1"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 dark:from-blue-400 dark:via-purple-400 dark:to-pink-400 bg-clip-text text-transparent animate-gradient">
                    Hệ Thống Giám Sát Giao Thông Thông Minh
                  </span>
                </motion.h1>
                <motion.div
                  className="flex items-center space-x-2"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400">
                    Giám sát và phân tích giao thông thời gian thực
                  </p>
                  {isAnyConnected && (
                    <Badge variant="outline" className="bg-green-500/10 text-green-600 dark:text-green-400 border-green-500/20">
                      <span className="flex items-center space-x-1">
                        <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                        <span className="text-xs">Live</span>
                      </span>
                    </Badge>
                  )}
                </motion.div>
              </div>
            </div>

            <motion.div
              className="flex items-center space-x-2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Button
                variant="outline"
                size="icon"
                onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                className="glass border-white/20 dark:border-white/10 hover:bg-white/20 dark:hover:bg-white/10 transition-all duration-300"
              >
                {theme === "dark" ? (
                  <Sun className="h-4 w-4 text-yellow-500" />
                ) : (
                  <Moon className="h-4 w-4 text-purple-600" />
                )}
              </Button>
              <Button
                variant="outline"
                size="icon"
                onClick={() => setIsFullscreen(!isFullscreen)}
                className="glass border-white/20 dark:border-white/10 hover:bg-white/20 dark:hover:bg-white/10 transition-all duration-300"
              >
                {isFullscreen ? (
                  <Minimize2 className="h-4 w-4" />
                ) : (
                  <Maximize2 className="h-4 w-4" />
                )}
              </Button>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <Tabs defaultValue="monitor" className="space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <TabsList className="grid w-full grid-cols-3 h-14 glass rounded-xl p-1.5 shadow-lg border border-white/20 dark:border-white/10">
            <TabsTrigger
              value="monitor"
              className="text-sm sm:text-base py-3 px-4 sm:px-6 font-medium rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-500 data-[state=active]:to-purple-600 data-[state=active]:text-white data-[state=active]:shadow-lg transition-all duration-300"
            >
              <div className="flex items-center space-x-2">
                <MapPin className="h-4 w-4 sm:h-5 sm:w-5" />
                <span className="hidden sm:inline">Giám Sát</span>
                <span className="sm:hidden">Giám Sát</span>
              </div>
            </TabsTrigger>
            <TabsTrigger
              value="analytics"
              className="text-sm sm:text-base py-3 px-4 sm:px-6 font-medium rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-500 data-[state=active]:to-pink-600 data-[state=active]:text-white data-[state=active]:shadow-lg transition-all duration-300"
            >
              <div className="flex items-center space-x-2">
                <Settings className="h-4 w-4 sm:h-5 sm:w-5" />
                <span className="hidden sm:inline">Phân Tích</span>
                <span className="sm:hidden">Phân Tích</span>
              </div>
            </TabsTrigger>
            <TabsTrigger
              value="chat"
              className="text-sm sm:text-base py-3 px-4 sm:px-6 font-medium rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-orange-600 data-[state=active]:text-white data-[state=active]:shadow-lg transition-all duration-300"
            >
              <div className="flex items-center space-x-2">
                <MessageCircle className="h-4 w-4 sm:h-5 sm:w-5" />
                <span className="hidden sm:inline">Trợ Lý AI</span>
                <span className="sm:hidden">AI</span>
              </div>
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

            {/* Traffic Status Cards */}
            {!isFullscreen && (
              <div className="space-y-4">
                <Card className="glass border-white/20 dark:border-white/10 shadow-xl overflow-hidden">
                  <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500" />
                  <CardHeader className="pb-3">
                    <CardTitle className="flex items-center space-x-2 text-lg">
                      <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
                        <MapPin className="h-4 w-4 text-white" />
                      </div>
                      <span>Tình Trạng Giao Thông</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <AnimatePresence>
                      {allowedRoads.map((road, index) => {
                        const {
                          status,
                          color,
                          icon: Icon,
                        } = getTrafficStatus(road);
                        const data = trafficData[road];

                        const gradientClass =
                          color === "red"
                            ? "from-red-500/10 to-orange-500/10"
                            : color === "yellow"
                            ? "from-yellow-500/10 to-amber-500/10"
                            : "from-green-500/10 to-emerald-500/10";

                        return (
                          <motion.div
                            key={road}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ scale: 1.02, x: 4 }}
                            className={`relative flex items-center justify-between p-3 rounded-xl bg-gradient-to-r ${gradientClass} border border-white/10 hover:border-white/30 dark:hover:border-white/20 transition-all cursor-pointer group overflow-hidden`}
                            onClick={() => setSelectedRoad(road)}
                          >
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />

                            <div className="flex items-center space-x-3 relative z-10">
                              <div className={`p-2 rounded-lg bg-gradient-to-br ${
                                color === "red"
                                  ? "from-red-500 to-orange-600"
                                  : color === "yellow"
                                  ? "from-yellow-500 to-amber-600"
                                  : "from-green-500 to-emerald-600"
                              } shadow-lg`}>
                                <Icon className="h-3 w-3 text-white" />
                              </div>
                              <span className="font-semibold text-sm">{road}</span>
                            </div>
                            <div className="flex items-center space-x-2 relative z-10">
                              <Badge
                                variant={
                                  color === "red"
                                    ? "destructive"
                                    : color === "yellow"
                                    ? "secondary"
                                    : "default"
                                }
                                className="text-xs font-medium shadow-sm"
                              >
                                {getStatusText(status)}
                              </Badge>
                              {data && (
                                <div className="text-xs text-gray-600 dark:text-gray-300 flex items-center space-x-1 bg-white/50 dark:bg-black/20 px-2 py-1 rounded-lg">
                                  <Car className="h-3 w-3" />
                                  <span className="font-medium">{String(data.count_car)}</span>
                                  <Bike className="h-3 w-3 ml-1" />
                                  <span className="font-medium">{String(data.count_motor)}</span>
                                </div>
                              )}
                            </div>
                          </motion.div>
                        );
                      })}
                    </AnimatePresence>
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
        </TabsContent>

        <TabsContent value="analytics">
          <TrafficAnalytics
            trafficData={trafficData}
            allowedRoads={allowedRoads}
          />
        </TabsContent>

        <TabsContent value="chat">
          <ChatInterface trafficData={trafficData} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default TrafficDashboard;
