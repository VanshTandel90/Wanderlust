import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchInput, setSearchInput] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const { user, logout, loading } = useAuth();

  const handleSearchChange = (e) => {
    setSearchInput(e.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      navigate(`/search?destination=${encodeURIComponent(searchInput.trim())}`);
      setSearchInput('');
      setIsExpanded(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    setIsExpanded(false);
    navigate('/');
  };

  const toggleNavbar = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <nav className="navbar navbar-expand-lg bg-body-light bg-light border-bottom sticky-top">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          <span className="brand-icon">🧭</span>
        </Link>
        <button 
          className="navbar-toggler" 
          type="button" 
          onClick={toggleNavbar}
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className={`collapse navbar-collapse ${isExpanded ? 'show' : ''}`}>
          <div className="navbar-nav">
            <Link className="nav-link" to="/">Explore</Link>
          </div>

          {location.pathname !== '/login' && location.pathname !== '/signup' && (
            <div className="navbar-nav ms-auto">
              <form className="d-flex" role="search" onSubmit={handleSearchSubmit}>
                <input 
                  className="form-control me-2 search-inp" 
                  type="search" 
                  placeholder="Search destinations" 
                  value={searchInput}
                  onChange={handleSearchChange}
                  required
                />
                <button className="btn search-btn" type="submit">
                  <span className="search-icon">🔍</span>
                  Search
                </button>
              </form>
            </div>
          )}

          <div className="navbar-nav ms-auto">
            {/* <Link className="nav-link" to="/listings/new">Airbnb your home</Link> */}
            {!loading && (
              user ? (
                <>
                  <span className="nav-link">Welcome, {user.username}!</span>
                  <button className="nav-link btn" onClick={handleLogout}><b>Log out</b></button>
                </>
              ) : (
                <>
                  <Link className="nav-link" to="/signup"><b>Sign up</b></Link>
                  <Link className="nav-link" to="/login"><b>Log in</b></Link>
                </>
              )
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;