/**
 * ViolationsOverview Component - Cards tổng quan về vi phạm
 *
 * Component này hiển thị các cards overview cho vi phạm:
 * - Tổng số vi phạm
 * - Chưa xử lý
 * - Đã xử lý
 * - Xu hướng hôm nay
 */

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  AlertTriangle,
  Clock,
  CheckCircle,
  TrendingUp,
  TrendingDown,
  ArrowRight,
} from 'lucide-react';
import { getViolations, type Violation } from '@/services/violationService';
import { Link } from 'react-router-dom';

/**
 * Component ViolationsOverview
 */
export default function ViolationsOverview() {
  // ==================== STATE ====================

  const [stats, setStats] = useState({
    total: 0,
    unprocessed: 0,
    processed: 0,
    todayCount: 0,
    trendPercentage: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  // ==================== FETCH DATA ====================

  /**
   * Tải dữ liệu thống kê
   */
  const fetchStats = async () => {
    try {
      setIsLoading(true);

      // Lấy 500 vi phạm gần nhất
      const violations = await getViolations({ limit: 500 });

      const total = violations.length;
      const unprocessed = violations.filter((v) => !v.is_processed).length;
      const processed = violations.filter((v) => v.is_processed).length;

      // Vi phạm hôm nay
      const today = new Date().toISOString().split('T')[0];
      const todayCount = violations.filter((v) => v.date === today).length;

      // Xu hướng so với hôm qua
      const yesterday = new Date(Date.now() - 86400000)
        .toISOString()
        .split('T')[0];
      const yesterdayCount = violations.filter((v) => v.date === yesterday).length;

      const trendPercentage =
        yesterdayCount > 0
          ? ((todayCount - yesterdayCount) / yesterdayCount) * 100
          : 0;

      setStats({
        total,
        unprocessed,
        processed,
        todayCount,
        trendPercentage,
      });
    } catch (error) {
      console.error('Error fetching violation stats:', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Load khi mount
   */
  useEffect(() => {
    fetchStats();

    // Refresh mỗi 60 giây
    const interval = setInterval(fetchStats, 60000);
    return () => clearInterval(interval);
  }, []);

  // ==================== RENDER ====================

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i}>
            <CardContent className="pt-6">
              <div className="h-20 animate-pulse bg-muted rounded" />
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Tổng vi phạm */}
        <Card className="hover:shadow-lg transition-shadow">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground font-medium">
                  Tổng vi phạm
                </p>
                <p className="text-3xl font-bold mt-2">{stats.total}</p>
              </div>
              <div className="size-12 rounded-full bg-destructive/10 flex items-center justify-center">
                <AlertTriangle className="size-6 text-destructive" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Chưa xử lý */}
        <Card className="hover:shadow-lg transition-shadow">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground font-medium">
                  Chưa xử lý
                </p>
                <p className="text-3xl font-bold mt-2 text-warning">
                  {stats.unprocessed}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Cần xử lý ngay
                </p>
              </div>
              <div className="size-12 rounded-full bg-warning/10 flex items-center justify-center">
                <Clock className="size-6 text-warning" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Đã xử lý */}
        <Card className="hover:shadow-lg transition-shadow">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground font-medium">
                  Đã xử lý
                </p>
                <p className="text-3xl font-bold mt-2 text-success">
                  {stats.processed}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Đã hoàn thành
                </p>
              </div>
              <div className="size-12 rounded-full bg-success/10 flex items-center justify-center">
                <CheckCircle className="size-6 text-success" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Hôm nay */}
        <Card className="hover:shadow-lg transition-shadow">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground font-medium">
                  Vi phạm hôm nay
                </p>
                <p className="text-3xl font-bold mt-2">{stats.todayCount}</p>
                <div className="flex items-center gap-1 mt-1">
                  {stats.trendPercentage >= 0 ? (
                    <TrendingUp className="size-4 text-destructive" />
                  ) : (
                    <TrendingDown className="size-4 text-success" />
                  )}
                  <span
                    className={`text-sm font-medium ${
                      stats.trendPercentage >= 0
                        ? 'text-destructive'
                        : 'text-success'
                    }`}
                  >
                    {Math.abs(stats.trendPercentage).toFixed(1)}%
                  </span>
                  <span className="text-xs text-muted-foreground">
                    so với hôm qua
                  </span>
                </div>
              </div>
              <div className="size-12 rounded-full bg-primary/10 flex items-center justify-center">
                <AlertTriangle className="size-6 text-primary" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Hành động nhanh</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            <Link to="/violations">
              <Button variant="default">
                <AlertTriangle className="size-4" />
                Xem danh sách vi phạm
                <ArrowRight className="size-4" />
              </Button>
            </Link>
            <Link to="/violations?tab=statistics">
              <Button variant="outline">
                Xem thống kê chi tiết
                <ArrowRight className="size-4" />
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
