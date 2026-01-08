import { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from "next-themes";
import { Toaster } from "sonner";
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ErrorBoundary from './components/ErrorBoundary';
import ProtectedRoute from './components/ProtectedRoute';
import "./App.css";

// Lazy load heavy components for better initial load time
const TrafficDashboard = lazy(() => import("./components/TrafficDashboard"));
const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Violations = lazy(() => import('./pages/Violations'));
const RedLightSetup = lazy(() => import('./components/RedLightSetup'));

// Loading component - Vietnam Transport Theme
const PageLoader = () => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #030712 0%, #0A1628 50%, #0A2463 100%)',
    color: '#06B6D4',
    fontSize: '1.5rem',
    flexDirection: 'column',
    gap: '20px'
  }}>
    <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-cyan-400"></div>
    <div style={{ color: '#f8fafc' }}>Đang tải...</div>
  </div>
);

// Wrapper component to handle authenticated route redirects
function AuthenticatedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #030712 0%, #0A1628 50%, #0A2463 100%)',
        color: '#f8fafc',
        fontSize: '1.5rem',
      }}>
        Đang tải...
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}

// Main dashboard wrapper with theme - Vietnam Transport Theme
function DashboardWrapper() {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
      <div className="min-h-screen relative overflow-hidden" style={{
        background: 'linear-gradient(135deg, #030712 0%, #0A0E1A 50%, #030712 100%)'
      }}>
        {/* Animated background elements - Cyan/Navy Theme */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {/* Cyan Orb - Top Left */}
          <div className="absolute top-0 -left-4 w-96 h-96 rounded-full animate-blob animation-delay-0"
            style={{
              background: 'radial-gradient(circle, rgba(6, 182, 212, 0.25) 0%, rgba(14, 116, 144, 0.1) 50%, transparent 100%)',
              filter: 'blur(80px)',
            }}
          ></div>

          {/* Navy Orb - Top Right */}
          <div className="absolute top-0 -right-4 w-[500px] h-[500px] rounded-full animate-blob animation-delay-2000"
            style={{
              background: 'radial-gradient(circle, rgba(30, 58, 138, 0.25) 0%, rgba(10, 36, 99, 0.15) 50%, transparent 100%)',
              filter: 'blur(80px)',
            }}
          ></div>

          {/* Cyan Orb - Bottom Left */}
          <div className="absolute -bottom-8 left-20 w-80 h-80 rounded-full animate-blob animation-delay-4000"
            style={{
              background: 'radial-gradient(circle, rgba(6, 182, 212, 0.2) 0%, rgba(8, 145, 178, 0.1) 50%, transparent 100%)',
              filter: 'blur(80px)',
            }}
          ></div>

          {/* Tech Blue Orb - Bottom Right */}
          <div className="absolute bottom-20 right-40 w-64 h-64 rounded-full animate-blob animation-delay-6000"
            style={{
              background: 'radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.1) 50%, transparent 100%)',
              filter: 'blur(80px)',
            }}
          ></div>

          {/* Floating Glow Particles */}
          <div className="particles-container">
            {[...Array(25)].map((_, i) => (
              <div
                key={`glow-${i}`}
                className="glow-particle"
                style={{
                  left: `${Math.random() * 100}%`,
                  animationDelay: `${Math.random() * 8}s`,
                  animationDuration: `${10 + Math.random() * 15}s`,
                }}
              />
            ))}
          </div>

          {/* Light Rays */}
          <div className="light-rays">
            <div className="ray ray-1"></div>
            <div className="ray ray-2"></div>
            <div className="ray ray-3"></div>
            <div className="ray ray-4"></div>
          </div>

          {/* Twinkling Stars */}
          <div className="stars-container">
            {[...Array(30)].map((_, i) => (
              <div
                key={`star-${i}`}
                className="star"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                  animationDelay: `${Math.random() * 5}s`,
                }}
              />
            ))}
          </div>

          {/* Floating Tech Rings */}
          <div className="tech-ring ring-1"></div>
          <div className="tech-ring ring-2"></div>
          <div className="tech-ring ring-3"></div>

          {/* Grid pattern */}
          <div className="absolute inset-0" style={{
            backgroundImage: 'linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px)',
            backgroundSize: '60px 60px'
          }}></div>

          {/* Moving scan line */}
          <div className="scan-line-horizontal"></div>
        </div>

        {/* Main content */}
        <div className="relative z-10">
          <TrafficDashboard />
        </div>

        <Toaster position="top-right" richColors theme="dark" />
      </div>
    </ThemeProvider>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <AuthProvider>
          <Suspense fallback={<PageLoader />}>
            <Routes>
              {/* Public routes - redirect to dashboard if already logged in */}
              <Route
                path="/login"
                element={
                  <AuthenticatedRoute>
                    <Login />
                  </AuthenticatedRoute>
                }
              />
              <Route
                path="/register"
                element={
                  <AuthenticatedRoute>
                    <Register />
                  </AuthenticatedRoute>
                }
              />

              {/* Protected routes - require authentication */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                }
              />

              {/* Violations management page - protected */}
              <Route
                path="/violations"
                element={
                  <ProtectedRoute>
                    <Violations />
                  </ProtectedRoute>
                }
              />

              {/* Red Light Setup page - protected */}
              <Route
                path="/red-light-setup"
                element={
                  <ProtectedRoute>
                    <RedLightSetup />
                  </ProtectedRoute>
                }
              />

              {/* Main traffic dashboard - protected */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <DashboardWrapper />
                  </ProtectedRoute>
                }
              />

              {/* Catch all - redirect to login */}
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          </Suspense>
        </AuthProvider>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
