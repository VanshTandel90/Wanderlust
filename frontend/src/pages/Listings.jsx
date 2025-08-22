import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getAllListings, getListingsByCategory, getNearbyListings } from '../api/listings';
import ListingCard from '../components/ListingCard';
import CategoryFilter from '../components/CategoryFilter';
import './Listings.css';
import { useAuth } from '../context/AuthContext';

const Listings = () => {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [header, setHeader] = useState("All Listings");
  const { category } = useParams();
  const { user } = useAuth(); 


  const fetchDefaultListings = async () => {
    try {
      setLoading(true);
      setHeader(category ? `Category: ${category}` : "All Listings");
      const data = category
        ? await getListingsByCategory(category)
        : await getAllListings();
      setListings(data || []);
      setError(null);
    } catch (err) {
      console.error('Error fetching default listings:', err);
      setError('Failed to fetch listings. Please try again later.');
      setListings([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDefaultListings();
  }, [category]);

  const handleNearbyClick = async () => {
    if (!user) {
      alert("Please log in to see listings near you.");
      return;
    }
    try {
      setLoading(true);
      setHeader("Listings Near You");
      const data = await getNearbyListings();
      setListings(data.nearby_listings || []);
      setError(null);
    } catch (err) {
      console.error('Error fetching nearby listings:', err);
      setError('Could not fetch nearby listings. Please try again.');
      setListings([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  }

  if (error) {
    return <div className="alert alert-danger my-5" role="alert">{error}</div>;
  }

  return (
    <div className="container-fluid p-0">
      <CategoryFilter onNearbyClick={handleNearbyClick} />
      
      <div className="container mt-4">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h3>{header}</h3>
          <Link to="/listings/new" className="btn btn-primary create-listing-btn">
            <span className="me-2">➕</span> Add New Listing
          </Link>
        </div>
        <div className="row row-cols-lg-3 row-cols-md-2 row-cols-sm-1 mt-3">
          {listings.length > 0 ? (
            listings.map(listing => (
              <div key={listing._id} className="col">
                <ListingCard listing={listing} />
              </div>
            ))
          ) : (
            <div className="col-12 text-center my-5">
              <h3>No listings found</h3>
              <p>Try a different search, category, or <Link to="/">view all listings</Link>.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Listings;