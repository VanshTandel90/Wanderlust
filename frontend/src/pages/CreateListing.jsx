import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createListing } from '../api/listings';
import './CreateListing.css';

const CATEGORIES = [
  'Trending', 'Rooms', 'Iconic Cities', 'Mountains', 
  'Castles', 'Amazing Pools', 'Camping', 'Farms', 'Arctic', 'Boats'
];

const CreateListing = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    location: '',
    country: '',
    category: ['Trending'], // Default category
    image: null
  });

  // Form validation state
  const [validation, setValidation] = useState({
    title: false,
    description: false,
    price: false,
    location: false,
    country: false,
    image: false
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleCategoryChange = (e) => {
    const { value, checked } = e.target;
    
    if (checked) {
      setFormData({
        ...formData,
        category: [...formData.category, value]
      });
    } else {
      setFormData({
        ...formData,
        category: formData.category.filter(cat => cat !== value)
      });
    }
  };

  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFormData({
        ...formData,
        image: e.target.files[0]
      });
    }
  };

  const validateForm = () => {
    const newValidation = {
      title: !!formData.title.trim(),
      description: !!formData.description.trim(),
      price: !isNaN(formData.price) && Number(formData.price) > 0,
      location: !!formData.location.trim(),
      country: !!formData.country.trim(),
      image: !!formData.image
    };
    
    setValidation(newValidation);
    
    return Object.values(newValidation).every(isValid => isValid);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      setError('Please fill all required fields correctly');
      return;
    }
    
    try {
      setIsSubmitting(true);
      setError('');
      
      const response = await createListing(formData);
      
      // Redirect to the new listing's detail page after successful creation
      if (response && response.listing && response.listing._id) {
        navigate(`/listings/${response.listing._id}`);
      } else {
        // Fallback if the response format is unexpected
        navigate('/');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create listing');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="create-listing-container">
      <div className="create-listing-form-container">
        <h2>Create New Listing</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit} className="create-listing-form" noValidate>
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              placeholder="Enter a catchy title"
              className={validation.title === false ? 'invalid' : ''}
              required
            />
            {validation.title === false && 
              <div className="invalid-feedback">Please provide a title</div>
            }
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="Describe your place"
              className={validation.description === false ? 'invalid' : ''}
              required
            />
            {validation.description === false && 
              <div className="invalid-feedback">Please provide a description</div>
            }
          </div>

          <div className="form-group">
            <label htmlFor="image">Upload Image</label>
            <input
              type="file"
              id="image"
              name="image"
              onChange={handleImageChange}
              accept="image/*"
              className={validation.image === false ? 'invalid' : ''}
              required
            />
            {validation.image === false && 
              <div className="invalid-feedback">Please upload an image</div>
            }
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="price">Price (per night)</label>
              <input
                type="number"
                id="price"
                name="price"
                value={formData.price}
                onChange={handleInputChange}
                placeholder="99"
                min="1"
                className={validation.price === false ? 'invalid' : ''}
                required
              />
              {validation.price === false && 
                <div className="invalid-feedback">Please provide a valid price</div>
              }
            </div>

            <div className="form-group">
              <label htmlFor="country">Country</label>
              <input
                type="text"
                id="country"
                name="country"
                value={formData.country}
                onChange={handleInputChange}
                placeholder="India"
                className={validation.country === false ? 'invalid' : ''}
                required
              />
              {validation.country === false && 
                <div className="invalid-feedback">Please provide a country</div>
              }
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleInputChange}
              placeholder="Kolak, Valsad"
              className={validation.location === false ? 'invalid' : ''}
              required
            />
            {validation.location === false && 
              <div className="invalid-feedback">Please provide a location</div>
            }
          </div>

          <div className="form-group categories-group">
            <label>Categories</label>
            <div className="categories-container">
              {CATEGORIES.map(category => (
                <div key={category} className="category-checkbox">
                  <input
                    type="checkbox"
                    id={`category-${category}`}
                    name="category"
                    value={category}
                    checked={formData.category.includes(category)}
                    onChange={handleCategoryChange}
                  />
                  <label htmlFor={`category-${category}`}>{category}</label>
                </div>
              ))}
            </div>
          </div>

          <button 
            type="submit" 
            className="create-btn"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Creating...' : 'Create Listing'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateListing;