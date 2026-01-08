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
      try {
        // If not authenticated (no token), stop loading immediately
        if (!authService.isAuthenticated()) {
          return;
        }

        // Create a timeout promise (15 seconds - Relaxed)
        const timeoutPromise = new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Auth check timeout')), 15000)
        );

        // Race between fetching user and timeout
        const currentUser = await Promise.race([
          authService.getCurrentUser(),
          timeoutPromise
        ]);

        if (isMounted) {
          setUser(currentUser as User);
        }
      } catch (error) {
        console.warn('Auth check failed or timed out:', error);
        if (isMounted) {
          authService.logout();
          setUser(null);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
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
    setIsLoading(true);
    try {
      // Create a timeout promise (15 seconds for login)
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Login request timed out')), 15000)
      );

      // Race between login request and timeout
      const response = await Promise.race([
        authService.login(credentials),
        timeoutPromise
      ]) as any; // Cast to any or AuthResponse to avoid TS issues with race

      setUser(response.user);
    } catch (error) {
      console.error("Login failed:", error);
      throw error; // Re-throw to let the UI handler know (e.g. show toast)
    } finally {
      setIsLoading(false);
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
