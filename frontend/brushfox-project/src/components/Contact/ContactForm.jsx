import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../../services/api';
import { isValidEmail } from '../../utils/helpers';
import Button from '../Common/Button';
import { toast } from 'react-toastify';
import './ContactForm.css';

const ContactForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    topic: '',
    message: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Imię jest wymagane';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email jest wymagany';
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = 'Nieprawidłowy adres email';
    }

    if (!formData.topic.trim()) {
      newErrors.topic = 'Temat jest wymagany';
    }

    if (!formData.message.trim()) {
      newErrors.message = 'Wiadomość jest wymagana';
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);

    try {
      await apiService.sendMessage(formData);
      toast.success('Wiadomość została wysłana!');
      setFormData({ name: '', email: '', topic: '', message: '' });
      setTimeout(() => navigate('/'), 2000);
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Błąd podczas wysyłania wiadomości');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="contact-form">
      <h2>Skontaktuj się ze mną</h2>
      <p className="form-description">
        Masz pytanie lub chcesz nawiązać współpracę? Wypełnij formularz poniżej!
      </p>

      <div className="form-group">
        <label htmlFor="name">Imię *</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Twoje imię"
          className={errors.name ? 'error' : ''}
        />
        {errors.name && <span className="error-text">{errors.name}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="email">Email *</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="twoj@email.pl"
          className={errors.email ? 'error' : ''}
        />
        {errors.email && <span className="error-text">{errors.email}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="topic">Temat *</label>
        <input
          type="text"
          id="topic"
          name="topic"
          value={formData.topic}
          onChange={handleChange}
          placeholder="Temat wiadomości"
          className={errors.topic ? 'error' : ''}
        />
        {errors.topic && <span className="error-text">{errors.topic}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="message">Wiadomość *</label>
        <textarea
          id="message"
          name="message"
          value={formData.message}
          onChange={handleChange}
          placeholder="Twoja wiadomość..."
          rows="6"
          className={errors.message ? 'error' : ''}
        />
        {errors.message && <span className="error-text">{errors.message}</span>}
      </div>

      <Button type="submit" fullWidth disabled={loading}>
        {loading ? 'Wysyłanie...' : 'Wyślij wiadomość'}
      </Button>
    </form>
  );
};

export default ContactForm;
