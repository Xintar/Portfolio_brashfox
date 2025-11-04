import PhotoCard from './PhotoCard';
import Loading from '../Common/Loading';
import ErrorMessage from '../Common/ErrorMessage';
import './PhotoGallery.css';

const PhotoGallery = ({ photos, loading, error, onRetry }) => {
  if (loading) return <Loading message="Ładowanie galerii..." />;
  if (error) return <ErrorMessage message={error} onRetry={onRetry} />;
  if (!photos || photos.length === 0) {
    return (
      <div className="no-photos">
        <p>Brak zdjęć w galerii.</p>
      </div>
    );
  }

  return (
    <div className="photo-gallery">
      {photos.map((photo) => (
        <PhotoCard key={photo.id} photo={photo} />
      ))}
    </div>
  );
};

export default PhotoGallery;
