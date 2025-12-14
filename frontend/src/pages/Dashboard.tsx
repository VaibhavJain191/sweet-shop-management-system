/**
 * Dashboard page - displays all sweets with search and filter.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { sweetsAPI } from '../services/api';
import SweetCard from '../components/sweets/SweetCard';
import SearchBar from '../components/sweets/SearchBar';
import './Dashboard.css';

interface Sweet {
    id: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    description?: string;
    image_url?: string;
}

const Dashboard: React.FC = () => {
    const [sweets, setSweets] = useState<Sweet[]>([]);
    const [filteredSweets, setFilteredSweets] = useState<Sweet[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const { user, logout, isAdmin } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        fetchSweets();
    }, []);

    const fetchSweets = async () => {
        try {
            setLoading(true);
            const data = await sweetsAPI.getAll();
            setSweets(data);
            setFilteredSweets(data);
        } catch (err: any) {
            setError('Failed to load sweets');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (searchParams: {
        name?: string;
        category?: string;
        minPrice?: number;
        maxPrice?: number;
    }) => {
        try {
            if (!searchParams.name && !searchParams.category && !searchParams.minPrice && !searchParams.maxPrice) {
                setFilteredSweets(sweets);
                return;
            }

            const data = await sweetsAPI.search({
                name: searchParams.name,
                category: searchParams.category,
                min_price: searchParams.minPrice,
                max_price: searchParams.maxPrice,
            });
            setFilteredSweets(data);
        } catch (err) {
            console.error('Search failed:', err);
        }
    };

    const handlePurchase = async (sweetId: string, quantity: number) => {
        try {
            await sweetsAPI.purchase(sweetId, quantity);
            await fetchSweets(); // Refresh the list
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Purchase failed');
        }
    };

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    if (loading) {
        return (
            <div className="dashboard-container">
                <div className="loading">Loading sweets... 🍬</div>
            </div>
        );
    }

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>🍬 Sweet Shop</h1>
                    <div className="header-actions">
                        <span className="user-info">
                            Welcome, <strong>{user?.name || user?.email}</strong>
                            {isAdmin && <span className="admin-badge">Admin</span>}
                        </span>
                        {isAdmin && (
                            <button
                                className="btn-secondary"
                                onClick={() => navigate('/admin')}
                            >
                                Admin Panel
                            </button>
                        )}
                        <button className="btn-logout" onClick={handleLogout}>
                            Logout
                        </button>
                    </div>
                </div>
            </header>

            <main className="dashboard-main">
                <div className="dashboard-content">
                    <SearchBar onSearch={handleSearch} />

                    {error && <div className="error-banner">{error}</div>}

                    {filteredSweets.length === 0 ? (
                        <div className="no-sweets">
                            <p>No sweets found. {isAdmin && 'Add some from the Admin Panel!'}</p>
                        </div>
                    ) : (
                        <div className="sweets-grid">
                            {filteredSweets.map((sweet) => (
                                <SweetCard
                                    key={sweet.id}
                                    sweet={sweet}
                                    onPurchase={handlePurchase}
                                />
                            ))}
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
