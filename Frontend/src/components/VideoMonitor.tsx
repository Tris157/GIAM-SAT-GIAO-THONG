import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Video,
  Car,
  Bike,
  AlertTriangle,
  CheckCircle,
  Clock,
  Gauge,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import VideoModal from "./VideoModal";

interface VehicleData {
  count_car: number;
  count_motor: number;
  speed_car: number;
  speed_motor: number;
}

interface FrameData {
  [roadName: string]: {
    frame: string; // Now contains blob URL
  };
}

interface TrafficData {
  [roadName: string]: VehicleData;
}

interface VideoMonitorProps {
  frameData: FrameData;
  trafficData: TrafficData;
  allowedRoads: string[];
  selectedRoad: string | null;
  setSelectedRoad: (road: string | null) => void;
  loading: boolean;
  isFullscreen: boolean;
}

const VideoMonitor = ({
  frameData,
  trafficData,
  allowedRoads,
  selectedRoad,
  loading,
  isFullscreen,
}: VideoMonitorProps) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [modalRoadName, setModalRoadName] = useState<string>("");

  const getTrafficStatus = (roadName: string) => {
    const data = trafficData[roadName];
    if (!data)
      return {
        status: "unknown",
        color: "gray",
        icon: Clock,
        text: "Không rõ",
      };

    const totalVehicles = data.count_car + data.count_motor;
    if (totalVehicles > 20)
      return {
        status: "congested",
        color: "red",
        icon: AlertTriangle,
        text: "Tắc nghẽn",
      };
    if (totalVehicles > 8)
      return { status: "busy", color: "yellow", icon: Clock, text: "Đông đúc" };
    return {
      status: "clear",
      color: "green",
      icon: CheckCircle,
      text: "Thông thoáng",
    };
  };

  const getStatusBadgeVariant = (color: string) => {
    switch (color) {
      case "red":
        return "destructive";
      case "yellow":
        return "secondary";
      case "green":
        return "default";
      default:
        return "outline";
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Video className="h-4 w-4 sm:h-5 sm:w-5" />
            <span className="text-sm sm:text-base">Giám Sát Video</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div
            className={`grid gap-3 sm:gap-4 ${
              isFullscreen
                ? "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
                : "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"
            }`}
          >
            {allowedRoads.map((road) => (
              <div key={road} className="space-y-2 sm:space-y-3">
                <Skeleton className="aspect-[3/2] w-full max-w-sm mx-auto rounded-lg" />
                <Skeleton className="h-3 sm:h-4 w-3/4" />
                <Skeleton className="h-3 sm:h-4 w-1/2" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full glass border-white/20 dark:border-white/10 shadow-xl overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500" />
      <CardHeader className="px-3 sm:px-6 pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2 text-base sm:text-lg">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow-md">
              <Video className="h-4 w-4 sm:h-5 sm:w-5 text-white" />
            </div>
            <span>Camera Giao Thông</span>
          </CardTitle>
        </div>
      </CardHeader>
      <CardContent className="px-3 sm:px-6">
        <div
          className={`grid gap-4 sm:gap-6 ${
            isFullscreen
              ? "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
              : "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"
          }`}
        >
          <AnimatePresence>
            {allowedRoads.map((roadName) => {
              const frame = frameData[roadName];
              const data = trafficData[roadName];
              const { color, icon: Icon, text } = getTrafficStatus(roadName);
              const isSelected = selectedRoad === roadName;

              return (
                <motion.div
                  key={roadName}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{
                    opacity: 1,
                    scale: isSelected ? 1.03 : 1,
                    transition: { duration: 0.3, ease: "easeOut" },
                  }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  whileHover={{ scale: 1.02, y: -4 }}
                  className={`group relative overflow-hidden rounded-2xl border-2 transition-all duration-300 cursor-pointer inline-block w-full max-w-sm mx-auto shadow-lg hover:shadow-2xl ${
                    isSelected
                      ? "border-blue-500 shadow-blue-500/30 ring-4 ring-blue-500/20"
                      : "border-white/20 dark:border-white/10 hover:border-blue-400/50"
                  }`}
                  onClick={() => {
                    setModalRoadName(roadName);
                    setModalOpen(true);
                  }}
                >
                  {/* Gradient overlay for selected state */}
                  {isSelected && (
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 via-purple-500/10 to-pink-500/10 pointer-events-none z-10" />
                  )}

                  {/* Video Frame (responsive) */}
                  <div className="relative w-full max-w-sm mx-auto aspect-[3/2] bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 overflow-hidden">
                    {frame?.frame ? (
                      <img
                        src={frame.frame}
                        alt={`Camera ${roadName}`}
                        className="w-full h-full object-contain block transition-transform duration-300 group-hover:scale-105"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <div className="relative">
                          <Video className="h-8 w-8 sm:h-12 sm:w-12 text-gray-400 animate-pulse" />
                          <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-xl animate-pulse" />
                        </div>
                      </div>
                    )}

                    {/* Click to expand hint */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300 flex items-center justify-center">
                      <motion.div
                        initial={{ scale: 0.8, opacity: 0 }}
                        whileHover={{ scale: 1, opacity: 1 }}
                        className="glass px-3 py-2 sm:px-4 sm:py-2.5 rounded-xl text-white text-xs sm:text-sm font-semibold shadow-lg border border-white/30"
                      >
                        🔍 Click để phóng to
                      </motion.div>
                    </div>

                    {/* Live indicator */}
                    {frame?.frame && (
                      <div className="absolute top-3 right-3 z-20">
                        <div className="flex items-center space-x-1.5 glass px-2.5 py-1.5 rounded-full border border-white/30">
                          <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse shadow-lg shadow-red-500/50" />
                          <span className="text-xs font-semibold text-white">LIVE</span>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Info Panel (responsive) */}
                  <div className="relative bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm p-3 sm:p-4 border-t border-white/20 dark:border-white/10">
                    <h3 className="font-bold text-base sm:text-lg mb-2 sm:mb-3 flex items-center justify-between">
                      <span className="truncate bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
                        {roadName}
                      </span>
                    </h3>

                    {/* Status */}
                    <div className="mb-3 sm:mb-4">
                      <Badge
                        variant={getStatusBadgeVariant(color)}
                        className={`flex items-center space-x-1.5 sm:space-x-2 text-xs shadow-md ${
                          color === "red"
                            ? "bg-gradient-to-r from-red-500 to-orange-600"
                            : color === "yellow"
                            ? "bg-gradient-to-r from-yellow-500 to-amber-600"
                            : "bg-gradient-to-r from-green-500 to-emerald-600"
                        } text-white border-none`}
                      >
                        <Icon className="h-3 w-3 sm:h-4 sm:w-4" />
                        <span className="text-xs font-semibold">{text}</span>
                      </Badge>
                    </div>

                    {data ? (
                      <div className="grid grid-cols-2 gap-3 sm:gap-4">
                        {/* Car Stats */}
                        <motion.div
                          whileHover={{ scale: 1.05 }}
                          className="flex flex-col p-2 sm:p-3 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 rounded-xl border border-blue-200/50 dark:border-blue-700/30 shadow-sm"
                        >
                          <div className="flex items-center space-x-2 mb-1.5">
                            <div className="p-1.5 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-md">
                              <Car className="h-3 w-3 sm:h-4 sm:w-4 text-white" />
                            </div>
                            <p className="text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300">
                              Ô tô
                            </p>
                          </div>
                          <p className="font-bold text-lg sm:text-xl text-blue-600 dark:text-blue-400 mb-0.5">
                            {data.count_car}
                          </p>
                          <p className="text-xs text-gray-600 dark:text-gray-400 flex items-center">
                            <Gauge className="h-3 w-3 mr-1" />
                            {data.speed_car.toFixed(1)} km/h
                          </p>
                        </motion.div>

                        {/* Motorbike Stats */}
                        <motion.div
                          whileHover={{ scale: 1.05 }}
                          className="flex flex-col p-2 sm:p-3 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/30 dark:to-green-800/30 rounded-xl border border-green-200/50 dark:border-green-700/30 shadow-sm"
                        >
                          <div className="flex items-center space-x-2 mb-1.5">
                            <div className="p-1.5 bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow-md">
                              <Bike className="h-3 w-3 sm:h-4 sm:w-4 text-white" />
                            </div>
                            <p className="text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300">
                              Xe máy
                            </p>
                          </div>
                          <p className="font-bold text-lg sm:text-xl text-green-600 dark:text-green-400 mb-0.5">
                            {data.count_motor}
                          </p>
                          <p className="text-xs text-gray-600 dark:text-gray-400 flex items-center">
                            <Gauge className="h-3 w-3 mr-1" />
                            {data.speed_motor.toFixed(1)} km/h
                          </p>
                        </motion.div>
                      </div>
                    ) : (
                      <div className="flex items-center justify-center py-4 sm:py-6">
                        <div className="text-center">
                          <div className="relative inline-block mb-2">
                            <Gauge className="h-8 w-8 sm:h-10 sm:w-10 text-gray-400 animate-pulse" />
                            <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-xl animate-pulse" />
                          </div>
                          <p className="text-xs sm:text-sm text-gray-500 font-medium">
                            Đang tải dữ liệu...
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      </CardContent>

      {/* Video Modal */}
      <VideoModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        roadName={modalRoadName}
        frameData={frameData[modalRoadName]?.frame || null}
        trafficData={trafficData[modalRoadName]}
      />
    </Card>
  );
};

export default VideoMonitor;
