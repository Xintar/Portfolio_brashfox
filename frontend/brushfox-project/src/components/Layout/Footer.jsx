import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>BrashFox Portfolio</h3>
          <p>Fotografia i blog osobisty</p>
        </div>
        
        <div className="footer-section">
          <h4>Nawigacja</h4>
          <ul>
            <li><a href="/">Strona główna</a></li>
            <li><a href="/portfolio">Portfolio</a></li>
            <li><a href="/blog">Blog</a></li>
            <li><a href="/contact">Kontakt</a></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Social Media</h4>
          <div className="social-links">
            <a href="#" aria-label="Facebook">📘</a>
            <a href="#" aria-label="Instagram">📷</a>
            <a href="#" aria-label="Twitter">🐦</a>
          </div>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; {currentYear} BrashFox. Wszystkie prawa zastrzeżone.</p>
      </div>
    </footer>
  );
};

export default Footer;
