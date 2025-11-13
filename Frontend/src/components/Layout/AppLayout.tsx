/**
 * AppLayout Component - Layout chính của ứng dụng
 *
 * Component này bọc toàn bộ nội dung trang với:
 * - Sidebar navigation
 * - Header (optional)
 * - Main content area
 * - Footer (optional)
 */

import { type ReactNode } from 'react';
import Sidebar from './Sidebar';

/**
 * Props cho AppLayout
 */
interface AppLayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
}

/**
 * Component Layout chính
 */
export default function AppLayout({ children, title, description }: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="lg:ml-0">
        {/* Page Header (Optional) */}
        {(title || description) && (
          <div className="border-b bg-card">
            <div className="container mx-auto px-6 py-8">
              {title && <h1 className="text-3xl font-bold mb-2">{title}</h1>}
              {description && (
                <p className="text-muted-foreground">{description}</p>
              )}
            </div>
          </div>
        )}

        {/* Page Content */}
        <div className="min-h-[calc(100vh-4rem)]">
          {children}
        </div>
      </main>
    </div>
  );
}
