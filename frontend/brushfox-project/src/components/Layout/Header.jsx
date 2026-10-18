import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { useAuth } from '../../context/AuthContext';
import { NAV_ITEMS } from '../../utils/constants';
import { openAdminPanel } from '../../utils/adminPanel';
import './Header.css';

const Header = () => {
  const { isAuthenticated, user, logout } = useAuth();

  const handleAdminClick = () => {
    openAdminPanel().catch(() => {
      toast.info('Nie udało się zalogować automatycznie — zaloguj się w panelu ręcznie.');
    });
  };

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <h1>Fox Brush</h1>
        </Link>
        
        <nav className="main-nav">
          <ul className="nav-list">
            {NAV_ITEMS.map((item) => (
              <li key={item.path}>
                <Link to={item.path} className="nav-link">
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="auth-section">
          {isAuthenticated ? (
            <div className="user-menu">
              <span className="user-name">Witaj, {user?.username || 'Użytkownik'}</span>
              {user?.is_superuser && (
                <button type="button" onClick={handleAdminClick} className="btn-admin">
                  Panel admina
                </button>
              )}
              <button onClick={logout} className="btn-logout">
                Wyloguj
              </button>
            </div>
          ) : (
            <div className="auth-buttons">
              <Link to="/login" className="btn-login">
                Zaloguj
              </Link>
              <Link to="/register" className="btn-register">
                Rejestracja
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
