import ContactForm from '../components/Contact/ContactForm';
import './Contact.css';

const Contact = () => {
  return (
    <div className="contact-page">
      <div className="page-header">
        <h1>Kontakt</h1>
        <p className="page-subtitle">Masz pytanie? Chętnie odpowiem!</p>
      </div>

      <ContactForm />

      <div className="contact-info">
        <div className="info-card">
          <h3>📧 Email</h3>
          <p>kontakt@brashfox.pl</p>
        </div>
        <div className="info-card">
          <h3>📍 Lokalizacja</h3>
          <p>Polska</p>
        </div>
        <div className="info-card">
          <h3>⏰ Dostępność</h3>
          <p>Pon - Pt: 9:00 - 18:00</p>
        </div>
      </div>
    </div>
  );
};

export default Contact;
