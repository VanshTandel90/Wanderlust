import { useState } from 'react';
import { Link } from 'react-router-dom';
import './CategoryFilter.css';
import { useAuth } from '../context/AuthContext';

const CategoryFilter = ({ onNearbyClick }) => {
  const { user } = useAuth();
  const categories = [
    { name: 'Trending', emoji: '🔥' },
    { name: 'Rooms', emoji: '🛏️' },
    { name: 'Iconic Cities', emoji: '🏙️' },
    { name: 'Mountains', emoji: '⛰️' },
    { name: 'Castles', emoji: '🏰' },
    { name: 'Amazing Pools', emoji: '🏊' },
    { name: 'Camping', emoji: '⛺' },
    { name: 'Farms', emoji: '🐄' },
    { name: 'Arctic', emoji: '❄️' },
    { name: 'Boats', emoji: '🚢' }
  ];

  return (
    <div className="container-fluid px-3 py-2">
      <div className="row gx-3 gy-2 align-items-center">
        {categories.map((category, index) => (
          <div key={index} className="col-auto filter text-center">
            <Link to={`/categories/${category.name}`}>
              <div className="category-icon">{category.emoji}</div>
              <p>{category.name}</p>
            </Link>
          </div>
        ))}

        {/* Tax Toggle */}
       {user && (
              <button className="btn col-12 col-md-auto mt-2 ms-auto tax-toggle" onClick={onNearbyClick}>
                📍 Show Nearby Listings
              </button>
        )}
      </div>
    </div>
  );
};

export default CategoryFilter;