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
    loading: boolean;
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
    const [loading, setLoading] = useState(true);

    // Load user and token from localStorage on mount
    useEffect(() => {
        const storedToken = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
            setToken(storedToken);
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    const login = async (email: string, password: string) => {
        try {
            const data = await authAPI.login(email, password);
            const accessToken = data.access_token;

            // Store token
            localStorage.setItem('token', accessToken);
            setToken(accessToken);

            // For login, we'll create a minimal user object
            const userObj: User = {
                id: '',
                email: email,
                name: email.split('@')[0],
                role: 'user'
            };

            localStorage.setItem('user', JSON.stringify(userObj));
            setUser(userObj);
        } catch (error: any) {
            throw new Error(error.response?.data?.detail || 'Login failed');
        }
    };

    const register = async (email: string, password: string, name: string) => {
        try {
            // First, register the user
            const userData = await authAPI.register(email, password, name);

            // Create user object with registration data
            const userObj: User = {
                id: userData.id,
                email: userData.email,
                name: userData.name,
                role: userData.role
            };

            // Store user data FIRST
            localStorage.setItem('user', JSON.stringify(userObj));
            setUser(userObj);

            // Then get the token by logging in
            const loginData = await authAPI.login(email, password);
            localStorage.setItem('token', loginData.access_token);
            setToken(loginData.access_token);

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
        loading,
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
