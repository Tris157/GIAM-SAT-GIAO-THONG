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
import { useAuth } from "../contexts/AuthContext";

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
  const { isAdmin } = useAuth();

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
        // Backend trả về array trực tiếp, không phải object
        const violationsData = Array.isArray(data) ? data : (data.violations || []);
        setViolations(violationsData);
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

        // Backend trả về array trực tiếp
        const allViolations = Array.isArray(allData) ? allData : (allData.violations || []);
        const unprocessedViolations = Array.isArray(unprocessedData) ? unprocessedData : (unprocessedData.violations || []);
        const processedViolations = Array.isArray(processedData) ? processedData : (processedData.violations || []);

        // Calculate today's violations
        const today = new Date().toISOString().split('T')[0];
        const todayViolations = allViolations.filter((v: Violation) =>
          v.violated_at.startsWith(today)
        ).length;

        setStats({
          total: allViolations.length,
          unprocessed: unprocessedViolations.length,
          processed: processedViolations.length,
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
          <Card className="glass-card glass-card-hover border border-border/20 shadow-2xl backdrop-blur-2xl bg-card/60">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Tổng Vi Phạm</p>
                  <p className="text-3xl font-bold text-accent">{stats.total}</p>
                </div>
                <div className="p-3 bg-accent/20 rounded-lg">
                  <AlertTriangle className="h-6 w-6 text-accent" />
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
          <Card className="glass-card glass-card-hover border border-border/20 shadow-2xl backdrop-blur-2xl bg-card/60">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Chưa Xử Lý</p>
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
          <Card className="glass-card glass-card-hover border border-border/20 shadow-2xl backdrop-blur-2xl bg-card/60">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Đã Xử Lý</p>
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
          <Card className="glass-card glass-card-hover border border-border/20 shadow-2xl backdrop-blur-2xl bg-card/60">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Hôm Nay</p>
                  <p className="text-3xl font-bold text-accent">{stats.today}</p>
                </div>
                <div className="p-3 bg-accent/20 rounded-lg">
                  <AlertTriangle className="h-6 w-6 text-accent" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Action Buttons */}
      <Card className="glass-card glass-card-hover border border-border/20 shadow-2xl backdrop-blur-2xl bg-card/60">
        <CardHeader className="border-b border-border/20">
          <div className="flex items-center justify-between">
            <CardTitle className="text-gradient-cyan">Quản Lý Vi Phạm</CardTitle>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={testTelegram}
                className="glass-card border-border/30 hover:bg-accent/10 hover:border-accent/40 transition-all duration-300"
              >
                <Send className="h-4 w-4 mr-2 text-accent" />
                Test Telegram
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => sendTelegramReport('today')}
                className="glass-card border-border/30 hover:bg-accent/10 hover:border-accent/40 transition-all duration-300"
              >
                <Send className="h-4 w-4 mr-2 text-accent" />
                Gửi Báo Cáo
              </Button>
              {isAdmin && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={quickSetupDetection}
                  className="glass-card border-border/30 hover:bg-accent/10 hover:border-accent/40 transition-all duration-300"
                >
                  <SettingsIcon className="h-4 w-4 mr-2 text-accent" />
                  Cấu Hình
                </Button>
              )}
              <Button
                variant="outline"
                size="sm"
                onClick={() => { fetchViolations(); fetchStats(); }}
                className="glass-card border-border/30 hover:bg-accent/10 hover:border-accent/40 transition-all duration-300"
              >
                <RefreshCw className="h-4 w-4 mr-2 text-accent" />
                Làm Mới
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="pt-6">
          {/* Filter Buttons */}
          <div className="flex gap-2 mb-4">
            <Button
              variant={filter === 'all' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilter('all')}
              className={filter === 'all' ? 'bg-gradient-navy-cyan text-white shadow-lg glow-effect' : 'glass-card border-border/30 hover:bg-accent/10 hover:border-accent/40 transition-all'}
            >
              <Filter className="h-4 w-4 mr-2" />
              Tất Cả ({stats.total})
            </Button>
            <Button
              variant={filter === 'unprocessed' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilter('unprocessed')}
              className={filter === 'unprocessed' ? 'bg-gradient-navy-cyan text-white shadow-lg glow-effect' : 'glass-card border-border/30 hover:bg-accent/10 hover:border-accent/40 transition-all'}
            >
              <Clock className="h-4 w-4 mr-2" />
              Chưa Xử Lý ({stats.unprocessed})
            </Button>
            <Button
              variant={filter === 'processed' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilter('processed')}
              className={filter === 'processed' ? 'bg-gradient-navy-cyan text-white shadow-lg glow-effect' : 'glass-card border-border/30 hover:bg-accent/10 hover:border-accent/40 transition-all'}
            >
              <CheckCircle className="h-4 w-4 mr-2" />
              Đã Xử Lý ({stats.processed})
            </Button>
          </div>

          {/* Violations List */}
          <div className="space-y-3 max-h-[600px] overflow-y-auto">
            {loading ? (
              <div className="text-center py-8 text-muted-foreground">
                <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-2 text-accent" />
                <p>Đang tải...</p>
              </div>
            ) : violations.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <AlertTriangle className="h-12 w-12 mx-auto mb-2 opacity-50 text-accent" />
                <p>Không có vi phạm</p>
              </div>
            ) : (
              violations.map((violation) => (
                <motion.div
                  key={violation.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="glass-card border border-border/20 rounded-lg p-4 hover:border-accent/50 hover:bg-card/80 transition-all duration-300 backdrop-blur-xl bg-card/40"
                >
                  <div className="flex gap-4">
                    {/* Thumbnail */}
                    <div className="flex-shrink-0">
                      <img
                        src={`${endpoints.base}/${violation.image_path}`}
                        alt="Violation"
                        className="w-32 h-24 object-cover rounded-lg border border-border/20"
                        onClick={() => setSelectedViolation(violation)}
                        style={{ cursor: 'pointer' }}
                      />
                    </div>

                    {/* Info */}
                    <div className="flex-1 space-y-2">
                      <div className="flex items-start justify-between">
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="font-semibold text-foreground">Vi phạm #{violation.id}</h4>
                            <Badge variant={violation.is_processed ? "outline" : "destructive"}
                              className={violation.is_processed ? "border-green-500 text-green-500 bg-green-500/10" : ""}>
                              {violation.is_processed ? 'Đã xử lý' : 'Chưa xử lý'}
                            </Badge>
                            <Badge variant="outline" className="border-accent text-accent">
                              {violation.camera_name}
                            </Badge>
                          </div>
                          <p className="text-sm text-muted-foreground mt-1">
                            {new Date(violation.violated_at).toLocaleString('vi-VN')}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-4 text-sm">
                        <div className="flex items-center gap-1">
                          {violation.vehicle_type === 'car' ? (
                            <Car className="h-4 w-4 text-accent" />
                          ) : (
                            <Bike className="h-4 w-4 text-accent" />
                          )}
                          <span className="text-foreground">{violation.vehicle_type === 'car' ? 'Ô tô' : 'Xe máy'}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <AlertTriangle className="h-4 w-4 text-red-400" />
                          <span className="text-foreground">
                            {violation.violation_type === 'speeding' ? 'Quá tốc độ' :
                              violation.violation_type === 'wrong_lane' ? 'Sai làn' : 'Vượt đèn đỏ'}
                          </span>
                        </div>
                        <div className="flex items-center gap-1">
                          <span className="text-muted-foreground">Độ chính xác:</span>
                          <span className="text-accent">{(violation.confidence * 100).toFixed(1)}%</span>
                        </div>
                      </div>

                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => setSelectedViolation(violation)}
                          className="glass-card border-border/30 hover:bg-accent/10 hover:border-accent/40 transition-all"
                        >
                          <Eye className="h-4 w-4 mr-1 text-accent" />
                          Xem Chi Tiết
                        </Button>
                        {!violation.is_processed && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => markAsProcessed(violation.id, 'Đã xử lý vi phạm')}
                            className="glass-card border-green-500/40 text-green-400 hover:bg-green-500/10 transition-all"
                          >
                            <CheckCircle className="h-4 w-4 mr-1" />
                            Đánh Dấu Xử Lý
                          </Button>
                        )}
                        {isAdmin && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => deleteViolation(violation.id)}
                            className="glass-card border-red-500/40 text-red-400 hover:bg-red-500/10 transition-all"
                          >
                            <Trash2 className="h-4 w-4 mr-1" />
                            Xóa
                          </Button>
                        )}
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
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4 backdrop-blur-sm"
          onClick={() => setSelectedViolation(null)}
        >
          <div
            className="glass-card border border-border/20 rounded-2xl max-w-4xl w-full overflow-hidden shadow-2xl backdrop-blur-2xl bg-card/90"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-4 border-b border-border/20 flex justify-between items-center">
              <h3 className="text-xl font-bold text-gradient-cyan">Vi Phạm #{selectedViolation.id}</h3>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setSelectedViolation(null)}
                className="glass-card border-border/30 hover:bg-accent/10 hover:border-accent/40 transition-all"
              >
                Đóng
              </Button>
            </div>
            <div className="p-6">
              <img
                src={`${endpoints.base}/${selectedViolation.image_path}`}
                alt="Violation Detail"
                className="w-full rounded-lg border border-border/20"
              />
              <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-muted-foreground">Camera:</p>
                  <p className="text-foreground font-semibold">{selectedViolation.camera_name}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Loại xe:</p>
                  <p className="text-foreground font-semibold">
                    {selectedViolation.vehicle_type === 'car' ? 'Ô tô' : 'Xe máy'}
                  </p>
                </div>
                <div>
                  <p className="text-muted-foreground">Thời gian:</p>
                  <p className="text-foreground font-semibold">
                    {new Date(selectedViolation.violated_at).toLocaleString('vi-VN')}
                  </p>
                </div>
                <div>
                  <p className="text-muted-foreground">Trạng thái đèn:</p>
                  <p className="text-red-400 font-semibold">{selectedViolation.traffic_light_status.toUpperCase()}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Vị trí:</p>
                  <p className="text-foreground font-semibold">
                    X: {selectedViolation.position_x.toFixed(0)}, Y: {selectedViolation.position_y.toFixed(0)}
                  </p>
                </div>
                <div>
                  <p className="text-muted-foreground">Độ chính xác:</p>
                  <p className="text-accent font-semibold">
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
