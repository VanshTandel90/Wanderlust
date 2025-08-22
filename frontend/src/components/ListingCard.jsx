import { Link } from 'react-router-dom';
import './ListingCard.css';

const ListingCard = ({ listing, showTax }) => {
  const formatPrice = (price) => {
    if (typeof price === 'number') {
      return price.toLocaleString("en-IN");
    }
    return price || 0;
  };

  return (
    <Link to={`/listings/${listing._id}`} className="listing-link">
      <div className="card listing-card">
        <img 
          src={listing.image?.url || 'https://via.placeholder.com/300x200?text=No+Image'} 
          className="card-img-top" 
          alt={listing.title} 
          style={{ height: '20rem' }}
        />
        <div className="card-img-overlay"></div>
        <div className="card-body">
          <p className="card-text">
            <b>{listing.title || 'Unnamed Listing'}<br /></b>
            ₹ {formatPrice(listing.price)} / night
            {showTax && <span className="tax-info"> +18% GST</span>}
          </p>
        </div>
      </div>
    </Link>
  );
};

export default ListingCard;