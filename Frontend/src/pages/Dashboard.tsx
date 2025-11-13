/**
 * Dashboard Page - Trang tổng quan hệ thống
 *
 * Trang dashboard chính với:
 * - Tổng quan vi phạm (cards)
 * - Quick actions
 * - Thống kê tổng hợp
 */

import AppLayout from '@/components/Layout/AppLayout';
import ViolationsOverview from '@/components/ViolationsOverview';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, Camera, Users } from 'lucide-react';

/**
 * Component Dashboard chính
 */
export default function Dashboard() {
  return (
    <AppLayout>
      <div className="container mx-auto py-6 px-4 space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold">Tổng quan Hệ thống</h1>
          <p className="text-muted-foreground mt-1">
            Giám sát và quản lý vi phạm giao thông
          </p>
        </div>

        {/* Violations Overview Cards */}
        <ViolationsOverview />

        {/* System Status */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <div className="size-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <Camera className="size-6 text-primary" />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Cameras hoạt động</p>
                  <p className="text-2xl font-bold">4</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <div className="size-12 rounded-full bg-success/10 flex items-center justify-center">
                  <Activity className="size-6 text-success" />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Trạng thái hệ thống</p>
                  <p className="text-2xl font-bold text-success">Hoạt động</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <div className="size-12 rounded-full bg-warning/10 flex items-center justify-center">
                  <Users className="size-6 text-warning" />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Người dùng online</p>
                  <p className="text-2xl font-bold">1</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  );
}
