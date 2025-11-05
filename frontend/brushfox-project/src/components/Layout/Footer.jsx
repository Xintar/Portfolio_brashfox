import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '../../services/api';
import './Footer.css';

// Social media icons served from Django static files
const STATIC_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const socialIcons = {
  facebook: `${STATIC_URL}/static/socials/facebook.png`,
  instagram: `${STATIC_URL}/static/socials/instagram.png`,
  pinterest: `${STATIC_URL}/static/socials/pinterest.png`,
};

const Footer = () => {
  const currentYear = new Date().getFullYear();
  const [socialLinks, setSocialLinks] = useState({});

  useEffect(() => {
    // Fetch AboutMe data to get social links
    const fetchSocialLinks = async () => {
      try {
        const data = await apiService.getAbout();
        if (data?.social_links) {
          setSocialLinks(data.social_links);
        }
      } catch (error) {
        console.error('Error fetching social links:', error);
        // Fallback to default links
        setSocialLinks({
          facebook: 'https://facebook.com',
          instagram: 'https://instagram.com',
          pinterest: 'https://pinterest.com'
        });
      }
    };

    fetchSocialLinks();
  }, []);

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-grid">
          <div className="footer-section footer-about">
            <h3>Fox Brush Studio</h3>
            <p className="footer-tagline">Marta Chojecka - Make Up Artist</p>
            <p className="footer-services">Charakteryzacja | Wizaż | Kostiumy</p>
          </div>
          
          <div className="footer-section footer-links">
            <h4>Nawigacja</h4>
            <ul>
              <li><Link to="/">Strona główna</Link></li>
              <li><Link to="/portfolio">Portfolio</Link></li>
              <li><Link to="/about">O mnie</Link></li>
              <li><Link to="/blog">Blog</Link></li>
              <li><Link to="/contact">Kontakt</Link></li>
            </ul>
          </div>
          
          <div className="footer-section footer-social">
            <h4>Śledź mnie</h4>
            <div className="social-icons">
              {socialLinks.facebook && (
                <a 
                  href={socialLinks.facebook} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  aria-label="Facebook"
                  title="Facebook"
                >
                  <img src={socialIcons.facebook} alt="Facebook" />
                </a>
              )}
              {socialLinks.instagram && (
                <a 
                  href={socialLinks.instagram} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  aria-label="Instagram"
                  title="Instagram"
                >
                  <img src={socialIcons.instagram} alt="Instagram" />
                </a>
              )}
              {socialLinks.pinterest && (
                <a 
                  href={socialLinks.pinterest} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  aria-label="Pinterest"
                  title="Pinterest"
                >
                  <img src={socialIcons.pinterest} alt="Pinterest" />
                </a>
              )}
            </div>
          </div>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p className="footer-copyright">
          &copy; {currentYear} Fox Brush Studio - Marta Chojecka. Wszystkie prawa zastrzeżone.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
