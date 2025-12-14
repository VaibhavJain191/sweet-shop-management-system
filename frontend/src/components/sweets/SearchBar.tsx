/**
 * SearchBar component - search and filter sweets.
 */
import React, { useState } from 'react';
import './SearchBar.css';

interface SearchBarProps {
    onSearch: (params: {
        name?: string;
        category?: string;
        minPrice?: number;
        maxPrice?: number;
    }) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
    const [name, setName] = useState('');
    const [category, setCategory] = useState('');
    const [minPrice, setMinPrice] = useState('');
    const [maxPrice, setMaxPrice] = useState('');

    const handleSearch = () => {
        onSearch({
            name: name || undefined,
            category: category || undefined,
            minPrice: minPrice ? Number(minPrice) : undefined,
            maxPrice: maxPrice ? Number(maxPrice) : undefined,
        });
    };

    const handleClear = () => {
        setName('');
        setCategory('');
        setMinPrice('');
        setMaxPrice('');
        onSearch({});
    };

    return (
        <div className="search-bar">
            <h2>Find Your Sweet Treat</h2>
            <div className="search-controls">
                <input
                    type="text"
                    placeholder="Search by name..."
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="search-input"
                />

                <input
                    type="text"
                    placeholder="Category..."
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="search-input"
                />

                <input
                    type="number"
                    placeholder="Min price"
                    value={minPrice}
                    onChange={(e) => setMinPrice(e.target.value)}
                    className="search-input price-input"
                    min="0"
                    step="0.01"
                />

                <input
                    type="number"
                    placeholder="Max price"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                    className="search-input price-input"
                    min="0"
                    step="0.01"
                />

                <button onClick={handleSearch} className="btn-search">
                    Search
                </button>

                <button onClick={handleClear} className="btn-clear">
                    Clear
                </button>
            </div>
        </div>
    );
};

export default SearchBar;
