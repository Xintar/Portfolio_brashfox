import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../../services/api';
import { slugify } from '../../utils/helpers';
import Button from '../Common/Button';
import { toast } from 'react-toastify';
import './BlogPostForm.css';

const BlogPostForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    post: '',
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title || !formData.post) {
      toast.error('Wypełnij wszystkie pola');
      return;
    }

    setLoading(true);

    try {
      const postData = {
        ...formData,
        slug: slugify(formData.title),
        author: 1, // This should come from auth context
      };

      await apiService.createPost(postData);
      toast.success('Post został utworzony!');
      navigate('/blog');
    } catch (error) {
      console.error('Error creating post:', error);
      toast.error('Błąd podczas tworzenia posta');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="blog-post-form">
      <h2>Dodaj nowy post</h2>
      
      <div className="form-group">
        <label htmlFor="title">Tytuł *</label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Wpisz tytuł posta"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="post">Treść *</label>
        <textarea
          id="post"
          name="post"
          value={formData.post}
          onChange={handleChange}
          placeholder="Wpisz treść posta"
          rows="10"
          required
        />
      </div>

      <div className="form-actions">
        <Button type="button" variant="secondary" onClick={() => navigate('/blog')}>
          Anuluj
        </Button>
        <Button type="submit" disabled={loading}>
          {loading ? 'Dodawanie...' : 'Dodaj post'}
        </Button>
      </div>
    </form>
  );
};

export default BlogPostForm;
