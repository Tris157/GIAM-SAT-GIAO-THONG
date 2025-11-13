/**
 * Sidebar Component - Thanh điều hướng bên trái
 *
 * Component này cung cấp menu điều hướng cho toàn bộ ứng dụng:
 * - Dashboard chính
 * - Quản lý vi phạm
 * - Quản lý camera
 * - Cài đặt
 * - Đăng xuất
 */

import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  AlertTriangle,
  Camera,
  Settings,
  LogOut,
  Menu,
  X,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import { cn } from '@/lib/utils';

/**
 * Interface cho menu item
 */
interface MenuItem {
  label: string;
  icon: React.ReactNode;
  path: string;
  badge?: string | number;
}

/**
 * Component Sidebar chính
 */
export default function Sidebar() {
  // ==================== STATE & HOOKS ====================

  const location = useLocation();
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  // Trạng thái thu gọn sidebar
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Trạng thái mobile menu
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // ==================== MENU ITEMS ====================

  /**
   * Danh sách menu chính
   */
  const menuItems: MenuItem[] = [
    {
      label: 'Tổng quan',
      icon: <LayoutDashboard className="size-5" />,
      path: '/dashboard',
    },
    {
      label: 'Vi phạm',
      icon: <AlertTriangle className="size-5" />,
      path: '/violations',
    },
    {
      label: 'Camera',
      icon: <Camera className="size-5" />,
      path: '/cameras',
    },
    {
      label: 'Cài đặt',
      icon: <Settings className="size-5" />,
      path: '/settings',
    },
  ];

  // ==================== HANDLERS ====================

  /**
   * Xử lý đăng xuất
   */
  const handleLogout = async () => {
    try {
      logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  /**
   * Kiểm tra xem route có active không
   */
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  /**
   * Toggle sidebar collapsed state
   */
  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  /**
   * Toggle mobile menu
   */
  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  // ==================== RENDER ====================

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={toggleMobileMenu}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-card border shadow-lg hover:bg-accent transition-colors"
        aria-label="Toggle menu"
      >
        {isMobileMenuOpen ? (
          <X className="size-6" />
        ) : (
          <Menu className="size-6" />
        )}
      </button>

      {/* Mobile Overlay */}
      {isMobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={toggleMobileMenu}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed top-0 left-0 z-40 h-screen transition-all duration-300',
          'bg-card border-r shadow-lg',
          'flex flex-col',
          // Desktop
          isCollapsed ? 'lg:w-20' : 'lg:w-64',
          // Mobile
          isMobileMenuOpen ? 'translate-x-0 w-64' : '-translate-x-full lg:translate-x-0'
        )}
      >
        {/* Header */}
        <div className="p-4 border-b">
          <div className="flex items-center justify-between">
            {!isCollapsed && (
              <div className="flex items-center gap-3">
                <div className="size-10 rounded-lg bg-primary flex items-center justify-center">
                  <Camera className="size-6 text-primary-foreground" />
                </div>
                <div>
                  <h1 className="font-bold text-lg">Traffic AI</h1>
                  <p className="text-xs text-muted-foreground">
                    Giám sát giao thông
                  </p>
                </div>
              </div>
            )}

            {/* Collapse Button - Desktop only */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleCollapse}
              className="hidden lg:flex"
            >
              {isCollapsed ? (
                <ChevronRight className="size-5" />
              ) : (
                <ChevronLeft className="size-5" />
              )}
            </Button>
          </div>

          {/* User Info */}
          {!isCollapsed && user && (
            <div className="mt-4 p-3 rounded-lg bg-accent/50">
              <p className="text-sm font-medium truncate">{user.full_name}</p>
              <p className="text-xs text-muted-foreground truncate">
                {user.email}
              </p>
            </div>
          )}
        </div>

        {/* Navigation Menu */}
        <nav className="flex-1 overflow-y-auto p-4">
          <ul className="space-y-2">
            {menuItems.map((item) => {
              const active = isActive(item.path);

              return (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={cn(
                      'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all',
                      'hover:bg-accent hover:text-accent-foreground',
                      active
                        ? 'bg-primary text-primary-foreground hover:bg-primary/90'
                        : 'text-muted-foreground',
                      isCollapsed && 'justify-center'
                    )}
                    title={isCollapsed ? item.label : undefined}
                  >
                    {item.icon}
                    {!isCollapsed && (
                      <span className="font-medium">{item.label}</span>
                    )}
                    {!isCollapsed && item.badge && (
                      <span className="ml-auto bg-destructive text-destructive-foreground text-xs px-2 py-0.5 rounded-full">
                        {item.badge}
                      </span>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Footer - Logout Button */}
        <div className="p-4 border-t">
          <Button
            variant="ghost"
            onClick={handleLogout}
            className={cn(
              'w-full justify-start text-muted-foreground hover:text-destructive',
              isCollapsed && 'justify-center px-0'
            )}
          >
            <LogOut className="size-5" />
            {!isCollapsed && <span className="ml-3">Đăng xuất</span>}
          </Button>
        </div>
      </aside>

      {/* Spacer for fixed sidebar - Desktop only */}
      <div
        className={cn(
          'hidden lg:block transition-all duration-300',
          isCollapsed ? 'lg:w-20' : 'lg:w-64'
        )}
      />
    </>
  );
}
