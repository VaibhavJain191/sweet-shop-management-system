/**
 * Authentication Context for managing user authentication state.
 */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '../services/api';

interface User {
    id: string;
    email: string;
    name: string;
    role: string;
}

interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string, name: string) => Promise<void>;
    logout: () => void;
    isAuthenticated: boolean;
    isAdmin: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);

    // Load user and token from localStorage on mount
    useEffect(() => {
        const storedToken = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
            setToken(storedToken);
            setUser(JSON.parse(storedUser));
        }
    }, []);

    const login = async (email: string, password: string) => {
        try {
            const data = await authAPI.login(email, password);
            const accessToken = data.access_token;

            // Store token
            localStorage.setItem('token', accessToken);
            setToken(accessToken);

            // Decode token to get user info (simplified - in production use jwt-decode)
            // For now, we'll fetch user info by registering/logging in
            // Since we don't have a /me endpoint, we'll store user data from registration
            // For login, we'll create a minimal user object
            const userObj: User = {
                id: '', // We don't have this from login response
                email: email,
                name: email.split('@')[0], // Temporary
                role: 'user' // Default, will be updated if admin
            };

            localStorage.setItem('user', JSON.stringify(userObj));
            setUser(userObj);
        } catch (error: any) {
            throw new Error(error.response?.data?.detail || 'Login failed');
        }
    };

    const register = async (email: string, password: string, name: string) => {
        try {
            const userData = await authAPI.register(email, password, name);

            // After registration, automatically log in
            await login(email, password);

            // Update user with registration data
            const userObj: User = {
                id: userData.id,
                email: userData.email,
                name: userData.name,
                role: userData.role
            };

            localStorage.setItem('user', JSON.stringify(userObj));
            setUser(userObj);
        } catch (error: any) {
            throw new Error(error.response?.data?.detail || 'Registration failed');
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setToken(null);
        setUser(null);
    };

    const value: AuthContextType = {
        user,
        token,
        login,
        register,
        logout,
        isAuthenticated: !!token && !!user,
        isAdmin: user?.role === 'admin',
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
