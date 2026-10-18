import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import './About.css';

const About = () => {
  const [aboutData, setAboutData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAboutData = async () => {
      try {
        const response = await apiService.getAbout();
        setAboutData(response.data);
        setLoading(false);
      } catch (err) {
        if (err.response?.status === 404) {
          setError('Treść strony „O mnie” nie została jeszcze dodana. Uzupełnij ją w panelu administratora Django.');
        } else {
          setError(err.response?.data?.detail || err.message);
        }
        setLoading(false);
      }
    };

    fetchAboutData();
  }, []);

  if (loading) {
    return (
      <div className="about-page">
        <div className="about-header">
          <h1>Ładowanie...</h1>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="about-page">
        <div className="about-header">
          <h1>Błąd</h1>
        </div>
        <div className="about-content">
          <p>Nie udało się załadować danych: {error}</p>
        </div>
      </div>
    );
  }

  if (!aboutData) {
    return (
      <div className="about-page">
        <div className="about-header">
          <h1>O mnie</h1>
        </div>
        <div className="about-content">
          <p>Brak danych do wyświetlenia.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="about-page">
      <div className="about-header">
        <h1>{aboutData.title}</h1>
      </div>

      <div className="about-content">
        <div className="about-image">
          {aboutData.profile_image_url ? (
            <img 
              src={aboutData.profile_image_url} 
              alt={aboutData.name}
              className="profile-photo"
            />
          ) : (
            <div className="image-placeholder">📷</div>
          )}
        </div>

        <div className="about-text">
          <h2>{aboutData.name}</h2>
          <div className="bio">
            {aboutData.bio.split('\n').map((paragraph, index) => (
              paragraph.trim() && <p key={index}>{paragraph}</p>
            ))}
          </div>

          {aboutData.specializations && aboutData.specializations.length > 0 && (
            <div className="skills">
              <h3>Specjalizacje</h3>
              <ul>
                {aboutData.specializations.map((spec, index) => (
                  <li key={index}>✨ {spec}</li>
                ))}
              </ul>
            </div>
          )}

          {(aboutData.email || aboutData.phone) && (
            <div className="contact-info">
              <h3>Kontakt</h3>
              {aboutData.email && <p>📧 {aboutData.email}</p>}
              {aboutData.phone && <p>📞 {aboutData.phone}</p>}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default About;
