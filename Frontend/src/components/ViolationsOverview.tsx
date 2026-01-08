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
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Tổng vi phạm */}
        <div className="animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          <Card className="glass-card glass-card-hover border-border/30 hover:border-accent/40 transition-all duration-300">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground font-semibold uppercase tracking-wider">
                    Tổng vi phạm
                  </p>
                  <p className="text-3xl font-bold mt-2 text-gradient-cyan">{stats.total}</p>
                </div>
                <div className="size-14 rounded-2xl bg-destructive/10 flex items-center justify-center relative group">
                  <div className="absolute inset-0 bg-destructive/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100"></div>
                  <AlertTriangle className="size-7 text-destructive relative z-10 group-hover:scale-110 transition-transform duration-300" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Chưa xử lý */}
        <div className="animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
          <Card className="glass-card glass-card-hover border-border/30 hover:border-yellow-500/40 transition-all duration-300">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground font-semibold uppercase tracking-wider">
                    Chưa xử lý
                  </p>
                  <p className="text-3xl font-bold mt-2 text-yellow-400">
                    {stats.unprocessed}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                    <span className="inline-block size-1.5 rounded-full bg-yellow-400 animate-pulse"></span>
                    Cần xử lý ngay
                  </p>
                </div>
                <div className="size-14 rounded-2xl bg-yellow-500/10 flex items-center justify-center relative group">
                  <div className="absolute inset-0 bg-yellow-500/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100"></div>
                  <Clock className="size-7 text-yellow-400 relative z-10 group-hover:scale-110 transition-transform duration-300" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Đã xử lý */}
        <div className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
          <Card className="glass-card glass-card-hover border-border/30 hover:border-green-500/40 transition-all duration-300">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground font-semibold uppercase tracking-wider">
                    Đã xử lý
                  </p>
                  <p className="text-3xl font-bold mt-2 text-green-400">
                    {stats.processed}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                    <CheckCircle className="size-3 text-green-400" />
                    Đã hoàn thành
                  </p>
                </div>
                <div className="size-14 rounded-2xl bg-green-500/10 flex items-center justify-center relative group">
                  <div className="absolute inset-0 bg-green-500/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100"></div>
                  <CheckCircle className="size-7 text-green-400 relative z-10 group-hover:scale-110 transition-transform duration-300" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Hôm nay */}
        <div className="animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
          <Card className="glass-card glass-card-hover border-border/30 hover:border-accent/40 transition-all duration-300">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground font-semibold uppercase tracking-wider">
                    Vi phạm hôm nay
                  </p>
                  <p className="text-3xl font-bold mt-2 text-accent">{stats.todayCount}</p>
                  <div className="flex items-center gap-1 mt-1">
                    {stats.trendPercentage >= 0 ? (
                      <TrendingUp className="size-4 text-destructive" />
                    ) : (
                      <TrendingDown className="size-4 text-green-400" />
                    )}
                    <span
                      className={`text-sm font-bold ${
                        stats.trendPercentage >= 0
                          ? 'text-destructive'
                          : 'text-green-400'
                      }`}
                    >
                      {Math.abs(stats.trendPercentage).toFixed(1)}%
                    </span>
                    <span className="text-xs text-muted-foreground">
                      so với hôm qua
                    </span>
                  </div>
                </div>
                <div className="size-14 rounded-2xl bg-accent/10 flex items-center justify-center relative group">
                  <div className="absolute inset-0 bg-accent/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100"></div>
                  <AlertTriangle className="size-7 text-accent relative z-10 group-hover:scale-110 transition-transform duration-300 animate-pulse-glow" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="animate-fade-in-up" style={{ animationDelay: '0.5s' }}>
        <Card className="glass-card border-accent/20 glow-effect">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-gradient-cyan">Hành động nhanh</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-3">
              <Link to="/violations">
                <Button className="btn-primary group">
                  <AlertTriangle className="size-4 group-hover:scale-110 transition-transform" />
                  Xem danh sách vi phạm
                  <ArrowRight className="size-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Link to="/violations?tab=statistics">
                <Button variant="outline" className="border-accent/30 hover:border-accent hover:bg-accent/10 transition-all">
                  Xem thống kê chi tiết
                  <ArrowRight className="size-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
