/**
 * Violations Page - Trang quản lý vi phạm giao thông
 *
 * Trang này cung cấp giao diện quản lý toàn bộ vi phạm giao thông:
 * - Xem danh sách vi phạm với bộ lọc
 * - Xem chi tiết từng vi phạm
 * - Đánh dấu đã xử lý
 * - Xóa vi phạm
 * - Xem thống kê
 */

import { useState, useEffect } from 'react';
import { AlertCircle, Eye, Trash2, CheckCircle, Filter, RefreshCw, BarChart3, List } from 'lucide-react';
import {
  getViolations,
  deleteViolation,
  markViolationProcessed,
  type Violation,
  type ViolationFilters,
  formatViolationTime,
  getViolationTypeLabel,
  getVehicleTypeLabel,
  getViolationImageUrl,
} from '@/services/violationService';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import AppLayout from '@/components/Layout/AppLayout';
import ViolationsStatistics from '@/components/ViolationsStatistics';

/**
 * Component chính - Trang quản lý vi phạm
 */
export default function ViolationsPage() {
  // ==================== STATE MANAGEMENT ====================

  // Tab hiện tại
  const [activeTab, setActiveTab] = useState<'list' | 'statistics'>('list');

  // Danh sách vi phạm
  const [violations, setViolations] = useState<Violation[]>([]);

  // Trạng thái loading và error
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Bộ lọc
  const [filters, setFilters] = useState<ViolationFilters>({
    is_processed: undefined,
    limit: 50,
    offset: 0,
  });

  // Vi phạm được chọn để xem chi tiết
  const [selectedViolation, setSelectedViolation] = useState<Violation | null>(null);

  // Dialog states
  const [showDetailDialog, setShowDetailDialog] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [violationToDelete, setViolationToDelete] = useState<number | null>(null);

  // Trạng thái xử lý action
  const [isProcessing, setIsProcessing] = useState(false);

  // ==================== DATA FETCHING ====================

  /**
   * Tải danh sách vi phạm từ API
   */
  const fetchViolations = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await getViolations(filters);
      setViolations(data);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Không thể tải danh sách vi phạm';
      setError(errorMessage);
      console.error('Error fetching violations:', err);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Tải lại danh sách khi filters thay đổi
   */
  useEffect(() => {
    fetchViolations();
  }, [filters]);

  // ==================== ACTION HANDLERS ====================

  /**
   * Xử lý xem chi tiết vi phạm
   */
  const handleViewDetail = (violation: Violation) => {
    setSelectedViolation(violation);
    setShowDetailDialog(true);
  };

  /**
   * Xử lý đánh dấu vi phạm đã xử lý
   */
  const handleMarkProcessed = async (violationId: number) => {
    setIsProcessing(true);

    try {
      await markViolationProcessed(violationId, 'Đã xử lý qua hệ thống');

      // Cập nhật danh sách local
      setViolations((prev) =>
        prev.map((v) =>
          v.id === violationId ? { ...v, is_processed: true } : v
        )
      );

      // Cập nhật selected violation nếu đang xem
      if (selectedViolation?.id === violationId) {
        setSelectedViolation((prev) =>
          prev ? { ...prev, is_processed: true } : null
        );
      }
    } catch (err) {
      console.error('Error marking violation as processed:', err);
      alert('Không thể đánh dấu đã xử lý. Vui lòng thử lại.');
    } finally {
      setIsProcessing(false);
    }
  };

  /**
   * Xử lý xóa vi phạm
   */
  const handleDeleteClick = (violationId: number) => {
    setViolationToDelete(violationId);
    setShowDeleteConfirm(true);
  };

  /**
   * Xác nhận xóa vi phạm
   */
  const handleDeleteConfirm = async () => {
    if (!violationToDelete) return;

    setIsProcessing(true);

    try {
      await deleteViolation(violationToDelete);

      // Xóa khỏi danh sách local
      setViolations((prev) => prev.filter((v) => v.id !== violationToDelete));

      // Đóng dialog nếu đang xem chi tiết
      if (selectedViolation?.id === violationToDelete) {
        setShowDetailDialog(false);
        setSelectedViolation(null);
      }

      setShowDeleteConfirm(false);
      setViolationToDelete(null);
    } catch (err) {
      console.error('Error deleting violation:', err);
      alert('Không thể xóa vi phạm. Vui lòng thử lại.');
    } finally {
      setIsProcessing(false);
    }
  };

  /**
   * Hủy xóa
   */
  const handleDeleteCancel = () => {
    setShowDeleteConfirm(false);
    setViolationToDelete(null);
  };

  /**
   * Chuyển đổi bộ lọc trạng thái xử lý
   */
  const handleFilterProcessed = (value: boolean | undefined) => {
    setFilters((prev) => ({ ...prev, is_processed: value, offset: 0 }));
  };

  /**
   * Làm mới danh sách
   */
  const handleRefresh = () => {
    fetchViolations();
  };

  // ==================== UTILITY FUNCTIONS ====================

  /**
   * Lấy màu badge cho loại vi phạm
   */
  const getViolationBadgeColor = (type: string) => {
    switch (type) {
      case 'red_light':
        return 'destructive';
      case 'speeding':
        return 'default';
      case 'wrong_lane':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  /**
   * Lấy màu badge cho trạng thái đèn
   */
  const getLightStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'red':
        return 'bg-red-500 text-white';
      case 'yellow':
        return 'bg-yellow-500 text-black';
      case 'green':
        return 'bg-green-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  // ==================== RENDER ====================

  return (
    <AppLayout>
      <div className="container mx-auto py-6 px-4 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Quản lý Vi phạm</h1>
            <p className="text-muted-foreground mt-1">
              Theo dõi và xử lý các vi phạm giao thông
            </p>
          </div>
          {activeTab === 'list' && (
            <Button onClick={handleRefresh} variant="outline" disabled={isLoading}>
              <RefreshCw className={isLoading ? 'animate-spin' : ''} />
              Làm mới
            </Button>
          )}
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as 'list' | 'statistics')}>
          <TabsList className="grid w-full max-w-md grid-cols-2">
            <TabsTrigger value="list" className="flex items-center gap-2">
              <List className="size-4" />
              Danh sách
            </TabsTrigger>
            <TabsTrigger value="statistics" className="flex items-center gap-2">
              <BarChart3 className="size-4" />
              Thống kê
            </TabsTrigger>
          </TabsList>

          {/* Tab: Danh sách vi phạm */}
          <TabsContent value="list" className="space-y-6 mt-6">
            {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="size-5" />
            Bộ lọc
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            <Button
              variant={filters.is_processed === undefined ? 'default' : 'outline'}
              size="sm"
              onClick={() => handleFilterProcessed(undefined)}
            >
              Tất cả ({violations.length})
            </Button>
            <Button
              variant={filters.is_processed === false ? 'default' : 'outline'}
              size="sm"
              onClick={() => handleFilterProcessed(false)}
            >
              Chưa xử lý ({violations.filter((v) => !v.is_processed).length})
            </Button>
            <Button
              variant={filters.is_processed === true ? 'default' : 'outline'}
              size="sm"
              onClick={() => handleFilterProcessed(true)}
            >
              Đã xử lý ({violations.filter((v) => v.is_processed).length})
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <div className="bg-destructive/10 border border-destructive rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="size-5 text-destructive shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-destructive">Lỗi</h3>
            <p className="text-sm text-muted-foreground">{error}</p>
          </div>
        </div>
      )}

      {/* Violations Table */}
      <Card>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="py-12 text-center text-muted-foreground">
              Đang tải...
            </div>
          ) : violations.length === 0 ? (
            <div className="py-12 text-center text-muted-foreground">
              Không có vi phạm nào
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Thời gian</TableHead>
                  <TableHead>Camera</TableHead>
                  <TableHead>Loại vi phạm</TableHead>
                  <TableHead>Phương tiện</TableHead>
                  <TableHead>Đèn tín hiệu</TableHead>
                  <TableHead>Trạng thái</TableHead>
                  <TableHead className="text-right">Hành động</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {violations.map((violation) => (
                  <TableRow key={violation.id}>
                    <TableCell className="font-mono">{violation.id}</TableCell>
                    <TableCell className="whitespace-nowrap">
                      {formatViolationTime(violation.violated_at)}
                    </TableCell>
                    <TableCell>{violation.camera_name}</TableCell>
                    <TableCell>
                      <Badge variant={getViolationBadgeColor(violation.violation_type)}>
                        {getViolationTypeLabel(violation.violation_type)}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      {getVehicleTypeLabel(violation.vehicle_type)}
                    </TableCell>
                    <TableCell>
                      <span
                        className={`px-2 py-1 rounded text-xs font-medium ${getLightStatusColor(
                          violation.traffic_light_status
                        )}`}
                      >
                        {violation.traffic_light_status.toUpperCase()}
                      </span>
                    </TableCell>
                    <TableCell>
                      {violation.is_processed ? (
                        <Badge variant="secondary">
                          <CheckCircle className="size-3" />
                          Đã xử lý
                        </Badge>
                      ) : (
                        <Badge variant="outline">Chưa xử lý</Badge>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center justify-end gap-2">
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleViewDetail(violation)}
                        >
                          <Eye className="size-4" />
                        </Button>
                        {!violation.is_processed && (
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleMarkProcessed(violation.id)}
                            disabled={isProcessing}
                          >
                            <CheckCircle className="size-4" />
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleDeleteClick(violation.id)}
                          disabled={isProcessing}
                        >
                          <Trash2 className="size-4 text-destructive" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Detail Dialog */}
      <Dialog open={showDetailDialog} onOpenChange={setShowDetailDialog}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>Chi tiết Vi phạm #{selectedViolation?.id}</DialogTitle>
            <DialogDescription>
              Thông tin chi tiết về vi phạm giao thông
            </DialogDescription>
          </DialogHeader>

          {selectedViolation && (
            <div className="space-y-4">
              {/* Ảnh bằng chứng */}
              <div className="rounded-lg border overflow-hidden">
                <img
                  src={getViolationImageUrl(selectedViolation.image_path)}
                  alt={`Vi phạm ${selectedViolation.id}`}
                  className="w-full h-auto"
                  onError={(e) => {
                    e.currentTarget.src = '/placeholder-image.png';
                  }}
                />
              </div>

              {/* Thông tin chi tiết */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground">Thời gian vi phạm</p>
                  <p className="font-medium">
                    {formatViolationTime(selectedViolation.violated_at)}
                  </p>
                </div>

                <div>
                  <p className="text-sm text-muted-foreground">Camera</p>
                  <p className="font-medium">{selectedViolation.camera_name}</p>
                </div>

                <div>
                  <p className="text-sm text-muted-foreground">Loại vi phạm</p>
                  <Badge variant={getViolationBadgeColor(selectedViolation.violation_type)}>
                    {getViolationTypeLabel(selectedViolation.violation_type)}
                  </Badge>
                </div>

                <div>
                  <p className="text-sm text-muted-foreground">Phương tiện</p>
                  <p className="font-medium">
                    {getVehicleTypeLabel(selectedViolation.vehicle_type)}
                  </p>
                </div>

                <div>
                  <p className="text-sm text-muted-foreground">Trạng thái đèn</p>
                  <span
                    className={`inline-block px-2 py-1 rounded text-xs font-medium ${getLightStatusColor(
                      selectedViolation.traffic_light_status
                    )}`}
                  >
                    {selectedViolation.traffic_light_status.toUpperCase()}
                  </span>
                </div>

                <div>
                  <p className="text-sm text-muted-foreground">Độ tin cậy</p>
                  <p className="font-medium">
                    {(selectedViolation.confidence * 100).toFixed(1)}%
                  </p>
                </div>

                <div>
                  <p className="text-sm text-muted-foreground">Vị trí</p>
                  <p className="font-medium font-mono text-sm">
                    ({selectedViolation.position_x.toFixed(0)},{' '}
                    {selectedViolation.position_y.toFixed(0)})
                  </p>
                </div>

                <div>
                  <p className="text-sm text-muted-foreground">Trạng thái xử lý</p>
                  {selectedViolation.is_processed ? (
                    <Badge variant="secondary">
                      <CheckCircle className="size-3" />
                      Đã xử lý
                    </Badge>
                  ) : (
                    <Badge variant="outline">Chưa xử lý</Badge>
                  )}
                </div>
              </div>

              {selectedViolation.note && (
                <div>
                  <p className="text-sm text-muted-foreground">Ghi chú</p>
                  <p className="mt-1 p-2 bg-muted rounded text-sm">
                    {selectedViolation.note}
                  </p>
                </div>
              )}
            </div>
          )}

          <DialogFooter>
            {selectedViolation && !selectedViolation.is_processed && (
              <Button
                onClick={() => handleMarkProcessed(selectedViolation.id)}
                disabled={isProcessing}
              >
                <CheckCircle />
                Đánh dấu đã xử lý
              </Button>
            )}
            <Button variant="outline" onClick={() => setShowDetailDialog(false)}>
              Đóng
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={showDeleteConfirm} onOpenChange={setShowDeleteConfirm}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Xác nhận xóa</DialogTitle>
            <DialogDescription>
              Bạn có chắc chắn muốn xóa vi phạm #{violationToDelete}? Hành động này
              không thể hoàn tác.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={handleDeleteCancel}
              disabled={isProcessing}
            >
              Hủy
            </Button>
            <Button
              variant="destructive"
              onClick={handleDeleteConfirm}
              disabled={isProcessing}
            >
              <Trash2 />
              Xóa
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
          </TabsContent>

          {/* Tab: Thống kê */}
          <TabsContent value="statistics" className="mt-6">
            <ViolationsStatistics />
          </TabsContent>
        </Tabs>
      </div>
    </AppLayout>
  );
}
