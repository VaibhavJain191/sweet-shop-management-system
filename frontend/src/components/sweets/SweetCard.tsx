/**
 * SweetCard component - displays individual sweet with purchase option.
 */
import React, { useState } from 'react';
import './SweetCard.css';

interface Sweet {
    id: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    description?: string;
    image_url?: string;
}

interface SweetCardProps {
    sweet: Sweet;
    onPurchase: (sweetId: string, quantity: number) => Promise<void>;
}

const SweetCard: React.FC<SweetCardProps> = ({ sweet, onPurchase }) => {
    const [purchaseQuantity, setPurchaseQuantity] = useState(1);
    const [purchasing, setPurchasing] = useState(false);

    const handlePurchase = async () => {
        if (purchaseQuantity < 1 || purchaseQuantity > sweet.quantity) {
            alert('Invalid quantity');
            return;
        }

        setPurchasing(true);
        try {
            await onPurchase(sweet.id, purchaseQuantity);
            setPurchaseQuantity(1);
        } finally {
            setPurchasing(false);
        }
    };

    const isOutOfStock = sweet.quantity === 0;

    return (
        <div className={`sweet-card ${isOutOfStock ? 'out-of-stock' : ''}`}>
            <div className="sweet-image">
                {sweet.image_url ? (
                    <img src={sweet.image_url} alt={sweet.name} />
                ) : (
                    <div className="sweet-placeholder">🍬</div>
                )}
                {isOutOfStock && <div className="out-of-stock-badge">Out of Stock</div>}
            </div>

            <div className="sweet-content">
                <div className="sweet-header">
                    <h3>{sweet.name}</h3>
                    <span className="sweet-category">{sweet.category}</span>
                </div>

                {sweet.description && (
                    <p className="sweet-description">{sweet.description}</p>
                )}

                <div className="sweet-footer">
                    <div className="sweet-info">
                        <span className="sweet-price">${sweet.price.toFixed(2)}</span>
                        <span className="sweet-stock">
                            {sweet.quantity} in stock
                        </span>
                    </div>

                    {!isOutOfStock && (
                        <div className="purchase-controls">
                            <input
                                type="number"
                                min="1"
                                max={sweet.quantity}
                                value={purchaseQuantity}
                                onChange={(e) => setPurchaseQuantity(Number(e.target.value))}
                                className="quantity-input"
                                disabled={purchasing}
                            />
                            <button
                                onClick={handlePurchase}
                                disabled={purchasing || isOutOfStock}
                                className="btn-purchase"
                            >
                                {purchasing ? 'Buying...' : 'Purchase'}
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default SweetCard;
