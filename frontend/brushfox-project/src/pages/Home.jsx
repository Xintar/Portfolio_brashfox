import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <p className="hero-kicker">Fox Brush Studio · kreatywna pracownia</p>
          <h1 className="hero-title">
            Zmieniamy <span>pomysły</span> w&nbsp;obrazy.
          </h1>
          <p className="hero-subtitle">
            Charakteryzacja | Makijaż | Stylizacja
          </p>
          <p className="hero-description">
            Odkryj magię przemiany. Od wizażu, przez charakteryzację, po kostiumy
            — razem stworzymy niepowtarzalny wizerunek dla Twojego projektu.
          </p>
          <div className="hero-buttons">
            <Link to="/portfolio" className="btn btn-primary">
              Zobacz portfolio <span aria-hidden="true">↗</span>
            </Link>
            <Link to="/blog" className="btn btn-outline">
              Poznaj kulisy
            </Link>
          </div>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="hero-art-orbit" />
          <div className="hero-art-shape">
            <span className="hero-art-word">F</span>
          </div>
          <div className="hero-art-tag">
            MAKEUP<br />SFX · COSTUME
          </div>
        </div>
      </section>

      <section className="features">
        <div className="feature-card">
          <span className="feature-number">01 / PRACE</span>
          <h3>Portfolio</h3>
          <p>Przeglądaj moją kolekcję prac - charakteryzacje, makijaże i kostiumy z różnych projektów.</p>
          <Link to="/portfolio">Zobacz więcej <span aria-hidden="true">↗</span></Link>
        </div>

        <div className="feature-card">
          <span className="feature-number">02 / INSPIRACJE</span>
          <h3>Blog</h3>
          <p>Czytaj moje przemyślenia, porady dotyczące makijażu i historie z planów filmowych.</p>
          <Link to="/blog">Czytaj teraz <span aria-hidden="true">↗</span></Link>
        </div>

        <div className="feature-card">
          <span className="feature-number">03 / WSPÓŁPRACA</span>
          <h3>Kontakt</h3>
          <p>Masz pytania lub chcesz nawiązać współpracę? Skontaktuj się ze mną!</p>
          <Link to="/contact">Napisz do mnie <span aria-hidden="true">↗</span></Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
