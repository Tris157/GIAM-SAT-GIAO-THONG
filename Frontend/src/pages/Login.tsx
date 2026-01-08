/**
 * Login Page - Smart City Traffic Control Center
 * Concept: Futuristic traffic control interface
 * - Split screen design (left: animation, right: form)
 * - Live traffic light simulation
 * - City map background with moving vehicles
 * - HUD scanning effects
 * - Professional government system theme
 */

import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Login.css';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [errors, setErrors] = useState({
    username: '',
    password: '',
    general: '',
  });

  const [isLoading, setIsLoading] = useState(false);
  const [trafficLight, setTrafficLight] = useState<'red' | 'yellow' | 'green'>('red');
  const [scanProgress, setScanProgress] = useState(0);
  const [vehicleCount, setVehicleCount] = useState(0);

  // Traffic light cycle
  useEffect(() => {
    const interval = setInterval(() => {
      setTrafficLight(prev => {
        if (prev === 'red') return 'green';
        if (prev === 'green') return 'yellow';
        return 'red';
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  // HUD scanning effect
  useEffect(() => {
    const interval = setInterval(() => {
      setScanProgress(prev => (prev + 1) % 100);
    }, 50);

    return () => clearInterval(interval);
  }, []);

  // Vehicle counter simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setVehicleCount(Math.floor(Math.random() * 150) + 50);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setErrors(prev => ({ ...prev, [name]: '', general: '' }));
  };

  const validate = (): boolean => {
    const newErrors = { username: '', password: '', general: '' };
    let isValid = true;

    if (!formData.username.trim()) {
      newErrors.username = 'Vui lòng nhập tên đăng nhập';
      isValid = false;
    }

    if (!formData.password) {
      newErrors.password = 'Vui lòng nhập mật khẩu';
      isValid = false;
    } else if (formData.password.length < 6) {
      newErrors.password = 'Mật khẩu phải có ít nhất 6 ký tự';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsLoading(true);

    try {
      await login(formData);
      navigate('/dashboard');
    } catch (error: any) {
      setErrors(prev => ({
        ...prev,
        general: error.message || 'Đăng nhập thất bại. Vui lòng thử lại.',
      }));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="smart-login-container">
      {/* HUD Scanlines overlay */}
      <div className="hud-scanlines"></div>

      {/* Grid background */}
      <div className="grid-background"></div>

      {/* Left Panel - Traffic Visualization */}
      <div className="visual-panel">
        {/* System Status Header */}
        <div className="system-header">
          <div className="system-logo">
            <div className="logo-hexagon">
              <svg viewBox="0 0 100 100" fill="none">
                <path d="M50 10 L85 30 L85 70 L50 90 L15 70 L15 30 Z" stroke="currentColor" strokeWidth="2" fill="rgba(6, 182, 212, 0.1)" />
              </svg>
              <span className="logo-text">🚦</span>
            </div>
          </div>
          <div className="system-info">
            <h2 className="system-title">HỆ THỐNG GIÁM SÁT THÔNG MINH</h2>
            <p className="system-subtitle">SMART MONITORING SYSTEM</p>
          </div>
        </div>

        {/* Traffic Light Simulator */}
        <div className="traffic-light-container">
          <div className="traffic-light-pole"></div>
          <div className="traffic-light-box">
            <div className={`light-bulb red ${trafficLight === 'red' ? 'active' : ''}`}>
              <div className="light-glow"></div>
            </div>
            <div className={`light-bulb yellow ${trafficLight === 'yellow' ? 'active' : ''}`}>
              <div className="light-glow"></div>
            </div>
            <div className={`light-bulb green ${trafficLight === 'green' ? 'active' : ''}`}>
              <div className="light-glow"></div>
            </div>
          </div>
        </div>

        {/* Live Statistics */}
        <div className="live-stats">
          <div className="stat-card">
            <div className="stat-icon">🚗</div>
            <div className="stat-content">
              <div className="stat-label">Xe lưu thông</div>
              <div className="stat-value">{vehicleCount}</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚡</div>
            <div className="stat-content">
              <div className="stat-label">Hệ thống</div>
              <div className="stat-value">Online</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📡</div>
            <div className="stat-content">
              <div className="stat-label">Cameras</div>
              <div className="stat-value">4/4</div>
            </div>
          </div>
        </div>

        {/* Scanning radar */}
        <div className="radar-container">
          <div className="radar-circle">
            <div className="radar-sweep" style={{ transform: `rotate(${scanProgress * 3.6}deg)` }}></div>
            <div className="radar-dot dot-1"></div>
            <div className="radar-dot dot-2"></div>
            <div className="radar-dot dot-3"></div>
          </div>
        </div>

        {/* City Skyline */}
        <div className="city-skyline">
          <div className="building building-1"></div>
          <div className="building building-2"></div>
          <div className="building building-3"></div>
          <div className="building building-4"></div>
          <div className="building building-5"></div>
        </div>

        {/* Moving vehicles */}
        <div className="road-container">
          <div className="vehicle vehicle-1">🚗</div>
          <div className="vehicle vehicle-2">🚕</div>
          <div className="vehicle vehicle-3">🏍️</div>
        </div>
      </div>

      {/* Right Panel - Login Form */}
      <div className="form-panel">
        <div className="form-container">
          {/* Access Terminal Header */}
          <div className="terminal-header">
            <div className="terminal-bar">
              <span className="terminal-indicator"></span>
              <span className="terminal-indicator"></span>
              <span className="terminal-indicator"></span>
            </div>
            <div className="access-badge">
              <span className="badge-icon">🔒</span>
              <span className="badge-text">AUTHORIZED ACCESS ONLY</span>
            </div>
          </div>

          <div className="form-content">
            <h1 className="form-title">TRUY CẬP HỆ THỐNG</h1>
            <p className="form-description">Vui lòng xác thực để tiếp tục</p>

            <form className="login-form" onSubmit={handleSubmit}>
              {/* General error */}
              {errors.general && (
                <div className="alert-box error-alert">
                  <svg className="alert-icon" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  <span>{errors.general}</span>
                </div>
              )}

              {/* Username */}
              <div className="field-group">
                <label className="field-label">
                  <span className="label-icon">👤</span>
                  <span>TÊN ĐĂNG NHẬP</span>
                </label>
                <div className={`input-container ${errors.username ? 'error' : ''}`}>
                  <input
                    type="text"
                    name="username"
                    className="field-input"
                    placeholder="Nhập tên đăng nhập..."
                    value={formData.username}
                    onChange={handleChange}
                    autoComplete="username"
                  />
                  <div className="input-border"></div>
                </div>
                {errors.username && <span className="field-error">{errors.username}</span>}
              </div>

              {/* Password */}
              <div className="field-group">
                <label className="field-label">
                  <span className="label-icon">🔑</span>
                  <span>MẬT KHẨU</span>
                </label>
                <div className={`input-container ${errors.password ? 'error' : ''}`}>
                  <input
                    type="password"
                    name="password"
                    className="field-input"
                    placeholder="Nhập mật khẩu..."
                    value={formData.password}
                    onChange={handleChange}
                    autoComplete="current-password"
                  />
                  <div className="input-border"></div>
                </div>
                {errors.password && <span className="field-error">{errors.password}</span>}
              </div>

              {/* Submit button */}
              <button
                type="submit"
                className={`access-button ${isLoading ? 'loading' : ''}`}
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <div className="button-spinner"></div>
                    <span>ĐANG XÁC THỰC...</span>
                  </>
                ) : (
                  <>
                    <span className="button-text">TRUY CẬP HỆ THỐNG</span>
                    <svg className="button-arrow" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </>
                )}
              </button>
            </form>

            {/* Register link */}
            <div className="form-footer">
              <div className="divider">
                <span className="divider-line"></span>
                <span className="divider-text">HOẶC</span>
                <span className="divider-line"></span>
              </div>
              <Link to="/register" className="register-button">
                <svg className="register-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z" />
                </svg>
                <span>Đăng ký tài khoản mới</span>
              </Link>
            </div>
          </div>
        </div>

        {/* Security Notice */}
        <div className="security-notice">
          <svg className="notice-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <span>Kết nối được mã hóa SSL/TLS</span>
        </div>
      </div>
    </div>
  );
}
