/**
 * Authentication Context
 * Manages authentication state across the application
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService } from '../services/authService';
import type { User, UserLogin, UserRegister } from '../services/authService';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (credentials: UserLogin) => Promise<void>;
  register: (data: UserRegister) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load user from localStorage on mount
  useEffect(() => {
    let isMounted = true; // Prevent memory leaks from async operations

    const loadUser = async () => {
      console.log('🔄 AuthContext: Starting loadUser...');
      try {
        if (!authService.isAuthenticated()) {
          console.log('ℹ️ AuthContext: No token found, user is unauthenticated');
          return;
        }

        console.log('⏳ AuthContext: Token found, fetching user info...');
        const timeoutPromise = new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Auth check timeout')), 15000)
        );

        const currentUser = await Promise.race([
          authService.getCurrentUser(),
          timeoutPromise
        ]);

        console.log('✅ AuthContext: User loaded successfully:', (currentUser as User).username);
        if (isMounted) {
          setUser(currentUser as User);
        }
      } catch (error) {
        console.warn('❌ AuthContext: Auth check failed or timed out:', error);
        if (isMounted) {
          authService.logout();
          setUser(null);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
          console.log('🏁 AuthContext: loadUser completed, isLoading = false');
        }
      }
    };

    loadUser();

    // Cleanup function to prevent memory leaks
    return () => {
      isMounted = false;
    };
  }, []);

  const login = async (credentials: UserLogin) => {
    console.log('🔑 AuthContext: Starting login for:', credentials.username);
    setIsLoading(true);
    try {
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Login request timed out')), 15000)
      );

      const response = await Promise.race([
        authService.login(credentials),
        timeoutPromise
      ]) as any;

      console.log('✅ AuthContext: Login successful, setting user:', response.user.username);
      setUser(response.user);
    } catch (error) {
      console.error("❌ AuthContext: Login failed:", error);
      throw error;
    } finally {
      setIsLoading(false);
      console.log('🏁 AuthContext: login completed, isLoading = false');
    }
  };

  const register = async (data: UserRegister) => {
    setIsLoading(true);
    try {
      const response = await authService.register(data);
      setUser(response.user);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  const refreshUser = async () => {
    try {
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      console.error('Failed to refresh user:', error);
      logout();
    }
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    isAdmin: user?.role_id === 0,
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
