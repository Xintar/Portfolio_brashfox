import { Link } from 'react-router-dom';
import './PhotoCard.css';

const PhotoCard = ({ photo }) => {
  const imageUrl = photo.image?.startsWith('http') 
    ? photo.image 
    : `http://localhost:8000${photo.image}`;

  return (
    <div className="photo-card">
      <Link to={`/portfolio/${photo.id}`}>
        <div className="photo-card-image">
          <img src={imageUrl} alt={photo.name} loading="lazy" />
          <div className="photo-card-overlay">
            <span className="view-details">Zobacz szczegóły</span>
          </div>
        </div>
        <div className="photo-card-info">
          <h3>{photo.name}</h3>
          {photo.author && <p className="photo-author">📷 {photo.author}</p>}
        </div>
      </Link>
    </div>
  );
};

export default PhotoCard;
