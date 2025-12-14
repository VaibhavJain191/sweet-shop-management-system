/**
 * API service layer for communicating with the backend.
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with base configuration
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    register: async (email: string, password: string, name: string) => {
        const response = await api.post('/api/auth/register', { email, password, name });
        return response.data;
    },

    login: async (email: string, password: string) => {
        const response = await api.post('/api/auth/login', { email, password });
        return response.data;
    },
};

// Sweets API
export const sweetsAPI = {
    getAll: async () => {
        const response = await api.get('/api/sweets');
        return response.data;
    },

    search: async (params: { name?: string; category?: string; min_price?: number; max_price?: number }) => {
        const response = await api.get('/api/sweets/search', { params });
        return response.data;
    },

    create: async (sweetData: any) => {
        const response = await api.post('/api/sweets', sweetData);
        return response.data;
    },

    update: async (id: string, sweetData: any) => {
        const response = await api.put(`/api/sweets/${id}`, sweetData);
        return response.data;
    },

    delete: async (id: string) => {
        const response = await api.delete(`/api/sweets/${id}`);
        return response.data;
    },

    purchase: async (id: string, quantity: number) => {
        const response = await api.post(`/api/sweets/${id}/purchase`, { quantity });
        return response.data;
    },

    restock: async (id: string, quantity: number) => {
        const response = await api.post(`/api/sweets/${id}/restock`, { quantity });
        return response.data;
    },
};

export default api;
