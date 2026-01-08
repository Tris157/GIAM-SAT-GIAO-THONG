/**
 * Dashboard Page - Vietnam Transport Theme
 *
 * Trang dashboard chính với:
 * - Glassmorphism cards
 * - Cyan glow effects
 * - Professional navy-cyan color scheme
 */

import AppLayout from '@/components/Layout/AppLayout';
import ViolationsOverview from '@/components/ViolationsOverview';
import { Card, CardContent } from '@/components/ui/card';
import { Activity, Camera, Users, TrendingUp, AlertTriangle, CheckCircle2 } from 'lucide-react';

/**
 * Component Dashboard chính
 */
export default function Dashboard() {
  return (
    <AppLayout>
      <div className="container mx-auto py-6 px-4 space-y-8 animate-fade-in-up">
        {/* Header with gradient text */}
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-navy-cyan opacity-20 blur-3xl rounded-full"></div>
          <div className="relative">
            <h1 className="text-4xl font-bold text-gradient-cyan">
              Tổng quan Hệ thống
            </h1>
            <p className="text-muted-foreground mt-2 text-lg">
              Giám sát và quản lý vi phạm giao thông thông minh
            </p>
          </div>
        </div>

        {/* Violations Overview Cards with animation */}
        <div className="animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <ViolationsOverview />
        </div>

        {/* System Status Cards - Glassmorphism Style */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Cameras Active Card */}
          <div className="animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            <Card className="glass-card glass-card-hover border-border/30 hover:border-accent/40 transition-all duration-300">
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="size-16 rounded-2xl bg-primary/10 flex items-center justify-center relative group">
                    <div className="absolute inset-0 bg-primary/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100"></div>
                    <Camera className="size-8 text-primary relative z-10 group-hover:scale-110 transition-transform duration-300" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground uppercase tracking-wider font-semibold">
                      Cameras hoạt động
                    </p>
                    <div className="flex items-baseline gap-2 mt-1">
                      <p className="text-3xl font-bold text-gradient-cyan">4</p>
                      <span className="badge-success text-xs">
                        <CheckCircle2 className="size-3 mr-1" />
                        Online
                      </span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* System Status Card */}
          <div className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <Card className="glass-card glass-card-hover border-border/30 hover:border-accent/40 transition-all duration-300">
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="size-16 rounded-2xl bg-accent/10 flex items-center justify-center relative group">
                    <div className="absolute inset-0 bg-accent/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100"></div>
                    <Activity className="size-8 text-accent relative z-10 group-hover:scale-110 transition-transform duration-300 animate-pulse-glow" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground uppercase tracking-wider font-semibold">
                      Trạng thái hệ thống
                    </p>
                    <div className="flex items-baseline gap-2 mt-1">
                      <p className="text-3xl font-bold text-accent">Hoạt động</p>
                      <span className="badge-cyan text-xs">
                        <TrendingUp className="size-3 mr-1" />
                        99.9%
                      </span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Users Online Card */}
          <div className="animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            <Card className="glass-card glass-card-hover border-border/30 hover:border-accent/40 transition-all duration-300">
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="size-16 rounded-2xl bg-secondary/50 flex items-center justify-center relative group">
                    <div className="absolute inset-0 bg-secondary/30 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100"></div>
                    <Users className="size-8 text-primary relative z-10 group-hover:scale-110 transition-transform duration-300" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground uppercase tracking-wider font-semibold">
                      Người dùng online
                    </p>
                    <div className="flex items-baseline gap-2 mt-1">
                      <p className="text-3xl font-bold text-foreground">1</p>
                      <span className="badge-navy text-xs">
                        Admin
                      </span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Quick Stats Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="animate-fade-in-up" style={{ animationDelay: '0.5s' }}>
            <Card className="glass-card border-border/20 hover:border-accent/30 transition-all duration-300">
              <CardContent className="pt-5 pb-5">
                <div className="text-center space-y-2">
                  <div className="inline-flex items-center justify-center size-12 rounded-xl bg-primary/10 mb-2">
                    <TrendingUp className="size-6 text-primary" />
                  </div>
                  <p className="text-2xl font-bold text-gradient-cyan">142</p>
                  <p className="text-xs text-muted-foreground uppercase tracking-wider">
                    FPS Processing
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
            <Card className="glass-card border-border/20 hover:border-accent/30 transition-all duration-300">
              <CardContent className="pt-5 pb-5">
                <div className="text-center space-y-2">
                  <div className="inline-flex items-center justify-center size-12 rounded-xl bg-accent/10 mb-2">
                    <CheckCircle2 className="size-6 text-accent" />
                  </div>
                  <p className="text-2xl font-bold text-accent">88.9%</p>
                  <p className="text-xs text-muted-foreground uppercase tracking-wider">
                    Model Accuracy
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="animate-fade-in-up" style={{ animationDelay: '0.7s' }}>
            <Card className="glass-card border-border/20 hover:border-accent/30 transition-all duration-300">
              <CardContent className="pt-5 pb-5">
                <div className="text-center space-y-2">
                  <div className="inline-flex items-center justify-center size-12 rounded-xl bg-green-500/10 mb-2">
                    <Camera className="size-6 text-green-400" />
                  </div>
                  <p className="text-2xl font-bold text-green-400">100K+</p>
                  <p className="text-xs text-muted-foreground uppercase tracking-wider">
                    Vehicles Detected
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="animate-fade-in-up" style={{ animationDelay: '0.8s' }}>
            <Card className="glass-card border-border/20 hover:border-accent/30 transition-all duration-300">
              <CardContent className="pt-5 pb-5">
                <div className="text-center space-y-2">
                  <div className="inline-flex items-center justify-center size-12 rounded-xl bg-yellow-500/10 mb-2">
                    <AlertTriangle className="size-6 text-yellow-400" />
                  </div>
                  <p className="text-2xl font-bold text-yellow-400">&#60;100ms</p>
                  <p className="text-xs text-muted-foreground uppercase tracking-wider">
                    Latency
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* System Info Banner */}
        <div className="animate-fade-in-up" style={{ animationDelay: '0.9s' }}>
          <Card className="glass-card border-accent/20 glow-effect">
            <CardContent className="pt-6 pb-6">
              <div className="flex items-center gap-4">
                <div className="flex-shrink-0">
                  <div className="size-14 rounded-2xl bg-gradient-navy-cyan flex items-center justify-center">
                    <CheckCircle2 className="size-7 text-white" />
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-foreground mb-1">
                    Hệ thống đang hoạt động bình thường
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Tất cả các services đang chạy ổn định. Last updated: {new Date().toLocaleTimeString('vi-VN')}
                  </p>
                </div>
                <div className="flex-shrink-0">
                  <div className="px-4 py-2 rounded-xl bg-accent/20 border border-accent/30">
                    <span className="text-accent font-bold text-sm uppercase tracking-wider">
                      All Systems Go
                    </span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  );
}
