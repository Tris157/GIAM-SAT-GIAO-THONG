import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
    AlertTriangle,
    TrendingUp,
    TrendingDown,
    Minus,
    Clock,
    Car,
    Bike,
    Bell,
    Activity,
} from "lucide-react";
import { endpoints } from "../config";

// Types
interface DashboardStatsData {
    today_violations: number;
    yesterday_violations: number;
    change_percent: number;
    change_direction: "up" | "down" | "same";
    total_violations: number;
    unprocessed_count: number;
    by_vehicle_type: Record<string, number>;
    peak_hour: number | null;
    recent_violations: Array<{
        id: number;
        vehicle_type: string;
        violated_at: string;
        camera_name: string;
    }>;
    timestamp: string;
}

interface ToastNotification {
    id: string;
    message: string;
    type: "violation" | "info";
    timestamp: Date;
}

// Animated Counter Component
const AnimatedCounter = ({
    value,
    duration = 1000,
}: {
    value: number;
    duration?: number;
}) => {
    const [displayValue, setDisplayValue] = useState(0);
    const previousValue = useRef(0);

    useEffect(() => {
        const startValue = previousValue.current;
        const endValue = value;
        const startTime = Date.now();

        const animate = () => {
            const now = Date.now();
            const progress = Math.min((now - startTime) / duration, 1);

            // Easing function (ease-out)
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.round(
                startValue + (endValue - startValue) * easeOut
            );

            setDisplayValue(currentValue);

            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                previousValue.current = endValue;
            }
        };

        requestAnimationFrame(animate);
    }, [value, duration]);

    return <span>{displayValue}</span>;
};

// Toast Component
const ToastNotificationItem = ({
    notification,
    onClose,
}: {
    notification: ToastNotification;
    onClose: () => void;
}) => {
    useEffect(() => {
        const timer = setTimeout(onClose, 5000);
        return () => clearTimeout(timer);
    }, [onClose]);

    return (
        <motion.div
            initial={{ opacity: 0, y: -50, x: 50 }}
            animate={{ opacity: 1, y: 0, x: 0 }}
            exit={{ opacity: 0, x: 100 }}
            className="glass-card border border-red-500/50 bg-red-500/10 backdrop-blur-xl rounded-xl p-4 shadow-2xl max-w-sm"
        >
            <div className="flex items-start space-x-3">
                <div className="p-2 bg-red-500/20 rounded-lg">
                    <AlertTriangle className="h-5 w-5 text-red-400" />
                </div>
                <div className="flex-1">
                    <p className="font-semibold text-white text-sm">Vi phạm mới!</p>
                    <p className="text-gray-300 text-xs mt-1">{notification.message}</p>
                    <p className="text-gray-500 text-xs mt-1">
                        {notification.timestamp.toLocaleTimeString("vi-VN")}
                    </p>
                </div>
                <button
                    onClick={onClose}
                    className="text-gray-400 hover:text-white transition-colors"
                >
                    ×
                </button>
            </div>
        </motion.div>
    );
};

// Main Dashboard Stats Component
const DashboardStats = () => {
    const [stats, setStats] = useState<DashboardStatsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [toasts, setToasts] = useState<ToastNotification[]>([]);
    const previousViolationCount = useRef<number>(0);

    // Fetch stats
    const fetchStats = async () => {
        try {
            const res = await fetch(`${endpoints.base}/api/v1/violations/dashboard-stats`);
            if (res.ok) {
                const data: DashboardStatsData = await res.json();

                // Check for new violations
                if (
                    previousViolationCount.current > 0 &&
                    data.today_violations > previousViolationCount.current
                ) {
                    const newCount = data.today_violations - previousViolationCount.current;
                    addToast(`Phát hiện ${newCount} vi phạm mới!`);
                }
                previousViolationCount.current = data.today_violations;

                setStats(data);
            }
        } catch (error) {
            console.error("Failed to fetch dashboard stats:", error);
        } finally {
            setLoading(false);
        }
    };

    // Add toast notification
    const addToast = (message: string) => {
        const id = Math.random().toString(36).substr(2, 9);
        setToasts((prev) => [...prev, { id, message, type: "violation", timestamp: new Date() }]);
    };

    // Remove toast
    const removeToast = (id: string) => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
    };

    // Polling for updates
    useEffect(() => {
        fetchStats();
        const interval = setInterval(fetchStats, 10000); // Update every 10 seconds
        return () => clearInterval(interval);
    }, []);

    // Get change icon
    const getChangeIcon = () => {
        if (!stats) return <Minus className="h-4 w-4" />;
        switch (stats.change_direction) {
            case "up":
                return <TrendingUp className="h-4 w-4 text-red-400" />;
            case "down":
                return <TrendingDown className="h-4 w-4 text-green-400" />;
            default:
                return <Minus className="h-4 w-4 text-gray-400" />;
        }
    };

    // Get change color
    const getChangeColor = () => {
        if (!stats) return "text-gray-400";
        switch (stats.change_direction) {
            case "up":
                return "text-red-400";
            case "down":
                return "text-green-400";
            default:
                return "text-gray-400";
        }
    };

    if (loading) {
        return (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[1, 2, 3, 4].map((i) => (
                    <Card key={i} className="glass-card animate-pulse">
                        <CardContent className="p-4">
                            <div className="h-16 bg-white/5 rounded-lg" />
                        </CardContent>
                    </Card>
                ))}
            </div>
        );
    }

    return (
        <>
            {/* Toast Notifications */}
            <div className="fixed top-4 right-4 z-50 space-y-2">
                <AnimatePresence>
                    {toasts.map((toast) => (
                        <ToastNotificationItem
                            key={toast.id}
                            notification={toast}
                            onClose={() => removeToast(toast.id)}
                        />
                    ))}
                </AnimatePresence>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                {/* Card 1: Violations Today */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <Card className="glass-card glass-card-hover border border-red-500/20 bg-gradient-to-br from-red-500/10 to-transparent">
                        <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-gray-400">Hôm nay</span>
                                <div className="p-2 bg-red-500/20 rounded-lg">
                                    <AlertTriangle className="h-4 w-4 text-red-400" />
                                </div>
                            </div>
                            <div className="text-3xl font-bold text-white">
                                <AnimatedCounter value={stats?.today_violations || 0} />
                            </div>
                            <div className={`flex items-center space-x-1 mt-1 text-xs ${getChangeColor()}`}>
                                {getChangeIcon()}
                                <span>{Math.abs(stats?.change_percent || 0)}% so với hôm qua</span>
                            </div>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* Card 2: Total Violations */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <Card className="glass-card glass-card-hover border border-accent/20 bg-gradient-to-br from-accent/10 to-transparent">
                        <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-gray-400">Tổng cộng</span>
                                <div className="p-2 bg-accent/20 rounded-lg">
                                    <Activity className="h-4 w-4 text-accent" />
                                </div>
                            </div>
                            <div className="text-3xl font-bold text-white">
                                <AnimatedCounter value={stats?.total_violations || 0} />
                            </div>
                            <div className="text-xs text-gray-500 mt-1">
                                {stats?.unprocessed_count || 0} chưa xử lý
                            </div>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* Card 3: By Vehicle Type */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <Card className="glass-card glass-card-hover border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-transparent">
                        <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-gray-400">Theo loại xe</span>
                                <div className="p-2 bg-blue-500/20 rounded-lg">
                                    <Car className="h-4 w-4 text-blue-400" />
                                </div>
                            </div>
                            <div className="flex items-center space-x-4">
                                <div className="flex items-center space-x-1">
                                    <Car className="h-4 w-4 text-blue-400" />
                                    <span className="text-xl font-bold text-white">
                                        {stats?.by_vehicle_type?.car || stats?.by_vehicle_type?.oto || 0}
                                    </span>
                                </div>
                                <div className="flex items-center space-x-1">
                                    <Bike className="h-4 w-4 text-green-400" />
                                    <span className="text-xl font-bold text-white">
                                        {stats?.by_vehicle_type?.motorbike || stats?.by_vehicle_type?.["xe máy"] || 0}
                                    </span>
                                </div>
                            </div>
                            <div className="text-xs text-gray-500 mt-1">Ô tô / Xe máy</div>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* Card 4: Peak Hour */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                >
                    <Card className="glass-card glass-card-hover border border-yellow-500/20 bg-gradient-to-br from-yellow-500/10 to-transparent">
                        <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-gray-400">Giờ cao điểm</span>
                                <div className="p-2 bg-yellow-500/20 rounded-lg">
                                    <Clock className="h-4 w-4 text-yellow-400" />
                                </div>
                            </div>
                            <div className="text-3xl font-bold text-white">
                                {stats && stats.peak_hour !== null && stats.peak_hour !== undefined ? `${stats.peak_hour}:00` : "--:--"}
                            </div>
                            <div className="text-xs text-gray-500 mt-1">Nhiều vi phạm nhất</div>
                        </CardContent>
                    </Card>
                </motion.div>
            </div>
        </>
    );
};

export default DashboardStats;
