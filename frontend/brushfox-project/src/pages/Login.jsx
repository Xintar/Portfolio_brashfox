import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Button from '../components/Common/Button';
import { toast } from 'react-toastify';
import './Login.css';

const Login = () => {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);

  // Redirect if already logged in
  if (isAuthenticated) {
    navigate('/');
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.username || !formData.password) {
      toast.error('Wypełnij wszystkie pola');
      return;
    }

    setLoading(true);

    const result = await login(formData.username, formData.password);
    
    setLoading(false);

    if (result.success) {
      toast.success('Zalogowano pomyślnie!');
      navigate('/');
    } else {
      toast.error(result.error || 'Błąd logowania');
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Zaloguj się</h1>
        <p className="login-subtitle">Witaj ponownie!</p>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Nazwa użytkownika</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Twoja nazwa użytkownika"
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Hasło</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Twoje hasło"
              autoComplete="current-password"
            />
          </div>

          <Button type="submit" fullWidth disabled={loading}>
            {loading ? 'Logowanie...' : 'Zaloguj się'}
          </Button>
        </form>

        <p className="signup-link">
          Nie masz konta? <Link to="/register">Zarejestruj się</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
