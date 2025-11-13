import { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from "next-themes";
import { Toaster } from "sonner";
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ErrorBoundary from './components/ErrorBoundary';
import ProtectedRoute from './components/ProtectedRoute'; // Not lazy - needed immediately
import "./App.css";

// Lazy load heavy components for better initial load time
const TrafficDashboard = lazy(() => import("./components/TrafficDashboard"));
const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Violations = lazy(() => import('./pages/Violations'));

// Loading component
const PageLoader = () => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    fontSize: '1.5rem',
    flexDirection: 'column',
    gap: '20px'
  }}>
    <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-white"></div>
    <div>Loading...</div>
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
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        fontSize: '1.5rem',
      }}>
        Loading...
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}

// Main dashboard wrapper with theme
function DashboardWrapper() {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
      <div className="min-h-screen relative overflow-hidden rainbow-gradient">
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {/* 3D Floating orbs với gradient */}
          <div className="absolute top-0 -left-4 w-96 h-96 rounded-full animate-blob animation-delay-0 neon-glow"
            style={{
              background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.2))',
              backdropFilter: 'blur(40px)',
              boxShadow: '0 0 100px rgba(102, 126, 234, 0.4), inset 0 0 60px rgba(255, 255, 255, 0.1)'
            }}
          ></div>
          <div className="absolute top-0 -right-4 w-[500px] h-[500px] rounded-full animate-blob animation-delay-2000 neon-glow"
            style={{
              background: 'linear-gradient(135deg, rgba(240, 147, 251, 0.3), rgba(245, 87, 108, 0.2))',
              backdropFilter: 'blur(40px)',
              boxShadow: '0 0 100px rgba(240, 147, 251, 0.4), inset 0 0 60px rgba(255, 255, 255, 0.1)'
            }}
          ></div>
          <div className="absolute -bottom-8 left-20 w-80 h-80 rounded-full animate-blob animation-delay-4000 neon-glow"
            style={{
              background: 'linear-gradient(135deg, rgba(79, 172, 254, 0.3), rgba(0, 242, 254, 0.2))',
              backdropFilter: 'blur(40px)',
              boxShadow: '0 0 100px rgba(79, 172, 254, 0.4), inset 0 0 60px rgba(255, 255, 255, 0.1)'
            }}
          ></div>
          <div className="absolute bottom-20 right-40 w-64 h-64 rounded-full animate-blob animation-delay-6000 neon-glow"
            style={{
              background: 'linear-gradient(135deg, rgba(67, 233, 123, 0.3), rgba(56, 249, 215, 0.2))',
              backdropFilter: 'blur(40px)',
              boxShadow: '0 0 100px rgba(67, 233, 123, 0.4), inset 0 0 60px rgba(255, 255, 255, 0.1)'
            }}
          ></div>

          {/* Grid pattern */}
          <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>

          {/* Dots pattern overlay */}
          <div className="absolute inset-0 bg-dots-pattern opacity-5"></div>

          {/* Scanline effect */}
          <div className="absolute inset-0 bg-scanline opacity-5"></div>

          {/* Horizontal scan line */}
          <div className="scan-line" style={{ top: '30%' }}></div>
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
