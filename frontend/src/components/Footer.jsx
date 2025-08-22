import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="f-info">
        <div className="f-info-brand">
          <span>&copy; 2025 RentEasy</span>
        </div>
        <div className="f-info-links">
          <a href="/privacy">Privacy</a>
          <a href="/terms">Terms</a>
          <a href="/about">About</a>
        </div>
        <div className="f-info-socials">
          <a href="https://facebook.com" aria-label="Facebook">
            <span className="social-icon">📘</span>
          </a>
          <a href="https://instagram.com" aria-label="Instagram">
            <span className="social-icon">📷</span>
          </a>
          <a href="https://twitter.com" aria-label="Twitter">
            <span className="social-icon">🐦</span>
          </a>
          <a href="https://linkedin.com" aria-label="LinkedIn">
            <span className="social-icon">💼</span>
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 