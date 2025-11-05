import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { NAV_ITEMS } from '../../utils/constants';
import './Header.css';

const Header = () => {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <h1>BrashFox</h1>
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
