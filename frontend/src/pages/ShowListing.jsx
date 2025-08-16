import { useState, useEffect, useContext } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getListingById, createReview, deleteReview, deleteListing } from '../api/listings';
import { useAuth } from '../context/AuthContext.jsx';
import Map from '../components/Map.jsx';
import './ShowListing.css';

const ShowListing = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [listing, setListing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reviewRating, setReviewRating] = useState(3);
  const [reviewComment, setReviewComment] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [reviews, setReviews] = useState([]);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    const fetchListing = async () => {
      try {
        setLoading(true);
        const data = await getListingById(id);
        setListing(data);
        setReviews(data?.reviews || []);
        setError(null);
      } catch (err) {
        console.error('Error fetching listing:', err);
        setError('Failed to fetch listing details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchListing();
  }, [id, refreshKey]);

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    
    if (!user) {
      alert('You must be logged in to leave a review');
      navigate('/login', { state: { from: `/listings/${id}` } });
      return;
    }
    
    if (!reviewComment.trim()) {
      alert('Please enter a comment');
      return;
    }
    
    try {
      setSubmitting(true);
      
      const reviewData = {
        rating: reviewRating,
        comment: reviewComment
      };
      
      // Call the API to create a review
      const response = await createReview(id, reviewData);
      
      // Refresh the listing data to include the new review
      setRefreshKey(oldKey => oldKey + 1);
      
      // Reset form
      setReviewComment('');
      setReviewRating(3);
      
    } catch (err) {
      console.error('Error submitting review:', err);
      alert('Failed to submit review. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteReview = async (reviewId) => {
    if (!user) {
      alert('You must be logged in to delete a review');
      return;
    }
    
    if (window.confirm('Are you sure you want to delete this review?')) {
      try {
        await deleteReview(id, reviewId);
        
        // Refresh the listing data
        setRefreshKey(oldKey => oldKey + 1);
        
      } catch (err) {
        console.error('Error deleting review:', err);
        alert('Failed to delete review. Please try again.');
      }
    }
  };

  const handleLocationClick = () => {
    // In a real implementation, this would use a mapping library
    alert(`Showing location: ${listing?.location}, ${listing?.country}`);
  };

  const handleEditClick = () => {
    navigate(`/listings/${id}/edit`);
  };

  const handleDeleteListing = async () => {
    if (window.confirm('Are you sure you want to delete this listing?')) {
      try {
        await deleteListing(id);
        navigate('/');
      } catch (err) {
        console.error('Error deleting listing:', err);
        alert('Failed to delete listing. Please try again.');
      }
    }
  };

  if (loading) {
    return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  }

  if (error || !listing) {
    return <div className="alert alert-danger my-5" role="alert">{error || "Listing not found"}</div>;
  }

  const isOwner = user && listing.owner && user._id === listing.owner._id;
  const locationString = `${listing.location}, ${listing.country}`;

  return (
    <div className="container mt-4">
      <div className="row mt-3">
        <div className="col-md-8 offset-md-2">
          <h3 className="mb-3">{listing.title}</h3>
        </div>
        
        <div className="col-md-8 offset-md-2">
          <div className="card listing-card show-card mb-4">
            <img 
              src={listing.image?.url || 'https://via.placeholder.com/800x600?text=No+Image'} 
              className="show-img" 
              alt={listing.title}
            />
            <div className="card-body p-3">
              <p className="card-text">Owned by: <i>{listing.owner?.username || 'Unknown'}</i></p>
              <p className="card-text">{listing.description}</p>
              <p className="card-text price">₹{listing.price?.toLocaleString("en-IN") || '0'}</p>
              <p className="card-text location">
                <span className="location-icon">📍</span> {listing.location}, {listing.country}
              </p>
              
              <div className="category-tags mt-3">
                {listing.category?.map((cat, index) => (
                  <Link key={index} to={`/categories/${cat}`} className="category-tag">
                    {cat}
                  </Link>
                ))}
              </div>
            </div>
          </div>
          
          {isOwner && (
            <div className="action-buttons mb-4">
              <button onClick={handleEditClick} className="btn btn-primary edit-btn me-2">
                <span>✏️</span> Edit
              </button>
              <button onClick={handleDeleteListing} className="btn btn-danger">
                <span>🗑️</span> Delete
              </button>
            </div>
          )}
          
          <div className="map-section mb-4">
            <h4 className="mb-3">Where you'll be</h4>
            <div className="map-container">
              <Map locationString={locationString} />
            </div>
          </div>
          
          <hr />
          
          <div className="reviews-section">
            {user ? (
              <div className="review-form mb-4">
                <h4>Leave a Review</h4>
                <form onSubmit={handleReviewSubmit}>
                  <div className="mb-3">
                    <label htmlFor="rating" className="form-label">Rating</label>
                    <div className="star-rating">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <span 
                          key={star}
                          className={`star ${reviewRating >= star ? 'active' : ''}`}
                          onClick={() => setReviewRating(star)}
                        >
                          ★
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="mb-3">
                    <label htmlFor="comment" className="form-label">Comment</label>
                    <textarea
                      className="form-control"
                      id="comment"
                      rows="3"
                      value={reviewComment}
                      onChange={(e) => setReviewComment(e.target.value)}
                      required
                      placeholder="Share your experience..."
                    ></textarea>
                  </div>
                  <button 
                    type="submit" 
                    className="btn btn-success"
                    disabled={submitting}
                  >
                    {submitting ? 'Submitting...' : 'Submit Review'}
                  </button>
                </form>
              </div>
            ) : (
              <div className="alert alert-info mb-4">
                <p className="mb-0">
                  <Link to="/login" className="alert-link">Login</Link> or <Link to="/signup" className="alert-link">Sign up</Link> to leave a review
                </p>
              </div>
            )}
            
            <h4 className="mb-3">Reviews ({reviews.length})</h4>
            
            {reviews.length === 0 ? (
              <p className="text-muted">No reviews yet. Be the first to leave a review!</p>
            ) : (
              <div className="reviews-list">
                {reviews.map((review) => (
                  <div key={review._id} className="review-card">
                    <div className="review-header">
                      <div className="reviewer-info">
                        <span className="reviewer-name">{review.author?.username || 'Anonymous'}</span>
                        <div className="review-rating">
                          {[...Array(5)].map((_, i) => (
                            <span key={i} className={`star ${i < review.rating ? 'active' : ''}`}>★</span>
                          ))}
                        </div>
                      </div>
                      <div className="review-date">
                        {new Date(review.createdAt).toLocaleDateString()}
                      </div>
                    </div>
                    <p className="review-comment">{review.comment}</p>
                    
                    {user && review.author && user._id === review.author._id && (
                      <button 
                        onClick={() => handleDeleteReview(review._id)} 
                        className="btn btn-sm btn-outline-danger"
                      >
                        Delete
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShowListing;