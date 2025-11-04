import './About.css';

const About = () => {
  return (
    <div className="about-page">
      <div className="about-header">
        <h1>O mnie</h1>
      </div>

      <div className="about-content">
        <div className="about-image">
          <div className="image-placeholder">📷</div>
        </div>

        <div className="about-text">
          <h2>BrashFox - Photographer & Blogger</h2>
          <p>
            Witaj! Jestem pasjonatem fotografii z wieloletnim doświadczeniem w uwiecznianiu
            wyjątkowych chwil i tworzeniu unikalnych kompozycji wizualnych.
          </p>
          <p>
            Moja podróż z fotografią rozpoczęła się wiele lat temu i od tego czasu
            nieustannie rozwijam swoje umiejętności, eksperymentuję z różnymi stylami
            i technikami.
          </p>
          <p>
            Na tym blogu dzielę się moimi pracami, przemyśleniami i poradami dotyczącymi
            fotografii. Mam nadzieję, że znajdziesz tu inspirację!
          </p>

          <div className="skills">
            <h3>Specjalizacje</h3>
            <ul>
              <li>📸 Fotografia portretowa</li>
              <li>🌄 Fotografia krajobrazowa</li>
              <li>🎉 Fotografia eventowa</li>
              <li>🎨 Retusz i obróbka zdjęć</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
