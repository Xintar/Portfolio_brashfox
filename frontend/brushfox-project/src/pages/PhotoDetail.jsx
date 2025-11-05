import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getMediaUrl } from '../utils/constants';
import useFetch from '../hooks/useFetch';
import { apiService } from '../services/api';
import { formatDate } from '../utils/helpers';
import Loading from '../components/Common/Loading';
import ErrorMessage from '../components/Common/ErrorMessage';
import Button from '../components/Common/Button';
import { toast } from 'react-toastify';
import './PhotoDetail.css';

const PhotoDetail = () => {
  const { id } = useParams();
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  
  const { data: photo, loading, error, refetch } = useFetch(
    () => apiService.getPhotoById(id),
    [id]
  );

  const handleDelete = async () => {
    if (!window.confirm('Czy na pewno chcesz usunąć to zdjęcie?')) {
      return;
    }

    try {
      await apiService.deletePhoto(id);
      toast.success('Zdjęcie zostało usunięte');
      navigate('/portfolio');
    } catch (err) {
      console.error('Error deleting photo:', err);
      toast.error('Błąd podczas usuwania zdjęcia');
    }
  };

  if (loading) return <Loading message="Ładowanie zdjęcia..." />;
  if (error) return <ErrorMessage message={error} onRetry={refetch} />;
  if (!photo) return <ErrorMessage message="Zdjęcie nie zostało znalezione" />;

  const imageUrl = getMediaUrl(photo.image);

  const isOwner = isAuthenticated && (user?.username === photo.author || user?.is_staff);

  return (
    <div className="photo-detail">
      <div className="photo-detail-header">
        <Link to="/portfolio" className="back-link">← Powrót do portfolio</Link>
      </div>

      <div className="photo-detail-content">
        <div className="photo-detail-image">
          <img src={imageUrl} alt={photo.name} />
        </div>

        <div className="photo-detail-info">
          <h1 className="photo-title">{photo.name}</h1>
          
          <div className="photo-meta">
            {photo.author && (
              <div className="meta-item">
                <span className="meta-label">📷 Autor:</span>
                <span className="meta-value">{photo.author}</span>
              </div>
            )}
            
            {photo.foto_category && (
              <div className="meta-item">
                <span className="meta-label">🏷️ Kategoria:</span>
                <span className="meta-value">{photo.foto_category.category}</span>
              </div>
            )}

            {photo.event && (
              <div className="meta-item">
                <span className="meta-label">🎬 Wydarzenie:</span>
                <span className="meta-value">{photo.event}</span>
              </div>
            )}
            
            <div className="meta-item">
              <span className="meta-label">📅 Dodano:</span>
              <span className="meta-value">{formatDate(photo.created)}</span>
            </div>

            {photo.edited && photo.edited !== photo.created && (
              <div className="meta-item">
                <span className="meta-label">✏️ Edytowano:</span>
                <span className="meta-value">{formatDate(photo.edited)}</span>
              </div>
            )}
          </div>

          {isOwner && (
            <div className="photo-actions">
              <Button variant="secondary">Edytuj</Button>
              <Button variant="danger" onClick={handleDelete}>Usuń</Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PhotoDetail;
