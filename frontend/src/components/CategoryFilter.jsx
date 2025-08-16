import { useState } from 'react';
import { Link } from 'react-router-dom';
import './CategoryFilter.css';

const CategoryFilter = ({ onTaxToggle }) => {
  const [taxChecked, setTaxChecked] = useState(false);
  
  const handleTaxToggle = (e) => {
    const isChecked = e.target.checked;
    setTaxChecked(isChecked);
    if (onTaxToggle) {
      onTaxToggle(e.target.checked);
    }
  };
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
      <div className="row gx-3 gy-2">
        {categories.map((category, index) => (
          <div key={index} className="col-6 col-sm-4 col-md-3 col-lg-2 filter text-center">
            <Link to={`/categories/${category.name}`}>
              <div className="category-icon">
                {category.emoji}
              </div>
              <p>{category.name}</p>
            </Link>
          </div>
        ))}

        {/* Tax Toggle */}
        <div className="col-12 col-md-auto mt-2 ms-auto">
          <div className="tax-toggle">
            <div className="form-check-reverse form-switch">
              <input 
                className="form-check-input" 
                type="checkbox" 
                role="switch" 
                id="taxToggle" 
                checked={taxChecked}
                onChange={handleTaxToggle}
              />
              <label className="form-check-label tax-label" htmlFor="taxToggle">
                Display Total with GST
              </label>            
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CategoryFilter;