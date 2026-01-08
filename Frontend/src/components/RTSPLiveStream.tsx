import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Video, VideoOff, RefreshCw, Maximize2, Minimize2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface RTSPLiveStreamProps {
  streamName?: string;
}

const RTSPLiveStream = ({ streamName = "camera_live" }: RTSPLiveStreamProps) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const imgRef = useRef<HTMLImageElement>(new Image());
  const containerRef = useRef<HTMLDivElement | null>(null);

  const connectWebSocket = () => {
    try {
      setError(null);
      const ws = new WebSocket(`ws://localhost:8000/ws/rtsp/${streamName}`);
      ws.binaryType = "arraybuffer"; // Set binary type để nhận ArrayBuffer

      ws.onopen = () => {
        console.log("✅ RTSP WebSocket connected");
        setIsConnected(true);
        setError(null);
      };

      ws.onmessage = (event) => {
        try {
          // Backend gửi binary JPEG frames
          if (event.data instanceof ArrayBuffer) {
            // Convert ArrayBuffer to Blob
            const blob = new Blob([event.data], { type: "image/jpeg" });
            const url = URL.createObjectURL(blob);

            imgRef.current.onload = () => {
              const canvas = canvasRef.current;
              if (canvas) {
                const ctx = canvas.getContext("2d");
                if (ctx) {
                  canvas.width = imgRef.current.width;
                  canvas.height = imgRef.current.height;
                  ctx.drawImage(imgRef.current, 0, 0);
                }
              }
              URL.revokeObjectURL(url);
            };

            imgRef.current.onerror = () => {
              console.error("Failed to load image");
              URL.revokeObjectURL(url);
            };

            imgRef.current.src = url;
          } else if (event.data instanceof Blob) {
            // Fallback nếu nhận Blob trực tiếp
            const url = URL.createObjectURL(event.data);
            imgRef.current.onload = () => {
              const canvas = canvasRef.current;
              if (canvas) {
                const ctx = canvas.getContext("2d");
                if (ctx) {
                  canvas.width = imgRef.current.width;
                  canvas.height = imgRef.current.height;
                  ctx.drawImage(imgRef.current, 0, 0);
                }
              }
              URL.revokeObjectURL(url);
            };
            imgRef.current.src = url;
          }
        } catch (err) {
          console.error("Error processing frame:", err);
          setError("Lỗi xử lý khung hình");
        }
      };

      ws.onerror = (error) => {
        console.error("❌ RTSP WebSocket error:", error);
        setError("Lỗi kết nối WebSocket");
        setIsConnected(false);
      };

      ws.onclose = () => {
        console.log("🔌 RTSP WebSocket disconnected");
        setIsConnected(false);
      };

      wsRef.current = ws;
    } catch (err) {
      console.error("Error connecting to WebSocket:", err);
      setError("Không thể kết nối đến camera");
    }
  };

  const disconnect = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setIsConnected(false);
  };

  const reconnect = () => {
    disconnect();
    setTimeout(() => connectWebSocket(), 500);
  };

  const toggleFullscreen = () => {
    if (!containerRef.current) return;

    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  useEffect(() => {
    connectWebSocket();

    return () => {
      disconnect();
    };
  }, [streamName]);

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener("fullscreenchange", handleFullscreenChange);
    return () => {
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
    };
  }, []);

  return (
    <div ref={containerRef} className={isFullscreen ? "fixed inset-0 z-50 bg-black" : ""}>
      <Card className={`glass border border-white/10 shadow-2xl ${isFullscreen ? "h-full rounded-none" : ""}`}>
        <CardHeader className="border-b border-white/10">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-3">
              <motion.div
                animate={{
                  scale: isConnected ? [1, 1.2, 1] : 1,
                }}
                transition={{ duration: 2, repeat: isConnected ? Infinity : 0 }}
              >
                {isConnected ? (
                  <Video className="h-6 w-6 text-green-400" />
                ) : (
                  <VideoOff className="h-6 w-6 text-red-400" />
                )}
              </motion.div>
              <span className="gradient-text text-xl">Camera Trực Tiếp (RTSP)</span>
              <Badge
                variant={isConnected ? "default" : "destructive"}
                className="animate-pulse"
              >
                {isConnected ? "🟢 Live" : "🔴 Offline"}
              </Badge>
            </CardTitle>

            <div className="flex items-center space-x-2">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={reconnect}
                  className="glass border-white/20 hover:bg-white/10"
                  title="Kết nối lại"
                >
                  <RefreshCw className="h-4 w-4" />
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={toggleFullscreen}
                  className="glass border-white/20 hover:bg-white/10"
                  title={isFullscreen ? "Thu nhỏ" : "Toàn màn hình"}
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
        </CardHeader>

        <CardContent className={`p-0 ${isFullscreen ? "h-[calc(100%-80px)]" : ""}`}>
          <div className={`relative bg-gray-900 ${isFullscreen ? "h-full" : "aspect-video"} flex items-center justify-center overflow-hidden`}>
            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="absolute top-4 left-1/2 -translate-x-1/2 z-10"
                >
                  <div className="glass bg-red-500/20 border border-red-500/50 px-4 py-2 rounded-lg">
                    <p className="text-red-200 text-sm font-medium">{error}</p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {!isConnected && !error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="absolute inset-0 flex flex-col items-center justify-center space-y-4"
              >
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                >
                  <RefreshCw className="h-12 w-12 text-gray-400" />
                </motion.div>
                <p className="text-gray-400 text-lg">Đang kết nối đến camera...</p>
              </motion.div>
            )}

            <canvas
              ref={canvasRef}
              className={`${isFullscreen ? "max-h-full max-w-full object-contain" : "w-full h-full object-cover"} ${
                isConnected ? "opacity-100" : "opacity-0"
              } transition-opacity duration-500`}
            />

            {/* Live indicator */}
            {isConnected && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                className="absolute top-4 right-4 flex items-center space-x-2 glass bg-red-500/20 border border-red-500/50 px-3 py-1.5 rounded-full"
              >
                <motion.div
                  animate={{ scale: [1, 1.3, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                  className="w-2 h-2 bg-red-500 rounded-full"
                />
                <span className="text-red-200 text-xs font-bold">LIVE</span>
              </motion.div>
            )}

            {/* Camera info */}
            {isConnected && (
              <div className="absolute bottom-4 left-4 glass bg-black/40 backdrop-blur-md px-3 py-2 rounded-lg border border-white/10">
                <p className="text-white text-xs font-medium">
                  📹 Camera: {streamName}
                </p>
                <p className="text-gray-300 text-xs">
                  🌐 RTSP Stream
                </p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default RTSPLiveStream;
