import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Witaj w Fox Brush Studio</h1>
          <p className="hero-subtitle">
            Charakteryzacja | Makijaż | Stylizacja
          </p>
          <p className="hero-description">
            Odkryj magię przemiany. Od wizażu, przez charakteryzację, po kostiumy - 
            razem stworzymy niepowtarzalny wizerunek dla Twojego projektu.
          </p>
          <div className="hero-buttons">
            <Link to="/portfolio" className="btn btn-primary">
              Zobacz Portfolio
            </Link>
            <Link to="/blog" className="btn btn-outline">
              Czytaj Blog
            </Link>
          </div>
        </div>
      </section>

      <section className="features">
        <div className="feature-card">
          <div className="feature-icon">🎨</div>
          <h3>Portfolio</h3>
          <p>Przeglądaj moją kolekcję prac - charakteryzacje, makijaże i kostiumy z różnych projektów.</p>
          <Link to="/portfolio">Zobacz więcej →</Link>
        </div>

        <div className="feature-card">
          <div className="feature-icon">✍️</div>
          <h3>Blog</h3>
          <p>Czytaj moje przemyślenia, porady dotyczące makijażu i historie z planów filmowych.</p>
          <Link to="/blog">Czytaj teraz →</Link>
        </div>

        <div className="feature-card">
          <div className="feature-icon">💬</div>
          <h3>Kontakt</h3>
          <p>Masz pytania lub chcesz nawiązać współpracę? Skontaktuj się ze mną!</p>
          <Link to="/contact">Napisz do mnie →</Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
