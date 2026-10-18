import { useFetch } from '../../hooks/useFetch';
import { apiService } from '../../services/api';
import './Footer.css';

const SOCIAL_PLATFORMS = {
  facebook: {
    label: 'Facebook',
    icon: (
      <path d="M13.4 21v-8.2h2.8l.4-3.2h-3.2v-2c0-.9.3-1.6 1.6-1.6h1.7V3.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.3H7.2v3.2H10V21h3.4Z" />
    ),
  },
  instagram: {
    label: 'Instagram',
    icon: (
      <>
        <rect x="3.5" y="3.5" width="17" height="17" rx="5" />
        <circle cx="12" cy="12" r="4" />
        <circle className="social-dot" cx="17.7" cy="6.7" r="1" />
      </>
    ),
  },
  x: {
    label: 'X',
    icon: (
      <path d="M18.9 3H21l-6.9 7.9L22.2 21h-6.4l-5-6.5L5.1 21H3l7.4-8.5L2.6 3h6.5l4.5 6 5.3-6Zm-1.1 16.2H19L8.1 4.7H6.8l11 14.5Z" />
    ),
  },
  tiktok: {
    label: 'TikTok',
    icon: (
      <path d="M19.6 8.2a6.7 6.7 0 0 1-4.1-1.4v7.1a5.5 5.5 0 1 1-4.8-5.4v3.2a2.4 2.4 0 1 0 1.6 2.2V3h3.2c.3 2.1 1.9 3.8 4.1 4.1v3.2Z" />
    ),
  },
  youtube: {
    label: 'YouTube',
    icon: (
      <>
        <path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4a2.5 2.5 0 0 0-1.8 1.8A26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8Z" />
        <path className="social-play" d="m10 15.5 5.2-3.5L10 8.5v7Z" />
      </>
    ),
  },
  pinterest: {
    label: 'Pinterest',
    icon: (
      <path d="M12 2a10 10 0 0 0-3.6 19.3c0-.8 0-1.8.2-2.7l1.3-5.4s-.3-.6-.3-1.5c0-1.4.8-2.5 1.9-2.5.9 0 1.3.7 1.3 1.5 0 .9-.6 2.3-.9 3.6-.3 1.1.5 2 1.6 2 1.9 0 3.4-2 3.4-4.9 0-2.5-1.8-4.2-4.3-4.2-2.9 0-4.6 2.2-4.6 4.5 0 .9.3 1.9.8 2.4.1.1.1.2.1.4l-.3 1.1c0 .2-.2.3-.4.2-1.3-.6-2.1-2.4-2.1-3.9 0-3.2 2.3-6.1 6.7-6.1 3.5 0 6.2 2.5 6.2 5.8 0 3.5-2.2 6.4-5.2 6.4-1 0-2-.6-2.4-1.2l-.7 2.7c-.2 1-.9 2-1.3 2.7A10 10 0 1 0 12 2Z" />
    ),
  },
  linkedin: {
    label: 'LinkedIn',
    icon: (
      <path d="M6.5 8.5a2 2 0 1 0 0-4 2 2 0 0 0 0 4ZM4.8 10h3.4v10H4.8V10Zm5.4 0h3.3v1.4h.1a3.6 3.6 0 0 1 3.2-1.7c3.4 0 4 2.2 4 5.1V20h-3.4v-4.6c0-1.1 0-2.6-1.6-2.6s-1.9 1.2-1.9 2.5V20h-3.4V10Z" />
    ),
  },
};

const Footer = () => {
  const currentYear = new Date().getFullYear();
  const { data, loading, error } = useFetch(() => apiService.getAbout());
  const socialLinks = Array.isArray(data?.social_links) ? data.social_links : [];

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>Fox Brush Studio</h3>
          <p>Charakteryzacja, makijaż i kreacja kostiumów</p>
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
          <p className="social-note">
            {loading
              ? 'Ładowanie profili...'
              : error
                ? 'Nie udało się pobrać profili społecznościowych.'
                : socialLinks.length
                  ? 'Znajdź mnie również tutaj'
                  : 'Profile pojawią się wkrótce'}
          </p>
          <ul className="social-links">
            {socialLinks.map(({ platform, url }) => {
              const socialPlatform = SOCIAL_PLATFORMS[platform];
              if (!socialPlatform) return null;

              return (
                <li className="social-item" key={platform}>
                  <a
                    className="social-link"
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={socialPlatform.label}
                  >
                    <span className="social-icon" aria-hidden="true">
                      <svg viewBox="0 0 24 24" focusable="false">
                        {socialPlatform.icon}
                      </svg>
                    </span>
                    <span className="social-name">{socialPlatform.label}</span>
                  </a>
                </li>
              );
            })}
          </ul>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; {currentYear} Fox Brush Studio - Marta Chojecka. Wszystkie prawa zastrzeżone.</p>
      </div>
    </footer>
  );
};

export default Footer;
