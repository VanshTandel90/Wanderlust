import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getListingById, updateListing } from '../api/listings';
import { useAuth } from '../context/AuthContext.jsx';
import './UpdateListing.css';

const CATEGORIES = [
  'Trending', 'Rooms', 'Iconic Cities', 'Mountains', 
  'Castles', 'Amazing Pools', 'Camping', 'Farms', 'Arctic', 'Boats'
];

const UpdateListing = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    location: '',
    country: '',
    category: [],
    image: null
  });
  const [originalImage, setOriginalImage] = useState('');

  // Form validation state
  const [validation, setValidation] = useState({
    title: true,
    description: true,
    price: true,
    location: true,
    country: true
  });

  // Fetch listing data
  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    const fetchListing = async () => {
      try {
        setIsLoading(true);
        const listing = await getListingById(id);
        
        if (!listing) {
          setError('Listing not found');
          return;
        }
        
        if (listing.owner._id !== user._id) {
          setError("You don't have permission to edit this listing.");
          setTimeout(() => navigate('/'), 2000);
          return;
        }

        const categories = Array.isArray(listing.category) ? listing.category : [];

        setFormData({
          title: listing.title || '',
          description: listing.description || '',
          price: listing.price || '',
          location: listing.location || '',
          country: listing.country || '',
          category: categories,
          image: null
        });
        
        if (listing.image && listing.image.url) {
          setOriginalImage(listing.image.url);
        }
      } catch (err) {
        setError('Failed to load listing data');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchListing();
  }, [id, user, navigate]);

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
      country: !!formData.country.trim()
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
      
      await updateListing(id, formData);
      
      navigate(`/listings/${id}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update listing');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="update-listing-loading">
        <div className="spinner"></div>
        <p>Loading listing data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="update-listing-container">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="update-listing-container">
      <div className="update-listing-form-container">
        <h2>Update Listing</h2>
        
        <form onSubmit={handleSubmit} className="update-listing-form" noValidate>
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
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
              className={validation.description === false ? 'invalid' : ''}
              required
            />
            {validation.description === false && 
              <div className="invalid-feedback">Please provide a description</div>
            }
          </div>

          {originalImage && (
            <div className="form-group original-image-container">
              <label>Current Image</label>
              <img 
                src={originalImage} 
                alt="Current listing" 
                className="original-image" 
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="image">Upload New Image (optional)</label>
            <input
              type="file"
              id="image"
              name="image"
              onChange={handleImageChange}
              accept="image/*"
            />
            <small className="image-hint">Leave empty to keep the current image</small>
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

          <div className="button-group">
            <button 
              type="button" 
              className="cancel-btn"
              onClick={() => navigate(`/listings/${id}`)}
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="update-btn"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Updating...' : 'Update Listing'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UpdateListing;