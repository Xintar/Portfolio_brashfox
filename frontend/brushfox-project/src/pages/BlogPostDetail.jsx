import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import useFetch from '../hooks/useFetch';
import { apiService } from '../services/api';
import { formatDate } from '../utils/helpers';
import Loading from '../components/Common/Loading';
import ErrorMessage from '../components/Common/ErrorMessage';
import Button from '../components/Common/Button';
import { toast } from 'react-toastify';
import './BlogPostDetail.css';

const BlogPostDetail = () => {
  const { slug } = useParams();
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  
  const { data: post, loading, error, refetch } = useFetch(
    () => apiService.getPostBySlug(slug),
    [slug]
  );

  const handleDelete = async () => {
    if (!window.confirm('Czy na pewno chcesz usunąć ten post?')) {
      return;
    }

    try {
      await apiService.deletePost(slug);  // Use slug instead of post.id
      toast.success('Post został usunięty');
      navigate('/blog');
    } catch (err) {
      console.error('Error deleting post:', err);
      toast.error('Błąd podczas usuwania posta');
    }
  };

  if (loading) return <Loading message="Ładowanie posta..." />;
  if (error) return <ErrorMessage message={error} onRetry={refetch} />;
  if (!post) return <ErrorMessage message="Post nie został znaleziony" />;

  const isAuthor = isAuthenticated && user?.id === post.author?.id;

  return (
    <div className="blog-post-detail">
      <article className="post-content">
        <header className="post-header">
          <Link to="/blog" className="back-link">← Powrót do bloga</Link>
          
          <h1 className="post-title">{post.title}</h1>
          
          <div className="post-meta">
            <span className="author">👤 {post.author?.username || 'Autor'}</span>
            <span className="date">📅 {formatDate(post.created)}</span>
            {post.edited && post.edited !== post.created && (
              <span className="edited">✏️ Edytowano: {formatDate(post.edited)}</span>
            )}
          </div>
        </header>

        <div className="post-body">
          <p>{post.post}</p>
        </div>

        {isAuthor && (
          <div className="post-actions">
            <Button variant="secondary">Edytuj</Button>
            <Button variant="danger" onClick={handleDelete}>Usuń</Button>
          </div>
        )}
      </article>

      <section className="comments-section">
        <h2>Komentarze</h2>
        <p className="coming-soon">Sekcja komentarzy wkrótce dostępna...</p>
      </section>
    </div>
  );
};

export default BlogPostDetail;
