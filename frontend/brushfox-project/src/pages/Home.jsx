import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Witaj w BrashFox Portfolio</h1>
          <p className="hero-subtitle">
            Fotografia | Blog | Kreatywność
          </p>
          <p className="hero-description">
            Odkryj moją pasję do fotografii i dołącz do mojej podróży poprzez
            wizualne opowieści i inspirujące treści.
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
          <div className="feature-icon">📷</div>
          <h3>Portfolio</h3>
          <p>Przeglądaj moją kolekcję profesjonalnych fotografii z różnych wydarzeń i sesji.</p>
          <Link to="/portfolio">Zobacz więcej →</Link>
        </div>

        <div className="feature-card">
          <div className="feature-icon">✍️</div>
          <h3>Blog</h3>
          <p>Czytaj moje przemyślenia, porady fotograficzne i historie z planu zdjęciowego.</p>
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
