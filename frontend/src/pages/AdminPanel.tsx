/**
 * Admin Panel - manage sweets (CRUD operations).
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { sweetsAPI } from '../services/api';
import './AdminPanel.css';

interface Sweet {
    id: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    description?: string;
}

const AdminPanel: React.FC = () => {
    const [sweets, setSweets] = useState<Sweet[]>([]);
    const [formData, setFormData] = useState({
        name: '',
        category: '',
        price: '',
        quantity: '',
        description: '',
    });
    const [editingId, setEditingId] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const { isAdmin } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAdmin) {
            navigate('/dashboard');
            return;
        }
        fetchSweets();
    }, [isAdmin, navigate]);

    const fetchSweets = async () => {
        try {
            const data = await sweetsAPI.getAll();
            setSweets(data);
        } catch (err) {
            console.error('Failed to fetch sweets:', err);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            const sweetData = {
                name: formData.name,
                category: formData.category,
                price: Number(formData.price),
                quantity: Number(formData.quantity),
                description: formData.description || undefined,
            };

            if (editingId) {
                await sweetsAPI.update(editingId, sweetData);
            } else {
                await sweetsAPI.create(sweetData);
            }

            setFormData({ name: '', category: '', price: '', quantity: '', description: '' });
            setEditingId(null);
            await fetchSweets();
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Operation failed');
        } finally {
            setLoading(false);
        }
    };

    const handleEdit = (sweet: Sweet) => {
        setFormData({
            name: sweet.name,
            category: sweet.category,
            price: sweet.price.toString(),
            quantity: sweet.quantity.toString(),
            description: sweet.description || '',
        });
        setEditingId(sweet.id);
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Are you sure you want to delete this sweet?')) return;

        try {
            await sweetsAPI.delete(id);
            await fetchSweets();
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Delete failed');
        }
    };

    const handleRestock = async (id: string) => {
        const quantity = prompt('Enter quantity to add:');
        if (!quantity || isNaN(Number(quantity))) return;

        try {
            await sweetsAPI.restock(id, Number(quantity));
            await fetchSweets();
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Restock failed');
        }
    };

    return (
        <div className="admin-container">
            <header className="admin-header">
                <h1>🍬 Admin Panel</h1>
                <button onClick={() => navigate('/dashboard')} className="btn-back">
                    Back to Dashboard
                </button>
            </header>

            <div className="admin-content">
                <div className="admin-form-section">
                    <h2>{editingId ? 'Edit Sweet' : 'Add New Sweet'}</h2>
                    <form onSubmit={handleSubmit} className="admin-form">
                        <input
                            type="text"
                            placeholder="Name"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            required
                        />
                        <input
                            type="text"
                            placeholder="Category"
                            value={formData.category}
                            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                            required
                        />
                        <input
                            type="number"
                            placeholder="Price"
                            value={formData.price}
                            onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                            step="0.01"
                            min="0"
                            required
                        />
                        <input
                            type="number"
                            placeholder="Quantity"
                            value={formData.quantity}
                            onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                            min="0"
                            required
                        />
                        <textarea
                            placeholder="Description (optional)"
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            rows={3}
                        />
                        <div className="form-buttons">
                            <button type="submit" disabled={loading} className="btn-submit">
                                {loading ? 'Saving...' : editingId ? 'Update' : 'Add Sweet'}
                            </button>
                            {editingId && (
                                <button
                                    type="button"
                                    onClick={() => {
                                        setEditingId(null);
                                        setFormData({ name: '', category: '', price: '', quantity: '', description: '' });
                                    }}
                                    className="btn-cancel"
                                >
                                    Cancel
                                </button>
                            )}
                        </div>
                    </form>
                </div>

                <div className="admin-list-section">
                    <h2>Manage Sweets</h2>
                    <div className="sweets-table">
                        {sweets.map((sweet) => (
                            <div key={sweet.id} className="sweet-row">
                                <div className="sweet-info-admin">
                                    <h3>{sweet.name}</h3>
                                    <p>{sweet.category} • ${sweet.price} • {sweet.quantity} in stock</p>
                                </div>
                                <div className="sweet-actions">
                                    <button onClick={() => handleEdit(sweet)} className="btn-edit">
                                        Edit
                                    </button>
                                    <button onClick={() => handleRestock(sweet.id)} className="btn-restock">
                                        Restock
                                    </button>
                                    <button onClick={() => handleDelete(sweet.id)} className="btn-delete">
                                        Delete
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdminPanel;
