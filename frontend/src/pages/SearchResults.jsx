import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { searchListings } from '../api/listings';
import ListingCard from '../components/ListingCard';
import CategoryFilter from '../components/CategoryFilter';
import './Listings.css';

const SearchResults = () => {
  const [searchParams] = useSearchParams();
  const destination = searchParams.get('destination') || '';
  
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showTax, setShowTax] = useState(false);

  useEffect(() => {
    const fetchSearchResults = async () => {
      if (!destination) {
        setListings([]);
        setLoading(false);
        return;
      }
      
      try {
        setLoading(true);
        const data = await searchListings(destination);
        setListings(data || []);
        setError(null);
      } catch (err) {
        console.error('Error searching listings:', err);
        setError('Failed to search listings. Please try again later.');
        setListings([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSearchResults();
  }, [destination]);

  const handleTaxToggle = (isChecked) => {
    setShowTax(isChecked);
  };

  if (loading) {
    return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  }

  return (
    <div className="container-fluid p-0">
      <CategoryFilter onTaxToggle={handleTaxToggle} />
      
      <div className="container mt-4">
        <h3 className="mb-4">Search Results for: "{destination}"</h3>
        
        <div className="row row-cols-lg-3 row-cols-md-2 row-cols-sm-1 mt-3">
          {listings && listings.length > 0 ? (
            listings.map(listing => (
              <div key={listing._id} className="col">
                <ListingCard listing={listing} showTax={showTax} />
              </div>
            ))
          ) : (
            <div className="col-12 text-center my-5">
              <h4>No listings found for "{destination}"</h4>
              <p>Try a different search term or browse our categories above.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchResults;