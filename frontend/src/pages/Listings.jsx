import { useState, useEffect } from 'react';
import { useParams , Link } from 'react-router-dom';
import { getAllListings, getListingsByCategory } from '../api/listings';
import ListingCard from '../components/ListingCard';
import CategoryFilter from '../components/CategoryFilter';
import './Listings.css';

const Listings = () => {

  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { category } = useParams();
  const [showTax, setShowTax] = useState(false);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        setLoading(true);
        let data;
        
        if (category) {
          data = await getListingsByCategory(category);
        } else {
          data = await getAllListings();
        }
        
        setListings(data || []);
        setError(null);
      } catch (err) {
        console.error('Error fetching listings:', err);
        setError('Failed to fetch listings. Please try again later.');
        setListings([]);
      } finally {
        setLoading(false);
      }
    };

    fetchListings();
  }, [category]);

  const handleTaxToggle = (isChecked) => {
    setShowTax(isChecked);
  };

  if (loading) {
    return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  }

  if (error) {
    return <div className="alert alert-danger my-5" role="alert">{error}</div>;
  }

  return (
    <div className="container-fluid p-0">
      <CategoryFilter onTaxToggle={handleTaxToggle} />
      
      <div className="container mt-4">
        <div className="d-flex justify-content-between align-items-center mb-4">
          {category && <h3>Category: {category}</h3>}
          {!category && <h3>All Listings</h3>}
          <Link to="/listings/new" className="btn btn-primary create-listing-btn">
            <span className="me-2">➕</span> Add New Listing
          </Link>
        </div>
        <div className="row row-cols-lg-3 row-cols-md-2 row-cols-sm-1 mt-3">
          {listings && listings.length > 0 ? (
            listings.map(listing => (
              <div key={listing._id} className="col">
                <ListingCard listing={listing} showTax={showTax} />
              </div>
            ))
          ) : (
            <div className="col-12 text-center my-5">
              <h3>No listings found</h3>
              {category && <p>No listings found for category: {category}</p>}
              <Link to="/listings/new" className="btn btn-primary mt-3">
                Create Your First Listing
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Listings;