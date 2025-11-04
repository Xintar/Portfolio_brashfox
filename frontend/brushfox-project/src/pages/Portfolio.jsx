import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import useFetch from '../hooks/useFetch';
import { apiService } from '../services/api';
import PhotoGallery from '../components/Portfolio/PhotoGallery';
import Button from '../components/Common/Button';
import './Portfolio.css';

const Portfolio = () => {
  const { isAuthenticated } = useAuth();
  const { data, loading, error, refetch } = useFetch(() => apiService.getPhotos());

  // Handle paginated response
  const photos = data?.results || data || [];

  return (
    <div className="portfolio-page">
      <div className="page-header">
        <h1>Portfolio</h1>
        <p className="page-subtitle">Galeria moich prac fotograficznych</p>
        {isAuthenticated && (
          <Link to="/portfolio/new">
            <Button>📷 Dodaj zdjęcie</Button>
          </Link>
        )}
      </div>

      <PhotoGallery 
        photos={photos} 
        loading={loading} 
        error={error} 
        onRetry={refetch}
      />
    </div>
  );
};

export default Portfolio;
