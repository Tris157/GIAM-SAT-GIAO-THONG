import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  AlertTriangle,
  CheckCircle,
  Clock,
  Car,
  Bike,
  Filter,
  Download,
  Eye,
  Trash2,
  RefreshCw,
  Settings as SettingsIcon,
  Send
} from "lucide-react";
import { motion } from "framer-motion";
import { endpoints } from "../config";

type Violation = {
  id: number;
  camera_name: string;
  violation_type: string;
  vehicle_type: string;
  image_path: string;
  position_x: number;
  position_y: number;
  traffic_light_status: string;
  violated_at: string;
  is_processed: boolean;
  confidence: number;
  note?: string;
};

type ViolationStats = {
  total: number;
  unprocessed: number;
  processed: number;
  today: number;
};

const ViolationsManagement = () => {
  const [violations, setViolations] = useState<Violation[]>([]);
  const [stats, setStats] = useState<ViolationStats>({
    total: 0,
    unprocessed: 0,
    processed: 0,
    today: 0,
  });
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState<'all' | 'processed' | 'unprocessed'>('all');
  const [selectedViolation, setSelectedViolation] = useState<Violation | null>(null);

  // Fetch violations
  const fetchViolations = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const params = new URLSearchParams();

      if (filter === 'processed') params.append('is_processed', 'true');
      if (filter === 'unprocessed') params.append('is_processed', 'false');

      const response = await fetch(`${endpoints.base}/api/v1/violations/list?${params}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setViolations(data.violations || []);
      }
    } catch (error) {
      console.error('Error fetching violations:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch statistics
  const fetchStats = async () => {
    try {
      const token = localStorage.getItem('access_token');

      // Get all violations
      const allResponse = await fetch(`${endpoints.base}/api/v1/violations/list`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      // Get unprocessed
      const unprocessedResponse = await fetch(`${endpoints.base}/api/v1/violations/list?is_processed=false`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      // Get processed
      const processedResponse = await fetch(`${endpoints.base}/api/v1/violations/list?is_processed=true`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (allResponse.ok && unprocessedResponse.ok && processedResponse.ok) {
        const allData = await allResponse.json();
        const unprocessedData = await unprocessedResponse.json();
        const processedData = await processedResponse.json();

        // Calculate today's violations
        const today = new Date().toISOString().split('T')[0];
        const todayViolations = allData.violations?.filter((v: Violation) =>
          v.violated_at.startsWith(today)
        ).length || 0;

        setStats({
          total: allData.violations?.length || 0,
          unprocessed: unprocessedData.violations?.length || 0,
          processed: processedData.violations?.length || 0,
          today: todayViolations,
        });
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  // Mark violation as processed
  const markAsProcessed = async (violationId: number, note: string = '') => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${endpoints.base}/api/v1/violations/${violationId}/process`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ note }),
      });

      if (response.ok) {
        fetchViolations();
        fetchStats();
      }
    } catch (error) {
      console.error('Error marking violation:', error);
    }
  };

  // Delete violation
  const deleteViolation = async (violationId: number) => {
    if (!confirm('Bạn có chắc muốn xóa vi phạm này?')) return;

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${endpoints.base}/api/v1/violations/${violationId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        fetchViolations();
        fetchStats();
        setSelectedViolation(null);
      }
    } catch (error) {
      console.error('Error deleting violation:', error);
    }
  };

  // Quick setup detection
  const quickSetupDetection = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${endpoints.base}/api/v1/violations/quick-setup/camera_live`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        alert('✅ Đã cấu hình phát hiện vi phạm thành công!');
      }
    } catch (error) {
      console.error('Error setting up detection:', error);
      alert('❌ Lỗi cấu hình phát hiện vi phạm');
    }
  };

  // Send system report via Telegram
  const sendTelegramReport = async (period: 'today' | 'week' | 'month') => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${endpoints.base}/api/v1/violations/send-report?period=${period}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const result = await response.json();

      if (result.success) {
        alert(result.message);
      } else {
        alert(result.message);
      }
    } catch (error) {
      console.error('Error sending Telegram report:', error);
      alert('❌ Lỗi gửi báo cáo Telegram');
    }
  };

  // Test Telegram connection
  const testTelegram = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${endpoints.base}/api/v1/violations/test-telegram`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const result = await response.json();
      alert(result.message);
    } catch (error) {
      console.error('Error testing Telegram:', error);
      alert('❌ Lỗi test Telegram Bot');
    }
  };

  useEffect(() => {
    fetchViolations();
    fetchStats();

    // Auto refresh every 30 seconds
    const interval = setInterval(() => {
      fetchViolations();
      fetchStats();
    }, 30000);

    return () => clearInterval(interval);
  }, [filter]);

  return (
    <div className="space-y-6">
      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="glass border-white/10">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400">Tổng Vi Phạm</p>
                  <p className="text-3xl font-bold text-purple-400">{stats.total}</p>
                </div>
                <div className="p-3 bg-purple-500/20 rounded-lg">
                  <AlertTriangle className="h-6 w-6 text-purple-400" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card className="glass border-white/10">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400">Chưa Xử Lý</p>
                  <p className="text-3xl font-bold text-red-400">{stats.unprocessed}</p>
                </div>
                <div className="p-3 bg-red-500/20 rounded-lg">
                  <Clock className="h-6 w-6 text-red-400" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card className="glass border-white/10">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400">Đã Xử Lý</p>
                  <p className="text-3xl font-bold text-green-400">{stats.processed}</p>
                </div>
                <div className="p-3 bg-green-500/20 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-green-400" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card className="glass border-white/10">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400">Hôm Nay</p>
                  <p className="text-3xl font-bold text-blue-400">{stats.today}</p>
                </div>
                <div className="p-3 bg-blue-500/20 rounded-lg">
                  <AlertTriangle className="h-6 w-6 text-blue-400" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Action Buttons */}
      <Card className="glass border-white/10">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-white">Quản Lý Vi Phạm</CardTitle>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={testTelegram}
                className="glass border-white/20 bg-blue-500/10 hover:bg-blue-500/20"
              >
                <Send className="h-4 w-4 mr-2" />
                Test Telegram
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => sendTelegramReport('today')}
                className="glass border-white/20 bg-green-500/10 hover:bg-green-500/20"
              >
                <Send className="h-4 w-4 mr-2" />
                Gửi Báo Cáo
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={quickSetupDetection}
                className="glass border-white/20"
              >
                <SettingsIcon className="h-4 w-4 mr-2" />
                Cấu Hình
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => { fetchViolations(); fetchStats(); }}
                className="glass border-white/20"
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Làm Mới
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Filter Buttons */}
          <div className="flex gap-2 mb-4">
            <Button
              variant={filter === 'all' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilter('all')}
              className={filter === 'all' ? 'bg-purple-600' : 'glass border-white/20'}
            >
              <Filter className="h-4 w-4 mr-2" />
              Tất Cả ({stats.total})
            </Button>
            <Button
              variant={filter === 'unprocessed' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilter('unprocessed')}
              className={filter === 'unprocessed' ? 'bg-red-600' : 'glass border-white/20'}
            >
              <Clock className="h-4 w-4 mr-2" />
              Chưa Xử Lý ({stats.unprocessed})
            </Button>
            <Button
              variant={filter === 'processed' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilter('processed')}
              className={filter === 'processed' ? 'bg-green-600' : 'glass border-white/20'}
            >
              <CheckCircle className="h-4 w-4 mr-2" />
              Đã Xử Lý ({stats.processed})
            </Button>
          </div>

          {/* Violations List */}
          <div className="space-y-3 max-h-[600px] overflow-y-auto">
            {loading ? (
              <div className="text-center py-8 text-gray-400">
                <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-2" />
                <p>Đang tải...</p>
              </div>
            ) : violations.length === 0 ? (
              <div className="text-center py-8 text-gray-400">
                <AlertTriangle className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>Không có vi phạm</p>
              </div>
            ) : (
              violations.map((violation) => (
                <motion.div
                  key={violation.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="glass border-white/10 rounded-lg p-4 hover:bg-white/5 transition-colors"
                >
                  <div className="flex gap-4">
                    {/* Thumbnail */}
                    <div className="flex-shrink-0">
                      <img
                        src={`${endpoints.base}/${violation.image_path}`}
                        alt="Violation"
                        className="w-32 h-24 object-cover rounded-lg border border-white/20"
                        onClick={() => setSelectedViolation(violation)}
                        style={{ cursor: 'pointer' }}
                      />
                    </div>

                    {/* Info */}
                    <div className="flex-1 space-y-2">
                      <div className="flex items-start justify-between">
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="font-semibold text-white">Vi phạm #{violation.id}</h4>
                            <Badge variant={violation.is_processed ? "success" : "destructive"}>
                              {violation.is_processed ? 'Đã xử lý' : 'Chưa xử lý'}
                            </Badge>
                            <Badge variant="outline" className="border-purple-400 text-purple-400">
                              {violation.camera_name}
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-400 mt-1">
                            {new Date(violation.violated_at).toLocaleString('vi-VN')}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-4 text-sm">
                        <div className="flex items-center gap-1">
                          {violation.vehicle_type === 'car' ? (
                            <Car className="h-4 w-4 text-blue-400" />
                          ) : (
                            <Bike className="h-4 w-4 text-green-400" />
                          )}
                          <span className="text-gray-300">{violation.vehicle_type === 'car' ? 'Ô tô' : 'Xe máy'}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <AlertTriangle className="h-4 w-4 text-red-400" />
                          <span className="text-gray-300">Vượt đèn đỏ</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <span className="text-gray-400">Độ chính xác:</span>
                          <span className="text-yellow-400">{(violation.confidence * 100).toFixed(1)}%</span>
                        </div>
                      </div>

                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => setSelectedViolation(violation)}
                          className="glass border-white/20"
                        >
                          <Eye className="h-4 w-4 mr-1" />
                          Xem Chi Tiết
                        </Button>
                        {!violation.is_processed && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => markAsProcessed(violation.id, 'Đã xử lý vi phạm')}
                            className="glass border-green-500/40 text-green-400"
                          >
                            <CheckCircle className="h-4 w-4 mr-1" />
                            Đánh Dấu Xử Lý
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => deleteViolation(violation.id)}
                          className="glass border-red-500/40 text-red-400"
                        >
                          <Trash2 className="h-4 w-4 mr-1" />
                          Xóa
                        </Button>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Modal for viewing full image */}
      {selectedViolation && (
        <div
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedViolation(null)}
        >
          <div
            className="glass border-white/20 rounded-2xl max-w-4xl w-full overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-4 border-b border-white/10 flex justify-between items-center">
              <h3 className="text-xl font-bold text-white">Vi Phạm #{selectedViolation.id}</h3>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setSelectedViolation(null)}
                className="glass border-white/20"
              >
                Đóng
              </Button>
            </div>
            <div className="p-6">
              <img
                src={`${endpoints.base}/${selectedViolation.image_path}`}
                alt="Violation Detail"
                className="w-full rounded-lg border border-white/20"
              />
              <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-400">Camera:</p>
                  <p className="text-white font-semibold">{selectedViolation.camera_name}</p>
                </div>
                <div>
                  <p className="text-gray-400">Loại xe:</p>
                  <p className="text-white font-semibold">
                    {selectedViolation.vehicle_type === 'car' ? 'Ô tô' : 'Xe máy'}
                  </p>
                </div>
                <div>
                  <p className="text-gray-400">Thời gian:</p>
                  <p className="text-white font-semibold">
                    {new Date(selectedViolation.violated_at).toLocaleString('vi-VN')}
                  </p>
                </div>
                <div>
                  <p className="text-gray-400">Trạng thái đèn:</p>
                  <p className="text-red-400 font-semibold">{selectedViolation.traffic_light_status.toUpperCase()}</p>
                </div>
                <div>
                  <p className="text-gray-400">Vị trí:</p>
                  <p className="text-white font-semibold">
                    X: {selectedViolation.position_x.toFixed(0)}, Y: {selectedViolation.position_y.toFixed(0)}
                  </p>
                </div>
                <div>
                  <p className="text-gray-400">Độ chính xác:</p>
                  <p className="text-yellow-400 font-semibold">
                    {(selectedViolation.confidence * 100).toFixed(2)}%
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ViolationsManagement;
